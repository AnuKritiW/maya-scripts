import maya.cmds as cmds

BALL_RADIUS = 1
"""
keys: string names
values: list of tuples
        each tuple contains the step name at [0] and the center coordinate at [1]
stair_info
{
    'First_Step' : [('First_Step', (x, y, z))],
    'Flight_of_Stairs_1' : [('pCube1', (x, y, z)), ('pCube2', (x, y, z), ...)]
    ...
}
"""

def get_stairs_info():
    stairs_info = {'First_Step' : [('First_Step', get_top_centre('First_Step'))]}

    for flight_idx in range(1,5): #TODO: abstract out number of flights of stairs
        flight_name = ('Flight_of_Stairs_' + str(flight_idx)) # TODO: abstract name out
        step_names_in_flight = cmds.ls(cmds.listRelatives(flight_name, children=True), shortNames=True)
        stairs_info[flight_name] = []
        for step_name in step_names_in_flight:
            stairs_info[flight_name].append((step_name, (get_top_centre(step_name))))

    # print(stairs_info)
    return stairs_info

def get_top_centre(p_step_name):
    # Get the bounding box of the step
    bounding_box = cmds.xform(p_step_name, query=True, boundingBox=True, ws=True) # [xmin, ymin, zmin, xmax, ymax, zmax].

    top_center = [
            (bounding_box[0] + bounding_box[3]) / 2,  # X average
            bounding_box[4] + BALL_RADIUS, # Y max (top)
            (bounding_box[2] + bounding_box[5]) / 2   # Z average
        ]

    return top_center

"""
The ball will definitely hit all of the (x, z) locations of each step.
y will be the only thing that needs adjustment on each step.
"""
def animate_ball(ball, fixed_pts, fps=25, duration=10):
    total_frames = fps * duration
    num_points = len(fixed_pts)

    # Calculate the interval for keyframes based on the number of points
    interval = total_frames / num_points if num_points > 0 else 0

    for i, pt in enumerate(fixed_pts):
        frame_number = int(i * interval)
        cmds.xform(ball, t=pt)  # Move the ball to the point
        cmds.setKeyframe(ball, t=frame_number)  # Set a keyframe at the frame number

def create_ball():
    # turning_pts = [value[-1][1] for value in get_stairs_info().values()]
    # turning_pts.append(turning_pts[0])

    # turning_pts.reverse() # So the ball is descending instead of ascending

    all_coords = [coord for value in get_stairs_info().values() for _, coord in value]
    all_coords.append(all_coords[0])
    all_coords.reverse()

    ball = cmds.polySphere(radius=BALL_RADIUS)[0]
    cmds.xform(ball, t=all_coords[0])

    animate_ball(ball, all_coords)

create_ball()
get_stairs_info()