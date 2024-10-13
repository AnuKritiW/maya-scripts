import maya.cmds as mc

def main():
    mc.select(all=True)
    mc.delete()  # Clean the scene

    num_steps = 0
    x_coord = -6
    z_coord = 6
    cube_height = 20

    while num_steps < 7:
        z_coord -= 2
        cube_height = create_cube(cube_height, x_coord, z_coord)
        num_steps += 1

    num_steps = 0
    while num_steps < 5:
        x_coord += 2
        cube_height = create_cube(cube_height, x_coord, z_coord)
        num_steps += 1

    num_steps = 0
    while num_steps < 4:
        z_coord += 2
        cube_height = create_cube(cube_height, x_coord, z_coord)
        num_steps += 1

    num_steps = 0

    while num_steps < 2:
        x_coord -= 2
        cube_height = create_cube(cube_height, x_coord, z_coord)
        num_steps += 1


def create_cube(p_cube_height, p_x_coord, p_z_coord):
    # Create cube
    curr_cube = mc.polyCube(d=2, h=p_cube_height, w=2)[0]  # Get the cube object

    # Ensure that the newly created cube is the active selection
    mc.select(curr_cube)
    
    # Move pivot to the bottom of the cube (Y = -p_cube_height / 2)
    mc.xform(curr_cube, pivots=(0, -p_cube_height / 2, 0), ws=True)
    
    # Move the cube so its base aligns with Y = 0 and position it along the X-axis
    mc.move(p_x_coord, -10 + (p_cube_height / 2), p_z_coord, curr_cube, ws=True)  # y = p_cube_height / 2 keeps the base at Y=0

    return (p_cube_height + 0.25)

main()

# TODO: polyExtrude front face of first cube
# TODO: add light source
# TODO: add perspective camera
# TODO: abstract out common code
