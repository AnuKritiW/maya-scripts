import os
import maya.cmds as cmds

def create_textures():

        portraits = ['slytherin', 'gryffindor', 'ravenclaw', 'hufflepuff', 'greylady', 'bloodybaron', 'nick', 'fatfriar', 'peeves', 'dumbledore']
        # portraits = ['peeves'] # for testing that textures have different offsets
        materials = []

        # TODO: clean up logic here
        for portrait in portraits:
                materials.append(create_material(portrait, 0))
                materials.append(create_material(portrait, 3))
                materials.append(create_material(portrait, 1.5))

        return materials

def create_material(p_portrait, p_offset_level):
        image_sequence_path = f'./portraits/{p_portrait}_seq/{p_portrait}_1.png'
        # image_sequence_path= f'C:/Users/anukr/Desktop/Code/maya-scripts/portraits/{p_portrait}_seq/{p_portrait}_1.png'

        # Create a new material (Lambert or Phong)
        material = cmds.shadingNode('lambert', asShader=True, name=f'{p_portrait}_material')
        cmds.setAttr(material + '.color', 1, 1, 1, type='double3')  # Default white color

        # Create the File texture node for the image sequence
        file_node = cmds.shadingNode('file', asTexture=True, name='imageSequenceFile')
        cmds.setAttr(file_node + '.fileTextureName', image_sequence_path, type='string')

        # Enable the image sequence
        cmds.setAttr(file_node + '.useFrameExtension', 1)  # Enable frame extension (looping)

        if cmds.attributeQuery('imageCache', node=file_node, exists=True):
                cmds.setAttr(file_node + '.imageCache', 1)


        if cmds.attributeQuery('resolution', node=file_node, exists=True):
                cmds.setAttr(file_node + '.resolution', 256)  # Set to a lower value for preview

        # Connect the texture to the material
        cmds.connectAttr(file_node + '.outColor', material + '.color', force=True)

        # Create a new shading group
        shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name='imageSequenceSG')
        cmds.connectAttr(material + '.outColor', shading_group + '.surfaceShader', force=True)

        # Set the Timeline Range for Playback
        start_frame = 1
        parent_directory = os.path.dirname(image_sequence_path)
        end_frame = len(os.listdir(parent_directory)) - 1

        frame_offset = 0
        if (p_offset_level != 0):
                frame_offset = int(end_frame / p_offset_level)

        cmds.playbackOptions(min=start_frame, max=end_frame)
        cmds.playbackOptions(loop="continuous")  # Enable looping for the timeline playback

        # Create an Expression to Loop the Frame Extension Attribute
        # expression = f"{file_node}.frameExtension = (frame % {end_frame}) + 1;"
        expression = f"{file_node}.frameExtension = ((frame + {frame_offset}) % {end_frame}) + 1;"
        cmds.expression(s=expression, o="", ae=True, uc="all")

        return material

def create_leather_material(material_name='leatherMaterial', shading_group_name='leatherSG'):
    # Create a Blinn material (or use another type if preferred)
    material = cmds.shadingNode('blinn', asShader=True, name=material_name)

    # Create a shading group and connect the material
    shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=shading_group_name)
    cmds.connectAttr(f'{material}.outColor', f'{shading_group}.surfaceShader', force=True)

    # Create a leather texture node
    leather_texture = cmds.shadingNode('leather', asTexture=True, name='leatherTexture')

    # Create a place3dTexture node and connect it to the leather texture
    place_3d_texture = cmds.shadingNode('place3dTexture', asUtility=True, name='place3dTexture1')
    cmds.connectAttr(f'{place_3d_texture}.worldMatrix[0]', f'{leather_texture}.placementMatrix', force=True)

    # Connect the leather texture to the color attribute of the material
    cmds.connectAttr(f'{leather_texture}.outColor', f'{material}.color', force=True)

    # Adjust the leather texture's attributes (e.g., color, scale)
    cmds.setAttr(f'{leather_texture}.creaseColor', 0.174, 0.087, 0.0, type='double3')
    cmds.setAttr(f'{leather_texture}.cellColor', 0.110, 0.046, 0.017, type='double3')
    cmds.setAttr(f'{leather_texture}.cellSize', 0.2)  # Adjust the cell size

    return material

def assign_material_to_object(material, object):
    cmds.select(object)
    cmds.hyperShade(assign=material)
