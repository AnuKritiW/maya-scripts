import maya.cmds as mc

def generate_stairs():
    mc.select(all=True)
    mc.delete()  # Clear the scene

    num_steps = 0
    cube_height = 20
    coord_dict = {'x': -6, 'z': 6}

    cube_height = generate_flight_of_stairs(coord_dict, 0, -2, cube_height, 7)
    cube_height = generate_flight_of_stairs(coord_dict, 2, 0, cube_height, 5)
    cube_height = generate_flight_of_stairs(coord_dict, 0, 2, cube_height, 4)
    cube_height = generate_flight_of_stairs(coord_dict, -2, 0, cube_height, 2)

def generate_flight_of_stairs(p_coord_dict, p_x_change, p_z_change, p_cube_height, p_num_steps_in_flight):
    num_steps = 0
    while num_steps < p_num_steps_in_flight:
        p_coord_dict['x'] += p_x_change
        p_coord_dict['z'] += p_z_change
        p_cube_height = create_cube(p_cube_height, p_coord_dict['x'], p_coord_dict['z'])
        num_steps += 1

    return p_cube_height

def create_cube(p_cube_height, p_x_coord, p_z_coord):
    curr_cube = mc.polyCube(d = 2, h = p_cube_height, w = 2)[0]

    # Ensure that the newly created cube is the active selection
    mc.select(curr_cube)
    
    # Move pivot to the bottom of the cube (Y = -p_cube_height / 2)
    mc.xform(curr_cube, pivots=(0, -p_cube_height / 2, 0), ws=True)
    
    # Move the cube so its base aligns with Y = 0 and position it along the X-axis
    mc.move(p_x_coord, -10 + (p_cube_height / 2), p_z_coord, curr_cube, ws=True)  # y = p_cube_height / 2 keeps the base at Y=0

    return (p_cube_height + 0.25)

generate_stairs()

# TODO: polyExtrude front face of first cube
# TODO: add light source
# TODO: add perspective camera
