import maya.cmds as cmds
import importlib.util
import os

# Manually specify the directory where your scripts are located
# script_dir = r'C:\Users\anukr\Desktop\Code\maya-scripts'  # Use raw string for Windows path
script_dir = r'/home/s5647918/Code/maya-scripts'
# TODO: get path dynamically; change path to match machine until then

# Function to dynamically import a module from a file
def import_module(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def clear_scene():
    cmds.select(all=True)
    cmds.delete()

def main():
    clear_scene()

    # List of scripts to load
    scripts_to_import = ['impossibleStairs.py', 'scene.py', 'camera.py']

    for script in scripts_to_import:
        script_path = os.path.join(script_dir, script)
        module_name = script[:-3]  # Remove the .py extension
        globals()[module_name] = import_module(module_name, script_path)

    # Populate scene
    impossibleStairs.generate_stairs()
    camera.set_perspective_camera()
    walls_grp = scene.create_walls()

    # TODO: clean up this code and move it out of main as much as possible
    left_wall_grp = cmds.listRelatives(walls_grp)[0]
    left_wall = cmds.listRelatives(left_wall_grp)[0]
    print(left_wall)

    hallway_grp = scene.create_hallway_with_arch(p_width=10, p_height=10, p_depth=100)
    hallway_arch = cmds.listRelatives(hallway_grp)[0]
    print(hallway_arch)

    hollowed_wall = cmds.polyBoolOp(hallway_arch, left_wall, op=2, name="Hollowed_Wall")[0]
    cmds.polyNormal(hallway_arch, normalMode=0)  # 0 flips normals

    scene.create_floor()

main()
