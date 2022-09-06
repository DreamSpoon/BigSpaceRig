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

from .node_other import (ensure_node_groups, node_group_name_for_name_and_type, get_node_group_for_type)

SAMPLE_3E_DUO_NG_NAME = "Sample3e.BSR"
NOISE_3E_DUO_NG_NAME = "Noise3e.BSR"

# depending on the name passed to function, create the right set of nodes in a group and pass back
def create_prereq_noise_node_group(node_group_name, node_tree_type):
    if node_group_name == SAMPLE_3E_DUO_NG_NAME:
        return create_duo_ng_sample_3e(node_tree_type)
    elif node_group_name == NOISE_3E_DUO_NG_NAME:
        return create_duo_ng_noise_3e(node_tree_type)

    # error
    print("Unknown name passed to create_custom_geo_node_group: " + str(node_group_name))
    return None

def create_duo_ng_sample_3e(node_tree_type):
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=node_group_name_for_name_and_type(SAMPLE_3E_DUO_NG_NAME,
                                                                                     node_tree_type),
                                              type=node_tree_type)
    new_node_group.inputs.new(type='NodeSocketVector', name="Vector 0e")
    new_node_group.inputs.new(type='NodeSocketVector', name="Vector World")
    new_node_group.outputs.new(type='NodeSocketVector', name="Vector")
    tree_nodes = new_node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-340, 0)
    node.operation = "DIVIDE"
    node.inputs[1].default_value = (1000.0, 1000.0, 1000.0)
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-340, -200)
    node.operation = "DIVIDE"
    node.inputs[1].default_value = (1000.0, 1000.0, 1000.0)
    new_nodes["Vector Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (20, 0)
    node.operation = "ADD"
    new_nodes["Vector Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (200, 0)
    node.operation = "FRACTION"
    new_nodes["Vector Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-160, 0)
    node.operation = "FRACTION"
    new_nodes["Vector Math.001"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-520, 0)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (380, 0)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Vector Math"].outputs[0], new_nodes["Vector Math.001"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Vector Math.004"].inputs[0])
    tree_links.new(new_nodes["Vector Math.001"].outputs[0], new_nodes["Vector Math.002"].inputs[0])
    tree_links.new(new_nodes["Vector Math.004"].outputs[0], new_nodes["Vector Math.002"].inputs[1])
    tree_links.new(new_nodes["Vector Math.002"].outputs[0], new_nodes["Vector Math.003"].inputs[0])
    tree_links.new(new_nodes["Vector Math.003"].outputs[0], new_nodes["Group Output"].inputs[0])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group

def create_duo_ng_noise_3e(node_tree_type):
    # initialize variables
    if node_tree_type == 'GeometryNodeTree':
        node_group_type = 'GeometryNodeGroup'
    else:
        node_group_type = 'ShaderNodeGroup'

    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=node_group_name_for_name_and_type(NOISE_3E_DUO_NG_NAME,
                                                                                     node_tree_type),
                                              type=node_tree_type)
    new_node_group.inputs.new(type='NodeSocketVector', name="Vector 0e")
    new_node_group.inputs.new(type='NodeSocketVector', name="Vector World")
    new_node_group.inputs.new(type='NodeSocketFloat', name="W")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Scale")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Detail")
    new_node_group.inputs.new(type='NodeSocketFloatFactor', name="Roughness")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Distortion")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Value")
    new_node_group.outputs.new(type='NodeSocketColor', name="Color")
    tree_nodes = new_node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type=node_group_type)
    node.location = (-280, 720)
    node.node_tree = bpy.data.node_groups.get(node_group_name_for_name_and_type(SAMPLE_3E_DUO_NG_NAME, node_tree_type))
    new_nodes["Group"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.label = "cosine"
    node.location = (260, 720)
    new_nodes["Separate XYZ"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.label = "sine"
    node.location = (260, 580)
    new_nodes["Separate XYZ.001"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (1080, 520)
    new_nodes["Combine XYZ"] = node

    node = tree_nodes.new(type="ShaderNodeTexNoise")
    node.location = (1440, 720)
    node.noise_dimensions = "4D"
    new_nodes["Noise Texture"] = node

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
    new_nodes["Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (720, 360)
    node.operation = "MULTIPLY"
    new_nodes["Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (540, 360)
    node.operation = "MULTIPLY"
    new_nodes["Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (720, 160)
    node.operation = "MULTIPLY"
    new_nodes["Math.006"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (540, 160)
    node.operation = "MULTIPLY"
    new_nodes["Math.007"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Z"
    node.location = (900, 160)
    node.operation = "SUBTRACT"
    new_nodes["Math.008"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (540, 0)
    node.operation = "MULTIPLY"
    new_nodes["Math.009"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (720, 0)
    node.operation = "MULTIPLY"
    new_nodes["Math.010"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (540, 880)
    node.operation = "MULTIPLY"
    new_nodes["Math.011"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (720, 880)
    node.operation = "MULTIPLY"
    new_nodes["Math.012"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (540, 720)
    node.operation = "MULTIPLY"
    new_nodes["Math.013"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (720, 720)
    node.operation = "MULTIPLY"
    new_nodes["Math.014"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (720, 1240)
    node.operation = "MULTIPLY"
    new_nodes["Math.015"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (540, 1240)
    node.operation = "MULTIPLY"
    new_nodes["Math.016"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (540, 1080)
    node.operation = "MULTIPLY"
    new_nodes["Math.017"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (720, 1080)
    node.operation = "MULTIPLY"
    new_nodes["Math.018"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "W"
    node.location = (900, 1080)
    node.operation = "ADD"
    new_nodes["Math.019"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "X"
    node.location = (900, 720)
    node.operation = "SUBTRACT"
    new_nodes["Math.020"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1260, 720)
    node.operation = "ADD"
    new_nodes["Math.021"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1080, 900)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = 1000.0
    new_nodes["Math.002"] = node

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

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-460, 720)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (1620, 720)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Noise Texture"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Noise Texture"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Noise Texture"].inputs[4])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Noise Texture"].inputs[5])
    tree_links.new(new_nodes["Math.016"].outputs[0], new_nodes["Math.015"].inputs[0])
    tree_links.new(new_nodes["Math.017"].outputs[0], new_nodes["Math.018"].inputs[0])
    tree_links.new(new_nodes["Math.015"].outputs[0], new_nodes["Math.019"].inputs[0])
    tree_links.new(new_nodes["Math.018"].outputs[0], new_nodes["Math.019"].inputs[1])
    tree_links.new(new_nodes["Math.011"].outputs[0], new_nodes["Math.012"].inputs[0])
    tree_links.new(new_nodes["Math.013"].outputs[0], new_nodes["Math.014"].inputs[0])
    tree_links.new(new_nodes["Math.012"].outputs[0], new_nodes["Math.020"].inputs[0])
    tree_links.new(new_nodes["Math.014"].outputs[0], new_nodes["Math.020"].inputs[1])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Math.005"].outputs[0], new_nodes["Math.004"].inputs[0])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Math.003"].inputs[0])
    tree_links.new(new_nodes["Math.004"].outputs[0], new_nodes["Math.003"].inputs[1])
    tree_links.new(new_nodes["Math.007"].outputs[0], new_nodes["Math.006"].inputs[0])
    tree_links.new(new_nodes["Math.009"].outputs[0], new_nodes["Math.010"].inputs[0])
    tree_links.new(new_nodes["Math.006"].outputs[0], new_nodes["Math.008"].inputs[0])
    tree_links.new(new_nodes["Math.010"].outputs[0], new_nodes["Math.008"].inputs[1])
    tree_links.new(new_nodes["Math.020"].outputs[0], new_nodes["Combine XYZ"].inputs[0])
    tree_links.new(new_nodes["Math.003"].outputs[0], new_nodes["Combine XYZ"].inputs[1])
    tree_links.new(new_nodes["Math.008"].outputs[0], new_nodes["Combine XYZ"].inputs[2])
    tree_links.new(new_nodes["Combine XYZ"].outputs[0], new_nodes["Vector Math.003"].inputs[0])
    tree_links.new(new_nodes["Vector Math.002"].outputs[0], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Vector Math.002"].outputs[0], new_nodes["Vector Math.001"].inputs[0])
    tree_links.new(new_nodes["Vector Math"].outputs[0], new_nodes["Separate XYZ"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ"].outputs[0], new_nodes["Math.016"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ"].outputs[0], new_nodes["Math.011"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ"].outputs[0], new_nodes["Math.001"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ"].outputs[0], new_nodes["Math.009"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ"].outputs[1], new_nodes["Math.016"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ"].outputs[1], new_nodes["Math.011"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ"].outputs[1], new_nodes["Math.005"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ"].outputs[1], new_nodes["Math.007"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ"].outputs[2], new_nodes["Math.015"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ"].outputs[2], new_nodes["Math.014"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ"].outputs[2], new_nodes["Math"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ"].outputs[2], new_nodes["Math.006"].inputs[1])
    tree_links.new(new_nodes["Vector Math.001"].outputs[0], new_nodes["Separate XYZ.001"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[0], new_nodes["Math.017"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[0], new_nodes["Math.013"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[0], new_nodes["Math.005"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[0], new_nodes["Math.007"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[1], new_nodes["Math.009"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[1], new_nodes["Math.001"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[1], new_nodes["Math.013"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[1], new_nodes["Math.017"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[2], new_nodes["Math.010"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[2], new_nodes["Math.004"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[2], new_nodes["Math.012"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[2], new_nodes["Math.018"].inputs[1])
    tree_links.new(new_nodes["Noise Texture"].outputs[1], new_nodes["Group Output"].inputs[1])
    tree_links.new(new_nodes["Noise Texture"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Group"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Group"].inputs[1])
    tree_links.new(new_nodes["Group"].outputs[0], new_nodes["Vector Math.002"].inputs[0])
    tree_links.new(new_nodes["Vector Math.003"].outputs[0], new_nodes["Noise Texture"].inputs[0])
    tree_links.new(new_nodes["Math.021"].outputs[0], new_nodes["Noise Texture"].inputs[1])
    tree_links.new(new_nodes["Math.019"].outputs[0], new_nodes["Math.002"].inputs[0])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Math.021"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Math.021"].inputs[1])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group

def create_duo_node_noise_3e(context, override_create, node_tree_type):
    ensure_node_groups(override_create, [SAMPLE_3E_DUO_NG_NAME, NOISE_3E_DUO_NG_NAME],
        node_tree_type, create_prereq_noise_node_group)
    node = context.space_data.edit_tree.nodes.new(type=get_node_group_for_type(node_tree_type))
    node.node_tree = bpy.data.node_groups.get(node_group_name_for_name_and_type(NOISE_3E_DUO_NG_NAME, node_tree_type))
    node.inputs[3].default_value = 1.0
    node.inputs[4].default_value = 2.0
    node.inputs[5].default_value = 0.5

class BSR_Noise3eCreateDuoNode(bpy.types.Operator):
    bl_description = "Add a tiled noise texture node"
    bl_idname = "big_space_rig.noise_3e_create_duo_node"
    bl_label = "Noise 3e"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        s = context.space_data
        if s.type == 'NODE_EDITOR' and s.node_tree != None and \
            s.tree_type in ('CompositorNodeTree', 'ShaderNodeTree', 'TextureNodeTree', 'GeometryNodeTree'):
            return True
        return False

    def execute(self, context):
        bpy.ops.node.select_all(action='DESELECT')
        create_duo_node_noise_3e(context, False, context.space_data.edit_tree.bl_idname)
        return {'FINISHED'}
