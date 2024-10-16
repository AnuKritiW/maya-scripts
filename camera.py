import maya.cmds as cmds

def set_perspective_camera():
    # Camera settings: retrieved by manually creating a camera and looking at the attribute values
    camera_name     = "Perspective_Stairs_Cam"
    translate       = [18.65003909667751,  46.65651136436399, -20.5378338921984]
    rotate          = [139.96122876136397, 49.33971297600335, 179.99999999999895]
    film_aperture   = [1.4173200000000001, 0.94488]
    focal_length    = 35.0
    resolution      = [960, 540]
    aspect_ratio    = 1.7777776718139648

    new_camera = cmds.camera(name = camera_name)[0]

    # Set translation and rotation
    cmds.setAttr(new_camera + ".translate", *translate)
    cmds.setAttr(new_camera + ".rotate",    *rotate)

    # Set the film gate (aperture) and focal length
    cmds.setAttr(new_camera + ".horizontalFilmAperture", film_aperture[0])
    cmds.setAttr(new_camera + ".verticalFilmAperture",   film_aperture[1])
    cmds.setAttr(new_camera + ".focalLength",            focal_length)

    # Set render resolution and aspect ratio
    cmds.setAttr("defaultResolution.width",             resolution[0])
    cmds.setAttr("defaultResolution.height",            resolution[1])
    cmds.setAttr("defaultResolution.deviceAspectRatio", aspect_ratio)

    # Lock translation, rotation, and scale
    for attr in ["translate", "rotate", "scale"]:
        cmds.setAttr(f"{new_camera}.{attr}", lock=True)

    # Look through the new camera
    cmds.lookThru(new_camera)
