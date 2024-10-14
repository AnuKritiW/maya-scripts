import maya.cmds as mc

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
    mc.polyExtrudeFacet(first_cube + ".f[0]", ltz=0.5)  # 0.5 determined after manual testing

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
    camera_translation = [15.153791664496037, 32.66329062323789, -17.244592819031862]
    camera_rotation = [136.36122876136037, 50.13971297600645, 179.99999999999983]
    focal_length = 35.0

    new_camera = mc.camera()[0]
    mc.xform(new_camera, ws = True, t = camera_translation)
    mc.xform(new_camera, ws = True, ro = camera_rotation)
    mc.setAttr(new_camera + ".focalLength", focal_length)

    mc.lookThru(new_camera)

def main():
    clear_scene()
    generate_stairs()
    set_perspective_camera()

main()

# TODO: add light source