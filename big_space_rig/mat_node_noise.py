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

MOD_DUO_NG_NAME = "TexMod.BSR"
PING_PONG_DUO_NG_NAME = "TexPingPong.BSR"
NOISE_9E_DUO_NG_NAME = "Noise9e.BSR"
NOISE_6E_DUO_NG_NAME = "Noise6e.BSR"

# depending on the name passed to function, create the right set of nodes in a group and pass back
def create_prereq_duo_node_group(node_group_name, node_tree_type):
    if node_group_name == MOD_DUO_NG_NAME:
        return create_duo_ng_tex_mod(node_tree_type)
    elif node_group_name == PING_PONG_DUO_NG_NAME:
        return create_duo_ng_tex_ping_pong(node_tree_type)
    elif node_group_name == NOISE_9E_DUO_NG_NAME:
        return create_duo_ng_noise_9e(node_tree_type)
    elif node_group_name == NOISE_6E_DUO_NG_NAME:
        return create_duo_ng_noise_6e(node_tree_type)
    # error
    print("Unknown name passed to create_custom_geo_node_group: " + str(node_group_name))
    return None

def create_duo_ng_tex_mod(node_tree_type):
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=node_group_name_for_name_and_type(MOD_DUO_NG_NAME, node_tree_type),
                                              type=node_tree_type)
    new_node_group.inputs.new(type='NodeSocketVector', name="Vec 6e")
    new_node_group.inputs.new(type='NodeSocketVector', name="Vec 0e")
    new_node_group.outputs.new(type='NodeSocketVector', name="Vector")
    tree_nodes = new_node_group.nodes
    # delete old nodes before adding new nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-10, -420)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = 1000.0
    new_nodes["Math.039"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-10, 240)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = 1000.0
    new_nodes["Math.031"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-10, 80)
    node.operation = "DIVIDE"
    node.inputs[1].default_value = 1000.0
    new_nodes["Math.035"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-10, -80)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = 1000.0
    new_nodes["Math.036"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (190, 0)
    node.operation = "ADD"
    new_nodes["Math.037"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-10, -260)
    node.operation = "DIVIDE"
    node.inputs[1].default_value = 1000.0
    new_nodes["Math.038"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-190, -20)
    node.operation = "MODULO"
    node.inputs[1].default_value = 1.0
    new_nodes["Math.034"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-10, 420)
    node.operation = "DIVIDE"
    node.inputs[1].default_value = 1000.0
    new_nodes["Math.032"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (-430, 100)
    new_nodes["Separate XYZ.002"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (-450, -200)
    new_nodes["Separate XYZ.003"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (450, 60)
    new_nodes["Combine XYZ"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (190, -260)
    node.operation = "ADD"
    new_nodes["Math.040"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-190, -260)
    node.operation = "MODULO"
    node.inputs[1].default_value = 1.0
    new_nodes["Math.041"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-190, 240)
    node.operation = "MODULO"
    node.inputs[1].default_value = 1.0
    new_nodes["Math.030"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (190, 240)
    node.operation = "ADD"
    new_nodes["Math.033"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-650, 0)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (640, 0)
    new_nodes["Group Output"] = node

    # links between nodes
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Separate XYZ.003"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Separate XYZ.002"].inputs[0])
    tree_links.new(new_nodes["Combine XYZ"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.003"].outputs[0], new_nodes["Math.030"].inputs[0])
    tree_links.new(new_nodes["Math.030"].outputs[0], new_nodes["Math.031"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.002"].outputs[0], new_nodes["Math.032"].inputs[0])
    tree_links.new(new_nodes["Math.032"].outputs[0], new_nodes["Math.033"].inputs[0])
    tree_links.new(new_nodes["Math.031"].outputs[0], new_nodes["Math.033"].inputs[1])
    tree_links.new(new_nodes["Math.034"].outputs[0], new_nodes["Math.036"].inputs[0])
    tree_links.new(new_nodes["Math.035"].outputs[0], new_nodes["Math.037"].inputs[0])
    tree_links.new(new_nodes["Math.036"].outputs[0], new_nodes["Math.037"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.003"].outputs[1], new_nodes["Math.034"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.002"].outputs[1], new_nodes["Math.035"].inputs[0])
    tree_links.new(new_nodes["Math.041"].outputs[0], new_nodes["Math.039"].inputs[0])
    tree_links.new(new_nodes["Math.038"].outputs[0], new_nodes["Math.040"].inputs[0])
    tree_links.new(new_nodes["Math.039"].outputs[0], new_nodes["Math.040"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.002"].outputs[2], new_nodes["Math.038"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.003"].outputs[2], new_nodes["Math.041"].inputs[0])
    tree_links.new(new_nodes["Math.033"].outputs[0], new_nodes["Combine XYZ"].inputs[0])
    tree_links.new(new_nodes["Math.037"].outputs[0], new_nodes["Combine XYZ"].inputs[1])
    tree_links.new(new_nodes["Math.040"].outputs[0], new_nodes["Combine XYZ"].inputs[2])

    return new_node_group

def create_duo_ng_tex_ping_pong(node_tree_type):
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=node_group_name_for_name_and_type(PING_PONG_DUO_NG_NAME,
                                                                                     node_tree_type),
                                              type=node_tree_type)
    new_node_group.inputs.new(type='NodeSocketVector', name="Vector")
    new_node_group.inputs.new(type='NodeSocketVector', name="Offset")
    new_node_group.outputs.new(type='NodeSocketVector', name="Vector")
    tree_nodes = new_node_group.nodes
    # delete old nodes before adding new nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (0, -70)
    node.operation = "PINGPONG"
    new_nodes["Math.012"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (0, -250)
    node.operation = "SIGN"
    new_nodes["Math.043"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (0, -390)
    node.operation = "PINGPONG"
    node.inputs[1].default_value = 0.5
    new_nodes["Math.016"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (180, -230)
    node.operation = "MULTIPLY"
    new_nodes["Math.044"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (0, 390)
    node.operation = "SIGN"
    new_nodes["Math.045"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (0, 250)
    node.operation = "PINGPONG"
    node.inputs[1].default_value = 0.5
    new_nodes["Math.007"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (0, 70)
    node.operation = "SIGN"
    new_nodes["Math.029"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (180, 70)
    node.operation = "MULTIPLY"
    new_nodes["Math.042"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (180, 310)
    node.operation = "MULTIPLY"
    new_nodes["Math.028"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (400, 130)
    new_nodes["Combine XYZ.001"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (810, 0)
    new_nodes["Group Output"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-820, -80)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-620, -20)
    node.operation = "DIVIDE"
    node.inputs[1].default_value = (1000.0, 1000.0, 1000.0)
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-440, -20)
    node.operation = "ADD"
    new_nodes["Vector Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (-260, -20)
    new_nodes["Separate XYZ.001"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (580, 100)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = (1000.0, 1000.0, 1000.0)
    new_nodes["Vector Math.002"] = node

    # links between nodes
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Vector Math.002"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Math.045"].outputs[0], new_nodes["Math.028"].inputs[0])
    tree_links.new(new_nodes["Math.029"].outputs[0], new_nodes["Math.042"].inputs[0])
    tree_links.new(new_nodes["Math.043"].outputs[0], new_nodes["Math.044"].inputs[0])
    tree_links.new(new_nodes["Vector Math.001"].outputs[0], new_nodes["Separate XYZ.001"].inputs[0])
    tree_links.new(new_nodes["Vector Math"].outputs[0], new_nodes["Vector Math.001"].inputs[0])
    tree_links.new(new_nodes["Math.007"].outputs[0], new_nodes["Math.028"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[0], new_nodes["Math.045"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[0], new_nodes["Math.007"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[1], new_nodes["Math.012"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[1], new_nodes["Math.029"].inputs[0])
    tree_links.new(new_nodes["Math.012"].outputs[0], new_nodes["Math.042"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[2], new_nodes["Math.043"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[2], new_nodes["Math.016"].inputs[0])
    tree_links.new(new_nodes["Math.016"].outputs[0], new_nodes["Math.044"].inputs[1])
    tree_links.new(new_nodes["Combine XYZ.001"].outputs[0], new_nodes["Vector Math.002"].inputs[0])
    tree_links.new(new_nodes["Math.028"].outputs[0], new_nodes["Combine XYZ.001"].inputs[0])
    tree_links.new(new_nodes["Math.042"].outputs[0], new_nodes["Combine XYZ.001"].inputs[1])
    tree_links.new(new_nodes["Math.044"].outputs[0], new_nodes["Combine XYZ.001"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Vector Math.001"].inputs[1])

    return new_node_group

def create_duo_ng_noise_9e(node_tree_type):
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=node_group_name_for_name_and_type(NOISE_9E_DUO_NG_NAME,
                                                                                     node_tree_type),
                                              type=node_tree_type)
    new_node_group.inputs.new(type='NodeSocketVector', name="Loc 6e")
    new_node_group.inputs.new(type='NodeSocketVector', name="Loc 0e")
    new_node_group.inputs.new(type='NodeSocketFloat', name="W")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Detail")
    new_node_group.inputs.new(type='NodeSocketFloatFactor', name="Roughness")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Distortion")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Fac")
    new_node_group.outputs.new(type='NodeSocketColor', name="Color")
    tree_nodes = new_node_group.nodes
    # delete old nodes before adding new nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeTexNoise")
    node.location = (-200, 120)
    node.noise_dimensions = '4D'
    node.inputs[2].default_value = 1.0
    new_nodes["Noise Texture.005"] = node

    node = tree_nodes.new(type="ShaderNodeTexNoise")
    node.location = (340, 560)
    node.noise_dimensions = '4D'
    node.inputs[2].default_value = 1.0
    new_nodes["Noise Texture.003"] = node

    node = tree_nodes.new(type="ShaderNodeTexNoise")
    node.location = (520, 760)
    node.noise_dimensions = '4D'
    node.inputs[2].default_value = 1.0
    new_nodes["Noise Texture.002"] = node

    node = tree_nodes.new(type="ShaderNodeTexNoise")
    node.location = (-20, 340)
    node.noise_dimensions = '4D'
    node.inputs[2].default_value = 1.0
    new_nodes["Noise Texture.004"] = node

    node = tree_nodes.new(type="ShaderNodeTexNoise")
    node.location = (880, 1020)
    node.noise_dimensions = '4D'
    node.inputs[2].default_value = 1.0
    new_nodes["Noise Texture.001"] = node

    node = tree_nodes.new(type="ShaderNodeTexNoise")
    node.location = (1060, 1240)
    node.noise_dimensions = '4D'
    node.inputs[2].default_value = 1.0
    new_nodes["Noise Texture"] = node

    node = tree_nodes.new(type=get_node_group_for_type(node_tree_type))
    node.location = (340, 780)
    node.node_tree = bpy.data.node_groups.get(node_group_name_for_name_and_type(PING_PONG_DUO_NG_NAME, node_tree_type))
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    new_nodes["Group.002"] = node

    node = tree_nodes.new(type=get_node_group_for_type(node_tree_type))
    node.location = (-200, 340)
    node.node_tree = bpy.data.node_groups.get(node_group_name_for_name_and_type(PING_PONG_DUO_NG_NAME, node_tree_type))
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    new_nodes["Group.004"] = node

    node = tree_nodes.new(type=get_node_group_for_type(node_tree_type))
    node.location = (160, 560)
    node.node_tree = bpy.data.node_groups.get(node_group_name_for_name_and_type(PING_PONG_DUO_NG_NAME, node_tree_type))
    node.inputs[1].default_value = (0.5, 0.5, 0.5)
    new_nodes["Group.003"] = node

    node = tree_nodes.new(type=get_node_group_for_type(node_tree_type))
    node.location = (-380, 80)
    node.node_tree = bpy.data.node_groups.get(node_group_name_for_name_and_type(PING_PONG_DUO_NG_NAME, node_tree_type))
    node.inputs[1].default_value = (0.5, 0.5, 0.5)
    new_nodes["Group.005"] = node

    node = tree_nodes.new(type=get_node_group_for_type(node_tree_type))
    node.location = (880, 1240)
    node.node_tree = bpy.data.node_groups.get(node_group_name_for_name_and_type(PING_PONG_DUO_NG_NAME, node_tree_type))
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    new_nodes["Group.001"] = node

    node = tree_nodes.new(type=get_node_group_for_type(node_tree_type))
    node.location = (520, 1020)
    node.node_tree = bpy.data.node_groups.get(node_group_name_for_name_and_type(PING_PONG_DUO_NG_NAME, node_tree_type))
    node.inputs[1].default_value = (0.5, 0.5, 0.5)
    new_nodes["Group"] = node

    node = tree_nodes.new(type=get_node_group_for_type(node_tree_type))
    node.location = (-100, 580)
    node.node_tree = bpy.data.node_groups.get(node_group_name_for_name_and_type(MOD_DUO_NG_NAME, node_tree_type))
    new_nodes["Group.006"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (700, 920)
    node.operation = "ADD"
    new_nodes["Math"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (1240, 1240)
    new_nodes["Group Output"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-840, 520)
    new_nodes["Group Input"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Noise Texture"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Group.006"].inputs[0])
    tree_links.new(new_nodes["Group"].outputs[0], new_nodes["Noise Texture.001"].inputs[0])
    tree_links.new(new_nodes["Noise Texture.003"].outputs[0], new_nodes["Noise Texture.002"].inputs[1])
    tree_links.new(new_nodes["Noise Texture.005"].outputs[0], new_nodes["Noise Texture.004"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Group.006"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Noise Texture.005"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Noise Texture.005"].inputs[4])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Noise Texture.005"].inputs[5])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Noise Texture.004"].inputs[5])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Noise Texture.004"].inputs[4])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Noise Texture.004"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Noise Texture.003"].inputs[5])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Noise Texture.003"].inputs[4])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Noise Texture.003"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Noise Texture.002"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Noise Texture.002"].inputs[4])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Noise Texture.002"].inputs[5])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Noise Texture.001"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Noise Texture.001"].inputs[4])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Noise Texture.001"].inputs[5])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Noise Texture"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Noise Texture"].inputs[4])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Noise Texture"].inputs[5])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Noise Texture.005"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Group"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Group.001"].inputs[0])
    tree_links.new(new_nodes["Group.001"].outputs[0], new_nodes["Noise Texture"].inputs[0])
    tree_links.new(new_nodes["Group.006"].outputs[0], new_nodes["Group.002"].inputs[0])
    tree_links.new(new_nodes["Group.002"].outputs[0], new_nodes["Noise Texture.002"].inputs[0])
    tree_links.new(new_nodes["Group.006"].outputs[0], new_nodes["Group.003"].inputs[0])
    tree_links.new(new_nodes["Group.003"].outputs[0], new_nodes["Noise Texture.003"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Group.004"].inputs[0])
    tree_links.new(new_nodes["Group.004"].outputs[0], new_nodes["Noise Texture.004"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Group.005"].inputs[0])
    tree_links.new(new_nodes["Group.005"].outputs[0], new_nodes["Noise Texture.005"].inputs[0])
    tree_links.new(new_nodes["Noise Texture.001"].outputs[0], new_nodes["Noise Texture"].inputs[1])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Noise Texture.001"].inputs[1])
    tree_links.new(new_nodes["Noise Texture.002"].outputs[0], new_nodes["Math"].inputs[1])
    tree_links.new(new_nodes["Noise Texture.004"].outputs[0], new_nodes["Noise Texture.003"].inputs[1])
    tree_links.new(new_nodes["Noise Texture"].outputs[1], new_nodes["Group Output"].inputs[1])

    return new_node_group

def create_duo_node_noise_9e(context, override_create, node_tree_type):
    ensure_node_groups(override_create, [MOD_DUO_NG_NAME, PING_PONG_DUO_NG_NAME, NOISE_9E_DUO_NG_NAME],
        node_tree_type, create_prereq_duo_node_group)
    node = context.space_data.edit_tree.nodes.new(type=get_node_group_for_type(node_tree_type))
    node.node_tree = bpy.data.node_groups.get(node_group_name_for_name_and_type(NOISE_9E_DUO_NG_NAME, node_tree_type))
    node.inputs[3].default_value = 2
    node.inputs[4].default_value = 0.5

class BSR_Noise9eCreateDuoNode(bpy.types.Operator):
    bl_description = "Add a Giga Noise Texture node"
    bl_idname = "big_space_rig.noise_9e_create_duo_node"
    bl_label = "Noise 9e (Giga)"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        s = context.space_data
        if s.type == 'NODE_EDITOR' and s.node_tree != None and \
            s.tree_type in ('CompositorNodeTree', 'ShaderNodeTree', 'TextureNodeTree', 'GeometryNodeTree'):
            return True
        return False

    def execute(self, context):
        create_duo_node_noise_9e(context, False, context.space_data.edit_tree.bl_idname)
        return {'FINISHED'}

def create_duo_ng_noise_6e(node_tree_type):
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=node_group_name_for_name_and_type(NOISE_6E_DUO_NG_NAME,
                                                                                     node_tree_type),
                                              type=node_tree_type)
    new_node_group.inputs.new(type='NodeSocketVector', name="Loc 6e")
    new_node_group.inputs.new(type='NodeSocketVector', name="Loc 0e")
    new_node_group.inputs.new(type='NodeSocketFloat', name="W")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Detail")
    new_node_group.inputs.new(type='NodeSocketFloatFactor', name="Roughness")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Distortion")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Fac")
    new_node_group.outputs.new(type='NodeSocketColor', name="Color")
    tree_nodes = new_node_group.nodes
    # delete old nodes before adding nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeTexNoise")
    node.location = (40, 300)
    node.noise_dimensions = '4D'
    node.inputs[2].default_value = 1.0
    new_nodes["Noise Texture.001"] = node

    node = tree_nodes.new(type="ShaderNodeTexNoise")
    node.location = (220, 500)
    node.noise_dimensions = '4D'
    node.inputs[2].default_value = 1.0
    new_nodes["Noise Texture.002"] = node

    node = tree_nodes.new(type="ShaderNodeTexNoise")
    node.location = (580, 760)
    node.noise_dimensions = '4D'
    node.inputs[2].default_value = 1.0
    new_nodes["Noise Texture.004"] = node

    node = tree_nodes.new(type="ShaderNodeTexNoise")
    node.location = (760, 980)
    node.noise_dimensions = '4D'
    node.inputs[2].default_value = 1.0
    new_nodes["Noise Texture.005"] = node

    node = tree_nodes.new(type=get_node_group_for_type(node_tree_type))
    node.location = (40, 520)
    node.node_tree = bpy.data.node_groups.get(node_group_name_for_name_and_type(PING_PONG_DUO_NG_NAME, node_tree_type))
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    new_nodes["Group"] = node

    node = tree_nodes.new(type=get_node_group_for_type(node_tree_type))
    node.location = (-140, 300)
    node.node_tree = bpy.data.node_groups.get(node_group_name_for_name_and_type(PING_PONG_DUO_NG_NAME, node_tree_type))
    node.inputs[1].default_value = (0.5, 0.5, 0.5)
    new_nodes["Group.002"] = node

    node = tree_nodes.new(type=get_node_group_for_type(node_tree_type))
    node.location = (580, 980)
    node.node_tree = bpy.data.node_groups.get(node_group_name_for_name_and_type(PING_PONG_DUO_NG_NAME, node_tree_type))
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    new_nodes["Group.004"] = node

    node = tree_nodes.new(type=get_node_group_for_type(node_tree_type))
    node.location = (220, 760)
    node.node_tree = bpy.data.node_groups.get(node_group_name_for_name_and_type(PING_PONG_DUO_NG_NAME, node_tree_type))
    node.inputs[1].default_value = (0.5, 0.5, 0.5)
    new_nodes["Group.005"] = node

    node = tree_nodes.new(type=get_node_group_for_type(node_tree_type))
    node.location = (-400, 320)
    node.node_tree = bpy.data.node_groups.get(node_group_name_for_name_and_type(MOD_DUO_NG_NAME, node_tree_type))
    new_nodes["Group.006"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (400, 660)
    node.operation = "ADD"
    new_nodes["Math"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-740, 480)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (940, 980)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Noise Texture.005"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Group.006"].inputs[0])
    tree_links.new(new_nodes["Group.005"].outputs[0], new_nodes["Noise Texture.004"].inputs[0])
    tree_links.new(new_nodes["Noise Texture.001"].outputs[0], new_nodes["Noise Texture.002"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Group.006"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Noise Texture.001"].inputs[5])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Noise Texture.001"].inputs[4])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Noise Texture.001"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Noise Texture.002"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Noise Texture.002"].inputs[4])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Noise Texture.002"].inputs[5])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Noise Texture.004"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Noise Texture.004"].inputs[4])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Noise Texture.004"].inputs[5])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Noise Texture.005"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Noise Texture.005"].inputs[4])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Noise Texture.005"].inputs[5])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Group.005"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Group.004"].inputs[0])
    tree_links.new(new_nodes["Group.004"].outputs[0], new_nodes["Noise Texture.005"].inputs[0])
    tree_links.new(new_nodes["Group.006"].outputs[0], new_nodes["Group"].inputs[0])
    tree_links.new(new_nodes["Group"].outputs[0], new_nodes["Noise Texture.002"].inputs[0])
    tree_links.new(new_nodes["Group.006"].outputs[0], new_nodes["Group.002"].inputs[0])
    tree_links.new(new_nodes["Group.002"].outputs[0], new_nodes["Noise Texture.001"].inputs[0])
    tree_links.new(new_nodes["Noise Texture.004"].outputs[0], new_nodes["Noise Texture.005"].inputs[1])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Noise Texture.004"].inputs[1])
    tree_links.new(new_nodes["Noise Texture.002"].outputs[0], new_nodes["Math"].inputs[1])
    tree_links.new(new_nodes["Noise Texture.005"].outputs[1], new_nodes["Group Output"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Noise Texture.001"].inputs[1])

    return new_node_group

def create_duo_node_noise_6e(context, override_create, node_tree_type):
    ensure_node_groups(override_create, [MOD_DUO_NG_NAME, PING_PONG_DUO_NG_NAME, NOISE_6E_DUO_NG_NAME],
        node_tree_type, create_prereq_duo_node_group)
    node = context.space_data.edit_tree.nodes.new(type=get_node_group_for_type(node_tree_type))
    node.node_tree = bpy.data.node_groups.get(node_group_name_for_name_and_type(NOISE_6E_DUO_NG_NAME, node_tree_type))
    node.inputs[3].default_value = 2
    node.inputs[4].default_value = 0.5

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
