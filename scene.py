import maya.cmds as cmds
import random
import math

SQ_WALL_SIZE = 67

# TODO: optimize this function
def is_overlap(p_x_pos, p_y_pos, p_fr_width, p_fr_height, p_frame_data_list):
    for frame_data in p_frame_data_list:
        curr_fr_x, curr_fr_y, curr_fr_width, curr_fr_height = frame_data

        min_dist_between_fr = 0.2
        # Check for overlap by comparing bounding boxes
        if not ((p_x_pos + (p_fr_width / 2)  + min_dist_between_fr) < (curr_fr_x - (curr_fr_width  / 2)) or
                (p_x_pos - (p_fr_width / 2)  - min_dist_between_fr) > (curr_fr_x + (curr_fr_width  / 2)) or
                (p_y_pos + (p_fr_height / 2) + min_dist_between_fr) < (curr_fr_y - (curr_fr_height / 2)) or
                (p_y_pos - (p_fr_height / 2) - min_dist_between_fr) > (curr_fr_y + (curr_fr_height / 2))):
            return True

    return False

# TODO: if the wall remains a square, consider renaming the width parameter and removing the height parameter
def is_frame_placed_on_wall(p_fr_width, p_fr_height, p_frame_data_list, p_wall_width, p_wall_height):
    # Try upto 100 times to place the frame
    max_attempts = 100
    for _ in range(max_attempts):
        # Randomly choose a position for the frame
        x_pos = random.uniform(((-p_wall_width / 2) + (p_fr_width / 2)), ((p_wall_width / 2) - (p_fr_width / 2)))
        y_pos = random.uniform((p_fr_height / 2), (p_wall_height - (p_fr_height / 2)))

        # Check if the frame overlaps with any existing frames
        if not is_overlap(x_pos, y_pos, p_fr_width, p_fr_height, p_frame_data_list):
            cmds.move(x_pos, y_pos, 0.25)  # Slight offset to keep frame on the wall
            p_frame_data_list.append((x_pos, y_pos, p_fr_width, p_fr_height))
            return True

    return False

def create_rectangular_frame(p_width, p_height):
    frame = cmds.polyCube(w = p_width, h = p_height, d = 0.2, name = "Rectangular_Frame")[0]
    return (frame, p_width, p_height)

def create_frames_on_wall():
    num_frames = 400
    frame_data_list = []
    frame_list = []
    for _ in range(num_frames):
        frame_type = 'rectangular' # TODO: Add more shapes

        if frame_type == 'rectangular':
            frame, fr_width, fr_height = create_rectangular_frame(p_width = random.uniform(2, 4), p_height = random.uniform(1, 3))

        # If placement fails, delete the frame
        sq_wall_size = (SQ_WALL_SIZE - 3) # padding around the boundaries of the wall

        # TODO: ensure frames are not touching the floor
        if not is_frame_placed_on_wall(fr_width, fr_height, frame_data_list, sq_wall_size, sq_wall_size):
            cmds.delete(frame)
        else:
            frame_list.append(frame)

    return frame_list

def create_wall(p_transform_dict, p_wall_name):
    wall = cmds.polyCube(w = p_transform_dict['sx'], h = p_transform_dict['sy'], d = p_transform_dict['sz'], name = p_wall_name)[0]
    cmds.move(0, p_transform_dict['sy'] / 2, 0)

    frames_list = create_frames_on_wall()
    frames_grp = cmds.group(frames_list, name = "Frames")

    wall_with_frames = cmds.group([wall, frames_grp], name = (p_wall_name + "_with_Frames"))

    cmds.xform(wall_with_frames,
        t  = [p_transform_dict['tx'], p_transform_dict['ty'], p_transform_dict['tz']],
        ro = [p_transform_dict['rx'], p_transform_dict['ry'], p_transform_dict['rz']],
        ws = True)

    return wall_with_frames

def create_walls():
    # left wall
    transform_dict = {'tx': -10.571,
                      'ty': -33,
                      'tz': 42.109,
                      'rx': 0,
                      'ry': 180,
                      'rz': 0,
                      'sx': SQ_WALL_SIZE,
                      'sy': SQ_WALL_SIZE,
                      'sz': 0.2}
    left_wall = create_wall(transform_dict, "Left_Wall")

    # right wall
    transform_dict['tx'] = -42.995
    transform_dict['tz'] = 8.603
    transform_dict['ry'] = 89.478 # Rotate to help with the illusion
    right_wall = create_wall(transform_dict, "Right_Wall")

    cmds.group([left_wall, right_wall], name = "Walls")

def create_floor():
    floor = cmds.polyCube(d = 90, h = 0.2, w = 90)[0]
    cmds.xform(floor, t = [0, -32, 0])


"""
Below, we create an arch that has two straight sides and a semi-circular top.
To create the semi-circular arch at the top, we can first create a curve, and then extrude it.

To create the curve, we can use the parametric eqns of a circle:
x = r cos(\Theta)
y = r sin(\Theta)

r is the radius of the circle. 2r will be the width of the arch base from left to right, and also the height of the arch from the base to the tip.

\Theta is in radians, and will span from 0 to pi rad (or 0 to 180 degrees)

To draw the curve, in addition to the width and the height of the curve, we will also need the number of vertices we intend to use to shape the curve.
The more the vertices, the smoother the curve.
"""

def create_arch(p_width, p_straight_height, p_vertices=20):
    """
    Creates a NURBS curve with straight sides and a semicircular top.

    Parameters:
    - p_width: Total width of the arch.
    - p_straight_height: Height of the straight vertical sections.
    - p_vertices: Number of vertices that form the semicircular part.
    """
    points = []

    radius = p_width / 2

    # 1: Add points for the left straight side
    # Bottom left corner (base of the left side)
    first_pt = (-radius, 0, 0)
    points.append(first_pt)
    # Top left corner (end of the straight section on the left side)
    points.append((-radius, p_straight_height, 0))

    # 2: Generate points for the semicircular top

    # Every vertex is angle_step away from the previous one
    angle_step = 180 / (p_vertices - 1)

    for i in range(p_vertices):
        angle_deg = 180 - (i * angle_step)  # Start from 180° and go to 0°
        angle_rad = math.radians(angle_deg)

        # Calculate points on the semicircle (centered at y = p_straight_height)
        x = radius * math.cos(angle_rad)
        y = (radius * math.sin(angle_rad)) + p_straight_height

        # Append each calculated point for the semicircular part
        points.append((x, y, 0))

    # 3. Add points for the right straight side
    # Top right corner (end of the straight section on the right side)
    points.append((radius, p_straight_height, 0))
    # Bottom right corner (base of the right side)
    last_pt = (radius, 0, 0)
    points.append(last_pt)

    # Step 4: Create the NURBS curve using the combined points
    arch_curve = cmds.curve(p = points, degree = 3, name = "Arch_Curve")
    # cmds.closeCurve(arch_curve, ch=False)

    floor_curve = create_floor_curve(first_pt, last_pt) # TODO: connect floor curve to arch curve and extrude together; consider using .extendCurve ?

    return arch_curve

def create_floor_curve(p_first_pt, p_last_pt):
    return cmds.curve(p=[p_first_pt, p_last_pt], degree = 1)

def extrude_arch(arch_curve, depth):
    # Create a straight line for the extrusion path
    extrude_path = cmds.curve(p = [(0, 0, 0), (0, 0, depth)], degree = 1, name = "Extrude_Path")

    # Extrude the arch along the path
    extruded_hallway = cmds.extrude(arch_curve, extrude_path, ch = True, rn = False, po = 1, et = 2, ucp = 1, name="Hallway_Arch")
    return extrude_path, extruded_hallway

def create_hallway_with_arch(p_width, p_height, p_depth):
    # Create the arch curve
    arch_curve = create_arch(p_width, p_height)

    # Extrude the arch curve to form the hallway
    extrude_path, hallway = extrude_arch(arch_curve, p_depth)

    hallway_curves_grp = cmds.group([arch_curve, extrude_path], name = "Hallway_Curves")
    cmds.hide(hallway_curves_grp)

    hallway_grp = cmds.group([hallway[0], hallway_curves_grp], name = "Hallway")

    # TODO: Move the hallway to final location
    cmds.move(0, -32, -10, hallway_curves_grp)

    return hallway_grp
