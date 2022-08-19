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

PINGPONG_WAVE_3E_DUO_NG_NAME = "PingPongWave3e.BSR"
SINE_WAVE_3E_DUO_NG_NAME = "SineWave3e.BSR"
COSINE_WAVE_3E_DUO_NG_NAME = "CosineWave3e.BSR"
SINE_WAVE_6E_DUO_NG_NAME = "SineWave6e.BSR"
COSINE_WAVE_6E_DUO_NG_NAME = "CosineWave6e.BSR"
PREP_SAMPLE_DUO_NG_NAME = "PrepSample.BSR"
NOISE_6E_DUO_NG_NAME = "Noise6e.BSR"

# depending on the name passed to function, create the right set of nodes in a group and pass back
def create_prereq_duo_node_group(node_group_name, node_tree_type):
    if node_group_name == PINGPONG_WAVE_3E_DUO_NG_NAME:
        return create_duo_ng_ping_pong_wave_3e(node_tree_type)
    elif node_group_name == SINE_WAVE_3E_DUO_NG_NAME:
        return create_duo_ng_sine_wave_3e(node_tree_type)
    elif node_group_name == COSINE_WAVE_3E_DUO_NG_NAME:
        return create_duo_ng_cosine_wave_3e(node_tree_type)
    elif node_group_name == SINE_WAVE_6E_DUO_NG_NAME:
        return create_duo_ng_sine_wave_6e(node_tree_type)
    elif node_group_name == COSINE_WAVE_6E_DUO_NG_NAME:
        return create_duo_ng_cosine_wave_6e(node_tree_type)
    elif node_group_name == PREP_SAMPLE_DUO_NG_NAME:
        return create_duo_ng_prep_sample(node_tree_type)
    elif node_group_name == NOISE_6E_DUO_NG_NAME:
        return create_duo_ng_noise_6e(node_tree_type)

    # error
    print("Unknown name passed to create_custom_geo_node_group: " + str(node_group_name))
    return None

def create_duo_ng_ping_pong_wave_3e(node_tree_type):
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=node_group_name_for_name_and_type(PINGPONG_WAVE_3E_DUO_NG_NAME,
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
    node.inputs[1].default_value = 2.0
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

    return new_node_group

def create_duo_ng_sine_wave_3e(node_tree_type):
    return create_duo_ng_sin_cos_wave_3e(node_tree_type, SINE_WAVE_3E_DUO_NG_NAME, "SINE")

def create_duo_ng_cosine_wave_3e(node_tree_type):
    return create_duo_ng_sin_cos_wave_3e(node_tree_type, COSINE_WAVE_3E_DUO_NG_NAME, "COSINE")

def create_duo_ng_sin_cos_wave_3e(node_tree_type, node_group_name, sin_cos_type):
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=node_group_name_for_name_and_type(node_group_name,
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
    node.location = (80, 0)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = math.pi * 2
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (440, 0)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = 1000.0
    new_nodes["Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (260, 0)
    node.operation = sin_cos_type
    new_nodes["Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-100, 0)
    node.operation = "FRACT"
    new_nodes["Math.006"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-280, 20)
    node.operation = "ADD"
    new_nodes["Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-460, 80)
    node.operation = "FRACT"
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-640, 80)
    node.operation = "DIVIDE"
    node.inputs[1].default_value = 1000.0
    new_nodes["Math"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-540, -80)
    node.operation = "DIVIDE"
    node.inputs[1].default_value = 1000.0
    new_nodes["Math.007"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-840, 0)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (620, 0)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Math.005"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Math.003"].inputs[0])
    tree_links.new(new_nodes["Math.003"].outputs[0], new_nodes["Math.005"].inputs[0])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Math.001"].inputs[0])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Math.004"].inputs[0])
    tree_links.new(new_nodes["Math.007"].outputs[0], new_nodes["Math.004"].inputs[1])
    tree_links.new(new_nodes["Math.004"].outputs[0], new_nodes["Math.006"].inputs[0])
    tree_links.new(new_nodes["Math.006"].outputs[0], new_nodes["Math.002"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Math.007"].inputs[0])

    return new_node_group

def create_duo_ng_sine_wave_6e(node_tree_type):
    return create_duo_ng_sin_cos_wave_6e(node_tree_type, SINE_WAVE_6E_DUO_NG_NAME, "SINE")

def create_duo_ng_cosine_wave_6e(node_tree_type):
    return create_duo_ng_sin_cos_wave_6e(node_tree_type, COSINE_WAVE_6E_DUO_NG_NAME, "COSINE")

def create_duo_ng_sin_cos_wave_6e(node_tree_type, node_group_name, sin_cos_type):
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=node_group_name_for_name_and_type(node_group_name,
                                                                                     node_tree_type),
                                              type=node_tree_type)
    new_node_group.inputs.new(type='NodeSocketFloat', name="Sample Hi")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Sample Mid")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Sample Lo")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Mid Multiplier")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Hi and Lo Multiplier")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Use Hi")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Use Lo")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Value")
    tree_nodes = new_node_group.nodes
    # delete old nodes before adding new nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-400, 160)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = math.pi * 2
    new_nodes["Math.013"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-400, 0)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = math.pi * 2
    new_nodes["Math.012"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-400, -160)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = math.pi * 2
    new_nodes["Math.014"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-220, -160)
    node.operation = sin_cos_type
    new_nodes["Math.011"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-220, 0)
    node.operation = sin_cos_type
    new_nodes["Math.009"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-220, 160)
    node.operation = sin_cos_type
    new_nodes["Math.010"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-20, -0)
    node.operation = "MULTIPLY"
    new_nodes["Math.021"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-20, -180)
    node.operation = "MULTIPLY"
    new_nodes["Math.019"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (220, -20)
    node.operation = "MULTIPLY_ADD"
    new_nodes["Math.027"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-20, 180)
    node.operation = "MULTIPLY"
    new_nodes["Math.020"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (580, -180)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = 1000.0
    new_nodes["Math.028"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (400, -180)
    node.operation = "MULTIPLY_ADD"
    new_nodes["Math.026"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-880, 0)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (760, -180)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Math.012"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Math.013"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Math.014"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Math.019"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Math.021"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Math.026"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Math.027"].inputs[1])
    tree_links.new(new_nodes["Math.028"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Math.012"].outputs[0], new_nodes["Math.009"].inputs[0])
    tree_links.new(new_nodes["Math.013"].outputs[0], new_nodes["Math.010"].inputs[0])
    tree_links.new(new_nodes["Math.014"].outputs[0], new_nodes["Math.011"].inputs[0])
    tree_links.new(new_nodes["Math.011"].outputs[0], new_nodes["Math.019"].inputs[0])
    tree_links.new(new_nodes["Math.010"].outputs[0], new_nodes["Math.020"].inputs[0])
    tree_links.new(new_nodes["Math.009"].outputs[0], new_nodes["Math.021"].inputs[0])
    tree_links.new(new_nodes["Math.019"].outputs[0], new_nodes["Math.026"].inputs[0])
    tree_links.new(new_nodes["Math.020"].outputs[0], new_nodes["Math.027"].inputs[0])
    tree_links.new(new_nodes["Math.021"].outputs[0], new_nodes["Math.027"].inputs[2])
    tree_links.new(new_nodes["Math.027"].outputs[0], new_nodes["Math.026"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Math.020"].inputs[1])
    tree_links.new(new_nodes["Math.026"].outputs[0], new_nodes["Math.028"].inputs[0])

    return new_node_group

def create_duo_ng_prep_sample(node_tree_type):
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=node_group_name_for_name_and_type(PREP_SAMPLE_DUO_NG_NAME,
                                                                                     node_tree_type),
                                              type=node_tree_type)
    new_node_group.inputs.new(type='NodeSocketFloat', name="Value 6e")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Value 0e")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Value World")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Sample Hi")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Sample Mid")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Sample Lo")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Mid Multiplier")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Hi and Lo Multiplier")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Use Hi")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Use Lo")
    tree_nodes = new_node_group.nodes
    # delete old nodes before adding new nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (160, 160)
    node.operation = "DIVIDE"
    node.inputs[1].default_value = 1000.0
    new_nodes["Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Other"
    node.location = (520, -200)
    node.operation = "SUBTRACT"
    node.inputs[0].default_value = 1.0
    new_nodes["Math.018"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Main"
    node.location = (520, -40)
    node.operation = "ADD"
    node.inputs[1].default_value = 0.5
    new_nodes["Math.017"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (520, -380)
    node.operation = "LESS_THAN"
    node.inputs[0].default_value = 0.5
    new_nodes["Math.024"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (520, -540)
    node.operation = "SUBTRACT"
    node.inputs[0].default_value = 1.0
    new_nodes["Math.025"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-100, 320)
    node.operation = "FRACT"
    new_nodes["Math.029"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (340, 320)
    node.operation = "ADD"
    new_nodes["Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (520, 320)
    node.operation = "ADD"
    node.inputs[1].default_value = 0.001
    new_nodes["Math.007"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (520, 160)
    node.operation = "SUBTRACT"
    node.inputs[1].default_value = 0.001
    new_nodes["Math.008"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (340, -40)
    node.operation = "PINGPONG"
    new_nodes["Math.015"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-380, -200)
    node.operation = "DIVIDE"
    node.inputs[1].default_value = 1000.0
    new_nodes["Math.026"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-200, -200)
    node.operation = "FRACT"
    new_nodes["Math.028"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-380, -380)
    node.operation = "DIVIDE"
    node.inputs[1].default_value = 1000.0
    new_nodes["Math.022"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-200, -380)
    node.operation = "FRACT"
    new_nodes["Math.023"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-20, -240)
    node.operation = "ADD"
    new_nodes["Math.009"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (160, -240)
    node.operation = "FRACT"
    new_nodes["Math.010"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-200, 160)
    node.operation = "FLOOR"
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-20, 160)
    node.operation = "ADD"
    new_nodes["Math.006"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-200, -20)
    node.operation = "FLOOR"
    new_nodes["Math.011"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-380, -20)
    node.operation = "DIVIDE"
    node.inputs[1].default_value = 1000.0
    new_nodes["Math.012"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-380, 160)
    node.operation = "DIVIDE"
    node.inputs[1].default_value = 1000.0
    new_nodes["Math.004"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-700, 180)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (820, 260)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Math.005"].outputs[0], new_nodes["Group Output"].inputs[1])
    tree_links.new(new_nodes["Math.007"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Math.008"].outputs[0], new_nodes["Group Output"].inputs[2])
    tree_links.new(new_nodes["Math.018"].outputs[0], new_nodes["Group Output"].inputs[4])
    tree_links.new(new_nodes["Math.017"].outputs[0], new_nodes["Group Output"].inputs[3])
    tree_links.new(new_nodes["Math.025"].outputs[0], new_nodes["Group Output"].inputs[6])
    tree_links.new(new_nodes["Math.024"].outputs[0], new_nodes["Group Output"].inputs[5])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Math.029"].inputs[0])
    tree_links.new(new_nodes["Math.004"].outputs[0], new_nodes["Math.002"].inputs[0])
    tree_links.new(new_nodes["Math.003"].outputs[0], new_nodes["Math.005"].inputs[1])
    tree_links.new(new_nodes["Math.005"].outputs[0], new_nodes["Math.007"].inputs[0])
    tree_links.new(new_nodes["Math.005"].outputs[0], new_nodes["Math.008"].inputs[0])
    tree_links.new(new_nodes["Math.017"].outputs[0], new_nodes["Math.018"].inputs[1])
    tree_links.new(new_nodes["Math.022"].outputs[0], new_nodes["Math.023"].inputs[0])
    tree_links.new(new_nodes["Math.024"].outputs[0], new_nodes["Math.025"].inputs[1])
    tree_links.new(new_nodes["Math.029"].outputs[0], new_nodes["Math.005"].inputs[0])
    tree_links.new(new_nodes["Math.023"].outputs[0], new_nodes["Math.009"].inputs[1])
    tree_links.new(new_nodes["Math.009"].outputs[0], new_nodes["Math.010"].inputs[0])
    tree_links.new(new_nodes["Math.010"].outputs[0], new_nodes["Math.015"].inputs[0])
    tree_links.new(new_nodes["Math.010"].outputs[0], new_nodes["Math.024"].inputs[1])
    tree_links.new(new_nodes["Math.026"].outputs[0], new_nodes["Math.028"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Math.026"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Math.022"].inputs[0])
    tree_links.new(new_nodes["Math.028"].outputs[0], new_nodes["Math.009"].inputs[0])
    tree_links.new(new_nodes["Math.015"].outputs[0], new_nodes["Math.017"].inputs[0])
    tree_links.new(new_nodes["Math.006"].outputs[0], new_nodes["Math.003"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Math.004"].inputs[0])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Math.006"].inputs[0])
    tree_links.new(new_nodes["Math.012"].outputs[0], new_nodes["Math.011"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Math.012"].inputs[0])
    tree_links.new(new_nodes["Math.011"].outputs[0], new_nodes["Math.006"].inputs[1])

    return new_node_group

def create_duo_ng_noise_6e(node_tree_type):
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=node_group_name_for_name_and_type(NOISE_6E_DUO_NG_NAME,
                                                                                     node_tree_type),
                                              type=node_tree_type)
    new_node_group.inputs.new(type='NodeSocketVector', name="Vector 6e")
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
    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (-1260, -1140)
    new_nodes["Separate XYZ.009"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (-1260, -1000)
    new_nodes["Separate XYZ.007"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (-1260, -1280)
    new_nodes["Separate XYZ.008"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (-1120, 1000)
    new_nodes["Separate XYZ.001"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (-1180, 120)
    new_nodes["Separate XYZ.004"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (-1120, 1300)
    new_nodes["Separate XYZ.003"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (-1120, 1160)
    new_nodes["Separate XYZ.002"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (-1180, -240)
    new_nodes["Separate XYZ.005"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (-1180, -60)
    new_nodes["Separate XYZ.006"] = node

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (-880, -1580)
    node.node_tree = bpy.data.node_groups.get(node_group_name_for_name_and_type(PREP_SAMPLE_DUO_NG_NAME,
                                                                                node_tree_type))
    new_nodes["Group.020"] = node

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (-820, 1700)
    node.node_tree = bpy.data.node_groups.get(node_group_name_for_name_and_type(PREP_SAMPLE_DUO_NG_NAME,
                                                                                node_tree_type))
    new_nodes["Group"] = node

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (-820, 240)
    node.node_tree = bpy.data.node_groups.get(node_group_name_for_name_and_type(PREP_SAMPLE_DUO_NG_NAME,
                                                                                node_tree_type))
    new_nodes["Group.013"] = node

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (-440, 1200)
    node.node_tree = bpy.data.node_groups.get(node_group_name_for_name_and_type(PINGPONG_WAVE_3E_DUO_NG_NAME,
                                                                                node_tree_type))
    new_nodes["Group.006"] = node

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (-440, 980)
    node.node_tree = bpy.data.node_groups.get(node_group_name_for_name_and_type(COSINE_WAVE_6E_DUO_NG_NAME,
                                                                                node_tree_type))
    new_nodes["Group.002"] = node

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (-440, 720)
    node.node_tree = bpy.data.node_groups.get(node_group_name_for_name_and_type(COSINE_WAVE_3E_DUO_NG_NAME,
                                                                                node_tree_type))
    new_nodes["Group.004"] = node

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (-440, 500)
    node.node_tree = bpy.data.node_groups.get(node_group_name_for_name_and_type(PINGPONG_WAVE_3E_DUO_NG_NAME,
                                                                                node_tree_type))
    new_nodes["Group.007"] = node

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (-440, -80)
    node.node_tree = bpy.data.node_groups.get(node_group_name_for_name_and_type(PINGPONG_WAVE_3E_DUO_NG_NAME,
                                                                                node_tree_type))
    new_nodes["Group.008"] = node

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (-440, -520)
    node.node_tree = bpy.data.node_groups.get(node_group_name_for_name_and_type(COSINE_WAVE_3E_DUO_NG_NAME,
                                                                                node_tree_type))
    new_nodes["Group.012"] = node

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (-440, -940)
    node.node_tree = bpy.data.node_groups.get(node_group_name_for_name_and_type(PINGPONG_WAVE_3E_DUO_NG_NAME,
                                                                                node_tree_type))
    new_nodes["Group.018"] = node

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (-440, -1120)
    node.node_tree = bpy.data.node_groups.get(node_group_name_for_name_and_type(SINE_WAVE_6E_DUO_NG_NAME,
                                                                                node_tree_type))
    new_nodes["Group.014"] = node

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (-440, -1360)
    node.node_tree = bpy.data.node_groups.get(node_group_name_for_name_and_type(SINE_WAVE_3E_DUO_NG_NAME,
                                                                                node_tree_type))
    new_nodes["Group.019"] = node

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (-440, -1540)
    node.node_tree = bpy.data.node_groups.get(node_group_name_for_name_and_type(COSINE_WAVE_6E_DUO_NG_NAME,
                                                                                node_tree_type))
    new_nodes["Group.016"] = node

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (-440, -1800)
    node.node_tree = bpy.data.node_groups.get(node_group_name_for_name_and_type(COSINE_WAVE_3E_DUO_NG_NAME,
                                                                                node_tree_type))
    new_nodes["Group.017"] = node

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (-440, 1540)
    node.node_tree = bpy.data.node_groups.get(node_group_name_for_name_and_type(SINE_WAVE_3E_DUO_NG_NAME,
                                                                                node_tree_type))
    new_nodes["Group.003"] = node

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (-440, 1800)
    node.node_tree = bpy.data.node_groups.get(node_group_name_for_name_and_type(SINE_WAVE_6E_DUO_NG_NAME,
                                                                                node_tree_type))
    new_nodes["Group.001"] = node

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (-440, 1340)
    node.node_tree = bpy.data.node_groups.get(node_group_name_for_name_and_type(PINGPONG_WAVE_3E_DUO_NG_NAME,
                                                                                node_tree_type))
    new_nodes["Group.005"] = node

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (-440, -780)
    node.node_tree = bpy.data.node_groups.get(node_group_name_for_name_and_type(PINGPONG_WAVE_3E_DUO_NG_NAME,
                                                                                node_tree_type))
    new_nodes["Group.015"] = node

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (-440, 60)
    node.node_tree = bpy.data.node_groups.get(node_group_name_for_name_and_type(SINE_WAVE_3E_DUO_NG_NAME,
                                                                                node_tree_type))
    new_nodes["Group.009"] = node

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (-440, 340)
    node.node_tree = bpy.data.node_groups.get(node_group_name_for_name_and_type(SINE_WAVE_6E_DUO_NG_NAME,
                                                                                node_tree_type))
    new_nodes["Group.010"] = node

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (-440, -260)
    node.node_tree = bpy.data.node_groups.get(node_group_name_for_name_and_type(COSINE_WAVE_6E_DUO_NG_NAME,
                                                                                node_tree_type))
    new_nodes["Group.011"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-180, 1200)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = 1000.0
    new_nodes["Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-180, 1360)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = 1000.0
    new_nodes["Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-180, 520)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = 1000.0
    new_nodes["Math.010"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-180, -60)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = 1000.0
    new_nodes["Math.008"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-180, -760)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = 1000.0
    new_nodes["Math.017"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-180, -940)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = 1000.0
    new_nodes["Math.020"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-180, 1640)
    node.operation = "MULTIPLY_ADD"
    node.inputs[1].default_value = 1000.0
    new_nodes["Math"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-180, 960)
    node.operation = "MULTIPLY_ADD"
    node.inputs[1].default_value = 1000.0
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-180, 180)
    node.operation = "MULTIPLY_ADD"
    node.inputs[1].default_value = 1000.0
    new_nodes["Math.006"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-180, -280)
    node.operation = "MULTIPLY_ADD"
    node.inputs[1].default_value = 1000.0
    new_nodes["Math.009"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-180, -1560)
    node.operation = "MULTIPLY_ADD"
    node.inputs[1].default_value = 1000.0
    new_nodes["Math.018"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-180, -1180)
    node.operation = "MULTIPLY_ADD"
    node.inputs[1].default_value = 1000.0
    new_nodes["Math.015"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (0, 1640)
    node.operation = "DIVIDE"
    node.inputs[1].default_value = 4.0
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (0, 180)
    node.operation = "DIVIDE"
    node.inputs[1].default_value = 4.0
    new_nodes["Math.007"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (0, -1180)
    node.operation = "DIVIDE"
    node.inputs[1].default_value = 4.0
    new_nodes["Math.016"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (0, -1560)
    node.operation = "DIVIDE"
    node.inputs[1].default_value = 4.0
    new_nodes["Math.019"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (0, -280)
    node.operation = "DIVIDE"
    node.inputs[1].default_value = 4.0
    new_nodes["Math.011"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (0, 960)
    node.operation = "DIVIDE"
    node.inputs[1].default_value = 4.0
    new_nodes["Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (240, -140)
    node.operation = "ADD"
    new_nodes["Math.021"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (180, 760)
    node.operation = "ADD"
    new_nodes["Math.022"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (220, -1060)
    node.operation = "ADD"
    new_nodes["Math.023"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (740, 360)
    node.operation = "ADD"
    new_nodes["Math.012"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (960, 160)
    node.operation = "ADD"
    new_nodes["Math.013"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1140, 160)
    node.operation = "DIVIDE"
    node.inputs[1].default_value = 3.0
    new_nodes["Math.014"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (200, 1400)
    new_nodes["Combine XYZ.002"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (240, 200)
    new_nodes["Combine XYZ.003"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (220, -840)
    new_nodes["Combine XYZ.004"] = node

    node = tree_nodes.new(type="ShaderNodeTexNoise")
    node.location = (500, 480)
    new_nodes["Noise Texture"] = node

    node = tree_nodes.new(type="ShaderNodeTexNoise")
    node.location = (500, 160)
    new_nodes["Noise Texture.001"] = node

    node = tree_nodes.new(type="ShaderNodeTexNoise")
    node.location = (480, -660)
    new_nodes["Noise Texture.002"] = node

    node = tree_nodes.new(type="ShaderNodeMixRGB")
    node.location = (740, 180)
    node.blend_type = "MIX"
    node.inputs[0].default_value = 0.5
    new_nodes["Mix"] = node

    node = tree_nodes.new(type="ShaderNodeMixRGB")
    node.location = (960, 0)
    node.blend_type = "MIX"
    node.inputs[0].default_value = 1.0 / 3.0
    new_nodes["Mix.001"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-1640, -360)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (1320, 20)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Separate XYZ.002"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Separate XYZ.003"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Separate XYZ.001"].inputs[0])
    tree_links.new(new_nodes["Math.014"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Mix.001"].outputs[0], new_nodes["Group Output"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[0], new_nodes["Group"].inputs[2])
    tree_links.new(new_nodes["Separate XYZ.002"].outputs[0], new_nodes["Group"].inputs[1])
    tree_links.new(new_nodes["Group"].outputs[1], new_nodes["Group.001"].inputs[1])
    tree_links.new(new_nodes["Group"].outputs[0], new_nodes["Group.001"].inputs[0])
    tree_links.new(new_nodes["Group"].outputs[2], new_nodes["Group.001"].inputs[2])
    tree_links.new(new_nodes["Group"].outputs[4], new_nodes["Group.001"].inputs[4])
    tree_links.new(new_nodes["Group"].outputs[3], new_nodes["Group.001"].inputs[3])
    tree_links.new(new_nodes["Group"].outputs[6], new_nodes["Group.001"].inputs[6])
    tree_links.new(new_nodes["Group"].outputs[5], new_nodes["Group.001"].inputs[5])
    tree_links.new(new_nodes["Separate XYZ.003"].outputs[0], new_nodes["Group"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[0], new_nodes["Group.003"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.002"].outputs[0], new_nodes["Group.003"].inputs[0])
    tree_links.new(new_nodes["Group"].outputs[0], new_nodes["Group.002"].inputs[0])
    tree_links.new(new_nodes["Group"].outputs[1], new_nodes["Group.002"].inputs[1])
    tree_links.new(new_nodes["Group"].outputs[2], new_nodes["Group.002"].inputs[2])
    tree_links.new(new_nodes["Group"].outputs[3], new_nodes["Group.002"].inputs[3])
    tree_links.new(new_nodes["Group"].outputs[4], new_nodes["Group.002"].inputs[4])
    tree_links.new(new_nodes["Group"].outputs[5], new_nodes["Group.002"].inputs[5])
    tree_links.new(new_nodes["Group"].outputs[6], new_nodes["Group.002"].inputs[6])
    tree_links.new(new_nodes["Group.001"].outputs[0], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Group.003"].outputs[0], new_nodes["Math"].inputs[2])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Math.001"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[0], new_nodes["Group.004"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.002"].outputs[0], new_nodes["Group.004"].inputs[0])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Math.003"].inputs[0])
    tree_links.new(new_nodes["Group.002"].outputs[0], new_nodes["Math.002"].inputs[0])
    tree_links.new(new_nodes["Group.004"].outputs[0], new_nodes["Math.002"].inputs[2])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[1], new_nodes["Group.005"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.002"].outputs[1], new_nodes["Group.005"].inputs[0])
    tree_links.new(new_nodes["Group.005"].outputs[0], new_nodes["Math.004"].inputs[0])
    tree_links.new(new_nodes["Group.006"].outputs[0], new_nodes["Math.005"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[2], new_nodes["Group.006"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.002"].outputs[2], new_nodes["Group.006"].inputs[0])
    tree_links.new(new_nodes["Math.022"].outputs[0], new_nodes["Noise Texture"].inputs[1])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Combine XYZ.002"].inputs[0])
    tree_links.new(new_nodes["Math.004"].outputs[0], new_nodes["Combine XYZ.002"].inputs[1])
    tree_links.new(new_nodes["Math.005"].outputs[0], new_nodes["Combine XYZ.002"].inputs[2])
    tree_links.new(new_nodes["Combine XYZ.002"].outputs[0], new_nodes["Noise Texture"].inputs[0])
    tree_links.new(new_nodes["Group.013"].outputs[1], new_nodes["Group.010"].inputs[1])
    tree_links.new(new_nodes["Group.013"].outputs[0], new_nodes["Group.010"].inputs[0])
    tree_links.new(new_nodes["Group.013"].outputs[2], new_nodes["Group.010"].inputs[2])
    tree_links.new(new_nodes["Group.013"].outputs[4], new_nodes["Group.010"].inputs[4])
    tree_links.new(new_nodes["Group.013"].outputs[3], new_nodes["Group.010"].inputs[3])
    tree_links.new(new_nodes["Group.013"].outputs[6], new_nodes["Group.010"].inputs[6])
    tree_links.new(new_nodes["Group.013"].outputs[5], new_nodes["Group.010"].inputs[5])
    tree_links.new(new_nodes["Group.013"].outputs[0], new_nodes["Group.011"].inputs[0])
    tree_links.new(new_nodes["Group.013"].outputs[1], new_nodes["Group.011"].inputs[1])
    tree_links.new(new_nodes["Group.013"].outputs[2], new_nodes["Group.011"].inputs[2])
    tree_links.new(new_nodes["Group.013"].outputs[3], new_nodes["Group.011"].inputs[3])
    tree_links.new(new_nodes["Group.013"].outputs[4], new_nodes["Group.011"].inputs[4])
    tree_links.new(new_nodes["Group.013"].outputs[5], new_nodes["Group.011"].inputs[5])
    tree_links.new(new_nodes["Group.013"].outputs[6], new_nodes["Group.011"].inputs[6])
    tree_links.new(new_nodes["Group.010"].outputs[0], new_nodes["Math.006"].inputs[0])
    tree_links.new(new_nodes["Group.009"].outputs[0], new_nodes["Math.006"].inputs[2])
    tree_links.new(new_nodes["Math.006"].outputs[0], new_nodes["Math.007"].inputs[0])
    tree_links.new(new_nodes["Math.009"].outputs[0], new_nodes["Math.011"].inputs[0])
    tree_links.new(new_nodes["Group.011"].outputs[0], new_nodes["Math.009"].inputs[0])
    tree_links.new(new_nodes["Group.012"].outputs[0], new_nodes["Math.009"].inputs[2])
    tree_links.new(new_nodes["Group.007"].outputs[0], new_nodes["Math.010"].inputs[0])
    tree_links.new(new_nodes["Group.008"].outputs[0], new_nodes["Math.008"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.005"].outputs[2], new_nodes["Group.008"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.006"].outputs[2], new_nodes["Group.008"].inputs[0])
    tree_links.new(new_nodes["Math.021"].outputs[0], new_nodes["Noise Texture.001"].inputs[1])
    tree_links.new(new_nodes["Math.008"].outputs[0], new_nodes["Combine XYZ.003"].inputs[2])
    tree_links.new(new_nodes["Combine XYZ.003"].outputs[0], new_nodes["Noise Texture.001"].inputs[0])
    tree_links.new(new_nodes["Math.010"].outputs[0], new_nodes["Combine XYZ.003"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.004"].outputs[1], new_nodes["Group.013"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.006"].outputs[1], new_nodes["Group.013"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.005"].outputs[1], new_nodes["Group.013"].inputs[2])
    tree_links.new(new_nodes["Separate XYZ.006"].outputs[1], new_nodes["Group.009"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.005"].outputs[1], new_nodes["Group.009"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.005"].outputs[0], new_nodes["Group.007"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.006"].outputs[0], new_nodes["Group.007"].inputs[0])
    tree_links.new(new_nodes["Math.007"].outputs[0], new_nodes["Combine XYZ.003"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.005"].outputs[1], new_nodes["Group.012"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.006"].outputs[1], new_nodes["Group.012"].inputs[0])
    tree_links.new(new_nodes["Noise Texture"].outputs[1], new_nodes["Mix"].inputs[1])
    tree_links.new(new_nodes["Noise Texture.001"].outputs[1], new_nodes["Mix"].inputs[2])
    tree_links.new(new_nodes["Noise Texture.001"].outputs[0], new_nodes["Math.012"].inputs[1])
    tree_links.new(new_nodes["Noise Texture"].outputs[0], new_nodes["Math.012"].inputs[0])
    tree_links.new(new_nodes["Mix"].outputs[0], new_nodes["Mix.001"].inputs[1])
    tree_links.new(new_nodes["Math.012"].outputs[0], new_nodes["Math.013"].inputs[0])
    tree_links.new(new_nodes["Math.013"].outputs[0], new_nodes["Math.014"].inputs[0])
    tree_links.new(new_nodes["Group.020"].outputs[1], new_nodes["Group.014"].inputs[1])
    tree_links.new(new_nodes["Group.020"].outputs[0], new_nodes["Group.014"].inputs[0])
    tree_links.new(new_nodes["Group.020"].outputs[2], new_nodes["Group.014"].inputs[2])
    tree_links.new(new_nodes["Group.020"].outputs[4], new_nodes["Group.014"].inputs[4])
    tree_links.new(new_nodes["Group.020"].outputs[3], new_nodes["Group.014"].inputs[3])
    tree_links.new(new_nodes["Group.020"].outputs[6], new_nodes["Group.014"].inputs[6])
    tree_links.new(new_nodes["Group.020"].outputs[5], new_nodes["Group.014"].inputs[5])
    tree_links.new(new_nodes["Group.020"].outputs[0], new_nodes["Group.016"].inputs[0])
    tree_links.new(new_nodes["Group.020"].outputs[1], new_nodes["Group.016"].inputs[1])
    tree_links.new(new_nodes["Group.020"].outputs[2], new_nodes["Group.016"].inputs[2])
    tree_links.new(new_nodes["Group.020"].outputs[3], new_nodes["Group.016"].inputs[3])
    tree_links.new(new_nodes["Group.020"].outputs[4], new_nodes["Group.016"].inputs[4])
    tree_links.new(new_nodes["Group.020"].outputs[5], new_nodes["Group.016"].inputs[5])
    tree_links.new(new_nodes["Group.020"].outputs[6], new_nodes["Group.016"].inputs[6])
    tree_links.new(new_nodes["Group.014"].outputs[0], new_nodes["Math.015"].inputs[0])
    tree_links.new(new_nodes["Group.019"].outputs[0], new_nodes["Math.015"].inputs[2])
    tree_links.new(new_nodes["Math.015"].outputs[0], new_nodes["Math.016"].inputs[0])
    tree_links.new(new_nodes["Math.018"].outputs[0], new_nodes["Math.019"].inputs[0])
    tree_links.new(new_nodes["Group.016"].outputs[0], new_nodes["Math.018"].inputs[0])
    tree_links.new(new_nodes["Group.017"].outputs[0], new_nodes["Math.018"].inputs[2])
    tree_links.new(new_nodes["Group.015"].outputs[0], new_nodes["Math.017"].inputs[0])
    tree_links.new(new_nodes["Group.018"].outputs[0], new_nodes["Math.020"].inputs[0])
    tree_links.new(new_nodes["Math.023"].outputs[0], new_nodes["Noise Texture.002"].inputs[1])
    tree_links.new(new_nodes["Combine XYZ.004"].outputs[0], new_nodes["Noise Texture.002"].inputs[0])
    tree_links.new(new_nodes["Math.017"].outputs[0], new_nodes["Combine XYZ.004"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.009"].outputs[1], new_nodes["Group.019"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.008"].outputs[1], new_nodes["Group.019"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.008"].outputs[0], new_nodes["Group.015"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.009"].outputs[0], new_nodes["Group.015"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.007"].outputs[2], new_nodes["Group.020"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.008"].outputs[2], new_nodes["Group.020"].inputs[2])
    tree_links.new(new_nodes["Separate XYZ.009"].outputs[2], new_nodes["Group.020"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.008"].outputs[2], new_nodes["Group.017"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.009"].outputs[2], new_nodes["Group.017"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.008"].outputs[1], new_nodes["Group.018"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.009"].outputs[1], new_nodes["Group.018"].inputs[0])
    tree_links.new(new_nodes["Math.016"].outputs[0], new_nodes["Combine XYZ.004"].inputs[2])
    tree_links.new(new_nodes["Math.020"].outputs[0], new_nodes["Combine XYZ.004"].inputs[1])
    tree_links.new(new_nodes["Noise Texture.002"].outputs[1], new_nodes["Mix.001"].inputs[2])
    tree_links.new(new_nodes["Noise Texture.002"].outputs[0], new_nodes["Math.013"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Separate XYZ.007"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Separate XYZ.009"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Separate XYZ.008"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Separate XYZ.004"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Separate XYZ.006"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Separate XYZ.005"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Noise Texture"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Noise Texture"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Noise Texture"].inputs[4])
    tree_links.new(new_nodes["Group Input"].outputs[7], new_nodes["Noise Texture"].inputs[5])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Noise Texture.001"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Noise Texture.001"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Noise Texture.001"].inputs[4])
    tree_links.new(new_nodes["Group Input"].outputs[7], new_nodes["Noise Texture.001"].inputs[5])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Noise Texture.002"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Noise Texture.002"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Noise Texture.002"].inputs[4])
    tree_links.new(new_nodes["Group Input"].outputs[7], new_nodes["Noise Texture.002"].inputs[5])
    tree_links.new(new_nodes["Math.011"].outputs[0], new_nodes["Math.021"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Math.021"].inputs[0])
    tree_links.new(new_nodes["Math.003"].outputs[0], new_nodes["Math.022"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Math.022"].inputs[1])
    tree_links.new(new_nodes["Math.019"].outputs[0], new_nodes["Math.023"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Math.023"].inputs[0])

    return new_node_group

def create_duo_node_noise_6e(context, override_create, node_tree_type):
    ensure_node_groups(override_create, [PINGPONG_WAVE_3E_DUO_NG_NAME,
                                         SINE_WAVE_3E_DUO_NG_NAME,
                                         COSINE_WAVE_3E_DUO_NG_NAME,
                                         SINE_WAVE_6E_DUO_NG_NAME,
                                         COSINE_WAVE_6E_DUO_NG_NAME,
                                         PREP_SAMPLE_DUO_NG_NAME,
                                         NOISE_6E_DUO_NG_NAME],
        node_tree_type, create_prereq_duo_node_group)
    node = context.space_data.edit_tree.nodes.new(type=get_node_group_for_type(node_tree_type))
    node.node_tree = bpy.data.node_groups.get(node_group_name_for_name_and_type(NOISE_6E_DUO_NG_NAME, node_tree_type))
    node.inputs[4].default_value = 1.0
    node.inputs[5].default_value = 2.0
    node.inputs[6].default_value = 0.5

class BSR_Noise6eCreateDuoNode(bpy.types.Operator):
    bl_description = "Add a Mega Noise Texture node"
    bl_idname = "big_space_rig.noise_6e_create_duo_node"
    bl_label = "Noise 6e (Mega)"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        s = context.space_data
        if s.type == 'NODE_EDITOR' and s.node_tree != None and \
            s.tree_type in ('CompositorNodeTree', 'ShaderNodeTree', 'TextureNodeTree', 'GeometryNodeTree'):
            return True
        return False

    def execute(self, context):
        create_duo_node_noise_6e(context, False, context.space_data.edit_tree.bl_idname)
        return {'FINISHED'}
