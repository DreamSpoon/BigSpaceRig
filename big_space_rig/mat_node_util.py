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

WORLD_COORDS_DUO_NG_NAME = "WorldCoords6e.BSR"
VEC_MULTIPLY_DUO_NG_NAME = "VecMultiply6e.BSR"

def create_prereq_duo_node_group(node_group_name, node_tree_type):
    if node_group_name == WORLD_COORDS_DUO_NG_NAME:
        return create_duo_ng_world_coords(node_tree_type)
    elif  node_group_name == VEC_MULTIPLY_DUO_NG_NAME:
        return create_duo_ng_vec_multiply(node_tree_type)
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
    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-240, -60)
    node.operation = "ROUND"
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-240, 240)
    node.operation = "ROUND"
    new_nodes["Math"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-240, 100)
    node.operation = "ROUND"
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-780, 80)
    node.operation = "ADD"
    new_nodes["Vector Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-960, -60)
    node.operation = "ADD"
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-600, 60)
    node.operation = "DIVIDE"
    node.inputs[1].default_value = (1e3, 1e3, 1e3)
    new_nodes["Vector Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (120, 240)
    node.operation = "DIVIDE"
    node.inputs[1].default_value = (1e3, 1e3, 1e3)
    new_nodes["Vector Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (120, 40)
    node.operation = "MODULO"
    node.inputs[1].default_value = (1e3, 1e3, 1e3)
    new_nodes["Vector Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-960, 140)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = (1e6, 1e6, 1e6)
    new_nodes["Vector Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (-420, 60)
    new_nodes["Separate XYZ"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (-60, 140)
    new_nodes["Combine XYZ"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-1160, 40)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (320, 60)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Vector Math"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Vector Math.001"].inputs[0])
    tree_links.new(new_nodes["Vector Math"].outputs[0], new_nodes["Vector Math.002"].inputs[1])
    tree_links.new(new_nodes["Vector Math.002"].outputs[0], new_nodes["Group Output"].inputs[2])
    tree_links.new(new_nodes["Vector Math.002"].outputs[0], new_nodes["Vector Math.003"].inputs[0])
    tree_links.new(new_nodes["Vector Math.003"].outputs[0], new_nodes["Separate XYZ"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ"].outputs[0], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ"].outputs[1], new_nodes["Math.001"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ"].outputs[2], new_nodes["Math.002"].inputs[0])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Combine XYZ"].inputs[0])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Combine XYZ"].inputs[1])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Combine XYZ"].inputs[2])
    tree_links.new(new_nodes["Combine XYZ"].outputs[0], new_nodes["Vector Math.004"].inputs[0])
    tree_links.new(new_nodes["Vector Math.004"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Vector Math"].outputs[0], new_nodes["Vector Math.005"].inputs[0])
    tree_links.new(new_nodes["Vector Math.005"].outputs[0], new_nodes["Group Output"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Vector Math.001"].outputs[0], new_nodes["Vector Math.002"].inputs[0])

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
    node.location = (140, 0)
    node.operation = "MODULO"
    node.inputs[1].default_value = (1e3, 1e3, 1e3)
    new_nodes["Vector Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (140, 200)
    node.operation = "DIVIDE"
    node.inputs[1].default_value = (1e3, 1e3, 1e3)
    new_nodes["Vector Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-940, 80)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = (1e6, 1e6, 1e6)
    new_nodes["Vector Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-760, 20)
    node.operation = "ADD"
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-580, -20)
    node.operation = "DIVIDE"
    node.inputs[1].default_value = (1e3, 1e3, 1e3)
    new_nodes["Vector Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-1120, -120)
    node.operation = "MULTIPLY"
    new_nodes["Vector Math.006"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-1120, 20)
    node.operation = "MULTIPLY"
    new_nodes["Vector Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-220, 220)
    node.operation = "ROUND"
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-220, 80)
    node.operation = "ROUND"
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-220, -60)
    node.operation = "ROUND"
    new_nodes["Math"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (-40, 120)
    new_nodes["Combine XYZ"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (-400, 20)
    new_nodes["Separate XYZ"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-1340, -60)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (360, 80)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Vector Math.001"].outputs[0], new_nodes["Vector Math.005"].inputs[0])
    tree_links.new(new_nodes["Vector Math"].outputs[0], new_nodes["Group Output"].inputs[2])
    tree_links.new(new_nodes["Vector Math"].outputs[0], new_nodes["Vector Math.002"].inputs[0])
    tree_links.new(new_nodes["Vector Math.002"].outputs[0], new_nodes["Separate XYZ"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ"].outputs[0], new_nodes["Math.001"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ"].outputs[1], new_nodes["Math.002"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ"].outputs[2], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Combine XYZ"].inputs[0])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Combine XYZ"].inputs[1])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Combine XYZ"].inputs[2])
    tree_links.new(new_nodes["Combine XYZ"].outputs[0], new_nodes["Vector Math.003"].inputs[0])
    tree_links.new(new_nodes["Vector Math.003"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Vector Math.004"].outputs[0], new_nodes["Group Output"].inputs[1])
    tree_links.new(new_nodes["Vector Math.005"].outputs[0], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Vector Math.001"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Vector Math.001"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Vector Math.006"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Vector Math.006"].inputs[0])
    tree_links.new(new_nodes["Vector Math.006"].outputs[0], new_nodes["Vector Math"].inputs[1])
    tree_links.new(new_nodes["Vector Math.006"].outputs[0], new_nodes["Vector Math.004"].inputs[0])

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
