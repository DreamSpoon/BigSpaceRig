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

import math

import bpy

from .node_other import (is_duo_node_group_name, ensure_node_groups, node_group_name_for_name_and_type,
    get_node_group_for_type)
from .rig import (PROXY_OBSERVER_0E_BNAME, PROXY_OBSERVER_6E_BNAME, OBSERVER_FOCUS_BNAME)
from .rig import get_6e_0e_from_place_bone_name

VEC_DIV_3E_MOD_3E_DUO_NG_NAME = "VecDiv3eMod3e.BSR"
VEC_DIV_6E_DUO_NG_NAME = "VecDiv6e.BSR"
VEC_DIV_5E_DUO_NG_NAME = "VecDiv5e.BSR"
VEC_DIV_4E_DUO_NG_NAME = "VecDiv4e.BSR"

TILE_XYZ_3E_DUO_NG_NAME = "TileXYZ3e.BSR"

SNAP_VERT_LOD_GEO_NG_NAME = "SnapVertexLOD.BSR.GeoNG"

SUBDIV_SURF_WITH_INDEX_GEO_NG_NAME = "SubdivSurfWithIndex.BSR.GeoNG"
SUBDIV_MESH_WITH_INDEX_GEO_NG_NAME = "SubdivMeshWithIndex.BSR.GeoNG"

# depending on the name passed to function, create the right set of nodes in a group and pass back
def create_prereq_util_node_group(node_group_name, node_tree_type):
    if is_duo_node_group_name(node_group_name, VEC_DIV_3E_MOD_3E_DUO_NG_NAME):
        return create_duo_vec_div3e_mod_3e(node_tree_type)
    elif is_duo_node_group_name(node_group_name, VEC_DIV_6E_DUO_NG_NAME):
        return create_duo_vec_div_6e(node_tree_type)
    elif is_duo_node_group_name(node_group_name, VEC_DIV_5E_DUO_NG_NAME):
        return create_duo_vec_div_5e(node_tree_type)
    elif is_duo_node_group_name(node_group_name, VEC_DIV_4E_DUO_NG_NAME):
        return create_duo_vec_div_4e(node_tree_type)
    elif is_duo_node_group_name(node_group_name, TILE_XYZ_3E_DUO_NG_NAME):
        return create_duo_ng_tile_xyz_3e(node_tree_type)

    if node_tree_type == 'GeometryNodeTree':
        if node_group_name == SNAP_VERT_LOD_GEO_NG_NAME:
            return create_geo_ng_snap_vertex_lod()
        elif node_group_name ==  SUBDIV_MESH_WITH_INDEX_GEO_NG_NAME:
            return create_geo_ng_subdiv_mesh_with_index()
        elif node_group_name ==  SUBDIV_SURF_WITH_INDEX_GEO_NG_NAME:
            return create_geo_ng_subdiv_surf_with_index()

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
    node.location.y = node.location.y + node_loc_offset[1] - 125
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

    node = tree_nodes.new(type=node_input_type)
    node.label = "Observer Focus"
    node.location.x = node.location.x + node_loc_offset[0]
    node.location.y = node.location.y + node_loc_offset[1] - 250
    if node_tree_type in ['CompositorNodeTree', 'ShaderNodeTree', 'TextureNodeTree']:
        # combine XYZ driver X
        drv_loc_x = node.inputs[0].driver_add('default_value').driver
        v_obs_loc_x = drv_loc_x.variables.new()
        v_obs_loc_x.type = 'TRANSFORMS'
        v_obs_loc_x.name = "var"
        v_obs_loc_x.targets[0].id = big_space_rig
        v_obs_loc_x.targets[0].bone_target = OBSERVER_FOCUS_BNAME
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
        v_obs_loc_y.targets[0].bone_target = OBSERVER_FOCUS_BNAME
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
        v_obs_loc_z.targets[0].bone_target = OBSERVER_FOCUS_BNAME
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
        v_obs_loc_x.targets[0].bone_target = OBSERVER_FOCUS_BNAME
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
        v_obs_loc_y.targets[0].bone_target = OBSERVER_FOCUS_BNAME
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
        v_obs_loc_z.targets[0].bone_target = OBSERVER_FOCUS_BNAME
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
        big_space_rig = bpy.data.objects.get(scn.BSR_NodeGetInputFromRig[1:len(scn.BSR_NodeGetInputFromRig)])
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

    place_bone_name_6e, place_bone_name_0e = get_6e_0e_from_place_bone_name(big_space_rig, bsr_place)
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
    node.location.y = node.location.y + node_loc_offset[1] - 125
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
        big_space_rig = bpy.data.objects.get(scn.BSR_NodeGetInputFromRig[1:len(scn.BSR_NodeGetInputFromRig)])
        if big_space_rig is None:
            self.report({'ERROR'}, "Unable to Create Place Position Input node because no Big Space Rig given.")
            return {'CANCELLED'}
        bsr_place = scn.BSR_NodeGetInputFromRigPlace[1:len(scn.BSR_NodeGetInputFromRigPlace)]
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
        big_space_rig = bpy.data.objects.get(scn.BSR_NodeGetInputFromRig[1:len(scn.BSR_NodeGetInputFromRig)])
        if big_space_rig is None:
            self.report({'ERROR'}, "Unable to Create Offset Place Position Input node because no Big Space Rig given.")
            return {'CANCELLED'}
        bsr_place = scn.BSR_NodeGetInputFromRigPlace[1:len(scn.BSR_NodeGetInputFromRigPlace)]
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
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-480, 20)
    node.operation = "ADD"
    new_nodes["Vector Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (60, 140)
    node.operation = "ADD"
    new_nodes["Vector Math.006"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-480, 180)
    node.operation = "FRACTION"
    new_nodes["Vector Math.012"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-300, 260)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = (1e3, 1e3, 1e3)
    new_nodes["Vector Math.011"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-120, 180)
    node.operation = "FLOOR"
    new_nodes["Vector Math.010"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-120, 20)
    node.operation = "FRACTION"
    new_nodes["Vector Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-300, 40)
    node.operation = "DIVIDE"
    node.inputs[1].default_value = (1e3, 1e3, 1e3)
    new_nodes["Vector Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-300, -180)
    node.operation = "ADD"
    new_nodes["Vector Math.008"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-120, -140)
    node.operation = "DIVIDE"
    node.inputs[1].default_value = (1e3, 1e3, 1e3)
    new_nodes["Vector Math.014"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (60, -80)
    node.operation = "FLOOR"
    new_nodes["Vector Math.013"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (240, 60)
    node.operation = "ADD"
    new_nodes["Vector Math.007"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-660, -60)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (420, 20)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Vector Math.012"].inputs[0])
    tree_links.new(new_nodes["Vector Math.007"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Vector Math.012"].outputs[0], new_nodes["Vector Math.011"].inputs[0])
    tree_links.new(new_nodes["Vector Math.011"].outputs[0], new_nodes["Vector Math.010"].inputs[0])
    tree_links.new(new_nodes["Vector Math.002"].outputs[0], new_nodes["Vector Math.005"].inputs[0])
    tree_links.new(new_nodes["Vector Math.010"].outputs[0], new_nodes["Vector Math.006"].inputs[0])
    tree_links.new(new_nodes["Vector Math.005"].outputs[0], new_nodes["Vector Math.006"].inputs[1])
    tree_links.new(new_nodes["Vector Math.014"].outputs[0], new_nodes["Vector Math.013"].inputs[0])
    tree_links.new(new_nodes["Vector Math.006"].outputs[0], new_nodes["Vector Math.007"].inputs[0])
    tree_links.new(new_nodes["Vector Math.013"].outputs[0], new_nodes["Vector Math.007"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Vector Math.004"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Vector Math.004"].inputs[1])
    tree_links.new(new_nodes["Vector Math.004"].outputs[0], new_nodes["Vector Math.002"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Vector Math.008"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Vector Math.008"].inputs[1])
    tree_links.new(new_nodes["Vector Math.008"].outputs[0], new_nodes["Vector Math.014"].inputs[0])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group

def create_duo_node_vec_div_3e_mod_3e(context, override_create, node_tree_type):
    ensure_node_groups(override_create, [node_group_name_for_name_and_type(VEC_DIV_3E_MOD_3E_DUO_NG_NAME,
                                                                           node_tree_type)],
        node_tree_type, create_prereq_util_node_group)
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
        bpy.ops.node.select_all(action='DESELECT')
        create_duo_node_vec_div_3e_mod_3e(context, scn.BSR_NodesOverrideCreate, context.space_data.edit_tree.bl_idname)
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
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-60, -280)
    node.operation = "FLOOR"
    new_nodes["Vector Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-240, -280)
    node.operation = "DIVIDE"
    node.inputs[1].default_value = (1000.0, 1000.0, 1000.0)
    new_nodes["Vector Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (120, -280)
    node.operation = "DIVIDE"
    node.inputs[1].default_value = (1000.0, 1000.0, 1000.0)
    new_nodes["Vector Math.007"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (120, -480)
    node.operation = "DIVIDE"
    node.inputs[1].default_value = (1000.0, 1000.0, 1000.0)
    new_nodes["Vector Math.008"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (300, -280)
    node.operation = "ADD"
    new_nodes["Vector Math.009"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (300, -480)
    node.operation = "ADD"
    new_nodes["Vector Math.010"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (300, -700)
    node.operation = "FRACTION"
    new_nodes["Vector Math.006"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-420, -280)
    node.operation = "ADD"
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (660, -480)
    node.operation = "MULTIPLY"
    new_nodes["Vector Math.013"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (840, -480)
    node.operation = "MULTIPLY_ADD"
    new_nodes["Vector Math.012"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (480, -640)
    node.operation = "SUBTRACT"
    node.inputs[0].default_value = (1.0, 1.0, 1.0)
    new_nodes["Vector Math.011"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-60, -480)
    node.operation = "ADD"
    node.inputs[1].default_value = (1.0, 1.0, 1.0)
    new_nodes["Vector Math.004"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-620, -440)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (1020, -480)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Vector Math"].inputs[1])
    tree_links.new(new_nodes["Vector Math"].outputs[0], new_nodes["Vector Math.005"].inputs[0])
    tree_links.new(new_nodes["Vector Math.005"].outputs[0], new_nodes["Vector Math.003"].inputs[0])
    tree_links.new(new_nodes["Vector Math.003"].outputs[0], new_nodes["Vector Math.004"].inputs[0])
    tree_links.new(new_nodes["Vector Math.005"].outputs[0], new_nodes["Vector Math.006"].inputs[0])
    tree_links.new(new_nodes["Vector Math.003"].outputs[0], new_nodes["Vector Math.007"].inputs[0])
    tree_links.new(new_nodes["Vector Math.004"].outputs[0], new_nodes["Vector Math.008"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Vector Math.009"].inputs[0])
    tree_links.new(new_nodes["Vector Math.007"].outputs[0], new_nodes["Vector Math.009"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Vector Math.010"].inputs[0])
    tree_links.new(new_nodes["Vector Math.008"].outputs[0], new_nodes["Vector Math.010"].inputs[1])
    tree_links.new(new_nodes["Vector Math.006"].outputs[0], new_nodes["Vector Math.011"].inputs[1])
    tree_links.new(new_nodes["Vector Math.009"].outputs[0], new_nodes["Vector Math.012"].inputs[0])
    tree_links.new(new_nodes["Vector Math.010"].outputs[0], new_nodes["Vector Math.013"].inputs[0])
    tree_links.new(new_nodes["Vector Math.013"].outputs[0], new_nodes["Vector Math.012"].inputs[2])
    tree_links.new(new_nodes["Vector Math.012"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Vector Math.006"].outputs[0], new_nodes["Vector Math.013"].inputs[1])
    tree_links.new(new_nodes["Vector Math.011"].outputs[0], new_nodes["Vector Math.012"].inputs[1])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group

def create_duo_node_vec_div_6e(context, override_create, node_tree_type):
    ensure_node_groups(override_create, [node_group_name_for_name_and_type(VEC_DIV_6E_DUO_NG_NAME, node_tree_type)],
        node_tree_type, create_prereq_util_node_group)
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
        bpy.ops.node.select_all(action='DESELECT')
        create_duo_node_vec_div_6e(context, scn.BSR_NodesOverrideCreate, context.space_data.edit_tree.bl_idname)
        return {'FINISHED'}

def create_duo_vec_div_5e(node_tree_type):
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=node_group_name_for_name_and_type(VEC_DIV_5E_DUO_NG_NAME,
                                                                                     node_tree_type),
                                              type=node_tree_type)
    new_node_group.inputs.new(type='NodeSocketVector', name="Vector 6e")
    new_node_group.inputs.new(type='NodeSocketVector', name="Vector 0e")
    new_node_group.inputs.new(type='NodeSocketVector', name="Vector World")
    new_node_group.outputs.new(type='NodeSocketVector', name="Vector")
    tree_nodes = new_node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-60, -280)
    node.operation = "FLOOR"
    new_nodes["Vector Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (120, -280)
    node.operation = "DIVIDE"
    node.inputs[1].default_value = (100.0, 100.0, 100.0)
    new_nodes["Vector Math.007"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (120, -480)
    node.operation = "DIVIDE"
    node.inputs[1].default_value = (100.0, 100.0, 100.0)
    new_nodes["Vector Math.008"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (300, -480)
    node.operation = "ADD"
    new_nodes["Vector Math.010"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (300, -700)
    node.operation = "FRACTION"
    new_nodes["Vector Math.006"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-420, -280)
    node.operation = "ADD"
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (660, -480)
    node.operation = "MULTIPLY"
    new_nodes["Vector Math.013"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (840, -480)
    node.operation = "MULTIPLY_ADD"
    new_nodes["Vector Math.012"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (480, -640)
    node.operation = "SUBTRACT"
    node.inputs[0].default_value = (1.0, 1.0, 1.0)
    new_nodes["Vector Math.011"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-60, -480)
    node.operation = "ADD"
    node.inputs[1].default_value = (1.0, 1.0, 1.0)
    new_nodes["Vector Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-240, -280)
    node.operation = "DIVIDE"
    node.inputs[1].default_value = (1000.0, 1000.0, 1000.0)
    new_nodes["Vector Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (300, -280)
    node.operation = "ADD"
    new_nodes["Vector Math.009"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-320, -580)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = (10.0, 10.0, 10.0)
    new_nodes["Vector Math.014"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-620, -440)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (1020, -480)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Vector Math"].inputs[1])
    tree_links.new(new_nodes["Vector Math"].outputs[0], new_nodes["Vector Math.005"].inputs[0])
    tree_links.new(new_nodes["Vector Math.005"].outputs[0], new_nodes["Vector Math.003"].inputs[0])
    tree_links.new(new_nodes["Vector Math.003"].outputs[0], new_nodes["Vector Math.004"].inputs[0])
    tree_links.new(new_nodes["Vector Math.005"].outputs[0], new_nodes["Vector Math.006"].inputs[0])
    tree_links.new(new_nodes["Vector Math.003"].outputs[0], new_nodes["Vector Math.007"].inputs[0])
    tree_links.new(new_nodes["Vector Math.004"].outputs[0], new_nodes["Vector Math.008"].inputs[0])
    tree_links.new(new_nodes["Vector Math.007"].outputs[0], new_nodes["Vector Math.009"].inputs[1])
    tree_links.new(new_nodes["Vector Math.008"].outputs[0], new_nodes["Vector Math.010"].inputs[1])
    tree_links.new(new_nodes["Vector Math.006"].outputs[0], new_nodes["Vector Math.011"].inputs[1])
    tree_links.new(new_nodes["Vector Math.009"].outputs[0], new_nodes["Vector Math.012"].inputs[0])
    tree_links.new(new_nodes["Vector Math.010"].outputs[0], new_nodes["Vector Math.013"].inputs[0])
    tree_links.new(new_nodes["Vector Math.013"].outputs[0], new_nodes["Vector Math.012"].inputs[2])
    tree_links.new(new_nodes["Vector Math.012"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Vector Math.006"].outputs[0], new_nodes["Vector Math.013"].inputs[1])
    tree_links.new(new_nodes["Vector Math.011"].outputs[0], new_nodes["Vector Math.012"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Vector Math.014"].inputs[0])
    tree_links.new(new_nodes["Vector Math.014"].outputs[0], new_nodes["Vector Math.009"].inputs[0])
    tree_links.new(new_nodes["Vector Math.014"].outputs[0], new_nodes["Vector Math.010"].inputs[0])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False
    return new_node_group

def create_duo_node_vec_div_5e(context, override_create, node_tree_type):
    ensure_node_groups(override_create, [node_group_name_for_name_and_type(VEC_DIV_5E_DUO_NG_NAME, node_tree_type)],
        node_tree_type, create_prereq_util_node_group)
    node = context.space_data.edit_tree.nodes.new(type=get_node_group_for_type(node_tree_type))
    node.node_tree = bpy.data.node_groups.get(node_group_name_for_name_and_type(VEC_DIV_5E_DUO_NG_NAME,
                                                                                node_tree_type))

class BSR_VecDiv5eCreateDuoNode(bpy.types.Operator):
    bl_description = "Add a vector division node for division by one hundred thousand (100,000)"
    bl_idname = "big_space_rig.vec_div_5e_create_duo_node"
    bl_label = "Divide 5e"
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
        bpy.ops.node.select_all(action='DESELECT')
        create_duo_node_vec_div_5e(context, scn.BSR_NodesOverrideCreate, context.space_data.edit_tree.bl_idname)
        return {'FINISHED'}

def create_duo_vec_div_4e(node_tree_type):
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=node_group_name_for_name_and_type(VEC_DIV_4E_DUO_NG_NAME,
                                                                                     node_tree_type),
                                              type=node_tree_type)
    new_node_group.inputs.new(type='NodeSocketVector', name="Vector 6e")
    new_node_group.inputs.new(type='NodeSocketVector', name="Vector 0e")
    new_node_group.inputs.new(type='NodeSocketVector', name="Vector World")
    new_node_group.outputs.new(type='NodeSocketVector', name="Vector")
    tree_nodes = new_node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-60, -280)
    node.operation = "FLOOR"
    new_nodes["Vector Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (120, -280)
    node.operation = "DIVIDE"
    node.inputs[1].default_value = (10.0, 10.0, 10.0)
    new_nodes["Vector Math.007"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (120, -480)
    node.operation = "DIVIDE"
    node.inputs[1].default_value = (10.0, 10.0, 10.0)
    new_nodes["Vector Math.008"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (300, -480)
    node.operation = "ADD"
    new_nodes["Vector Math.010"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (300, -700)
    node.operation = "FRACTION"
    new_nodes["Vector Math.006"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-420, -280)
    node.operation = "ADD"
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (660, -480)
    node.operation = "MULTIPLY"
    new_nodes["Vector Math.013"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (840, -480)
    node.operation = "MULTIPLY_ADD"
    new_nodes["Vector Math.012"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (480, -640)
    node.operation = "SUBTRACT"
    node.inputs[0].default_value = (1.0, 1.0, 1.0)
    new_nodes["Vector Math.011"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-60, -480)
    node.operation = "ADD"
    node.inputs[1].default_value = (1.0, 1.0, 1.0)
    new_nodes["Vector Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-240, -280)
    node.operation = "DIVIDE"
    node.inputs[1].default_value = (1000.0, 1000.0, 1000.0)
    new_nodes["Vector Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (300, -280)
    node.operation = "ADD"
    new_nodes["Vector Math.009"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-320, -580)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = (100.0, 100.0, 100.0)
    new_nodes["Vector Math.014"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-620, -440)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (1020, -480)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Vector Math"].inputs[1])
    tree_links.new(new_nodes["Vector Math"].outputs[0], new_nodes["Vector Math.005"].inputs[0])
    tree_links.new(new_nodes["Vector Math.005"].outputs[0], new_nodes["Vector Math.003"].inputs[0])
    tree_links.new(new_nodes["Vector Math.003"].outputs[0], new_nodes["Vector Math.004"].inputs[0])
    tree_links.new(new_nodes["Vector Math.005"].outputs[0], new_nodes["Vector Math.006"].inputs[0])
    tree_links.new(new_nodes["Vector Math.003"].outputs[0], new_nodes["Vector Math.007"].inputs[0])
    tree_links.new(new_nodes["Vector Math.004"].outputs[0], new_nodes["Vector Math.008"].inputs[0])
    tree_links.new(new_nodes["Vector Math.007"].outputs[0], new_nodes["Vector Math.009"].inputs[1])
    tree_links.new(new_nodes["Vector Math.008"].outputs[0], new_nodes["Vector Math.010"].inputs[1])
    tree_links.new(new_nodes["Vector Math.006"].outputs[0], new_nodes["Vector Math.011"].inputs[1])
    tree_links.new(new_nodes["Vector Math.009"].outputs[0], new_nodes["Vector Math.012"].inputs[0])
    tree_links.new(new_nodes["Vector Math.010"].outputs[0], new_nodes["Vector Math.013"].inputs[0])
    tree_links.new(new_nodes["Vector Math.013"].outputs[0], new_nodes["Vector Math.012"].inputs[2])
    tree_links.new(new_nodes["Vector Math.012"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Vector Math.006"].outputs[0], new_nodes["Vector Math.013"].inputs[1])
    tree_links.new(new_nodes["Vector Math.011"].outputs[0], new_nodes["Vector Math.012"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Vector Math.014"].inputs[0])
    tree_links.new(new_nodes["Vector Math.014"].outputs[0], new_nodes["Vector Math.009"].inputs[0])
    tree_links.new(new_nodes["Vector Math.014"].outputs[0], new_nodes["Vector Math.010"].inputs[0])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False
    return new_node_group

def create_duo_node_vec_div_4e(context, override_create, node_tree_type):
    ensure_node_groups(override_create, [node_group_name_for_name_and_type(VEC_DIV_4E_DUO_NG_NAME, node_tree_type)],
        node_tree_type, create_prereq_util_node_group)
    node = context.space_data.edit_tree.nodes.new(type=get_node_group_for_type(node_tree_type))
    node.node_tree = bpy.data.node_groups.get(node_group_name_for_name_and_type(VEC_DIV_4E_DUO_NG_NAME,
                                                                                node_tree_type))

class BSR_VecDiv4eCreateDuoNode(bpy.types.Operator):
    bl_description = "Add a vector division node for division by ten thousand (10,000)"
    bl_idname = "big_space_rig.vec_div_4e_create_duo_node"
    bl_label = "Divide 4e"
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
        bpy.ops.node.select_all(action='DESELECT')
        create_duo_node_vec_div_4e(context, scn.BSR_NodesOverrideCreate, context.space_data.edit_tree.bl_idname)
        return {'FINISHED'}

def create_geo_ng_snap_vertex_lod():
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=SNAP_VERT_LOD_GEO_NG_NAME, type='GeometryNodeTree')
    new_node_group.inputs.new(type='NodeSocketGeometry', name="Geometry")
    new_node_group.inputs.new(type='NodeSocketFloat', name="LOD inner verts")
    new_node_group.inputs.new(type='NodeSocketFloat', name="LOD outer verts")
    new_node_group.outputs.new(type='NodeSocketGeometry', name="Geometry")
    tree_nodes = new_node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="GeometryNodeProximity")
    node.location = (-200, -320)
    node.target_element = 'POINTS'
    new_nodes["Geometry Proximity"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (-380, -460)
    new_nodes["Position"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (-560, -640)
    new_nodes["Position.001"] = node

    node = tree_nodes.new(type="GeometryNodeSetPosition")
    node.location = (520, -120)
    new_nodes["Set Position"] = node

    node = tree_nodes.new(type="GeometryNodeSeparateGeometry")
    node.label = "Separate inner verts"
    node.location = (-380, -300)
    node.domain = 'POINT'
    new_nodes["Separate Geometry"] = node

    node = tree_nodes.new(type="GeometryNodeAttributeDomainSize")
    node.location = (-20, 20)
    new_nodes["Domain Size"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-20, -400)
    node.operation = "LESS_THAN"
    node.inputs[2].default_value = 0.5
    new_nodes["Math"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-200, -540)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = 0.15
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (160, 0)
    node.operation = "GREATER_THAN"
    node.inputs[1].default_value = 0.0
    new_nodes["Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-20, -180)
    node.operation = "GREATER_THAN"
    node.inputs[1].default_value = 0.5
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-580, -380)
    node.operation = "GREATER_THAN"
    node.inputs[1].default_value = 0.5
    new_nodes["Math.003"] = node

    node = tree_nodes.new(type="FunctionNodeBooleanMath")
    node.location = (340, -180)
    node.operation = 'AND'
    new_nodes["Boolean Math.001"] = node

    node = tree_nodes.new(type="FunctionNodeBooleanMath")
    node.location = (160, -260)
    node.operation = 'AND'
    new_nodes["Boolean Math"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-380, -600)
    node.operation = "LENGTH"
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-760, -200)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (700, -120)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Separate Geometry"].inputs[0])
    tree_links.new(new_nodes["Math.003"].outputs[0], new_nodes["Separate Geometry"].inputs[1])
    tree_links.new(new_nodes["Set Position"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Separate Geometry"].outputs[0], new_nodes["Geometry Proximity"].inputs[0])
    tree_links.new(new_nodes["Position"].outputs[0], new_nodes["Geometry Proximity"].inputs[1])
    tree_links.new(new_nodes["Geometry Proximity"].outputs[0], new_nodes["Set Position"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Set Position"].inputs[0])
    tree_links.new(new_nodes["Position.001"].outputs[0], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Math"].inputs[1])
    tree_links.new(new_nodes["Vector Math"].outputs[1], new_nodes["Math.002"].inputs[0])
    tree_links.new(new_nodes["Geometry Proximity"].outputs[1], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Boolean Math"].inputs[1])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Boolean Math"].inputs[0])
    tree_links.new(new_nodes["Boolean Math.001"].outputs[0], new_nodes["Set Position"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Math.003"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Math.001"].inputs[0])
    tree_links.new(new_nodes["Domain Size"].outputs[0], new_nodes["Math.004"].inputs[0])
    tree_links.new(new_nodes["Separate Geometry"].outputs[0], new_nodes["Domain Size"].inputs[0])
    tree_links.new(new_nodes["Boolean Math"].outputs[0], new_nodes["Boolean Math.001"].inputs[1])
    tree_links.new(new_nodes["Math.004"].outputs[0], new_nodes["Boolean Math.001"].inputs[0])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group

def create_geo_node_snap_vertex_lod(context, override_create):
    ensure_node_groups(override_create, [SNAP_VERT_LOD_GEO_NG_NAME],
                       'GeometryNodeTree', create_prereq_util_node_group)
    node = context.space_data.edit_tree.nodes.new(type='GeometryNodeGroup')
    node.node_tree = bpy.data.node_groups.get(SNAP_VERT_LOD_GEO_NG_NAME)

class BSR_SnapVertexLOD_CreateGeoNode(bpy.types.Operator):
    bl_description = "Create node to fix 'holes' between level-of-detail geometry in MegaSphere, which usually " \
        "show up after adding displacements to MegaSphere geometry - e.g. Noise texture displacements"
    bl_idname = "big_space_rig.snap_vertex_lod_create_geo_node"
    bl_label = "Snap Vertex LOD"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        s = context.space_data
        if s.type == 'NODE_EDITOR' and s.node_tree != None and s.tree_type == 'GeometryNodeTree':
            return True
        return False

    def execute(self, context):
        scn = context.scene
        big_space_rig = bpy.data.objects.get(scn.BSR_NodeGetInputFromRig[1:len(scn.BSR_NodeGetInputFromRig)])
        if big_space_rig is None:
            self.report({'ERROR'}, "Unable to create Snap Vertex LOD node because no Big Space Rig given.")
            return {'CANCELLED'}
        bsr_place = scn.BSR_NodeGetInputFromRigPlace[1:len(scn.BSR_NodeGetInputFromRigPlace)]
        if bsr_place is None:
            self.report({'ERROR'}, "Unable to create Snap Vertex LOD node because no Place given.")
            return {'CANCELLED'}
        bpy.ops.node.select_all(action='DESELECT')
        create_geo_node_snap_vertex_lod(context, scn.BSR_NodesOverrideCreate)
        return {'FINISHED'}

def create_duo_ng_tile_xyz_3e(node_tree_type):
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=node_group_name_for_name_and_type(TILE_XYZ_3E_DUO_NG_NAME,
                                                                                     node_tree_type),
                                              type=node_tree_type)
    new_node_group.inputs.new(type='NodeSocketVector', name="Vector 0e")
    new_node_group.inputs.new(type='NodeSocketVector', name="Vector World")
    new_node_group.outputs.new(type='NodeSocketVector', name="XYZ")
    new_node_group.outputs.new(type='NodeSocketFloat', name="W")
    tree_nodes = new_node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (260, 720)
    new_nodes["Separate XYZ"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (260, 580)
    new_nodes["Separate XYZ.001"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (1080, 520)
    new_nodes["Combine XYZ"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (720, 520)
    node.operation = "MULTIPLY"
    new_nodes["Math"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (540, 520)
    node.operation = "MULTIPLY"
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Y"
    node.location = (900, 520)
    node.operation = "ADD"
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (720, 360)
    node.operation = "MULTIPLY"
    new_nodes["Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (540, 360)
    node.operation = "MULTIPLY"
    new_nodes["Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (720, 160)
    node.operation = "MULTIPLY"
    new_nodes["Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (540, 160)
    node.operation = "MULTIPLY"
    new_nodes["Math.006"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Z"
    node.location = (900, 160)
    node.operation = "SUBTRACT"
    new_nodes["Math.007"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (540, 0)
    node.operation = "MULTIPLY"
    new_nodes["Math.008"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (720, 0)
    node.operation = "MULTIPLY"
    new_nodes["Math.009"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (540, 880)
    node.operation = "MULTIPLY"
    new_nodes["Math.010"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (720, 880)
    node.operation = "MULTIPLY"
    new_nodes["Math.011"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (540, 720)
    node.operation = "MULTIPLY"
    new_nodes["Math.012"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (720, 720)
    node.operation = "MULTIPLY"
    new_nodes["Math.013"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (720, 1240)
    node.operation = "MULTIPLY"
    new_nodes["Math.014"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (540, 1240)
    node.operation = "MULTIPLY"
    new_nodes["Math.015"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (540, 1080)
    node.operation = "MULTIPLY"
    new_nodes["Math.016"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (720, 1080)
    node.operation = "MULTIPLY"
    new_nodes["Math.017"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "W"
    node.location = (900, 1080)
    node.operation = "ADD"
    new_nodes["Math.018"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "X"
    node.location = (900, 720)
    node.operation = "SUBTRACT"
    new_nodes["Math.019"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (80, 720)
    node.operation = "COSINE"
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (80, 580)
    node.operation = "SINE"
    new_nodes["Vector Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-100, 720)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = (math.pi*2, math.pi*2, math.pi*2)
    new_nodes["Vector Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (1260, 520)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = (1000.0, 1000.0, 1000.0)
    new_nodes["Vector Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1260, 720)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = 1000.0
    new_nodes["Math.021"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-820, 720)
    node.operation = "DIVIDE"
    node.inputs[1].default_value = (1000.0, 1000.0, 1000.0)
    new_nodes["Vector Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-460, 720)
    node.operation = "ADD"
    new_nodes["Vector Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-640, 720)
    node.operation = "FRACTION"
    new_nodes["Vector Math.006"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-820, 520)
    node.operation = "DIVIDE"
    node.inputs[1].default_value = (1000.0, 1000.0, 1000.0)
    new_nodes["Vector Math.007"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-280, 720)
    node.operation = "FRACTION"
    new_nodes["Vector Math.008"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-1000, 720)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (1440, 720)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Math.015"].outputs[0], new_nodes["Math.014"].inputs[0])
    tree_links.new(new_nodes["Math.016"].outputs[0], new_nodes["Math.017"].inputs[0])
    tree_links.new(new_nodes["Math.014"].outputs[0], new_nodes["Math.018"].inputs[0])
    tree_links.new(new_nodes["Math.017"].outputs[0], new_nodes["Math.018"].inputs[1])
    tree_links.new(new_nodes["Math.010"].outputs[0], new_nodes["Math.011"].inputs[0])
    tree_links.new(new_nodes["Math.012"].outputs[0], new_nodes["Math.013"].inputs[0])
    tree_links.new(new_nodes["Math.011"].outputs[0], new_nodes["Math.019"].inputs[0])
    tree_links.new(new_nodes["Math.013"].outputs[0], new_nodes["Math.019"].inputs[1])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Math.004"].outputs[0], new_nodes["Math.003"].inputs[0])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Math.002"].inputs[0])
    tree_links.new(new_nodes["Math.003"].outputs[0], new_nodes["Math.002"].inputs[1])
    tree_links.new(new_nodes["Math.006"].outputs[0], new_nodes["Math.005"].inputs[0])
    tree_links.new(new_nodes["Math.008"].outputs[0], new_nodes["Math.009"].inputs[0])
    tree_links.new(new_nodes["Math.005"].outputs[0], new_nodes["Math.007"].inputs[0])
    tree_links.new(new_nodes["Math.009"].outputs[0], new_nodes["Math.007"].inputs[1])
    tree_links.new(new_nodes["Math.019"].outputs[0], new_nodes["Combine XYZ"].inputs[0])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Combine XYZ"].inputs[1])
    tree_links.new(new_nodes["Math.007"].outputs[0], new_nodes["Combine XYZ"].inputs[2])
    tree_links.new(new_nodes["Combine XYZ"].outputs[0], new_nodes["Vector Math.003"].inputs[0])
    tree_links.new(new_nodes["Vector Math.002"].outputs[0], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Vector Math.002"].outputs[0], new_nodes["Vector Math.001"].inputs[0])
    tree_links.new(new_nodes["Vector Math"].outputs[0], new_nodes["Separate XYZ"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ"].outputs[0], new_nodes["Math.015"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ"].outputs[0], new_nodes["Math.010"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ"].outputs[0], new_nodes["Math.001"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ"].outputs[0], new_nodes["Math.008"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ"].outputs[1], new_nodes["Math.015"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ"].outputs[1], new_nodes["Math.010"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ"].outputs[1], new_nodes["Math.004"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ"].outputs[1], new_nodes["Math.006"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ"].outputs[2], new_nodes["Math.014"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ"].outputs[2], new_nodes["Math.013"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ"].outputs[2], new_nodes["Math"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ"].outputs[2], new_nodes["Math.005"].inputs[1])
    tree_links.new(new_nodes["Vector Math.001"].outputs[0], new_nodes["Separate XYZ.001"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[0], new_nodes["Math.016"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[0], new_nodes["Math.012"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[0], new_nodes["Math.004"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[0], new_nodes["Math.006"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[1], new_nodes["Math.008"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[1], new_nodes["Math.001"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[1], new_nodes["Math.012"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[1], new_nodes["Math.016"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[2], new_nodes["Math.009"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[2], new_nodes["Math.003"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[2], new_nodes["Math.011"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[2], new_nodes["Math.017"].inputs[1])
    tree_links.new(new_nodes["Math.018"].outputs[0], new_nodes["Math.021"].inputs[0])
    tree_links.new(new_nodes["Vector Math.003"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Math.021"].outputs[0], new_nodes["Group Output"].inputs[1])
    tree_links.new(new_nodes["Vector Math.004"].outputs[0], new_nodes["Vector Math.006"].inputs[0])
    tree_links.new(new_nodes["Vector Math.006"].outputs[0], new_nodes["Vector Math.005"].inputs[0])
    tree_links.new(new_nodes["Vector Math.007"].outputs[0], new_nodes["Vector Math.005"].inputs[1])
    tree_links.new(new_nodes["Vector Math.005"].outputs[0], new_nodes["Vector Math.008"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Vector Math.004"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Vector Math.007"].inputs[0])
    tree_links.new(new_nodes["Vector Math.008"].outputs[0], new_nodes["Vector Math.002"].inputs[0])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group

def create_duo_node_tile_xyz_3e(context, override_create, node_tree_type):
    ensure_node_groups(override_create, [node_group_name_for_name_and_type(TILE_XYZ_3E_DUO_NG_NAME, node_tree_type)],
                       node_tree_type, create_prereq_util_node_group)
    node = context.space_data.edit_tree.nodes.new(type=get_node_group_for_type(node_tree_type))
    node.node_tree = bpy.data.node_groups.get(node_group_name_for_name_and_type(TILE_XYZ_3E_DUO_NG_NAME,
                                                                                node_tree_type))

class BSR_TileXYZ3eCreateDuoNode(bpy.types.Operator):
    bl_description = "Add a Tile XYZ 3e node"
    bl_idname = "big_space_rig.tile_xyz_3e_create_duo_node"
    bl_label = "Tile XYZ 3e"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        s = context.space_data
        if s.type == 'NODE_EDITOR' and s.node_tree != None and \
            s.tree_type in ('CompositorNodeTree', 'ShaderNodeTree', 'TextureNodeTree', 'GeometryNodeTree'):
            return True
        return False

    def execute(self, context):
        scn = context.scene
        bpy.ops.node.select_all(action='DESELECT')
        create_duo_node_tile_xyz_3e(context, scn.BSR_NodesOverrideCreate, context.space_data.edit_tree.bl_idname)
        return {'FINISHED'}

def create_geo_ng_subdiv_mesh_with_index():
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=SUBDIV_MESH_WITH_INDEX_GEO_NG_NAME, type='GeometryNodeTree')
    new_node_group.inputs.new(type='NodeSocketGeometry', name="Mesh")
    new_node_group.inputs.new(type='NodeSocketInt', name="Level")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Subdiv Index")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Level 0 Index")
    new_node_group.outputs.new(type='NodeSocketGeometry', name="Mesh")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Subdiv Index")
    tree_nodes = new_node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.location = (220, 180)
    node.data_type = "FLOAT"
    node.domain = "POINT"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-140, 60)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="FunctionNodeBooleanMath")
    node.location = (-320, 60)
    node.operation = "NOT"
    node.inputs[1].default_value = False
    new_nodes["Boolean Math"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-320, -60)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (40, 60)
    node.operation = "MULTIPLY_ADD"
    node.use_clamp = False
    new_nodes["Math"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.location = (-500, 180)
    node.data_type = "BOOLEAN"
    node.domain = "POINT"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = 0.000000
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = True
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute.001"] = node

    node = tree_nodes.new(type="GeometryNodeSubdivideMesh")
    node.location = (-140, 180)
    new_nodes["Subdivide Mesh"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-680, 0)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (400, 180)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Capture Attribute.001"].inputs[0])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Math"].inputs[2])
    tree_links.new(new_nodes["Boolean Math"].outputs[0], new_nodes["Math.001"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.001"].outputs[4], new_nodes["Boolean Math"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.001"].outputs[4], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Math"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Math.002"].inputs[0])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Math.001"].inputs[1])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Capture Attribute"].inputs[2])
    tree_links.new(new_nodes["Capture Attribute"].outputs[2], new_nodes["Group Output"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Math.002"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Subdivide Mesh"].inputs[1])
    tree_links.new(new_nodes["Capture Attribute.001"].outputs[0], new_nodes["Subdivide Mesh"].inputs[0])
    tree_links.new(new_nodes["Subdivide Mesh"].outputs[0], new_nodes["Capture Attribute"].inputs[0])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False
    return new_node_group

def create_geo_ng_subdiv_surf_with_index():
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=SUBDIV_SURF_WITH_INDEX_GEO_NG_NAME, type='GeometryNodeTree')
    new_node_group.inputs.new(type='NodeSocketGeometry', name="Mesh")
    new_node_group.inputs.new(type='NodeSocketInt', name="Level")
    new_node_group.inputs.new(type='NodeSocketFloatFactor', name="Crease")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Subdiv Index")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Level 0 Index")
    new_node_group.outputs.new(type='NodeSocketGeometry', name="Mesh")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Subdiv Index")
    tree_nodes = new_node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="GeometryNodeSubdivisionSurface")
    node.location = (40, 180)
    node.boundary_smooth = "ALL"
    node.uv_smooth = "PRESERVE_BOUNDARIES"
    new_nodes["Subdivision Surface"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-140, 0)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="FunctionNodeBooleanMath")
    node.location = (-320, 0)
    node.operation = "NOT"
    node.inputs[1].default_value = False
    new_nodes["Boolean Math"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (400, 180)
    new_nodes["Group Output"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.location = (-500, 180)
    node.data_type = "BOOLEAN"
    node.domain = "POINT"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = 0.000000
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = True
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute.001"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.location = (220, 180)
    node.data_type = "FLOAT"
    node.domain = "POINT"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-320, -120)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (40, 0)
    node.operation = "MULTIPLY_ADD"
    node.use_clamp = False
    new_nodes["Math"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-680, 0)
    new_nodes["Group Input"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Capture Attribute.001"].outputs[0], new_nodes["Subdivision Surface"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Subdivision Surface"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Subdivision Surface"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Capture Attribute.001"].inputs[0])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Math"].inputs[2])
    tree_links.new(new_nodes["Boolean Math"].outputs[0], new_nodes["Math.001"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.001"].outputs[4], new_nodes["Boolean Math"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.001"].outputs[4], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Subdivision Surface"].outputs[0], new_nodes["Capture Attribute"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Math"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Math.002"].inputs[0])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Math.001"].inputs[1])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Capture Attribute"].inputs[2])
    tree_links.new(new_nodes["Capture Attribute"].outputs[2], new_nodes["Group Output"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Math.002"].inputs[1])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False
    return new_node_group

def create_single_node_subdiv_surf_with_index(context, override_create, node_tree_type):
    ensure_node_groups(override_create, [SUBDIV_SURF_WITH_INDEX_GEO_NG_NAME], node_tree_type, create_prereq_util_node_group)
    node = context.space_data.edit_tree.nodes.new(type=get_node_group_for_type(node_tree_type))
    node.node_tree = bpy.data.node_groups.get(SUBDIV_SURF_WITH_INDEX_GEO_NG_NAME)

class BSR_SubdivSurfWithIndexCreateGeoNode(bpy.types.Operator):
    bl_description = "Add a 'Subdivide Surface With Index' node"
    bl_idname = "big_space_rig.subdiv_surf_with_index_create_duo_node"
    bl_label = "Subdiv Surface w/ Index"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        s = context.space_data
        return s.type == 'NODE_EDITOR' and s.node_tree != None and s.tree_type == 'GeometryNodeTree'

    def execute(self, context):
        scn = context.scene
        bpy.ops.node.select_all(action='DESELECT')
        create_single_node_subdiv_surf_with_index(context, scn.BSR_NodesOverrideCreate,
                                                  context.space_data.edit_tree.bl_idname)
        return {'FINISHED'}

def create_single_node_subdiv_mesh_with_index(context, override_create, node_tree_type):
    ensure_node_groups(override_create, [SUBDIV_MESH_WITH_INDEX_GEO_NG_NAME], node_tree_type, create_prereq_util_node_group)
    node = context.space_data.edit_tree.nodes.new(type=get_node_group_for_type(node_tree_type))
    node.node_tree = bpy.data.node_groups.get(SUBDIV_MESH_WITH_INDEX_GEO_NG_NAME)

class BSR_SubdivMeshWithIndexCreateGeoNode(bpy.types.Operator):
    bl_description = "Add a 'Subdivide Mesh With Index' node"
    bl_idname = "big_space_rig.subdiv_mesh_with_index_create_duo_node"
    bl_label = "Subdiv Mesh w/ Index"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        s = context.space_data
        return s.type == 'NODE_EDITOR' and s.node_tree != None and s.tree_type == 'GeometryNodeTree'

    def execute(self, context):
        scn = context.scene
        bpy.ops.node.select_all(action='DESELECT')
        create_single_node_subdiv_mesh_with_index(context, scn.BSR_NodesOverrideCreate,
                                                  context.space_data.edit_tree.bl_idname)
        return {'FINISHED'}
