# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 3
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import bpy

from .node_other import ensure_node_groups

CAMERA_CULL_GEO_NG_NAME = "CameraCull.BSR.GeoNG"

def create_geo_ng_camera_cull():
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=CAMERA_CULL_GEO_NG_NAME, type='GeometryNodeTree')
    new_node_group.inputs.new(type='NodeSocketVector', name="Point")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Point Radius")
    new_node_group.inputs.new(type='NodeSocketVector', name="Cam Loc")
    new_node_group.inputs.new(type='NodeSocketVector', name="Cam Rot")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Clip Sphere Radius")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Clip Start")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Clip End")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Cam Angle")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Aspect Ratio")
    new_node_group.outputs.new(type='NodeSocketBool', name="Boolean")
    tree_nodes = new_node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Greater than clip"
    node.location = (520, -280)
    node.operation = "GREATER_THAN"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Less than clip"
    node.location = (520, -120)
    node.operation = "LESS_THAN"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (520, -460)
    node.operation = "ABSOLUTE"
    node.use_clamp = False
    node.inputs[1].default_value = 0.500000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.009"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (520, -800)
    node.operation = "ABSOLUTE"
    node.use_clamp = False
    node.inputs[1].default_value = 0.500000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.012"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (520, -940)
    node.operation = "DIVIDE"
    node.use_clamp = True
    node.inputs[0].default_value = 1.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.016"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (520, -600)
    node.operation = "ADD"
    node.use_clamp = True
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.014"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (700, -800)
    node.operation = "DIVIDE"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.017"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (140, -700)
    new_nodes["Separate XYZ"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "x / z"
    node.location = (340, -620)
    node.operation = "DIVIDE"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.006"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "y / z"
    node.location = (340, -780)
    node.operation = "DIVIDE"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.013"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (520, 200)
    node.operation = "DISTANCE"
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (520, 60)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (340, -260)
    new_nodes["Separate XYZ.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (700, 160)
    node.operation = "GREATER_THAN"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math"] = node

    node = tree_nodes.new(type="FunctionNodeBooleanMath")
    node.location = (700, -200)
    node.operation = "OR"
    new_nodes["Boolean Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (700, -460)
    node.operation = "DIVIDE"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.015"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (880, -460)
    node.operation = "GREATER_THAN"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.007"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (880, -680)
    node.operation = "GREATER_THAN"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.010"] = node

    node = tree_nodes.new(type="FunctionNodeBooleanMath")
    node.location = (1060, -420)
    node.operation = "OR"
    new_nodes["Boolean Math.002"] = node

    node = tree_nodes.new(type="FunctionNodeBooleanMath")
    node.location = (1240, -280)
    node.operation = "AND"
    new_nodes["Boolean Math"] = node

    node = tree_nodes.new(type="FunctionNodeBooleanMath")
    node.location = (1420, -240)
    node.operation = "OR"
    new_nodes["Boolean Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-40, -460)
    node.operation = "ADD"
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeVectorRotate")
    node.location = (-220, -460)
    node.invert = True
    node.rotation_type = "EULER_XYZ"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 1.0)
    node.inputs[3].default_value = 0.000000
    new_nodes["Vector Rotate"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-400, -720)
    node.operation = "DIVIDE"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (-220, -720)
    node.inputs[0].default_value = 0.000000
    node.inputs[1].default_value = 0.000000
    new_nodes["Combine XYZ"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-400, -480)
    node.operation = "SUBTRACT"
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (1600, -240)
    new_nodes["Group Output"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-760, -860)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = 0.500000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-580, -860)
    node.operation = "TANGENT"
    node.use_clamp = False
    node.inputs[1].default_value = 0.500000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.008"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-980, -160)
    new_nodes["Group Input"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Math.003"].outputs[0], new_nodes["Math"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Math.001"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Vector Math.001"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Math.002"].inputs[1])
    tree_links.new(new_nodes["Vector Math.001"].outputs[1], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Vector Math"].outputs[0], new_nodes["Vector Rotate"].inputs[0])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Boolean Math.003"].inputs[0])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Boolean Math.003"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Vector Math"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Vector Math.001"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ"].outputs[2], new_nodes["Math.006"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ"].outputs[0], new_nodes["Math.006"].inputs[0])
    tree_links.new(new_nodes["Math.006"].outputs[0], new_nodes["Math.009"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ"].outputs[2], new_nodes["Math.013"].inputs[1])
    tree_links.new(new_nodes["Math.013"].outputs[0], new_nodes["Math.012"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ"].outputs[1], new_nodes["Math.013"].inputs[0])
    tree_links.new(new_nodes["Math.007"].outputs[0], new_nodes["Boolean Math.002"].inputs[0])
    tree_links.new(new_nodes["Math.010"].outputs[0], new_nodes["Boolean Math.002"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Vector Rotate"].inputs[4])
    tree_links.new(new_nodes["Math.014"].outputs[0], new_nodes["Math.015"].inputs[1])
    tree_links.new(new_nodes["Math.016"].outputs[0], new_nodes["Math.017"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[8], new_nodes["Math.016"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[8], new_nodes["Math.014"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[2], new_nodes["Math.001"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[2], new_nodes["Math.002"].inputs[0])
    tree_links.new(new_nodes["Math.012"].outputs[0], new_nodes["Math.017"].inputs[0])
    tree_links.new(new_nodes["Math.017"].outputs[0], new_nodes["Math.010"].inputs[0])
    tree_links.new(new_nodes["Math.009"].outputs[0], new_nodes["Math.015"].inputs[0])
    tree_links.new(new_nodes["Math.015"].outputs[0], new_nodes["Math.007"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Math.003"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Math.003"].inputs[0])
    tree_links.new(new_nodes["Vector Math.002"].outputs[0], new_nodes["Separate XYZ.001"].inputs[0])
    tree_links.new(new_nodes["Vector Math.002"].outputs[0], new_nodes["Separate XYZ"].inputs[0])
    tree_links.new(new_nodes["Vector Rotate"].outputs[0], new_nodes["Vector Math.002"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Math.004"].inputs[0])
    tree_links.new(new_nodes["Math.004"].outputs[0], new_nodes["Combine XYZ"].inputs[2])
    tree_links.new(new_nodes["Combine XYZ"].outputs[0], new_nodes["Vector Math.002"].inputs[1])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Boolean Math"].inputs[0])
    tree_links.new(new_nodes["Boolean Math.002"].outputs[0], new_nodes["Boolean Math"].inputs[1])
    tree_links.new(new_nodes["Boolean Math"].outputs[0], new_nodes["Boolean Math.001"].inputs[0])
    tree_links.new(new_nodes["Boolean Math.003"].outputs[0], new_nodes["Boolean Math.001"].inputs[1])
    tree_links.new(new_nodes["Boolean Math.001"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Math.005"].outputs[0], new_nodes["Math.008"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[7], new_nodes["Math.005"].inputs[0])
    tree_links.new(new_nodes["Math.008"].outputs[0], new_nodes["Math.004"].inputs[1])
    tree_links.new(new_nodes["Math.008"].outputs[0], new_nodes["Math.010"].inputs[1])
    tree_links.new(new_nodes["Math.008"].outputs[0], new_nodes["Math.007"].inputs[1])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False
    return new_node_group

def create_prereq_util_node_group(node_group_name, node_tree_type):
    if node_group_name == CAMERA_CULL_GEO_NG_NAME:
        return create_geo_ng_camera_cull()

    # error
    print("Unknown name passed to create_prereq_util_node_group: " + str(node_group_name))
    return None

def create_input_camera_cull_nodes(tree_nodes, tree_links, cam_obj_name, special_node):
    # initialize variables
    new_nodes = {}

    new_nodes["Group"] = special_node

    # create nodes
    node = tree_nodes.new(type="ShaderNodeValue")
    node.label = "Clip Start"
    node.location = (-340, -420)
    node.outputs[0].default_value = 0.01
    # add driver to get Camera clip start
    drv_clip_start = node.outputs[0].driver_add('default_value').driver
    v_clip_start = drv_clip_start.variables.new()
    v_clip_start.type = 'SINGLE_PROP'
    v_clip_start.name                 = "var"
    v_clip_start.targets[0].id_type = 'CAMERA'
    v_clip_start.targets[0].id        = bpy.data.cameras.get(cam_obj_name)
    v_clip_start.targets[0].data_path = "clip_start"
    drv_clip_start.expression = v_clip_start.name
    new_nodes["Value.001"] = node

    node = tree_nodes.new(type="ShaderNodeValue")
    node.label = "Clip End"
    node.location = (-340, -520)
    node.outputs[0].default_value = 1000.0
    # add driver to get Camera clip end
    drv_clip_end = node.outputs[0].driver_add('default_value').driver
    v_clip_end = drv_clip_end.variables.new()
    v_clip_end.type = 'SINGLE_PROP'
    v_clip_end.name                 = "var"
    v_clip_end.targets[0].id_type = 'CAMERA'
    v_clip_end.targets[0].id        = bpy.data.cameras.get(cam_obj_name)
    v_clip_end.targets[0].data_path = "clip_end"
    drv_clip_end.expression = v_clip_end.name
    new_nodes["Value.002"] = node

    node = tree_nodes.new(type="ShaderNodeValue")
    node.label = "Cam Angle"
    node.location = (-340, -620)
    # add driver to get Camera angle
    drv_cam_angle = node.outputs[0].driver_add('default_value').driver
    v_cam_angle = drv_cam_angle.variables.new()
    v_cam_angle.type = 'SINGLE_PROP'
    v_cam_angle.name                 = "var"
    v_cam_angle.targets[0].id_type = 'CAMERA'
    v_cam_angle.targets[0].id        = bpy.data.cameras.get(cam_obj_name)
    v_cam_angle.targets[0].data_path = "angle"
    drv_cam_angle.expression = v_cam_angle.name
    new_nodes["Value.004"] = node

    node = tree_nodes.new(type="GeometryNodeObjectInfo")
    node.location = (-340, -220)
    node.transform_space = "RELATIVE"
    node.inputs[0].default_value = bpy.data.objects.get(cam_obj_name)
    node.inputs[1].default_value = False
    new_nodes["Object Info"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (-340, -160)
    new_nodes["Position"] = node

    # create links
    tree_links.new(new_nodes["Value.001"].outputs[0], new_nodes["Group"].inputs[5])
    tree_links.new(new_nodes["Position"].outputs[0], new_nodes["Group"].inputs[0])
    tree_links.new(new_nodes["Value.002"].outputs[0], new_nodes["Group"].inputs[6])
    tree_links.new(new_nodes["Value.004"].outputs[0], new_nodes["Group"].inputs[7])
    tree_links.new(new_nodes["Object Info"].outputs[0], new_nodes["Group"].inputs[2])
    tree_links.new(new_nodes["Object Info"].outputs[1], new_nodes["Group"].inputs[3])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False
    return new_nodes

def create_camera_cull_geo_nodes(context, cam_obj_name, override_create):
    ensure_node_groups(override_create, [CAMERA_CULL_GEO_NG_NAME], 'GeometryNodeTree', create_prereq_util_node_group)

    # create group node that will do the work
    node = context.space_data.edit_tree.nodes.new(type='GeometryNodeGroup')
    node.location = (-160, -120)
    node.node_tree = bpy.data.node_groups.get(CAMERA_CULL_GEO_NG_NAME)
    node.inputs[8].default_value = 16.0 / 9.0

    # create the 'input' nodes
    tr = context.space_data.edit_tree
    create_input_camera_cull_nodes(tr.nodes, tr.links, cam_obj_name, node)

class BSR_CameraCullCreateNodes(bpy.types.Operator):
    bl_description = "Add nodes to current node tree that "
    bl_idname = "big_space_rig.camera_cull_create_geo_node"
    bl_label = "Camera Cull"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scn = context.scene
        create_camera_cull_geo_nodes(context, scn.BSR_CullCamera[1:len(scn.BSR_CullCamera)],
                                     scn.BSR_NodesOverrideCreate)
        return {'FINISHED'}
