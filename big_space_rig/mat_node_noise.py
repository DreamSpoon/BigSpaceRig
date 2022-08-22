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

PINGPONG_3E_DUO_NG_NAME = "PingPong3e.BSR"
SAMPLE_3E_DUO_NG_NAME = "Sample3e.BSR"
NOISE_3E_DUO_NG_NAME = "Noise3e.BSR"

# depending on the name passed to function, create the right set of nodes in a group and pass back
def create_prereq_duo_node_group(node_group_name, node_tree_type):
    if node_group_name == PINGPONG_3E_DUO_NG_NAME:
        return create_duo_ng_ping_pong_3e(node_tree_type)
    elif node_group_name == SAMPLE_3E_DUO_NG_NAME:
        return create_duo_ng_sample_3e(node_tree_type)
    elif node_group_name == NOISE_3E_DUO_NG_NAME:
        return create_duo_ng_noise_3e(node_tree_type)

    # error
    print("Unknown name passed to create_custom_geo_node_group: " + str(node_group_name))
    return None

def create_duo_ng_ping_pong_3e(node_tree_type):
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=node_group_name_for_name_and_type(PINGPONG_3E_DUO_NG_NAME,
                                                                                     node_tree_type),
                                              type=node_tree_type)
    new_node_group.inputs.new(type='NodeSocketFloat', name="Value 0e")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Value World")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Value")
    tree_nodes = new_node_group.nodes
    # delete old nodes before adding new nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (270, 0)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = 2000.0
    new_nodes["Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (90, 0)
    node.operation = "PINGPONG"
    node.inputs[1].default_value = 0.5
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-80, 0)
    node.operation = "FRACT"
    new_nodes["Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-440, 80)
    node.operation = "FRACT"
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-620, 80)
    node.operation = "DIVIDE"
    node.inputs[1].default_value = 1000.0
    new_nodes["Math"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-540, -80)
    node.operation = "DIVIDE"
    node.inputs[1].default_value = 1000.0
    new_nodes["Math.006"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-260, 20)
    node.operation = "ADD"
    new_nodes["Math.004"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-820, 0)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (460, 0)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Math.003"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Math.001"].inputs[0])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Math.003"].inputs[0])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Math.004"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Math.006"].inputs[0])
    tree_links.new(new_nodes["Math.006"].outputs[0], new_nodes["Math.004"].inputs[1])
    tree_links.new(new_nodes["Math.004"].outputs[0], new_nodes["Math.005"].inputs[0])
    tree_links.new(new_nodes["Math.005"].outputs[0], new_nodes["Math.002"].inputs[0])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group

def create_duo_ng_sample_3e(node_tree_type):
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=node_group_name_for_name_and_type(SAMPLE_3E_DUO_NG_NAME,
                                                                                     node_tree_type),
                                              type=node_tree_type)
    new_node_group.inputs.new(type='NodeSocketFloat', name="Value 0e")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Value World")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Value")
    tree_nodes = new_node_group.nodes
    # delete old nodes before adding new nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (200, 0)
    node.operation = "FRACT"
    new_nodes["Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (20, 20)
    node.operation = "ADD"
    new_nodes["Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-160, 80)
    node.operation = "FRACT"
    new_nodes["Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-340, 80)
    node.operation = "DIVIDE"
    node.inputs[1].default_value = 1000.0
    new_nodes["Math.006"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-240, -80)
    node.operation = "DIVIDE"
    node.inputs[1].default_value = 1000.0
    new_nodes["Math.007"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-540, 0)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (380, 0)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Math.006"].outputs[0], new_nodes["Math.005"].inputs[0])
    tree_links.new(new_nodes["Math.005"].outputs[0], new_nodes["Math.004"].inputs[0])
    tree_links.new(new_nodes["Math.007"].outputs[0], new_nodes["Math.004"].inputs[1])
    tree_links.new(new_nodes["Math.004"].outputs[0], new_nodes["Math.003"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Math.006"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Math.007"].inputs[0])
    tree_links.new(new_nodes["Math.003"].outputs[0], new_nodes["Group Output"].inputs[0])

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
    # delete old nodes before adding new nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type=node_group_type)
    node.location = (-560, 600)
    node.node_tree = bpy.data.node_groups.get(node_group_name_for_name_and_type(PINGPONG_3E_DUO_NG_NAME,
                                                                                node_tree_type))
    new_nodes["Group.016"] = node

    node = tree_nodes.new(type=node_group_type)
    node.location = (-560, 740)
    node.node_tree = bpy.data.node_groups.get(node_group_name_for_name_and_type(SAMPLE_3E_DUO_NG_NAME,
                                                                                node_tree_type))
    new_nodes["Group.005"] = node

    node = tree_nodes.new(type=node_group_type)
    node.location = (-560, 460)
    node.node_tree = bpy.data.node_groups.get(node_group_name_for_name_and_type(PINGPONG_3E_DUO_NG_NAME,
                                                                                node_tree_type))
    new_nodes["Group.003"] = node

    node = tree_nodes.new(type=node_group_type)
    node.location = (-560, -500)
    node.node_tree = bpy.data.node_groups.get(node_group_name_for_name_and_type(PINGPONG_3E_DUO_NG_NAME,
                                                                                node_tree_type))
    new_nodes["Group.008"] = node

    node = tree_nodes.new(type=node_group_type)
    node.location = (-560, -360)
    node.node_tree = bpy.data.node_groups.get(node_group_name_for_name_and_type(PINGPONG_3E_DUO_NG_NAME,
                                                                                node_tree_type))
    new_nodes["Group.019"] = node

    node = tree_nodes.new(type=node_group_type)
    node.location = (-560, -640)
    node.node_tree = bpy.data.node_groups.get(node_group_name_for_name_and_type(SAMPLE_3E_DUO_NG_NAME,
                                                                                node_tree_type))
    new_nodes["Group.007"] = node

    node = tree_nodes.new(type=node_group_type)
    node.location = (-560, 0)
    node.node_tree = bpy.data.node_groups.get(node_group_name_for_name_and_type(SAMPLE_3E_DUO_NG_NAME,
                                                                                node_tree_type))
    new_nodes["Group.006"] = node

    node = tree_nodes.new(type=node_group_type)
    node.location = (-560, 140)
    node.node_tree = bpy.data.node_groups.get(node_group_name_for_name_and_type(PINGPONG_3E_DUO_NG_NAME,
                                                                                node_tree_type))
    new_nodes["Group.018"] = node

    node = tree_nodes.new(type=node_group_type)
    node.location = (-560, -140)
    node.node_tree = bpy.data.node_groups.get(node_group_name_for_name_and_type(PINGPONG_3E_DUO_NG_NAME,
                                                                                node_tree_type))
    new_nodes["Group.004"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-360, 840)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = math.pi * 2
    new_nodes["Math.024"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-180, 800)
    node.operation = "SINE"
    new_nodes["Math.025"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (0, 760)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = 250.0
    new_nodes["Math.012"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-360, 640)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = math.pi * 2
    new_nodes["Math.026"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-180, 540)
    node.operation = "COSINE"
    new_nodes["Math.027"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (0, 480)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = 250.0
    new_nodes["Math.017"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (180, 420)
    node.operation = "ADD"
    new_nodes["Math.019"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (580, 440)
    node.operation = "ADD"
    new_nodes["Math.021"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (760, 260)
    node.operation = "ADD"
    new_nodes["Math.022"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (940, 260)
    node.operation = "DIVIDE"
    node.inputs[1].default_value = 3.0
    new_nodes["Math.023"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-200, 220)
    node.operation = "SINE"
    new_nodes["Math.032"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-200, -40)
    node.operation = "COSINE"
    new_nodes["Math.035"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-380, 60)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = math.pi * 2
    new_nodes["Math.034"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-20, 180)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = 250.0
    new_nodes["Math.013"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-20, -100)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = 250.0
    new_nodes["Math.018"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (180, -100)
    node.operation = "ADD"
    new_nodes["Math.036"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-200, -400)
    node.operation = "SINE"
    new_nodes["Math.037"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-200, -600)
    node.operation = "COSINE"
    new_nodes["Math.040"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-20, -580)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = 250.0
    new_nodes["Math.020"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-380, -620)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = math.pi * 2
    new_nodes["Math.039"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-380, -440)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = math.pi * 2
    new_nodes["Math.043"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-20, -380)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = 250.0
    new_nodes["Math.014"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (180, -460)
    node.operation = "ADD"
    new_nodes["Math.041"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-380, 260)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = math.pi * 2
    new_nodes["Math.031"] = node

    node = tree_nodes.new(type="ShaderNodeTexNoise")
    node.location = (380, 120)
    node.noise_dimensions = '4D'
    new_nodes["Noise Texture.001"] = node

    node = tree_nodes.new(type="ShaderNodeTexNoise")
    node.location = (380, 640)
    node.noise_dimensions = '4D'
    new_nodes["Noise Texture"] = node

    node = tree_nodes.new(type="ShaderNodeTexNoise")
    node.location = (380, -220)
    node.noise_dimensions = '4D'
    new_nodes["Noise Texture.002"] = node

    node = tree_nodes.new(type="ShaderNodeMixRGB")
    node.location = (760, 100)
    node.blend_type = "MIX"
    node.inputs[0].default_value = 1.0 / 3.0
    new_nodes["Mix.001"] = node

    node = tree_nodes.new(type="ShaderNodeMixRGB")
    node.location = (580, 260)
    node.blend_type = "MIX"
    node.inputs[0].default_value = 0.5
    new_nodes["Mix"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (-800, 60)
    new_nodes["Separate XYZ.008"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (-800, -100)
    new_nodes["Separate XYZ.004"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (-780, 480)
    new_nodes["Separate XYZ.003"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (-780, 640)
    new_nodes["Separate XYZ.006"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (-780, -460)
    new_nodes["Separate XYZ.010"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (-780, -600)
    new_nodes["Separate XYZ.011"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (180, 120)
    new_nodes["Combine XYZ.001"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (180, 680)
    new_nodes["Combine XYZ"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (180, -320)
    new_nodes["Combine XYZ.002"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-1120, -180)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (1160, 160)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Separate XYZ.006"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Separate XYZ.003"].inputs[0])
    tree_links.new(new_nodes["Mix.001"].outputs[0], new_nodes["Group Output"].inputs[1])
    tree_links.new(new_nodes["Math.025"].outputs[0], new_nodes["Math.012"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.003"].outputs[0], new_nodes["Group.005"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.006"].outputs[0], new_nodes["Group.005"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.003"].outputs[1], new_nodes["Group.016"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.006"].outputs[1], new_nodes["Group.016"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.003"].outputs[2], new_nodes["Group.003"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.006"].outputs[2], new_nodes["Group.003"].inputs[0])
    tree_links.new(new_nodes["Math.019"].outputs[0], new_nodes["Noise Texture"].inputs[1])
    tree_links.new(new_nodes["Math.012"].outputs[0], new_nodes["Combine XYZ"].inputs[0])
    tree_links.new(new_nodes["Combine XYZ"].outputs[0], new_nodes["Noise Texture"].inputs[0])
    tree_links.new(new_nodes["Noise Texture"].outputs[1], new_nodes["Mix"].inputs[1])
    tree_links.new(new_nodes["Noise Texture"].outputs[0], new_nodes["Math.021"].inputs[0])
    tree_links.new(new_nodes["Mix"].outputs[0], new_nodes["Mix.001"].inputs[1])
    tree_links.new(new_nodes["Math.021"].outputs[0], new_nodes["Math.022"].inputs[0])
    tree_links.new(new_nodes["Math.022"].outputs[0], new_nodes["Math.023"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Noise Texture"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Noise Texture"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Noise Texture"].inputs[4])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Noise Texture"].inputs[5])
    tree_links.new(new_nodes["Math.017"].outputs[0], new_nodes["Math.019"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Math.019"].inputs[1])
    tree_links.new(new_nodes["Math.024"].outputs[0], new_nodes["Math.025"].inputs[0])
    tree_links.new(new_nodes["Math.026"].outputs[0], new_nodes["Math.027"].inputs[0])
    tree_links.new(new_nodes["Math.027"].outputs[0], new_nodes["Math.017"].inputs[0])
    tree_links.new(new_nodes["Group.016"].outputs[0], new_nodes["Combine XYZ"].inputs[1])
    tree_links.new(new_nodes["Group.003"].outputs[0], new_nodes["Combine XYZ"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Separate XYZ.008"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Separate XYZ.004"].inputs[0])
    tree_links.new(new_nodes["Math.032"].outputs[0], new_nodes["Math.013"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.004"].outputs[2], new_nodes["Group.004"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.008"].outputs[2], new_nodes["Group.004"].inputs[0])
    tree_links.new(new_nodes["Math.036"].outputs[0], new_nodes["Noise Texture.001"].inputs[1])
    tree_links.new(new_nodes["Combine XYZ.001"].outputs[0], new_nodes["Noise Texture.001"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Noise Texture.001"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Noise Texture.001"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Noise Texture.001"].inputs[4])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Noise Texture.001"].inputs[5])
    tree_links.new(new_nodes["Math.018"].outputs[0], new_nodes["Math.036"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Math.036"].inputs[1])
    tree_links.new(new_nodes["Math.031"].outputs[0], new_nodes["Math.032"].inputs[0])
    tree_links.new(new_nodes["Math.034"].outputs[0], new_nodes["Math.035"].inputs[0])
    tree_links.new(new_nodes["Math.035"].outputs[0], new_nodes["Math.018"].inputs[0])
    tree_links.new(new_nodes["Group.004"].outputs[0], new_nodes["Combine XYZ.001"].inputs[2])
    tree_links.new(new_nodes["Math.013"].outputs[0], new_nodes["Combine XYZ.001"].inputs[1])
    tree_links.new(new_nodes["Group.018"].outputs[0], new_nodes["Combine XYZ.001"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.008"].outputs[0], new_nodes["Group.018"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.004"].outputs[0], new_nodes["Group.018"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.008"].outputs[1], new_nodes["Group.006"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.004"].outputs[1], new_nodes["Group.006"].inputs[1])
    tree_links.new(new_nodes["Noise Texture.001"].outputs[1], new_nodes["Mix"].inputs[2])
    tree_links.new(new_nodes["Math.023"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Noise Texture.001"].outputs[0], new_nodes["Math.021"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Separate XYZ.010"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Separate XYZ.011"].inputs[0])
    tree_links.new(new_nodes["Math.037"].outputs[0], new_nodes["Math.014"].inputs[0])
    tree_links.new(new_nodes["Math.041"].outputs[0], new_nodes["Noise Texture.002"].inputs[1])
    tree_links.new(new_nodes["Combine XYZ.002"].outputs[0], new_nodes["Noise Texture.002"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Noise Texture.002"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Noise Texture.002"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Noise Texture.002"].inputs[4])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Noise Texture.002"].inputs[5])
    tree_links.new(new_nodes["Math.020"].outputs[0], new_nodes["Math.041"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Math.041"].inputs[1])
    tree_links.new(new_nodes["Math.043"].outputs[0], new_nodes["Math.037"].inputs[0])
    tree_links.new(new_nodes["Math.039"].outputs[0], new_nodes["Math.040"].inputs[0])
    tree_links.new(new_nodes["Math.040"].outputs[0], new_nodes["Math.020"].inputs[0])
    tree_links.new(new_nodes["Group.019"].outputs[0], new_nodes["Combine XYZ.002"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.010"].outputs[0], new_nodes["Group.019"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.011"].outputs[0], new_nodes["Group.019"].inputs[1])
    tree_links.new(new_nodes["Noise Texture.002"].outputs[1], new_nodes["Mix.001"].inputs[2])
    tree_links.new(new_nodes["Noise Texture.002"].outputs[0], new_nodes["Math.022"].inputs[1])
    tree_links.new(new_nodes["Math.014"].outputs[0], new_nodes["Combine XYZ.002"].inputs[2])
    tree_links.new(new_nodes["Group.008"].outputs[0], new_nodes["Combine XYZ.002"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.010"].outputs[1], new_nodes["Group.008"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.011"].outputs[1], new_nodes["Group.008"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.011"].outputs[2], new_nodes["Group.007"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.010"].outputs[2], new_nodes["Group.007"].inputs[0])
    tree_links.new(new_nodes["Group.007"].outputs[0], new_nodes["Math.043"].inputs[0])
    tree_links.new(new_nodes["Group.007"].outputs[0], new_nodes["Math.039"].inputs[0])
    tree_links.new(new_nodes["Group.006"].outputs[0], new_nodes["Math.034"].inputs[0])
    tree_links.new(new_nodes["Group.006"].outputs[0], new_nodes["Math.031"].inputs[0])
    tree_links.new(new_nodes["Group.005"].outputs[0], new_nodes["Math.024"].inputs[0])
    tree_links.new(new_nodes["Group.005"].outputs[0], new_nodes["Math.026"].inputs[0])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group

def create_duo_node_noise_3e(context, override_create, node_tree_type):
    ensure_node_groups(override_create, [PINGPONG_3E_DUO_NG_NAME,
                                         SAMPLE_3E_DUO_NG_NAME,
                                         NOISE_3E_DUO_NG_NAME],
        node_tree_type, create_prereq_duo_node_group)
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
