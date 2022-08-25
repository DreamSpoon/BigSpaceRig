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

MERGE_VERT_LOD_GEO_NG_NAME = "MergeVertexLOD.BSR.GeoNG"

VEC_DIV_3E_MOD_3E_DUO_NG_NAME = "VecDiv3eMod3e.BSR"
VEC_DIV_6E_DUO_NG_NAME = "VecDiv6e.BSR"

# depending on the name passed to function, create the right set of nodes in a group and pass back
def create_prereq_mono_node_group(node_group_name, node_tree_type):
    if node_group_name == MERGE_VERT_LOD_GEO_NG_NAME:
        return create_geo_ng_merge_vertex_lod()

    # error
    print("Unknown name passed to create_custom_mono_node_group: " + str(node_group_name))
    return None

# depending on the name passed to function, create the right set of nodes in a group and pass back
def create_prereq_duo_node_group(node_group_name, node_tree_type):
    if node_group_name == VEC_DIV_3E_MOD_3E_DUO_NG_NAME:
        return create_duo_vec_div3e_mod_3e(node_tree_type)
    elif node_group_name == VEC_DIV_6E_DUO_NG_NAME:
        return create_duo_vec_div_6e(node_tree_type)

    # error
    print("Unknown name passed to create_custom_duo_node_group: " + str(node_group_name))
    return None

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

def create_duo_vec_div3e_mod_3e(node_tree_type):
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=node_group_name_for_name_and_type(VEC_DIV_3E_MOD_3E_DUO_NG_NAME,
                                                                                     node_tree_type),
                                              type=node_tree_type)
    new_node_group.inputs.new(type='NodeSocketVector', name="Vector 6e")
    new_node_group.inputs.new(type='NodeSocketVector', name="Vector 0e")
    new_node_group.inputs.new(type='NodeSocketVector', name="World")
    new_node_group.outputs.new(type='NodeSocketVector', name="Vector")
    tree_nodes = new_node_group.nodes
    # delete old nodes before adding new nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-450, 110)
    node.operation = "DIVIDE"
    node.inputs[1].default_value = (1e3, 1e3, 1e3)
    new_nodes["Vector Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-270, 110)
    node.operation = "FRACTION"
    new_nodes["Vector Math.006"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-450, -90)
    node.operation = "DIVIDE"
    node.inputs[1].default_value = (1e3, 1e3, 1e3)
    new_nodes["Vector Math.007"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-270, -90)
    node.operation = "FRACTION"
    new_nodes["Vector Math.008"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-90, 30)
    node.operation = "ADD"
    new_nodes["Vector Math.009"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (90, 30)
    node.operation = "FRACTION"
    new_nodes["Vector Math.010"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (270, 30)
    node.operation = "ADD"
    new_nodes["Vector Math.014"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (450, 30)
    node.operation = "ADD"
    new_nodes["Vector Math.015"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-170, -290)
    node.operation = "ADD"
    new_nodes["Vector Math.011"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (10, -250)
    node.operation = "DIVIDE"
    node.inputs[1].default_value = (1e3, 1e3, 1e3)
    new_nodes["Vector Math.012"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (90, 210)
    node.operation = "FLOOR"
    new_nodes["Vector Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-90, 290)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = (1e3, 1e3, 1e3)
    new_nodes["Vector Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-270, 290)
    node.operation = "FRACTION"
    new_nodes["Vector Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (190, -210)
    node.operation = "FLOOR"
    new_nodes["Vector Math.013"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-680, -20)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (640, -20)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Vector Math.002"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Vector Math.005"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Vector Math.007"].inputs[0])
    tree_links.new(new_nodes["Vector Math.015"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Vector Math.002"].outputs[0], new_nodes["Vector Math.003"].inputs[0])
    tree_links.new(new_nodes["Vector Math.003"].outputs[0], new_nodes["Vector Math.004"].inputs[0])
    tree_links.new(new_nodes["Vector Math.005"].outputs[0], new_nodes["Vector Math.006"].inputs[0])
    tree_links.new(new_nodes["Vector Math.007"].outputs[0], new_nodes["Vector Math.008"].inputs[0])
    tree_links.new(new_nodes["Vector Math.006"].outputs[0], new_nodes["Vector Math.009"].inputs[0])
    tree_links.new(new_nodes["Vector Math.008"].outputs[0], new_nodes["Vector Math.009"].inputs[1])
    tree_links.new(new_nodes["Vector Math.009"].outputs[0], new_nodes["Vector Math.010"].inputs[0])
    tree_links.new(new_nodes["Vector Math.011"].outputs[0], new_nodes["Vector Math.012"].inputs[0])
    tree_links.new(new_nodes["Vector Math.012"].outputs[0], new_nodes["Vector Math.013"].inputs[0])
    tree_links.new(new_nodes["Vector Math.004"].outputs[0], new_nodes["Vector Math.014"].inputs[0])
    tree_links.new(new_nodes["Vector Math.010"].outputs[0], new_nodes["Vector Math.014"].inputs[1])
    tree_links.new(new_nodes["Vector Math.014"].outputs[0], new_nodes["Vector Math.015"].inputs[0])
    tree_links.new(new_nodes["Vector Math.013"].outputs[0], new_nodes["Vector Math.015"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Vector Math.011"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Vector Math.011"].inputs[1])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group

def create_duo_node_vec_div_3e_mod_3e(context, override_create, node_tree_type):
    ensure_node_groups(override_create, [VEC_DIV_3E_MOD_3E_DUO_NG_NAME],
        node_tree_type, create_prereq_duo_node_group)
    node = context.space_data.edit_tree.nodes.new(type=get_node_group_for_type(node_tree_type))
    node.node_tree = bpy.data.node_groups.get(node_group_name_for_name_and_type(VEC_DIV_3E_MOD_3E_DUO_NG_NAME,
                                                                                node_tree_type))

class BSR_VecDiv3eMod3eCreateDuoNode(bpy.types.Operator):
    bl_description = "Add a vector Division (by 1000) and Modulus (by 1000) node"
    bl_idname = "big_space_rig.vec_div_3e_mod_3e_create_duo_node"
    bl_label = "Divide 3e Mod 3e"
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
            self.report({'ERROR'}, "Unable to create VecDiv3eMod3e node because no Big Space Rig given.")
            return {'CANCELLED'}
        bsr_place = scn.BSR_NodeGetInputFromRigPlace
        if bsr_place is None:
            self.report({'ERROR'}, "Unable to create VecDiv3eMod3e node because no Place given.")
            return {'CANCELLED'}
        bpy.ops.node.select_all(action='DESELECT')
        create_duo_node_vec_div_3e_mod_3e(context, False, context.space_data.edit_tree.bl_idname)
        return {'FINISHED'}

def create_duo_vec_div_6e(node_tree_type):
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=node_group_name_for_name_and_type(VEC_DIV_6E_DUO_NG_NAME,
                                                                                     node_tree_type),
                                              type=node_tree_type)
    new_node_group.inputs.new(type='NodeSocketVector', name="Vector 6e")
    new_node_group.inputs.new(type='NodeSocketVector', name="Vector 0e")
    new_node_group.inputs.new(type='NodeSocketVector', name="Vector World")
    new_node_group.outputs.new(type='NodeSocketVector', name="Vector")
    tree_nodes = new_node_group.nodes
    # delete old nodes before adding new nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-190, -70)
    node.operation = "ADD"
    new_nodes["Vector Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-10, -70)
    node.operation = "DIVIDE"
    node.inputs[1].default_value = (1e6, 1e6, 1e6)
    new_nodes["Vector Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (190, 70)
    node.operation = "ADD"
    new_nodes["Vector Math.004"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-390, 0)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (380, 0)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Vector Math.002"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Vector Math.002"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Vector Math.004"].inputs[0])
    tree_links.new(new_nodes["Vector Math.004"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Vector Math.002"].outputs[0], new_nodes["Vector Math.003"].inputs[0])
    tree_links.new(new_nodes["Vector Math.003"].outputs[0], new_nodes["Vector Math.004"].inputs[1])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group

def create_duo_node_vec_div_6e(context, override_create, node_tree_type):
    ensure_node_groups(override_create, [VEC_DIV_6E_DUO_NG_NAME],
        node_tree_type, create_prereq_duo_node_group)
    node = context.space_data.edit_tree.nodes.new(type=get_node_group_for_type(node_tree_type))
    node.node_tree = bpy.data.node_groups.get(node_group_name_for_name_and_type(VEC_DIV_6E_DUO_NG_NAME,
                                                                                node_tree_type))

class BSR_VecDiv6eCreateDuoNode(bpy.types.Operator):
    bl_description = "Add a vector division node for division by one million (1,000,000)"
    bl_idname = "big_space_rig.vec_div_6e_create_duo_node"
    bl_label = "Divide 6e"
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
            self.report({'ERROR'}, "Unable to create VecDiv6e node because no Big Space Rig given.")
            return {'CANCELLED'}
        bsr_place = scn.BSR_NodeGetInputFromRigPlace
        if bsr_place is None:
            self.report({'ERROR'}, "Unable to create VecDiv6e node because no Place given.")
            return {'CANCELLED'}
        bpy.ops.node.select_all(action='DESELECT')
        create_duo_node_vec_div_6e(context, False, context.space_data.edit_tree.bl_idname)
        return {'FINISHED'}

def create_geo_ng_merge_vertex_lod():
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=MERGE_VERT_LOD_GEO_NG_NAME, type='GeometryNodeTree')
    new_node_group.inputs.new(type='NodeSocketGeometry', name="Geometry")
    new_node_group.inputs.new(type='NodeSocketFloat', name="LOD inner verts")
    new_node_group.inputs.new(type='NodeSocketFloat', name="LOD outer verts")
    new_node_group.outputs.new(type='NodeSocketGeometry', name="Geometry")
    tree_nodes = new_node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-20, -280)
    node.operation = "LESS_THAN"
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="GeometryNodeProximity")
    node.location = (-200, -200)
    node.target_element = 'POINTS'
    new_nodes["Geometry Proximity"] = node

    node = tree_nodes.new(type="GeometryNodeSeparateGeometry")
    node.label = "Separate inner verts"
    node.location = (-380, -180)
    node.domain = 'POINT'
    new_nodes["Separate Geometry"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (-380, -340)
    new_nodes["Position.001"] = node

    node = tree_nodes.new(type="FunctionNodeBooleanMath")
    node.location = (160, -180)
    new_nodes["Boolean Math"] = node

    node = tree_nodes.new(type="GeometryNodeSetPosition")
    node.location = (340, -120)
    new_nodes["Set Position"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-160, -20)
    node.operation = "GREATER_THAN"
    node.inputs[1].default_value = 0.5
    new_nodes["Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-380, -480)
    node.operation = "LENGTH"
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-200, -420)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = 0.15
    new_nodes["Math"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-580, -300)
    node.operation = "GREATER_THAN"
    node.inputs[1].default_value = 0.5
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (-560, -520)
    new_nodes["Position"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-760, -140)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (520, -140)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Separate Geometry"].inputs[0])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Separate Geometry"].inputs[1])
    tree_links.new(new_nodes["Set Position"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Separate Geometry"].outputs[0], new_nodes["Geometry Proximity"].inputs[0])
    tree_links.new(new_nodes["Position.001"].outputs[0], new_nodes["Geometry Proximity"].inputs[1])
    tree_links.new(new_nodes["Geometry Proximity"].outputs[0], new_nodes["Set Position"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Set Position"].inputs[0])
    tree_links.new(new_nodes["Position"].outputs[0], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Math.001"].inputs[1])
    tree_links.new(new_nodes["Vector Math"].outputs[1], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Geometry Proximity"].outputs[1], new_nodes["Math.001"].inputs[0])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Boolean Math"].inputs[1])
    tree_links.new(new_nodes["Math.003"].outputs[0], new_nodes["Boolean Math"].inputs[0])
    tree_links.new(new_nodes["Boolean Math"].outputs[0], new_nodes["Set Position"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Math.002"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Math.003"].inputs[0])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group

def create_geo_node_merge_vertex_lod(context, override_create):
    ensure_node_groups(override_create, [MERGE_VERT_LOD_GEO_NG_NAME], 'GeometryNodeTree', create_prereq_mono_node_group)
    node = context.space_data.edit_tree.nodes.new(type='GeometryNodeGroup')
    node.node_tree = bpy.data.node_groups.get(MERGE_VERT_LOD_GEO_NG_NAME)

class BSR_MergeVertexLOD_CreateGeoNode(bpy.types.Operator):
    bl_description = "Create node to fix 'holes' between level-of-detail geometry in MegaSphere, which usually " \
        "show up after adding displacements to MegaSphere geometry - e.g. Noise texture displacements"
    bl_idname = "big_space_rig.merge_vertex_lod_create_geo_node"
    bl_label = "Merge Vertex LOD"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        s = context.space_data
        if s.type == 'NODE_EDITOR' and s.node_tree != None and \
            s.tree_type in ['GeometryNodeTree']:
            return True
        return False

    def execute(self, context):
        scn = context.scene
        big_space_rig = bpy.data.objects.get(scn.BSR_NodeGetInputFromRig)
        if big_space_rig is None:
            self.report({'ERROR'}, "Unable to create Merge Vertex LOD node because no Big Space Rig given.")
            return {'CANCELLED'}
        bsr_place = scn.BSR_NodeGetInputFromRigPlace
        if bsr_place is None:
            self.report({'ERROR'}, "Unable to create Merge Vertex LOD node because no Place given.")
            return {'CANCELLED'}
        bpy.ops.node.select_all(action='DESELECT')
        create_geo_node_merge_vertex_lod(context, False)
        return {'FINISHED'}
