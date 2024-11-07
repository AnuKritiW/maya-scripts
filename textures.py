import os
import maya.cmds as cmds

def create_textures():

    portraits = ['slytherin', 'gryffindor', 'ravenclaw', 'hufflepuff', 'greylady', 'bloodybaron', 'nick', 'fatfriar', 'peeves', 'dumbledore']

    for portrait in portraits:
        image_sequence_path = f'./portraits/{portrait}_seq/{portrait}_1.png'

        # Create a new material (Lambert or Phong)
        material = cmds.shadingNode('lambert', asShader=True, name='imageSequenceMaterial')
        cmds.setAttr(material + '.color', 1, 1, 1, type='double3')  # Default white color

        # Create the File texture node for the image sequence
        file_node = cmds.shadingNode('file', asTexture=True, name='imageSequenceFile')
        cmds.setAttr(file_node + '.fileTextureName', image_sequence_path, type='string')

        # Enable the image sequence
        cmds.setAttr(file_node + '.useFrameExtension', 1)  # Enable frame extension (looping)

        # Connect the texture to the material
        cmds.connectAttr(file_node + '.outColor', material + '.color', force=True)

        # Create a new shading group
        shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name='imageSequenceSG')
        cmds.connectAttr(material + '.outColor', shading_group + '.surfaceShader', force=True)

        # Create a New Cube
        cube = cmds.polyCube()[0]

        # Select the Front Face of the Cube (Face with ID 2 is usually the front face)
        cmds.select(cube + '.f[2]')  # Select the front face (facing along the positive Z-axis)

        # Apply the Material to the Selected Face
        cmds.hyperShade(assign=material)

        cmds.select(cube + '.f[2]')  # Select the front face (facing along the positive Z-axis)
        cmds.polyAutoProjection(cube + '.f[2]', lm=0, ibd=True)

        # Rotate the UVs so the textures are right side up
        cmds.polyEditUV(cube + '.map[0]', r=True, angle=180)  # Rotate the UVs by 180 degrees

        # Set the Timeline Range for Playback
        start_frame = 1
        parent_directory = os.path.dirname(image_sequence_path)
        end_frame = len(os.listdir(parent_directory))

        cmds.playbackOptions(min=start_frame, max=end_frame)
        cmds.playbackOptions(loop="continuous")  # Enable looping for the timeline playback

        # Create an Expression to Loop the Frame Extension Attribute
        expression = f"{file_node}.frameExtension = (frame % {end_frame}) + 1;"
        cmds.expression(s=expression, o="", ae=True, uc="all")

        # Print confirmation message
        print(f"Expression added to loop {file_node}.frameExtension every {end_frame} frames.")

create_textures()