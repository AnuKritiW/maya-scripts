import maya.cmds as mc
import random

SQ_STEP_SIZE = 2

def clear_scene():
    mc.select(all=True)
    mc.delete()

def generate_stairs():
    num_steps = 0
    step_height = 20
    coord_dict = {'x': -6, 'z': 4} # Values arbitrarily decided after manual testing

    # Generate the first step and extrude its front face
    step_height, first_step = create_step(step_height, coord_dict)

    first_step = mc.rename(first_step, "First_Step")

    # Polyextrude the front face of the first step
    mc.polyExtrudeFacet(first_step + ".f[0]", ltz=0.4)  # ltz determined after manual testing

    num_flights = 0
    step_height, first_flight  = generate_flight_of_stairs(coord_dict, 0,             -SQ_STEP_SIZE, step_height, 6, (num_flights + 1))
    step_height, second_flight = generate_flight_of_stairs(coord_dict, SQ_STEP_SIZE,  0,             step_height, 5, (num_flights + 1))
    step_height, third_flight  = generate_flight_of_stairs(coord_dict, 0,             SQ_STEP_SIZE,  step_height, 4, (num_flights + 1))
    step_height, fourth_flight = generate_flight_of_stairs(coord_dict, -SQ_STEP_SIZE, 0,             step_height, 2, (num_flights + 1))

    mc.group([first_step, first_flight, second_flight, third_flight, fourth_flight], name = "Impossible_Stairs")

def generate_flight_of_stairs(p_coord_dict, p_x_delta, p_z_delta, p_step_height, p_num_steps_in_flight, p_flight_num):
    num_steps = 0
    steps = []
    while num_steps < p_num_steps_in_flight:
        p_coord_dict['x'] += p_x_delta
        p_coord_dict['z'] += p_z_delta
        p_step_height, step = create_step(p_step_height, p_coord_dict)
        steps.append(step)
        num_steps += 1

    steps_grp = mc.group(steps, name = ("Flight_of_Stairs_" + str(p_flight_num)))
    return (p_step_height, steps_grp)

def create_step(p_step_height, p_coord_dict):
    curr_step = mc.polyCube(w = SQ_STEP_SIZE, h = p_step_height, d = SQ_STEP_SIZE)[0]

    # Ensure that the newly created step is the active selection
    mc.select(curr_step)
    
    # Move pivot to the bottom of the step (Y = -p_step_height / 2)
    mc.xform(curr_step, pivots=(0, (-p_step_height / 2), 0), ws = True)
    
    # Move the step so its base aligns with Y = 0 and position it along the X-axis
    mc.move(p_coord_dict['x'], (p_step_height / 2), p_coord_dict['z'], curr_step, ws = True)  # y = (p_step_height / 2) keeps the base at Y=0

    return ((p_step_height + 0.25), curr_step)

def set_perspective_camera():
    # Camera settings: retrieved by manually creating a camera and looking at the attribute values
    camera_name     = "Perspective_Stairs_Cam"
    translate       = [18.65003909667751,  46.65651136436399, -20.5378338921984]
    rotate          = [139.96122876136397, 49.33971297600335, 179.99999999999895]
    film_aperture   = [1.4173200000000001, 0.94488]
    focal_length    = 35.0
    resolution      = [960, 540]
    aspect_ratio    = 1.7777776718139648

    new_camera = mc.camera(name = camera_name)[0]

    # Set translation and rotation
    mc.setAttr(new_camera + ".translate", *translate)
    mc.setAttr(new_camera + ".rotate",    *rotate)

    # Set the film gate (aperture) and focal length
    mc.setAttr(new_camera + ".horizontalFilmAperture", film_aperture[0])
    mc.setAttr(new_camera + ".verticalFilmAperture",   film_aperture[1])
    mc.setAttr(new_camera + ".focalLength",            focal_length)

    # Set render resolution and aspect ratio
    mc.setAttr("defaultResolution.width",             resolution[0])
    mc.setAttr("defaultResolution.height",            resolution[1])
    mc.setAttr("defaultResolution.deviceAspectRatio", aspect_ratio)

    # Lock translation, rotation, and scale
    for attr in ["translate", "rotate", "scale"]:
        mc.setAttr(f"{new_camera}.{attr}", lock=True)

    # Look through the new camera
    mc.lookThru(new_camera)

# TODO: move into separate file
def create_walls():
    sq_wall_size = 67
    # left wall
    transform_dict = {'tx': -10.571,
                      'ty': -33,
                      'tz': 42.109,
                      'rx': 0,
                      'ry': 180,
                      'rz': 0,
                      'sx': sq_wall_size,
                      'sy': sq_wall_size,
                      'sz': 0.2}
    left_wall = create_wall(transform_dict, "Left_Wall")

    # right wall
    transform_dict['tx'] = -42.995
    transform_dict['tz'] = 8.603
    transform_dict['ry'] = 89.478 # Rotate to help with the illusion
    right_wall = create_wall(transform_dict, "Right_Wall")

    mc.group([left_wall, right_wall], name = "Walls")

def create_wall(p_transform_dict, p_wall_name):
    wall = mc.polyCube(w = p_transform_dict['sx'], h = p_transform_dict['sy'], d = p_transform_dict['sz'], name = p_wall_name)[0]
    mc.move(0, p_transform_dict['sy'] / 2, 0)

    frames_list = create_frames_on_wall(p_transform_dict['sx']) # The wall is a square. If changed, pass in width and height separately.
    frames_grp = mc.group(frames_list, name = "Frames")

    wall_with_frames = mc.group([wall, frames_grp], name = (p_wall_name + "_with_Frames"))

    mc.xform(wall_with_frames,
        t  = [p_transform_dict['tx'], p_transform_dict['ty'], p_transform_dict['tz']],
        ro = [p_transform_dict['rx'], p_transform_dict['ry'], p_transform_dict['rz']],
        ws = True)

    return wall_with_frames

def create_frames_on_wall(p_sq_wall_size):
    num_frames = 400
    frame_data_list = []
    frame_list = []
    for _ in range(num_frames):
        frame_type = 'rectangular' # TODO: Add more shapes

        if frame_type == 'rectangular':
            frame, fr_width, fr_height = create_rectangular_frame(p_width = random.uniform(2, 4), p_height = random.uniform(1, 3))

        # If placement fails, delete the frame
        sq_wall_size = (p_sq_wall_size - 3) # padding around the boundaries of the wall

        # TODO: ensure frames are not touching the floor
        if not is_frame_placed_on_wall(fr_width, fr_height, frame_data_list, sq_wall_size, sq_wall_size):
            mc.delete(frame)
        else:
            frame_list.append(frame)

    return frame_list

def create_rectangular_frame(p_width, p_height):
    frame = mc.polyCube(w = p_width, h = p_height, d = 0.2, name = "Rectangular_Frame")[0]
    return (frame, p_width, p_height)

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
            mc.move(x_pos, y_pos, 0.25)  # Slight offset to keep frame on the wall
            p_frame_data_list.append((x_pos, y_pos, p_fr_width, p_fr_height))
            return True

    return False

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

def create_floor():
    floor = mc.polyCube(d = 90, h = 0.2, w = 90)[0]
    mc.xform(floor, t = [0, -32, 0])

def main():
    clear_scene()
    generate_stairs()
    set_perspective_camera()
    create_walls()
    create_floor()

main()

# TODO: add light source
# TODO: reorder functions