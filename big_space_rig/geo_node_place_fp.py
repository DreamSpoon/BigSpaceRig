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

from .rig import (OBJ_PROP_FP_MIN_DIST, OBJ_PROP_FP_POWER, OBJ_PROP_FP_MIN_SCALE, OBJ_PROP_BONE_SCL_MULT,
    BSR_CUSTOM_NODE_GROUP_NAME, is_big_space_rig, get_parent_big_space_rig)

def create_place_custom_geo_node_group():
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=BSR_CUSTOM_NODE_GROUP_NAME, type='GeometryNodeTree')
    new_node_group.inputs.new(type='NodeSocketGeometry', name="Geometry")
    new_node_group.inputs.new(type='NodeSocketFloat', name="BSR FP Power")
    new_node_group.inputs.new(type='NodeSocketFloat', name="BSR FP Min Dist")
    new_node_group.inputs.new(type='NodeSocketFloat', name="BSR FP Min Scale")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Place Scale Mult")
    new_node_group.inputs.new(type='NodeSocketVector', name="Place Loc")
    new_node_group.inputs.new(type='NodeSocketVector', name="Place Scale")
    new_node_group.inputs.new(type='NodeSocketVector', name="Object Loc")
    new_node_group.inputs.new(type='NodeSocketVectorEuler', name="Object Rot")
    new_node_group.inputs.new(type='NodeSocketVector', name="Object Scale")
    new_node_group.outputs.new(type='NodeSocketGeometry', name="Geometry")
    tree_nodes = new_node_group.nodes
    # delete old nodes before adding new nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-1645, -95)
    node.operation = "DIVIDE"
    new_nodes["Vector Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.label = "Do Place Transform"
    node.location = (-1480, 15)
    node.operation = "ADD"
    new_nodes["Vector Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-835, -45)
    node.operation = "GREATER_THAN"
    node.inputs[1].default_value = 0.0
    new_nodes["Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-475, -30)
    node.operation = "ADD"
    node.inputs[1].default_value = 1.0
    new_nodes["Math"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-1190, -35)
    node.operation = "LENGTH"
    new_nodes["Vector Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1015, -40)
    node.operation = "SUBTRACT"
    new_nodes["Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Min Length is Zero"
    node.location = (-650, -40)
    node.operation = "MULTIPLY"
    new_nodes["Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (320, -25)
    node.operation = "MULTIPLY"
    new_nodes["Math.009"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.label = "Do Forced Perspective Transform"
    node.location = (960, 80)
    node.operation = "MULTIPLY"
    node.inputs[3].default_value = 1.0
    new_nodes["Vector Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (1180, -290)
    node.operation = "SUBTRACT"
    node.inputs[3].default_value = 1.0
    new_nodes["Vector Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-415, -195)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = -1.0
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (135, -165)
    node.operation = "SUBTRACT"
    node.inputs[0].default_value = 1.0
    new_nodes["Math.010"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (315, -195)
    node.operation = "MULTIPLY"
    new_nodes["Math.007"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Apply Min Scale"
    node.location = (505, -45)
    node.operation = "ADD"
    new_nodes["Math.008"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-50, -105)
    node.operation = "GREATER_THAN"
    new_nodes["Math.006"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-240, -70)
    node.operation = "POWER"
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (-2305, 75)
    new_nodes["Position"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.label = "Do Object Transform"
    node.location = (-1815, 50)
    node.operation = "MULTIPLY_ADD"
    node.inputs[3].default_value = 1.0
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="ShaderNodeVectorRotate")
    node.location = (-2020, 150)
    node.rotation_type = 'EULER_XYZ'
    new_nodes["Vector Rotate"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.label = "Undo Object Transform"
    node.location = (1920, -465)
    node.operation = "DIVIDE"
    new_nodes["Vector Math.008"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (2380, -460)
    new_nodes["Group Output"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (1550, -390)
    node.operation = "SUBTRACT"
    new_nodes["Vector Math.007"] = node

    node = tree_nodes.new(type="GeometryNodeSetPosition")
    node.location = (2185, -555)
    new_nodes["Set Position"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-2400, -290)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="ShaderNodeVectorRotate")
    node.location = (1735, -330)
    node.rotation_type = 'EULER_XYZ'
    node.invert = True
    new_nodes["Vector Rotate.001"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.label = "Undo Place Transform"
    node.location = (1355, -345)
    node.operation = "DIVIDE"
    new_nodes["Vector Math.006"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Apply Place Scale Mult"
    node.location = (705, -230)
    node.operation = "MULTIPLY"
    new_nodes["Math.011"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Set Position"].inputs[0])
    tree_links.new(new_nodes["Set Position"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Math.001"].inputs[1])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Math.001"].inputs[0])
    tree_links.new(new_nodes["Position"].outputs[0], new_nodes["Vector Rotate"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[8], new_nodes["Vector Rotate"].inputs[4])
    tree_links.new(new_nodes["Group Input"].outputs[9], new_nodes["Vector Math"].inputs[1])
    tree_links.new(new_nodes["Vector Rotate"].outputs[0], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[7], new_nodes["Vector Math"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Vector Math.001"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Vector Math.001"].inputs[1])
    tree_links.new(new_nodes["Vector Math.001"].outputs[0], new_nodes["Vector Math.002"].inputs[1])
    tree_links.new(new_nodes["Vector Math.002"].outputs[0], new_nodes["Vector Math.003"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Vector Math.005"].inputs[1])
    tree_links.new(new_nodes["Vector Math.004"].outputs[0], new_nodes["Vector Math.005"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Vector Math.006"].inputs[1])
    tree_links.new(new_nodes["Vector Math.005"].outputs[0], new_nodes["Vector Math.006"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[7], new_nodes["Vector Math.007"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[8], new_nodes["Vector Rotate.001"].inputs[4])
    tree_links.new(new_nodes["Vector Math.007"].outputs[0], new_nodes["Vector Rotate.001"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[9], new_nodes["Vector Math.008"].inputs[1])
    tree_links.new(new_nodes["Vector Rotate.001"].outputs[0], new_nodes["Vector Math.008"].inputs[0])
    tree_links.new(new_nodes["Vector Math.008"].outputs[0], new_nodes["Set Position"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Math.003"].inputs[1])
    tree_links.new(new_nodes["Vector Math.003"].outputs[1], new_nodes["Math.003"].inputs[0])
    tree_links.new(new_nodes["Math.003"].outputs[0], new_nodes["Math.004"].inputs[0])
    tree_links.new(new_nodes["Math.004"].outputs[0], new_nodes["Math.005"].inputs[0])
    tree_links.new(new_nodes["Math.003"].outputs[0], new_nodes["Math.005"].inputs[1])
    tree_links.new(new_nodes["Math.005"].outputs[0], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Math.006"].inputs[1])
    tree_links.new(new_nodes["Math.007"].outputs[0], new_nodes["Math.008"].inputs[1])
    tree_links.new(new_nodes["Math.009"].outputs[0], new_nodes["Math.008"].inputs[0])
    tree_links.new(new_nodes["Math.006"].outputs[0], new_nodes["Math.010"].inputs[1])
    tree_links.new(new_nodes["Math.006"].outputs[0], new_nodes["Math.009"].inputs[0])
    tree_links.new(new_nodes["Math.010"].outputs[0], new_nodes["Math.007"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Math.007"].inputs[1])
    tree_links.new(new_nodes["Vector Math.002"].outputs[0], new_nodes["Vector Math.004"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Math.011"].inputs[1])
    tree_links.new(new_nodes["Math.008"].outputs[0], new_nodes["Math.011"].inputs[0])
    tree_links.new(new_nodes["Math.011"].outputs[0], new_nodes["Vector Math.004"].inputs[1])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Math.006"].inputs[0])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Math.009"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Math.002"].inputs[0])
    tree_links.new(new_nodes["Vector Math"].outputs[0], new_nodes["Vector Math.002"].inputs[0])
    tree_links.new(new_nodes["Vector Math.006"].outputs[0], new_nodes["Vector Math.007"].inputs[0])

    return new_node_group

def add_place_fp_to_existing_group(existing_group_name, clear_node_tree, big_space_rig, big_space_rig_bone, attached_obj):
    existing_node_group = bpy.data.node_groups.get(existing_group_name)
    tree_nodes = existing_node_group.nodes
    # if needed, delete old nodes (clear tree) before adding new nodes
    if clear_node_tree:
        tree_nodes.clear()

    new_nodes = {}

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-260, 280)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="ShaderNodeValue")
    node.label = "Big Space Rig FP Power"
    node.location = (-260, 200)
    node.outputs[0].default_value = 0.5
    # add driver to get Big Space Rig FP Power
    drv_mm_fp_power = node.outputs[0].driver_add('default_value').driver
    v_mm_fp_power = drv_mm_fp_power.variables.new()
    v_mm_fp_power.type = 'SINGLE_PROP'
    v_mm_fp_power.name                 = "var"
    v_mm_fp_power.targets[0].id        = big_space_rig
    v_mm_fp_power.targets[0].data_path = "[\""+OBJ_PROP_FP_POWER+"\"]"
    drv_mm_fp_power.expression = v_mm_fp_power.name
    # finish
    new_nodes["Value"] = node

    node = tree_nodes.new(type="ShaderNodeValue")
    node.label = "Big Space Rig FP Min Dist"
    node.location = (-260, 110)
    node.outputs[0].default_value = 0.0
    # add driver to get Big Space Rig FP Min Dist
    drv_mm_fp_min_dist = node.outputs[0].driver_add('default_value').driver
    v_mm_fp_min_dist = drv_mm_fp_min_dist.variables.new()
    v_mm_fp_min_dist.type = 'SINGLE_PROP'
    v_mm_fp_min_dist.name                 = "var"
    v_mm_fp_min_dist.targets[0].id        = big_space_rig
    v_mm_fp_min_dist.targets[0].data_path = "[\""+OBJ_PROP_FP_MIN_DIST+"\"]"
    drv_mm_fp_min_dist.expression = v_mm_fp_min_dist.name
    # finish
    new_nodes["Value.001"] = node

    node = tree_nodes.new(type="ShaderNodeValue")
    node.label = "Big Space Rig FP Min Scale"
    node.location = (-260, 20)
    node.outputs[0].default_value = 0.0
    # add driver to get Big Space Rig FP Min Dist
    drv_mm_fp_min_scale = node.outputs[0].driver_add('default_value').driver
    v_mm_fp_min_scale = drv_mm_fp_min_scale.variables.new()
    v_mm_fp_min_scale.type = 'SINGLE_PROP'
    v_mm_fp_min_scale.name                 = "var"
    v_mm_fp_min_scale.targets[0].id        = big_space_rig
    v_mm_fp_min_scale.targets[0].data_path = "[\""+OBJ_PROP_FP_MIN_SCALE+"\"]"
    drv_mm_fp_min_scale.expression = v_mm_fp_min_scale.name
    # finish
    new_nodes["Value.002"] = node

    node = tree_nodes.new(type="ShaderNodeValue")
    node.label = "Place Scale Mult"
    node.location = (-260, -70)
    node.outputs[0].default_value = 1.0
    # add driver to get Place Scale Mult from rig
    drv_mm_place_scl_mult = node.outputs[0].driver_add('default_value').driver
    v_mm_place_scl_mult = drv_mm_place_scl_mult.variables.new()
    v_mm_place_scl_mult.type = 'SINGLE_PROP'
    v_mm_place_scl_mult.name                 = "var"
    v_mm_place_scl_mult.targets[0].id        = big_space_rig
    v_mm_place_scl_mult.targets[0].data_path = "pose.bones[\""+big_space_rig_bone+"\"][\""+OBJ_PROP_BONE_SCL_MULT+"\"]"
    drv_mm_place_scl_mult.expression = v_mm_place_scl_mult.name
    # finish
    new_nodes["Value.003"] = node

    node = tree_nodes.new(type="FunctionNodeInputVector")
    node.label = "Place Location"
    node.location = (-260, -155)
    # add drivers to get Place location from rig, in Transform space coordinates
    # Place location X
    drv_place_loc_x = node.driver_add('vector', 0).driver
    v_place_loc_x = drv_place_loc_x.variables.new()
    v_place_loc_x.type = 'TRANSFORMS'
    v_place_loc_x.name = "var"
    v_place_loc_x.targets[0].id = big_space_rig
    v_place_loc_x.targets[0].bone_target = big_space_rig_bone
    v_place_loc_x.targets[0].transform_type = 'LOC_X'
    v_place_loc_x.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_place_loc_x.targets[0].data_path = "location.x"
    drv_place_loc_x.expression = v_place_loc_x.name
    # Place location Y
    drv_place_loc_y = node.driver_add('vector', 1).driver
    v_place_loc_y = drv_place_loc_y.variables.new()
    v_place_loc_y.type = 'TRANSFORMS'
    v_place_loc_y.name = "var"
    v_place_loc_y.targets[0].id = big_space_rig
    v_place_loc_y.targets[0].bone_target = big_space_rig_bone
    v_place_loc_y.targets[0].transform_type = 'LOC_Y'
    v_place_loc_y.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_place_loc_y.targets[0].data_path = "location.y"
    drv_place_loc_y.expression = v_place_loc_y.name
    # Place location Z
    drv_place_loc_z = node.driver_add('vector', 2).driver
    v_place_loc_z = drv_place_loc_z.variables.new()
    v_place_loc_z.type = 'TRANSFORMS'
    v_place_loc_z.name = "var"
    v_place_loc_z.targets[0].id = big_space_rig
    v_place_loc_z.targets[0].bone_target = big_space_rig_bone
    v_place_loc_z.targets[0].transform_type = 'LOC_Z'
    v_place_loc_z.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_place_loc_z.targets[0].data_path = "location.z"
    drv_place_loc_z.expression = v_place_loc_z.name
    # finished adding drivers for Place location, in Transform space coordinates
    new_nodes["Vector"] = node

    node = tree_nodes.new(type="FunctionNodeInputVector")
    node.label = "Place Scale"
    node.vector = (1, 1, 1)
    node.location = (-260, -285)
    # add drivers to get Place scale from rig, in Transform space coordinates
    # Place scale X
    drv_place_scale_x = node.driver_add('vector', 0).driver
    v_place_scale_x = drv_place_scale_x.variables.new()
    v_place_scale_x.type = 'TRANSFORMS'
    v_place_scale_x.name = "var"
    v_place_scale_x.targets[0].id = big_space_rig
    v_place_scale_x.targets[0].bone_target = big_space_rig_bone
    v_place_scale_x.targets[0].transform_type = 'SCALE_X'
    v_place_scale_x.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_place_scale_x.targets[0].data_path = "scale.x"
    drv_place_scale_x.expression = v_place_scale_x.name
    # Place scale Y
    drv_place_scale_y = node.driver_add('vector', 1).driver
    v_place_scale_y = drv_place_scale_y.variables.new()
    v_place_scale_y.type = 'TRANSFORMS'
    v_place_scale_y.name = "var"
    v_place_scale_y.targets[0].id = big_space_rig
    v_place_scale_y.targets[0].bone_target = big_space_rig_bone
    v_place_scale_y.targets[0].transform_type = 'SCALE_Y'
    v_place_scale_y.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_place_scale_y.targets[0].data_path = "scale.y"
    drv_place_scale_y.expression = v_place_scale_y.name
    # Place scale Z
    drv_place_scale_z = node.driver_add('vector', 2).driver
    v_place_scale_z = drv_place_scale_z.variables.new()
    v_place_scale_z.type = 'TRANSFORMS'
    v_place_scale_z.name = "var"
    v_place_scale_z.targets[0].id = big_space_rig
    v_place_scale_z.targets[0].bone_target = big_space_rig_bone
    v_place_scale_z.targets[0].transform_type = 'SCALE_Z'
    v_place_scale_z.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_place_scale_z.targets[0].data_path = "scale.z"
    drv_place_scale_z.expression = v_place_scale_z.name
    # finished adding drivers for Place scale, in Transform space coordinates
    new_nodes["Vector.002"] = node

    node = tree_nodes.new(type="FunctionNodeInputVector")
    node.label = "Object World Loc"
    node.location = (-585, -415)
    # add drivers to get Object location, in World coordinates
    # Object location X
    drv_attached_obj_loc_x = node.driver_add('vector', 0).driver
    v_attached_obj_loc_x = drv_attached_obj_loc_x.variables.new()
    v_attached_obj_loc_x.type = 'TRANSFORMS'
    v_attached_obj_loc_x.name = "var"
    v_attached_obj_loc_x.targets[0].id = attached_obj
    v_attached_obj_loc_x.targets[0].transform_type = 'LOC_X'
    v_attached_obj_loc_x.targets[0].transform_space = 'WORLD_SPACE'
    v_attached_obj_loc_x.targets[0].data_path = "location.x"
    drv_attached_obj_loc_x.expression = v_attached_obj_loc_x.name
    # Object location Y
    drv_attached_obj_loc_y = node.driver_add('vector', 1).driver
    v_attached_obj_loc_y = drv_attached_obj_loc_y.variables.new()
    v_attached_obj_loc_y.type = 'TRANSFORMS'
    v_attached_obj_loc_y.name = "var"
    v_attached_obj_loc_y.targets[0].id = attached_obj
    v_attached_obj_loc_y.targets[0].transform_type = 'LOC_Y'
    v_attached_obj_loc_y.targets[0].transform_space = 'WORLD_SPACE'
    v_attached_obj_loc_y.targets[0].data_path = "location.y"
    drv_attached_obj_loc_y.expression = v_attached_obj_loc_y.name
    # Object location Z
    drv_attached_obj_loc_z = node.driver_add('vector', 2).driver
    v_attached_obj_loc_z = drv_attached_obj_loc_z.variables.new()
    v_attached_obj_loc_z.type = 'TRANSFORMS'
    v_attached_obj_loc_z.name = "var"
    v_attached_obj_loc_z.targets[0].id = attached_obj
    v_attached_obj_loc_z.targets[0].transform_type = 'LOC_Z'
    v_attached_obj_loc_z.targets[0].transform_space = 'WORLD_SPACE'
    v_attached_obj_loc_z.targets[0].data_path = "location.z"
    drv_attached_obj_loc_z.expression = v_attached_obj_loc_z.name
    # finished adding drivers for Object location
    new_nodes["Vector.003"] = node

    node = tree_nodes.new(type="FunctionNodeInputVector")
    node.label = "Object World Rot"
    node.location = (-585, -545)
    # add drivers to get Object rotation, in World coordinates
    # Object rotation Euler X
    drv_attached_obj_rot_x = node.driver_add('vector', 0).driver
    v_attached_obj_rot_x = drv_attached_obj_rot_x.variables.new()
    v_attached_obj_rot_x.type = 'TRANSFORMS'
    v_attached_obj_rot_x.name = "var"
    v_attached_obj_rot_x.targets[0].id = attached_obj
    v_attached_obj_rot_x.targets[0].transform_type = 'ROT_X'
    v_attached_obj_rot_x.targets[0].transform_space = 'WORLD_SPACE'
    v_attached_obj_rot_x.targets[0].data_path = "rotation.x"
    drv_attached_obj_rot_x.expression = v_attached_obj_rot_x.name
    # Object rotation Euler Y
    drv_attached_obj_rot_y = node.driver_add('vector', 1).driver
    v_attached_obj_rot_y = drv_attached_obj_rot_y.variables.new()
    v_attached_obj_rot_y.type = 'TRANSFORMS'
    v_attached_obj_rot_y.name = "var"
    v_attached_obj_rot_y.targets[0].id = attached_obj
    v_attached_obj_rot_y.targets[0].transform_type = 'ROT_Y'
    v_attached_obj_rot_y.targets[0].transform_space = 'WORLD_SPACE'
    v_attached_obj_rot_y.targets[0].data_path = "rotation.y"
    drv_attached_obj_rot_y.expression = v_attached_obj_rot_y.name
    # Object rotation Euler Z
    drv_attached_obj_rot_z = node.driver_add('vector', 2).driver
    v_attached_obj_rot_z = drv_attached_obj_rot_z.variables.new()
    v_attached_obj_rot_z.type = 'TRANSFORMS'
    v_attached_obj_rot_z.name = "var"
    v_attached_obj_rot_z.targets[0].id = attached_obj
    v_attached_obj_rot_z.targets[0].transform_type = 'ROT_Z'
    v_attached_obj_rot_z.targets[0].transform_space = 'WORLD_SPACE'
    v_attached_obj_rot_z.targets[0].data_path = "rotation.z"
    drv_attached_obj_rot_z.expression = v_attached_obj_rot_z.name
    # finished adding drivers for Object rotation
    new_nodes["Vector.004"] = node

    node = tree_nodes.new(type="FunctionNodeInputVector")
    node.label = "Object World Scale"
    node.vector = (1, 1, 1)
    node.location = (-585, -670)
    # add drivers to get Object scale, in World coordinates
    # Object scale X
    drv_attached_obj_scl_x = node.driver_add('vector', 0).driver
    v_attached_obj_scl_x = drv_attached_obj_scl_x.variables.new()
    v_attached_obj_scl_x.type = 'TRANSFORMS'
    v_attached_obj_scl_x.name = "var"
    v_attached_obj_scl_x.targets[0].id = attached_obj
    v_attached_obj_scl_x.targets[0].transform_type = 'SCALE_X'
    v_attached_obj_scl_x.targets[0].transform_space = 'WORLD_SPACE'
    v_attached_obj_scl_x.targets[0].data_path = "scale.x"
    drv_attached_obj_scl_x.expression = v_attached_obj_scl_x.name
    # Object scale Y
    drv_attached_obj_scl_y = node.driver_add('vector', 1).driver
    v_attached_obj_scl_y = drv_attached_obj_scl_y.variables.new()
    v_attached_obj_scl_y.type = 'TRANSFORMS'
    v_attached_obj_scl_y.name = "var"
    v_attached_obj_scl_y.targets[0].id = attached_obj
    v_attached_obj_scl_y.targets[0].transform_type = 'SCALE_Y'
    v_attached_obj_scl_y.targets[0].transform_space = 'WORLD_SPACE'
    v_attached_obj_scl_y.targets[0].data_path = "scale.y"
    drv_attached_obj_scl_y.expression = v_attached_obj_scl_y.name
    # Object scale Z
    drv_attached_obj_scl_z = node.driver_add('vector', 2).driver
    v_attached_obj_scl_z = drv_attached_obj_scl_z.variables.new()
    v_attached_obj_scl_z.type = 'TRANSFORMS'
    v_attached_obj_scl_z.name = "var"
    v_attached_obj_scl_z.targets[0].id = attached_obj
    v_attached_obj_scl_z.targets[0].transform_type = 'SCALE_Z'
    v_attached_obj_scl_z.targets[0].transform_space = 'WORLD_SPACE'
    v_attached_obj_scl_z.targets[0].data_path = "scale.z"
    drv_attached_obj_scl_z.expression = v_attached_obj_scl_z.name
    # finished adding drivers for Object scale
    new_nodes["Vector.005"] = node

    node = tree_nodes.new(type="FunctionNodeInputVector")
    node.label = "Place World Loc"
    node.location = (-585, -795)
    # add drivers to get Place location from rig, in World space coordinates
    # Place location X
    drv_place_world_loc_x = node.driver_add('vector', 0).driver
    v_place_world_loc_x = drv_place_world_loc_x.variables.new()
    v_place_world_loc_x.type = 'TRANSFORMS'
    v_place_world_loc_x.name = "var"
    v_place_world_loc_x.targets[0].id = big_space_rig
    v_place_world_loc_x.targets[0].bone_target = big_space_rig_bone
    v_place_world_loc_x.targets[0].transform_type = 'LOC_X'
    v_place_world_loc_x.targets[0].transform_space = 'WORLD_SPACE'
    v_place_world_loc_x.targets[0].data_path = "location.x"
    drv_place_world_loc_x.expression = v_place_world_loc_x.name
    # Place location Y
    drv_place_world_loc_y = node.driver_add('vector', 1).driver
    v_place_world_loc_y = drv_place_world_loc_y.variables.new()
    v_place_world_loc_y.type = 'TRANSFORMS'
    v_place_world_loc_y.name = "var"
    v_place_world_loc_y.targets[0].id = big_space_rig
    v_place_world_loc_y.targets[0].bone_target = big_space_rig_bone
    v_place_world_loc_y.targets[0].transform_type = 'LOC_Y'
    v_place_world_loc_y.targets[0].transform_space = 'WORLD_SPACE'
    v_place_world_loc_y.targets[0].data_path = "location.y"
    drv_place_world_loc_y.expression = v_place_world_loc_y.name
    # Place location Z
    drv_place_world_loc_z = node.driver_add('vector', 2).driver
    v_place_world_loc_z = drv_place_world_loc_z.variables.new()
    v_place_world_loc_z.type = 'TRANSFORMS'
    v_place_world_loc_z.name = "var"
    v_place_world_loc_z.targets[0].id = big_space_rig
    v_place_world_loc_z.targets[0].bone_target = big_space_rig_bone
    v_place_world_loc_z.targets[0].transform_type = 'LOC_Z'
    v_place_world_loc_z.targets[0].transform_space = 'WORLD_SPACE'
    v_place_world_loc_z.targets[0].data_path = "location.z"
    drv_place_world_loc_z.expression = v_place_world_loc_z.name
    # finished adding drivers for Place location, in World coordinates
    new_nodes["Vector.006"] = node

    node = tree_nodes.new(type="FunctionNodeInputVector")
    node.label = "Place World Scale"
    node.vector = (1, 1, 1)
    node.location = (-585, -920)
    # add drivers to get Place scale from rig, in Transform space coordinates
    # Place scale X
    drv_place_world_scale_x = node.driver_add('vector', 0).driver
    v_place_world_scale_x = drv_place_world_scale_x.variables.new()
    v_place_world_scale_x.type = 'TRANSFORMS'
    v_place_world_scale_x.name = "var"
    v_place_world_scale_x.targets[0].id = big_space_rig
    v_place_world_scale_x.targets[0].bone_target = big_space_rig_bone
    v_place_world_scale_x.targets[0].transform_type = 'SCALE_X'
    v_place_world_scale_x.targets[0].transform_space = 'WORLD_SPACE'
    v_place_world_scale_x.targets[0].data_path = "scale.x"
    drv_place_world_scale_x.expression = v_place_world_scale_x.name
    # Place scale Y
    drv_place_world_scale_y = node.driver_add('vector', 1).driver
    v_place_world_scale_y = drv_place_world_scale_y.variables.new()
    v_place_world_scale_y.type = 'TRANSFORMS'
    v_place_world_scale_y.name = "var"
    v_place_world_scale_y.targets[0].id = big_space_rig
    v_place_world_scale_y.targets[0].bone_target = big_space_rig_bone
    v_place_world_scale_y.targets[0].transform_type = 'SCALE_Y'
    v_place_world_scale_y.targets[0].transform_space = 'WORLD_SPACE'
    v_place_world_scale_y.targets[0].data_path = "scale.y"
    drv_place_world_scale_y.expression = v_place_world_scale_y.name
    # Place scale Z
    drv_place_world_scale_z = node.driver_add('vector', 2).driver
    v_place_world_scale_z = drv_place_world_scale_z.variables.new()
    v_place_world_scale_z.type = 'TRANSFORMS'
    v_place_world_scale_z.name = "var"
    v_place_world_scale_z.targets[0].id = big_space_rig
    v_place_world_scale_z.targets[0].bone_target = big_space_rig_bone
    v_place_world_scale_z.targets[0].transform_type = 'SCALE_Z'
    v_place_world_scale_z.targets[0].transform_space = 'WORLD_SPACE'
    v_place_world_scale_z.targets[0].data_path = "scale.z"
    drv_place_world_scale_z.expression = v_place_world_scale_z.name
    # finished adding drivers for Place scale, in World space coordinates
    new_nodes["Vector.008"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-420, -415)
    node.operation = "SUBTRACT"
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-260, -415)
    node.operation = "DIVIDE"
    new_nodes["Vector Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-260, -575)
    node.operation = "DIVIDE"
    new_nodes["Vector Math.003"] = node

    node = tree_nodes.new(type="GeometryNodeGroup")
    node.label = "BigSpaceRig Geo"
    node.node_tree = bpy.data.node_groups.get(BSR_CUSTOM_NODE_GROUP_NAME)
    node.location = (0, 0)
    new_nodes["BigSpaceRigGeoNodeGroup"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (230, 10)
    new_nodes["Group Output"] = node

    # create links
    tree_links = existing_node_group.links
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["BigSpaceRigGeoNodeGroup"].inputs[0])
    tree_links.new(new_nodes["Value"].outputs[0], new_nodes["BigSpaceRigGeoNodeGroup"].inputs[1])
    tree_links.new(new_nodes["Value.001"].outputs[0], new_nodes["BigSpaceRigGeoNodeGroup"].inputs[2])
    tree_links.new(new_nodes["Value.002"].outputs[0], new_nodes["BigSpaceRigGeoNodeGroup"].inputs[3])
    tree_links.new(new_nodes["Value.003"].outputs[0], new_nodes["BigSpaceRigGeoNodeGroup"].inputs[4])
    tree_links.new(new_nodes["Vector"].outputs[0], new_nodes["BigSpaceRigGeoNodeGroup"].inputs[5])
    tree_links.new(new_nodes["Vector.002"].outputs[0], new_nodes["BigSpaceRigGeoNodeGroup"].inputs[6])
    tree_links.new(new_nodes["Vector Math.001"].outputs[0], new_nodes["BigSpaceRigGeoNodeGroup"].inputs[7])
    tree_links.new(new_nodes["Vector.004"].outputs[0], new_nodes["BigSpaceRigGeoNodeGroup"].inputs[8])
    tree_links.new(new_nodes["Vector Math.003"].outputs[0], new_nodes["BigSpaceRigGeoNodeGroup"].inputs[9])
    tree_links.new(new_nodes["BigSpaceRigGeoNodeGroup"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Vector.006"].outputs[0], new_nodes["Vector Math"].inputs[1])
    tree_links.new(new_nodes["Vector Math"].outputs[0], new_nodes["Vector Math.001"].inputs[0])
    tree_links.new(new_nodes["Vector.008"].outputs[0], new_nodes["Vector Math.001"].inputs[1])
    tree_links.new(new_nodes["Vector.005"].outputs[0], new_nodes["Vector Math.003"].inputs[0])
    tree_links.new(new_nodes["Vector.008"].outputs[0], new_nodes["Vector Math.003"].inputs[1])
    tree_links.new(new_nodes["Vector.003"].outputs[0], new_nodes["Vector Math"].inputs[0])

def ensure_place_fp_node_group(override_create):
    # check if custom node group already exists, and create/override if necessary
    node_group = bpy.data.node_groups.get(BSR_CUSTOM_NODE_GROUP_NAME)
    if node_group is None or override_create:
        # create the custom node group
        new_node_group = create_place_custom_geo_node_group()
        # if override create is enabled, then ensure new group name will be "first", meaning:
        #     group name does not have suffix like '.001', '.002', etc.
        if override_create:
            new_node_group.name = BSR_CUSTOM_NODE_GROUP_NAME

def add_place_fp_geo_nodes_to_object(ob, override_create, alt_group_name, big_space_rig, big_space_rig_bone):
    ensure_place_fp_node_group(override_create)

    geo_nodes_mod = ob.modifiers.new(name="BigSpaceRig.GeometryNodes", type='NODES')
    # use alternate group, if needed and if available
    if alt_group_name != None:
        if bpy.data.node_groups.get(alt_group_name) is None:
            return  # TODO return error / throw exception
        # create nodes, but don't clear node tree before creating new nodes
        add_place_fp_to_existing_group(alt_group_name, False, big_space_rig, big_space_rig_bone, ob)
        geo_nodes_mod.node_group = bpy.data.node_groups.get(alt_group_name)
        return  # success, return
    # create nodes, and clear node tree before creating new nodes
    add_place_fp_to_existing_group(geo_nodes_mod.node_group.name, True, big_space_rig, big_space_rig_bone, ob)

class BSR_AddPlaceFP_GeoNodes(bpy.types.Operator):
    bl_description = "Add Geometry Nodes to selected object(s). Object(s) must already be attached to Big Space Rig "+\
                     "for this to work"
    bl_idname = "big_space_rig.add_place_fp_geo_nodes"
    bl_label = "Add Geometry Nodes"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scn = context.scene
        for ob in context.selected_objects:
            # skip non-mesh objects
            if ob.type != 'MESH':
                continue
            # skip objects that are not parented to a Big Space Rig
            mm_rig, mm_rig_bone = get_parent_big_space_rig(ob)
            if mm_rig is None:
                continue
            alt_group_name = None
            if scn.BSR_GeoNodesCreateUseAltGroup:
                if scn.BSR_GeoNodesCreateAltGroup is None:
                    self.report({'ERROR'}, "Unable to create geometry nodes because Alternate Group not found.")
                    return {'CANCELLED'}
                alt_group_name = scn.BSR_GeoNodesCreateAltGroup.name
            add_place_fp_geo_nodes_to_object(ob, scn.BSR_GeoNodesOverrideCreate, alt_group_name, mm_rig,
                                              mm_rig_bone)
        return {'FINISHED'}
