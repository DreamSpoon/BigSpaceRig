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

WORLD_COORDS_DUO_NG_NAME = "WorldCoords6e.BSR"
VEC_MULTIPLY_DUO_NG_NAME = "VecMultiply6e.BSR"
VEC_ADD_DUO_NG_NAME = "VecAdd6e.BSR"

def create_prereq_duo_node_group(node_group_name, node_tree_type):
    if node_group_name == WORLD_COORDS_DUO_NG_NAME:
        return create_duo_ng_world_coords(node_tree_type)
    elif node_group_name == VEC_MULTIPLY_DUO_NG_NAME:
        return create_duo_ng_vec_multiply(node_tree_type)
    elif node_group_name == VEC_ADD_DUO_NG_NAME:
        return create_duo_ng_vec_add(node_tree_type)
    # error
    print("Unknown name passed to create_custom_geo_node_group: " + str(node_group_name))
    return None

def create_duo_ng_world_coords(node_tree_type):
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=node_group_name_for_name_and_type(WORLD_COORDS_DUO_NG_NAME,
                                                                                     node_tree_type),
                                              type=node_tree_type)
    new_node_group.inputs.new(type='NodeSocketVector', name="In Loc 6e")
    new_node_group.inputs.new(type='NodeSocketVector', name="In Loc 0e")
    new_node_group.inputs.new(type='NodeSocketVector', name="World")
    new_node_group.outputs.new(type='NodeSocketVector', name="Out Loc 6e")
    new_node_group.outputs.new(type='NodeSocketVector', name="Out Loc 0e")
    new_node_group.outputs.new(type='NodeSocketVector', name="Combined Loc")
    tree_nodes = new_node_group.nodes
    # delete old nodes before adding new nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-960, 160)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = (1e6, 1e6, 1e6)
    new_nodes["Vector Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-960, -40)
    node.operation = "ADD"
    new_nodes["Vector Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-780, 80)
    node.operation = "ADD"
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-420, 60)
    node.operation = "FLOOR"
    new_nodes["Vector Math.006"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-240, -60)
    node.operation = "MODULO"
    node.inputs[1].default_value = (1e3, 1e3, 1e3)
    new_nodes["Vector Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-240, 140)
    node.operation = "DIVIDE"
    node.inputs[1].default_value = (1e3, 1e3, 1e3)
    new_nodes["Vector Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-600, 20)
    node.operation = "DIVIDE"
    node.inputs[1].default_value = (1e3, 1e3, 1e3)
    new_nodes["Vector Math.002"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-1140, 20)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (-60, 20)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Vector Math.001"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Vector Math.005"].inputs[0])
    tree_links.new(new_nodes["Vector Math.001"].outputs[0], new_nodes["Vector Math"].inputs[1])
    tree_links.new(new_nodes["Vector Math"].outputs[0], new_nodes["Group Output"].inputs[2])
    tree_links.new(new_nodes["Vector Math"].outputs[0], new_nodes["Vector Math.002"].inputs[0])
    tree_links.new(new_nodes["Vector Math.003"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Vector Math.001"].outputs[0], new_nodes["Vector Math.004"].inputs[0])
    tree_links.new(new_nodes["Vector Math.004"].outputs[0], new_nodes["Group Output"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Vector Math.001"].inputs[0])
    tree_links.new(new_nodes["Vector Math.005"].outputs[0], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Vector Math.002"].outputs[0], new_nodes["Vector Math.006"].inputs[0])
    tree_links.new(new_nodes["Vector Math.006"].outputs[0], new_nodes["Vector Math.003"].inputs[0])

    return new_node_group

def create_duo_node_world_coords(context, override_create, node_tree_type):
    ensure_node_groups(override_create, [WORLD_COORDS_DUO_NG_NAME], node_tree_type, create_prereq_duo_node_group)
    node = context.space_data.edit_tree.nodes.new(type=get_node_group_for_type(node_tree_type))
    node.node_tree = bpy.data.node_groups.get(node_group_name_for_name_and_type(WORLD_COORDS_DUO_NG_NAME,
                                                                                node_tree_type))

class BSR_WorldCoordsCreateDuoNode(bpy.types.Operator):
    bl_description = "Add a World Coords node"
    bl_idname = "big_space_rig.world_coords_create_duo_node"
    bl_label = "World Coords"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        s = context.space_data
        if s.type == 'NODE_EDITOR' and s.node_tree != None and \
            s.tree_type in ('CompositorNodeTree', 'ShaderNodeTree', 'TextureNodeTree', 'GeometryNodeTree'):
            return True
        return False

    def execute(self, context):
        create_duo_node_world_coords(context, False, context.space_data.edit_tree.bl_idname)
        return {'FINISHED'}

def create_duo_ng_vec_multiply(node_tree_type):
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=node_group_name_for_name_and_type(VEC_MULTIPLY_DUO_NG_NAME,
                                                                                     node_tree_type),
                                              type=node_tree_type)
    new_node_group.inputs.new(type='NodeSocketVector', name="Vector 6e")
    new_node_group.inputs.new(type='NodeSocketVector', name="Vector 0e")
    new_node_group.inputs.new(type='NodeSocketVector', name="Multiplier")
    new_node_group.outputs.new(type='NodeSocketVector', name="Vector 6e")
    new_node_group.outputs.new(type='NodeSocketVector', name="Vector 0e")
    new_node_group.outputs.new(type='NodeSocketVector', name="Combined")
    tree_nodes = new_node_group.nodes
    # delete old nodes before adding new nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-1120, -140)
    node.operation = "MULTIPLY"
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-1120, 20)
    node.operation = "MULTIPLY"
    new_nodes["Vector Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-220, -100)
    node.operation = "MODULO"
    node.inputs[1].default_value = (1e3 , 1e3, 1e3)
    new_nodes["Vector Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-220, 100)
    node.operation = "DIVIDE"
    node.inputs[1].default_value = (1e3 , 1e3, 1e3)
    new_nodes["Vector Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-760, -40)
    node.operation = "ADD"
    new_nodes["Vector Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-940, 40)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = (1e6 , 1e6, 1e6)
    new_nodes["Vector Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-580, -20)
    node.operation = "DIVIDE"
    node.inputs[1].default_value = (1e3 , 1e3, 1e3)
    new_nodes["Vector Math.006"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-400, 40)
    node.operation = "FLOOR"
    new_nodes["Vector Math.007"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-1300, -60)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (0, -40)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Vector Math.001"].outputs[0], new_nodes["Vector Math.005"].inputs[0])
    tree_links.new(new_nodes["Vector Math.004"].outputs[0], new_nodes["Group Output"].inputs[2])
    tree_links.new(new_nodes["Vector Math.004"].outputs[0], new_nodes["Vector Math.006"].inputs[0])
    tree_links.new(new_nodes["Vector Math.003"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Vector Math.002"].outputs[0], new_nodes["Group Output"].inputs[1])
    tree_links.new(new_nodes["Vector Math.005"].outputs[0], new_nodes["Vector Math.004"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Vector Math.001"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Vector Math"].outputs[0], new_nodes["Vector Math.004"].inputs[1])
    tree_links.new(new_nodes["Vector Math"].outputs[0], new_nodes["Vector Math.002"].inputs[0])
    tree_links.new(new_nodes["Vector Math.006"].outputs[0], new_nodes["Vector Math.007"].inputs[0])
    tree_links.new(new_nodes["Vector Math.007"].outputs[0], new_nodes["Vector Math.003"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Vector Math.001"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Vector Math"].inputs[1])

    return new_node_group

def create_duo_node_vec_multiply(context, override_create, node_tree_type):
    ensure_node_groups(override_create, [VEC_MULTIPLY_DUO_NG_NAME], node_tree_type, create_prereq_duo_node_group)
    node = context.space_data.edit_tree.nodes.new(type=get_node_group_for_type(node_tree_type))
    node.node_tree = bpy.data.node_groups.get(node_group_name_for_name_and_type(VEC_MULTIPLY_DUO_NG_NAME,
                                                                                node_tree_type))
    node.inputs[2].default_value = (1.0, 1.0, 1.0)

class BSR_VecMultiplyCreateDuoNode(bpy.types.Operator):
    bl_description = "Add a Vector Multiply node"
    bl_idname = "big_space_rig.vec_multiply_create_duo_node"
    bl_label = "Vector Multiply"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        s = context.space_data
        if s.type == 'NODE_EDITOR' and s.node_tree != None and \
            s.tree_type in ('CompositorNodeTree', 'ShaderNodeTree', 'TextureNodeTree', 'GeometryNodeTree'):
            return True
        return False

    def execute(self, context):
        create_duo_node_vec_multiply(context, False, context.space_data.edit_tree.bl_idname)
        return {'FINISHED'}

def create_duo_ng_vec_add(node_tree_type):
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=node_group_name_for_name_and_type(VEC_ADD_DUO_NG_NAME,
                                                                                     node_tree_type),
                                              type=node_tree_type)
    new_node_group.inputs.new(type='NodeSocketVector', name="A Vector 6e")
    new_node_group.inputs.new(type='NodeSocketVector', name="A Vector 0e")
    new_node_group.inputs.new(type='NodeSocketVector', name="B Vector 6e")
    new_node_group.inputs.new(type='NodeSocketVector', name="B Vector 0e")
    new_node_group.outputs.new(type='NodeSocketVector', name="Vector 6e")
    new_node_group.outputs.new(type='NodeSocketVector', name="Vector 0e")
    new_node_group.outputs.new(type='NodeSocketVector', name="Combined")
    tree_nodes = new_node_group.nodes
    # delete old nodes before adding new nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-1120, -140)
    node.operation = "ADD"
    new_nodes["Vector Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-1120, 20)
    node.operation = "ADD"
    new_nodes["Vector Math.006"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-220, -100)
    node.operation = "MODULO"
    node.inputs[1].default_value = (1e3, 1e3, 1e3)
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-220, 100)
    node.operation = "DIVIDE"
    node.inputs[1].default_value = (1e3, 1e3, 1e3)
    new_nodes["Vector Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-760, -40)
    node.operation = "ADD"
    new_nodes["Vector Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-940, 40)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = (1e6, 1e6, 1e6)
    new_nodes["Vector Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-580, -20)
    node.operation = "DIVIDE"
    node.inputs[1].default_value = (1e3, 1e3, 1e3)
    new_nodes["Vector Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-400, 40)
    node.operation = "FLOOR"
    new_nodes["Vector Math.007"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-1300, -60)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (0, -40)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Vector Math.006"].outputs[0], new_nodes["Vector Math.002"].inputs[0])
    tree_links.new(new_nodes["Vector Math.003"].outputs[0], new_nodes["Group Output"].inputs[2])
    tree_links.new(new_nodes["Vector Math.003"].outputs[0], new_nodes["Vector Math.004"].inputs[0])
    tree_links.new(new_nodes["Vector Math.001"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Vector Math"].outputs[0], new_nodes["Group Output"].inputs[1])
    tree_links.new(new_nodes["Vector Math.002"].outputs[0], new_nodes["Vector Math.003"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Vector Math.006"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Vector Math.005"].inputs[0])
    tree_links.new(new_nodes["Vector Math.005"].outputs[0], new_nodes["Vector Math.003"].inputs[1])
    tree_links.new(new_nodes["Vector Math.005"].outputs[0], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Vector Math.005"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Vector Math.006"].inputs[1])
    tree_links.new(new_nodes["Vector Math.004"].outputs[0], new_nodes["Vector Math.007"].inputs[0])
    tree_links.new(new_nodes["Vector Math.007"].outputs[0], new_nodes["Vector Math.001"].inputs[0])

    return new_node_group

def create_duo_node_vec_add(context, override_create, node_tree_type):
    ensure_node_groups(override_create, [VEC_ADD_DUO_NG_NAME], node_tree_type, create_prereq_duo_node_group)
    node = context.space_data.edit_tree.nodes.new(type=get_node_group_for_type(node_tree_type))
    node.node_tree = bpy.data.node_groups.get(node_group_name_for_name_and_type(VEC_ADD_DUO_NG_NAME,
                                                                                node_tree_type))

class BSR_VecAddCreateDuoNode(bpy.types.Operator):
    bl_description = "Add a Vector Add node"
    bl_idname = "big_space_rig.vec_add_create_duo_node"
    bl_label = "Vector Add"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        s = context.space_data
        if s.type == 'NODE_EDITOR' and s.node_tree != None and \
            s.tree_type in ('CompositorNodeTree', 'ShaderNodeTree', 'TextureNodeTree', 'GeometryNodeTree'):
            return True
        return False

    def execute(self, context):
        create_duo_node_vec_add(context, False, context.space_data.edit_tree.bl_idname)
        return {'FINISHED'}

def create_duo_node_observer_input(context, node_tree_type, big_space_rig):
    tree_nodes = context.space_data.edit_tree.nodes

    if node_tree_type in ['CompositorNodeTree', 'ShaderNodeTree', 'TextureNodeTree']:
        node_input_type = 'ShaderNodeCombineXYZ'
    elif node_tree_type == 'GeometryNodeTree':
        node_input_type = 'FunctionNodeInputVector'
    else:
        print("Error, unknown Observer input node tree type: " + str(node_tree_type))
        return None

    node = tree_nodes.new(type=node_input_type)
    node.label = "6e Observer"
    node.location.y = node.location.y + 70
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

    node = tree_nodes.new(type=node_input_type)
    node.label = "0e Observer"
    node.location.y = node.location.y - 70
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
        create_duo_node_observer_input(context, context.space_data.edit_tree.bl_idname, big_space_rig)
        return {'FINISHED'}

def create_duo_node_place_input(context, node_tree_type, big_space_rig, bsr_place):
    tree_nodes = context.space_data.edit_tree.nodes

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
    node.location.y = node.location.y + 70
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

    node = tree_nodes.new(type=node_input_type)
    node.label = "0e Place - " + place_bone_name_0e
    node.location.y = node.location.y - 70
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
        create_duo_node_place_input(context, context.space_data.edit_tree.bl_idname, big_space_rig, bsr_place)
        return {'FINISHED'}
