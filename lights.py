import maya.cmds as cmds

def create_area_light():
    # Ensure the Arnold plugin is loaded
    if not cmds.pluginInfo('mtoa', query=True, loaded=True):
        cmds.loadPlugin('mtoa')

    light_name = "brown_area_light"

    # Create a transform node with a specific name
    light_transform = cmds.createNode('transform', name=light_name)

    # Create an Arnold area light shape as a child of the transform node
    light_shape = cmds.createNode('aiAreaLight', name= (light_name + 'Shape'), parent=light_transform)

    # Apply transformations using xform on the transform node
    cmds.xform(light_transform, translation=(0, 32.969, -0.788), worldSpace=True)
    cmds.xform(light_transform, rotation=(-90.085, 47.608, -0.063), worldSpace=True)
    cmds.xform(light_transform, scale=(41.011, 41.011, 41.011))

    # Set Arnold area light attributes on the shape node
    cmds.setAttr(f'{light_shape}.color', 0.301, 0.181, 0.114, type='double3')
    cmds.setAttr(f'{light_shape}.intensity', 7.869)
    cmds.setAttr(f'{light_shape}.exposure', 0.249)
    cmds.setAttr(f'{light_shape}.normalize', 0)  # Disable normalization

    cmds.connectAttr(f'{light_transform}.instObjGroups', 'defaultLightSet.dagSetMembers', nextAvailable=True)

    # Check that 'illuminates by default' is already enabled (it should be by default)
    print(f"{light_transform} with {light_shape} created and configured.")
