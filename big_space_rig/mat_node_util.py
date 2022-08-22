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

from .node_other import (ensure_node_groups, node_group_name_for_name_and_type, get_node_group_for_type)
from .rig import (PROXY_OBSERVER_0E_BNAME, PROXY_OBSERVER_6E_BNAME)
from .node_other import (get_0e_6e_from_place_bone_name)

def create_duo_node_observer_input(context, node_tree_type, big_space_rig, node_loc_offset):
    tree_nodes = context.space_data.edit_tree.nodes
    new_nodes = []

    if node_tree_type in ['CompositorNodeTree', 'ShaderNodeTree', 'TextureNodeTree']:
        node_input_type = 'ShaderNodeCombineXYZ'
    elif node_tree_type == 'GeometryNodeTree':
        node_input_type = 'FunctionNodeInputVector'
    else:
        print("Error, unknown Observer input node tree type: " + str(node_tree_type))
        return None

    node = tree_nodes.new(type=node_input_type)
    node.label = "6e Observer"
    node.location.x = node.location.x + node_loc_offset[0]
    node.location.y = node.location.y + node_loc_offset[1]
    if node_tree_type in ['CompositorNodeTree', 'ShaderNodeTree', 'TextureNodeTree']:
        # combine XYZ driver X
        drv_loc_x = node.inputs[0].driver_add('default_value').driver
        v_obs_loc_x = drv_loc_x.variables.new()
        v_obs_loc_x.type = 'TRANSFORMS'
        v_obs_loc_x.name = "var"
        v_obs_loc_x.targets[0].id = big_space_rig
        v_obs_loc_x.targets[0].bone_target = PROXY_OBSERVER_6E_BNAME
        v_obs_loc_x.targets[0].transform_type = 'LOC_X'
        v_obs_loc_x.targets[0].transform_space = 'TRANSFORM_SPACE'
        v_obs_loc_x.targets[0].data_path = "location.x"
        drv_loc_x.expression = v_obs_loc_x.name
        # combine XYZ driver Y
        drv_loc_x = node.inputs[1].driver_add('default_value').driver
        v_obs_loc_y = drv_loc_x.variables.new()
        v_obs_loc_y.type = 'TRANSFORMS'
        v_obs_loc_y.name = "var"
        v_obs_loc_y.targets[0].id = big_space_rig
        v_obs_loc_y.targets[0].bone_target = PROXY_OBSERVER_6E_BNAME
        v_obs_loc_y.targets[0].transform_type = 'LOC_Y'
        v_obs_loc_y.targets[0].transform_space = 'TRANSFORM_SPACE'
        v_obs_loc_y.targets[0].data_path = "location.y"
        drv_loc_x.expression = v_obs_loc_y.name
        # combine XYZ driver Z
        drv_loc_x = node.inputs[2].driver_add('default_value').driver
        v_obs_loc_z = drv_loc_x.variables.new()
        v_obs_loc_z.type = 'TRANSFORMS'
        v_obs_loc_z.name = "var"
        v_obs_loc_z.targets[0].id = big_space_rig
        v_obs_loc_z.targets[0].bone_target = PROXY_OBSERVER_6E_BNAME
        v_obs_loc_z.targets[0].transform_type = 'LOC_Z'
        v_obs_loc_z.targets[0].transform_space = 'TRANSFORM_SPACE'
        v_obs_loc_z.targets[0].data_path = "location.z"
        drv_loc_x.expression = v_obs_loc_z.name
    elif node_tree_type == 'GeometryNodeTree':
        # vector input driver X
        drv_loc_x = node.driver_add('vector', 0).driver
        v_obs_loc_x = drv_loc_x.variables.new()
        v_obs_loc_x.type = 'TRANSFORMS'
        v_obs_loc_x.name = "var"
        v_obs_loc_x.targets[0].id = big_space_rig
        v_obs_loc_x.targets[0].bone_target = PROXY_OBSERVER_6E_BNAME
        v_obs_loc_x.targets[0].transform_type = 'LOC_X'
        v_obs_loc_x.targets[0].transform_space = 'TRANSFORM_SPACE'
        v_obs_loc_x.targets[0].data_path = "location.x"
        drv_loc_x.expression = v_obs_loc_x.name
        # vector input driver Y
        drv_loc_y = node.driver_add('vector', 1).driver
        v_obs_loc_y = drv_loc_y.variables.new()
        v_obs_loc_y.type = 'TRANSFORMS'
        v_obs_loc_y.name = "var"
        v_obs_loc_y.targets[0].id = big_space_rig
        v_obs_loc_y.targets[0].bone_target = PROXY_OBSERVER_6E_BNAME
        v_obs_loc_y.targets[0].transform_type = 'LOC_Y'
        v_obs_loc_y.targets[0].transform_space = 'TRANSFORM_SPACE'
        v_obs_loc_y.targets[0].data_path = "location.y"
        drv_loc_y.expression = v_obs_loc_y.name
        # vector input driver Z
        drv_loc_z = node.driver_add('vector', 2).driver
        v_obs_loc_z = drv_loc_z.variables.new()
        v_obs_loc_z.type = 'TRANSFORMS'
        v_obs_loc_z.name = "var"
        v_obs_loc_z.targets[0].id = big_space_rig
        v_obs_loc_z.targets[0].bone_target = PROXY_OBSERVER_6E_BNAME
        v_obs_loc_z.targets[0].transform_type = 'LOC_Z'
        v_obs_loc_z.targets[0].transform_space = 'TRANSFORM_SPACE'
        v_obs_loc_z.targets[0].data_path = "location.z"
        drv_loc_z.expression = v_obs_loc_z.name
    new_nodes.append(node)

    node = tree_nodes.new(type=node_input_type)
    node.label = "0e Observer"
    node.location.x = node.location.x + node_loc_offset[0]
    node.location.y = node.location.y + node_loc_offset[1] - 120
    if node_tree_type in ['CompositorNodeTree', 'ShaderNodeTree', 'TextureNodeTree']:
        # combine XYZ driver X
        drv_loc_x = node.inputs[0].driver_add('default_value').driver
        v_obs_loc_x = drv_loc_x.variables.new()
        v_obs_loc_x.type = 'TRANSFORMS'
        v_obs_loc_x.name = "var"
        v_obs_loc_x.targets[0].id = big_space_rig
        v_obs_loc_x.targets[0].bone_target = PROXY_OBSERVER_0E_BNAME
        v_obs_loc_x.targets[0].transform_type = 'LOC_X'
        v_obs_loc_x.targets[0].transform_space = 'TRANSFORM_SPACE'
        v_obs_loc_x.targets[0].data_path = "location.x"
        drv_loc_x.expression = v_obs_loc_x.name
        # combine XYZ driver Y
        drv_loc_x = node.inputs[1].driver_add('default_value').driver
        v_obs_loc_y = drv_loc_x.variables.new()
        v_obs_loc_y.type = 'TRANSFORMS'
        v_obs_loc_y.name = "var"
        v_obs_loc_y.targets[0].id = big_space_rig
        v_obs_loc_y.targets[0].bone_target = PROXY_OBSERVER_0E_BNAME
        v_obs_loc_y.targets[0].transform_type = 'LOC_Y'
        v_obs_loc_y.targets[0].transform_space = 'TRANSFORM_SPACE'
        v_obs_loc_y.targets[0].data_path = "location.y"
        drv_loc_x.expression = v_obs_loc_y.name
        # combine XYZ driver Z
        drv_loc_x = node.inputs[2].driver_add('default_value').driver
        v_obs_loc_z = drv_loc_x.variables.new()
        v_obs_loc_z.type = 'TRANSFORMS'
        v_obs_loc_z.name = "var"
        v_obs_loc_z.targets[0].id = big_space_rig
        v_obs_loc_z.targets[0].bone_target = PROXY_OBSERVER_0E_BNAME
        v_obs_loc_z.targets[0].transform_type = 'LOC_Z'
        v_obs_loc_z.targets[0].transform_space = 'TRANSFORM_SPACE'
        v_obs_loc_z.targets[0].data_path = "location.z"
        drv_loc_x.expression = v_obs_loc_z.name
    elif node_tree_type == 'GeometryNodeTree':
        # vector input driver X
        drv_loc_x = node.driver_add('vector', 0).driver
        v_obs_loc_x = drv_loc_x.variables.new()
        v_obs_loc_x.type = 'TRANSFORMS'
        v_obs_loc_x.name = "var"
        v_obs_loc_x.targets[0].id = big_space_rig
        v_obs_loc_x.targets[0].bone_target = PROXY_OBSERVER_0E_BNAME
        v_obs_loc_x.targets[0].transform_type = 'LOC_X'
        v_obs_loc_x.targets[0].transform_space = 'TRANSFORM_SPACE'
        v_obs_loc_x.targets[0].data_path = "location.x"
        drv_loc_x.expression = v_obs_loc_x.name
        # vector input driver Y
        drv_loc_y = node.driver_add('vector', 1).driver
        v_obs_loc_y = drv_loc_y.variables.new()
        v_obs_loc_y.type = 'TRANSFORMS'
        v_obs_loc_y.name = "var"
        v_obs_loc_y.targets[0].id = big_space_rig
        v_obs_loc_y.targets[0].bone_target = PROXY_OBSERVER_0E_BNAME
        v_obs_loc_y.targets[0].transform_type = 'LOC_Y'
        v_obs_loc_y.targets[0].transform_space = 'TRANSFORM_SPACE'
        v_obs_loc_y.targets[0].data_path = "location.y"
        drv_loc_y.expression = v_obs_loc_y.name
        # vector input driver Z
        drv_loc_z = node.driver_add('vector', 2).driver
        v_obs_loc_z = drv_loc_z.variables.new()
        v_obs_loc_z.type = 'TRANSFORMS'
        v_obs_loc_z.name = "var"
        v_obs_loc_z.targets[0].id = big_space_rig
        v_obs_loc_z.targets[0].bone_target = PROXY_OBSERVER_0E_BNAME
        v_obs_loc_z.targets[0].transform_type = 'LOC_Z'
        v_obs_loc_z.targets[0].transform_space = 'TRANSFORM_SPACE'
        v_obs_loc_z.targets[0].data_path = "location.z"
        drv_loc_z.expression = v_obs_loc_z.name
    new_nodes.append(node)

    return new_nodes

class BSR_ObserverInputCreateDuoNode(bpy.types.Operator):
    bl_description = "Add input from Observer nodes (6e and 0e), using active object Big Space Rig's observer"
    bl_idname = "big_space_rig.observer_input_create_duo_node"
    bl_label = "Observer Input"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        s = context.space_data
        if s.type == 'NODE_EDITOR' and s.node_tree != None and \
            s.tree_type in ['CompositorNodeTree', 'ShaderNodeTree', 'TextureNodeTree', 'GeometryNodeTree']:
            return True
        return False

    def execute(self, context):
        scn = context.scene
        big_space_rig = bpy.data.objects.get(scn.BSR_NodeGetInputFromRig)
        if big_space_rig is None:
            self.report({'ERROR'}, "Unable to Create Observer Position Input node because no Big Space Rig given.")
            return {'CANCELLED'}
        bpy.ops.node.select_all(action='DESELECT')
        create_duo_node_observer_input(context, context.space_data.edit_tree.bl_idname, big_space_rig, (0, 0))
        return {'FINISHED'}

def create_duo_node_place_input(context, node_tree_type, big_space_rig, bsr_place, node_loc_offset):
    tree_nodes = context.space_data.edit_tree.nodes
    new_nodes = []

    if node_tree_type in ['CompositorNodeTree', 'ShaderNodeTree', 'TextureNodeTree']:
        node_input_type = 'ShaderNodeCombineXYZ'
    elif node_tree_type == 'GeometryNodeTree':
        node_input_type = 'FunctionNodeInputVector'
    else:
        print("Error, unknown Place input node tree type: " + str(node_tree_type))
        return None

    place_bone_name_0e, place_bone_name_6e = get_0e_6e_from_place_bone_name(big_space_rig, bsr_place)
    if place_bone_name_0e is None or place_bone_name_6e is None:
        return

    node = tree_nodes.new(type=node_input_type)
    node.label = "6e Place - " + place_bone_name_6e
    node.location.x = node.location.x + node_loc_offset[0]
    node.location.y = node.location.y + node_loc_offset[1]
    if node_tree_type in ['CompositorNodeTree', 'ShaderNodeTree', 'TextureNodeTree']:
        # combine XYZ driver X
        drv_loc_x = node.inputs[0].driver_add('default_value').driver
        v_place_loc_x = drv_loc_x.variables.new()
        v_place_loc_x.type = 'TRANSFORMS'
        v_place_loc_x.name = "var"
        v_place_loc_x.targets[0].id = big_space_rig
        v_place_loc_x.targets[0].bone_target = place_bone_name_6e
        v_place_loc_x.targets[0].transform_type = 'LOC_X'
        v_place_loc_x.targets[0].transform_space = 'TRANSFORM_SPACE'
        v_place_loc_x.targets[0].data_path = "location.x"
        drv_loc_x.expression = v_place_loc_x.name
        # combine XYZ driver Y
        drv_loc_x = node.inputs[1].driver_add('default_value').driver
        v_place_loc_y = drv_loc_x.variables.new()
        v_place_loc_y.type = 'TRANSFORMS'
        v_place_loc_y.name = "var"
        v_place_loc_y.targets[0].id = big_space_rig
        v_place_loc_y.targets[0].bone_target = place_bone_name_6e
        v_place_loc_y.targets[0].transform_type = 'LOC_Y'
        v_place_loc_y.targets[0].transform_space = 'TRANSFORM_SPACE'
        v_place_loc_y.targets[0].data_path = "location.y"
        drv_loc_x.expression = v_place_loc_y.name
        # combine XYZ driver Z
        drv_loc_x = node.inputs[2].driver_add('default_value').driver
        v_place_loc_z = drv_loc_x.variables.new()
        v_place_loc_z.type = 'TRANSFORMS'
        v_place_loc_z.name = "var"
        v_place_loc_z.targets[0].id = big_space_rig
        v_place_loc_z.targets[0].bone_target = place_bone_name_6e
        v_place_loc_z.targets[0].transform_type = 'LOC_Z'
        v_place_loc_z.targets[0].transform_space = 'TRANSFORM_SPACE'
        v_place_loc_z.targets[0].data_path = "location.z"
        drv_loc_x.expression = v_place_loc_z.name
    elif node_tree_type == 'GeometryNodeTree':
        # vector input driver X
        drv_loc_x = node.driver_add('vector', 0).driver
        v_place_loc_x = drv_loc_x.variables.new()
        v_place_loc_x.type = 'TRANSFORMS'
        v_place_loc_x.name = "var"
        v_place_loc_x.targets[0].id = big_space_rig
        v_place_loc_x.targets[0].bone_target = place_bone_name_6e
        v_place_loc_x.targets[0].transform_type = 'LOC_X'
        v_place_loc_x.targets[0].transform_space = 'TRANSFORM_SPACE'
        v_place_loc_x.targets[0].data_path = "location.x"
        drv_loc_x.expression = v_place_loc_x.name
        # vector input driver Y
        drv_loc_y = node.driver_add('vector', 1).driver
        v_place_loc_y = drv_loc_y.variables.new()
        v_place_loc_y.type = 'TRANSFORMS'
        v_place_loc_y.name = "var"
        v_place_loc_y.targets[0].id = big_space_rig
        v_place_loc_y.targets[0].bone_target = place_bone_name_6e
        v_place_loc_y.targets[0].transform_type = 'LOC_Y'
        v_place_loc_y.targets[0].transform_space = 'TRANSFORM_SPACE'
        v_place_loc_y.targets[0].data_path = "location.y"
        drv_loc_y.expression = v_place_loc_y.name
        # vector input driver Z
        drv_loc_z = node.driver_add('vector', 2).driver
        v_place_loc_z = drv_loc_z.variables.new()
        v_place_loc_z.type = 'TRANSFORMS'
        v_place_loc_z.name = "var"
        v_place_loc_z.targets[0].id = big_space_rig
        v_place_loc_z.targets[0].bone_target = place_bone_name_6e
        v_place_loc_z.targets[0].transform_type = 'LOC_Z'
        v_place_loc_z.targets[0].transform_space = 'TRANSFORM_SPACE'
        v_place_loc_z.targets[0].data_path = "location.z"
        drv_loc_z.expression = v_place_loc_z.name
    new_nodes.append(node)

    node = tree_nodes.new(type=node_input_type)
    node.label = "0e Place - " + place_bone_name_0e
    node.location.x = node.location.x + node_loc_offset[0]
    node.location.y = node.location.y + node_loc_offset[1] - 120
    if node_tree_type in ['CompositorNodeTree', 'ShaderNodeTree', 'TextureNodeTree']:
        # combine XYZ driver X
        drv_loc_x = node.inputs[0].driver_add('default_value').driver
        v_place_loc_x = drv_loc_x.variables.new()
        v_place_loc_x.type = 'TRANSFORMS'
        v_place_loc_x.name = "var"
        v_place_loc_x.targets[0].id = big_space_rig
        v_place_loc_x.targets[0].bone_target = place_bone_name_0e
        v_place_loc_x.targets[0].transform_type = 'LOC_X'
        v_place_loc_x.targets[0].transform_space = 'TRANSFORM_SPACE'
        v_place_loc_x.targets[0].data_path = "location.x"
        drv_loc_x.expression = v_place_loc_x.name
        # combine XYZ driver Y
        drv_loc_x = node.inputs[1].driver_add('default_value').driver
        v_place_loc_y = drv_loc_x.variables.new()
        v_place_loc_y.type = 'TRANSFORMS'
        v_place_loc_y.name = "var"
        v_place_loc_y.targets[0].id = big_space_rig
        v_place_loc_y.targets[0].bone_target = place_bone_name_0e
        v_place_loc_y.targets[0].transform_type = 'LOC_Y'
        v_place_loc_y.targets[0].transform_space = 'TRANSFORM_SPACE'
        v_place_loc_y.targets[0].data_path = "location.y"
        drv_loc_x.expression = v_place_loc_y.name
        # combine XYZ driver Z
        drv_loc_x = node.inputs[2].driver_add('default_value').driver
        v_place_loc_z = drv_loc_x.variables.new()
        v_place_loc_z.type = 'TRANSFORMS'
        v_place_loc_z.name = "var"
        v_place_loc_z.targets[0].id = big_space_rig
        v_place_loc_z.targets[0].bone_target = place_bone_name_0e
        v_place_loc_z.targets[0].transform_type = 'LOC_Z'
        v_place_loc_z.targets[0].transform_space = 'TRANSFORM_SPACE'
        v_place_loc_z.targets[0].data_path = "location.z"
        drv_loc_x.expression = v_place_loc_z.name
    elif node_tree_type == 'GeometryNodeTree':
        # vector input driver X
        drv_loc_x = node.driver_add('vector', 0).driver
        v_place_loc_x = drv_loc_x.variables.new()
        v_place_loc_x.type = 'TRANSFORMS'
        v_place_loc_x.name = "var"
        v_place_loc_x.targets[0].id = big_space_rig
        v_place_loc_x.targets[0].bone_target = place_bone_name_0e
        v_place_loc_x.targets[0].transform_type = 'LOC_X'
        v_place_loc_x.targets[0].transform_space = 'TRANSFORM_SPACE'
        v_place_loc_x.targets[0].data_path = "location.x"
        drv_loc_x.expression = v_place_loc_x.name
        # vector input driver Y
        drv_loc_y = node.driver_add('vector', 1).driver
        v_place_loc_y = drv_loc_y.variables.new()
        v_place_loc_y.type = 'TRANSFORMS'
        v_place_loc_y.name = "var"
        v_place_loc_y.targets[0].id = big_space_rig
        v_place_loc_y.targets[0].bone_target = place_bone_name_0e
        v_place_loc_y.targets[0].transform_type = 'LOC_Y'
        v_place_loc_y.targets[0].transform_space = 'TRANSFORM_SPACE'
        v_place_loc_y.targets[0].data_path = "location.y"
        drv_loc_y.expression = v_place_loc_y.name
        # vector input driver Z
        drv_loc_z = node.driver_add('vector', 2).driver
        v_place_loc_z = drv_loc_z.variables.new()
        v_place_loc_z.type = 'TRANSFORMS'
        v_place_loc_z.name = "var"
        v_place_loc_z.targets[0].id = big_space_rig
        v_place_loc_z.targets[0].bone_target = place_bone_name_0e
        v_place_loc_z.targets[0].transform_type = 'LOC_Z'
        v_place_loc_z.targets[0].transform_space = 'TRANSFORM_SPACE'
        v_place_loc_z.targets[0].data_path = "location.z"
        drv_loc_z.expression = v_place_loc_z.name
    new_nodes.append(node)

    return new_nodes

class BSR_PlaceInputCreateDuoNode(bpy.types.Operator):
    bl_description = "Add input from Place nodes (6e and 0e), using active object Big Space Rig's selected Place"
    bl_idname = "big_space_rig.place_input_create_duo_node"
    bl_label = "Place Input"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        s = context.space_data
        if s.type == 'NODE_EDITOR' and s.node_tree != None and \
            s.tree_type in ['CompositorNodeTree', 'ShaderNodeTree', 'TextureNodeTree', 'GeometryNodeTree']:
            return True
        return False

    def execute(self, context):
        scn = context.scene
        big_space_rig = bpy.data.objects.get(scn.BSR_NodeGetInputFromRig)
        if big_space_rig is None:
            self.report({'ERROR'}, "Unable to Create Place Position Input node because no Big Space Rig given.")
            return {'CANCELLED'}
        bsr_place = scn.BSR_NodeGetInputFromRigPlace
        if bsr_place is None:
            self.report({'ERROR'}, "Unable to Create Place Position Input node because no Place given.")
            return {'CANCELLED'}
        bpy.ops.node.select_all(action='DESELECT')
        create_duo_node_place_input(context, context.space_data.edit_tree.bl_idname, big_space_rig, bsr_place, (0, 0))
        return {'FINISHED'}

def create_obs_place_offset_nodes(context, obs_nodes, place_nodes):
    tree_nodes = context.space_data.edit_tree.nodes

    vec_sub_nodes = []

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.label = "Offset 6e"
    node.location = (180, 0)
    node.operation = "SUBTRACT"
    vec_sub_nodes.append(node)

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.label = "Offset 0e"
    node.location = (180, -140)
    node.operation = "SUBTRACT"
    vec_sub_nodes.append(node)

    tree_links = context.space_data.edit_tree.links
    tree_links.new(obs_nodes[0].outputs[0], vec_sub_nodes[0].inputs[0])
    tree_links.new(obs_nodes[1].outputs[0], vec_sub_nodes[1].inputs[0])
    tree_links.new(place_nodes[0].outputs[0], vec_sub_nodes[0].inputs[1])
    tree_links.new(place_nodes[1].outputs[0], vec_sub_nodes[1].inputs[1])

class BSR_PlaceOffsetInputCreateDuoNode(bpy.types.Operator):
    bl_description = "Add nodes for input from Observer offset by Place (6e and 0e), using active object " \
        "Big Space Rig's selected Place"
    bl_idname = "big_space_rig.place_offset_input_create_duo_node"
    bl_label = "Offset Input"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        s = context.space_data
        if s.type == 'NODE_EDITOR' and s.node_tree != None and \
            s.tree_type in ['CompositorNodeTree', 'ShaderNodeTree', 'TextureNodeTree', 'GeometryNodeTree']:
            return True
        return False

    def execute(self, context):
        scn = context.scene
        big_space_rig = bpy.data.objects.get(scn.BSR_NodeGetInputFromRig)
        if big_space_rig is None:
            self.report({'ERROR'}, "Unable to Create Offset Place Position Input node because no Big Space Rig given.")
            return {'CANCELLED'}
        bsr_place = scn.BSR_NodeGetInputFromRigPlace
        if bsr_place is None:
            self.report({'ERROR'}, "Unable to Create Offset Place Position Input node because no Place given.")
            return {'CANCELLED'}
        bpy.ops.node.select_all(action='DESELECT')
        obs_nodes = create_duo_node_observer_input(context, context.space_data.edit_tree.bl_idname, big_space_rig,
                                                   (0, 0))
        place_nodes = create_duo_node_place_input(context, context.space_data.edit_tree.bl_idname, big_space_rig,
                                                  bsr_place, (0, -260))
        create_obs_place_offset_nodes(context, obs_nodes, place_nodes)
        return {'FINISHED'}
