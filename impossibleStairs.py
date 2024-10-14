import maya.cmds as mc
import random

CUBE_HEIGHT_WIDTH = 2

def clear_scene():
    mc.select(all=True)
    mc.delete()

def generate_stairs():
    num_steps = 0
    cube_height = 20
    coord_dict = {'x': -6, 'z': 4} # Values arbitrarily decided after manual testing

    # Generate the first step and extrude its front face
    cube_height, first_cube = create_cube(cube_height, coord_dict)

    # Polyextrude the front face of the first cube
    mc.polyExtrudeFacet(first_cube + ".f[0]", ltz=0.4)  # ltz determined after manual testing

    cube_height = generate_flight_of_stairs(coord_dict, 0,                  -CUBE_HEIGHT_WIDTH, cube_height, 6)
    cube_height = generate_flight_of_stairs(coord_dict, CUBE_HEIGHT_WIDTH,  0,                  cube_height, 5)
    cube_height = generate_flight_of_stairs(coord_dict, 0,                  CUBE_HEIGHT_WIDTH,  cube_height, 4)
    cube_height = generate_flight_of_stairs(coord_dict, -CUBE_HEIGHT_WIDTH, 0,                  cube_height, 2)

def generate_flight_of_stairs(p_coord_dict, p_x_delta, p_z_delta, p_cube_height, p_num_steps_in_flight):
    num_steps = 0
    while num_steps < p_num_steps_in_flight:
        p_coord_dict['x'] += p_x_delta
        p_coord_dict['z'] += p_z_delta
        p_cube_height = create_cube(p_cube_height, p_coord_dict)[0]
        num_steps += 1

    return p_cube_height

def create_cube(p_cube_height, p_coord_dict):
    curr_cube = mc.polyCube(d = CUBE_HEIGHT_WIDTH, h = p_cube_height, w = CUBE_HEIGHT_WIDTH)[0]

    # Ensure that the newly created cube is the active selection
    mc.select(curr_cube)
    
    # Move pivot to the bottom of the cube (Y = -p_cube_height / 2)
    mc.xform(curr_cube, pivots=(0, -p_cube_height / 2, 0), ws=True)
    
    # Move the cube so its base aligns with Y = 0 and position it along the X-axis
    mc.move(p_coord_dict['x'], -10 + (p_cube_height / 2), p_coord_dict['z'], curr_cube, ws=True)  # y = p_cube_height / 2 keeps the base at Y=0

    return ((p_cube_height + 0.25), curr_cube)

def set_perspective_camera():
    # Camera settings: retrieved by manually creating a camera and looking at the attribute values
    camera_translation = [19.84736949836961, 38.312038840075, -21.903529496661506]
    # camera_translation = [15.153791664496037, 32.66329062323789, -17.244592819031862]
    camera_rotation = [138.76122876136156, 48.93971297600498, 179.9999999999995]
    # camera_rotation = [136.36122876136037, 50.13971297600645, 179.99999999999983]
    focal_length = 35.0

    new_camera = mc.camera()[0]
    mc.xform(new_camera, ws = True, t = camera_translation)
    mc.xform(new_camera, ws = True, ro = camera_rotation)
    mc.setAttr(new_camera + ".focalLength", focal_length)

    mc.lookThru(new_camera)

# TODO: move into separate file
def create_walls():
    # left wall
    transform_dict = {'tx': -10.571,
                      'ty': 0,
                      'tz': 42.109,
                      'rx': 0,
                      'ry': 0,
                      'rz': 0,
                      'sx': 67,
                      'sy': 67,
                      'sz': 0.356}
    create_wall(transform_dict)

    # right wall
    transform_dict['tx'] = -42.995
    transform_dict['tz'] = 8.603
    transform_dict['ry'] = -89.478 # Rotate to help with the illusion
    create_wall(transform_dict)

def create_wall(p_transform_dict):
    wall = mc.polyCube()
    mc.xform(wall,
        translation = [p_transform_dict['tx'], p_transform_dict['ty'], p_transform_dict['tz']],
        rotation = [p_transform_dict['rx'], p_transform_dict['ry'], p_transform_dict['rz']],
        scale = [p_transform_dict['sx'], p_transform_dict['sy'], p_transform_dict['sz']],
        worldSpace=True)

    frames_list = create_frames_on_wall()
    frames_grp = mc.group(frames_list, name="frames")
    mc.xform(frames_grp,
             translation = [p_transform_dict['tx'], p_transform_dict['ty'], p_transform_dict['tz']],
             rotation = [p_transform_dict['rx'], p_transform_dict['ry'], p_transform_dict['rz']],
             worldSpace=True)
    # TODP: Ensure that frames are on the right side of each wall

def create_frames_on_wall():
    num_frames = 400
    frame_data_list = []
    frame_list = []
    for _ in range(num_frames):
        frame_type = 'rectangular' # TODO: Add more shapes

        if frame_type == 'rectangular':
            frame, fr_width, fr_height = create_rectangular_frame(p_width = random.uniform(2, 4), p_height = random.uniform(1, 3))

        # If placement fails, delete the frame
        if not is_frame_placed_on_wall(fr_width, fr_height, frame_data_list, 67, 67): # TODO: Get wall dimensions dynamically
            mc.delete(frame)
        else:
            frame_list.append(frame)

    return frame_list

def create_rectangular_frame(p_width, p_height):
    frame = mc.polyCube(w = p_width, h = p_height, d = 0.2, name = "Rectangular_Frame")[0]
    return (frame, p_width, p_height)

def is_frame_placed_on_wall(p_fr_width, p_fr_height, p_frame_data_list, p_wall_width, p_wall_height):
    # Try upto 100 times to place the frame
    max_attempts = 100
    for _ in range(max_attempts):
        # Randomly choose a position for the frame
        x_pos = random.uniform(-p_wall_width / 2 + p_fr_width / 2, p_wall_width / 2 - p_fr_width / 2)
        y_pos = random.uniform(p_fr_height / 2, p_wall_height - p_fr_height / 2)

        # Check if the frame overlaps with any existing frames
        if not is_overlap(x_pos, y_pos, p_fr_width, p_fr_height, p_frame_data_list):
            mc.move(x_pos, y_pos, 0.25)  # Slight offset to keep frame on the wall
            p_frame_data_list.append((x_pos, y_pos, p_fr_width, p_fr_height))
            return True

    return False

def is_overlap(p_x_pos, p_y_pos, p_fr_width, p_fr_height, p_frame_data_list):
    for frame_data in p_frame_data_list:
        curr_fr_x, curr_fr_y, curr_fr_width, curr_fr_height = frame_data

        min_dist_between_fr = 0.2
        # Check for overlap by comparing bounding boxes
        if not ((p_x_pos + (p_fr_width / 2) + min_dist_between_fr) < (curr_fr_x - (curr_fr_width / 2)) or
                (p_x_pos - (p_fr_width / 2) - min_dist_between_fr) > (curr_fr_x + (curr_fr_width / 2)) or
                (p_y_pos + (p_fr_height / 2) + min_dist_between_fr) < (curr_fr_y - (curr_fr_height / 2)) or
                (p_y_pos - (p_fr_height / 2) - min_dist_between_fr) > (curr_fr_y + (curr_fr_height / 2))):
            return True

    return False

def main():
    clear_scene()
    generate_stairs()
    set_perspective_camera()
    create_walls()

main()

# TODO: add light source