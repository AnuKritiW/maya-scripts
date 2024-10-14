import maya.cmds as mc

CUBE_HEIGHT_WIDTH = 2

def clear_scene():
    mc.select(all=True)
    mc.delete()

def generate_stairs():
    num_steps = 0
    cube_height = 20
    coord_dict = {'x': -6, 'z': 6}

    cube_height = generate_flight_of_stairs(coord_dict, 0,                  -CUBE_HEIGHT_WIDTH, cube_height, 7)
    cube_height = generate_flight_of_stairs(coord_dict, CUBE_HEIGHT_WIDTH,  0,                  cube_height, 5)
    cube_height = generate_flight_of_stairs(coord_dict, 0,                  CUBE_HEIGHT_WIDTH,  cube_height, 4)
    cube_height = generate_flight_of_stairs(coord_dict, -CUBE_HEIGHT_WIDTH, 0,                  cube_height, 2)

def generate_flight_of_stairs(p_coord_dict, p_x_delta, p_z_delta, p_cube_height, p_num_steps_in_flight):
    num_steps = 0
    while num_steps < p_num_steps_in_flight:
        p_coord_dict['x'] += p_x_delta
        p_coord_dict['z'] += p_z_delta
        p_cube_height = create_cube(p_cube_height, p_coord_dict)
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

    return (p_cube_height + 0.25)

clear_scene()
generate_stairs()

# TODO: polyExtrude front face of first cube
# TODO: add light source

# TODO: add perspective camera
