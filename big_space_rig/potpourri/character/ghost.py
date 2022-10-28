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

if bpy.app.version < (2,80,0):
    from ...imp_v27 import create_mesh_obj_from_pydata
else:
    from ...imp_v28 import create_mesh_obj_from_pydata

from ...node_other import (ensure_node_groups, ensure_materials)

GHOST_OBJNAME = "Ghost"
GHOST_GEO_NG_NAME = "Ghost.Potpourri.BSR.GeoNG"
GHOST_MAT_NAME = "GhostMat.Potpourri.BSR.Material"

def create_prereq_material(material_name, material):
    if material_name == GHOST_MAT_NAME:
        return create_mat_ghost(material)

    # error
    print("Unknown name passed to create_prereq_material: " + str(material_name))
    return None

def create_prereq_node_group(node_group_name, node_tree_type):
    if node_tree_type == 'GeometryNodeTree':
        if node_group_name == GHOST_GEO_NG_NAME:
            return create_geo_ng_ghost()

    # error
    print("Unknown name passed to create_prereq_node_group: " + str(node_group_name))
    return None

def create_mat_ghost(material):
    # initialize variables
    new_nodes = {}
    tree_nodes = material.node_tree.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-900, 1120)
    node.operation = "SUBTRACT"
    node.inputs[1].default_value = (0.12600000202655792, -0.23999999463558197, 0.39899998903274536)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-880, 580)
    node.operation = "SUBTRACT"
    node.inputs[1].default_value = (0.0, -0.30000001192092896, 0.23999999463558197)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-720, 1060)
    node.operation = "LENGTH"
    node.inputs[1].default_value = (0.0, 0.0, 1.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-540, 1060)
    node.operation = "LESS_THAN"
    node.use_clamp = False
    node.inputs[1].default_value = 0.075000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math"] = node

    node = tree_nodes.new(type="ShaderNodeAddShader")
    node.location = (-160, 380)
    new_nodes["Add Shader"] = node

    node = tree_nodes.new(type="ShaderNodeMixShader")
    node.location = (-340, 220)
    node.inputs[0].default_value = 0.600000
    new_nodes["Mix Shader"] = node

    node = tree_nodes.new(type="ShaderNodeTexCoord")
    node.location = (-1080, 1120)
    node.from_instancer = False
    new_nodes["Texture Coordinate"] = node

    node = tree_nodes.new(type="ShaderNodeMixShader")
    node.location = (-340, 380)
    node.inputs[0].default_value = 0.700000
    new_nodes["Mix Shader.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (20, 800)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeNewGeometry")
    node.location = (-160, 640)
    new_nodes["Geometry"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-160, 800)
    node.operation = "ADD"
    node.use_clamp = True
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-520, 580)
    node.operation = "LENGTH"
    node.inputs[1].default_value = (0.0, 0.0, 1.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeTexCoord")
    node.location = (-1060, 580)
    node.from_instancer = False
    new_nodes["Texture Coordinate.002"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-700, 580)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = (0.5, 1.0, 2.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.006"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-340, 580)
    node.operation = "LESS_THAN"
    node.use_clamp = False
    node.inputs[1].default_value = 0.075000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeBsdfTranslucent")
    node.location = (-700, 380)
    node.inputs[0].default_value = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
    new_nodes["Translucent BSDF"] = node

    node = tree_nodes.new(type="ShaderNodeBsdfPrincipled")
    node.location = (-800, 260)
    node.distribution = "GGX"
    node.subsurface_method = "RANDOM_WALK"
    node.inputs[0].default_value = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
    node.inputs[1].default_value = 0.100000
    node.inputs[2].default_value = (1.0, 0.20000000298023224, 0.10000000149011612)
    node.inputs[3].default_value = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
    node.inputs[4].default_value = 1.400000
    node.inputs[5].default_value = 0.000000
    node.inputs[6].default_value = 0.000000
    node.inputs[7].default_value = 0.001000
    node.inputs[8].default_value = 0.000000
    node.inputs[9].default_value = 0.800000
    node.inputs[10].default_value = 0.000000
    node.inputs[11].default_value = 0.000000
    node.inputs[12].default_value = 0.000000
    node.inputs[13].default_value = 0.500000
    node.inputs[14].default_value = 0.000000
    node.inputs[15].default_value = 0.030000
    node.inputs[16].default_value = 1.450000
    node.inputs[17].default_value = 0.000000
    node.inputs[18].default_value = 0.000000
    node.inputs[19].default_value = (0.0, 0.0, 0.0, 1.0)
    node.inputs[20].default_value = 1.000000
    node.inputs[21].default_value = 1.000000
    new_nodes["Principled BSDF"] = node

    node = tree_nodes.new(type="ShaderNodeBsdfTransparent")
    node.location = (-520, 220)
    node.inputs[0].default_value = (1.0, 1.0, 1.0, 1.0)
    new_nodes["Transparent BSDF"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-360, 860)
    node.operation = "ADD"
    node.use_clamp = True
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-540, 860)
    node.operation = "LESS_THAN"
    node.use_clamp = False
    node.inputs[1].default_value = 0.075000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-720, 860)
    node.operation = "LENGTH"
    node.inputs[1].default_value = (0.0, 0.0, 1.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-900, 860)
    node.operation = "SUBTRACT"
    node.inputs[1].default_value = (-0.12600000202655792, -0.23999999463558197, 0.39899998903274536)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeTexCoord")
    node.location = (-1080, 860)
    node.from_instancer = False
    new_nodes["Texture Coordinate.001"] = node

    node = tree_nodes.new(type="ShaderNodeMixShader")
    node.location = (200, 800)
    new_nodes["Mix Shader.002"] = node

    node = tree_nodes.new(type="ShaderNodeOutputMaterial")
    node.location = (380, 800)
    node.target = "ALL"
    new_nodes["Material Output"] = node

    # create links
    tree_links = material.node_tree.links
    tree_links.new(new_nodes["Translucent BSDF"].outputs[0], new_nodes["Mix Shader.001"].inputs[1])
    tree_links.new(new_nodes["Principled BSDF"].outputs[0], new_nodes["Mix Shader.001"].inputs[2])
    tree_links.new(new_nodes["Texture Coordinate"].outputs[3], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Vector Math"].outputs[0], new_nodes["Vector Math.003"].inputs[0])
    tree_links.new(new_nodes["Vector Math.003"].outputs[1], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Math.001"].inputs[0])
    tree_links.new(new_nodes["Texture Coordinate.001"].outputs[3], new_nodes["Vector Math.001"].inputs[0])
    tree_links.new(new_nodes["Vector Math.001"].outputs[0], new_nodes["Vector Math.004"].inputs[0])
    tree_links.new(new_nodes["Vector Math.004"].outputs[1], new_nodes["Math.002"].inputs[0])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Math.001"].inputs[1])
    tree_links.new(new_nodes["Mix Shader"].outputs[0], new_nodes["Add Shader"].inputs[1])
    tree_links.new(new_nodes["Transparent BSDF"].outputs[0], new_nodes["Mix Shader"].inputs[1])
    tree_links.new(new_nodes["Mix Shader.001"].outputs[0], new_nodes["Add Shader"].inputs[0])
    tree_links.new(new_nodes["Add Shader"].outputs[0], new_nodes["Mix Shader.002"].inputs[1])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Math.004"].inputs[0])
    tree_links.new(new_nodes["Texture Coordinate.002"].outputs[3], new_nodes["Vector Math.002"].inputs[0])
    tree_links.new(new_nodes["Vector Math.006"].outputs[0], new_nodes["Vector Math.005"].inputs[0])
    tree_links.new(new_nodes["Vector Math.005"].outputs[1], new_nodes["Math.005"].inputs[0])
    tree_links.new(new_nodes["Math.005"].outputs[0], new_nodes["Math.004"].inputs[1])
    tree_links.new(new_nodes["Vector Math.002"].outputs[0], new_nodes["Vector Math.006"].inputs[0])
    tree_links.new(new_nodes["Geometry"].outputs[6], new_nodes["Math.003"].inputs[1])
    tree_links.new(new_nodes["Math.003"].outputs[0], new_nodes["Mix Shader.002"].inputs[0])
    tree_links.new(new_nodes["Math.004"].outputs[0], new_nodes["Math.003"].inputs[0])
    tree_links.new(new_nodes["Mix Shader.002"].outputs[0], new_nodes["Material Output"].inputs[0])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_nodes

def create_geo_ng_ghost():
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=GHOST_GEO_NG_NAME, type='GeometryNodeTree')
    new_node_group.inputs.new(type='NodeSocketInt', name="Detail")
    new_node_group.inputs.new(type='NodeSocketMaterial', name="Material")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Time")
    new_node_group.outputs.new(type='NodeSocketGeometry', name="Geometry")
    tree_nodes = new_node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="GeometryNodeSetShadeSmooth")
    node.location = (1660, 300)
    node.inputs[2].default_value = True
    new_nodes["Set Shade Smooth"] = node

    node = tree_nodes.new(type="GeometryNodeSetMaterial")
    node.location = (1840, 300)
    new_nodes["Set Material"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (1120, 140)
    node.operation = "ADD"
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 0.500000
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (940, 140)
    node.operation = "SUBTRACT"
    node.inputs[1].default_value = (0.5, 0.5, 0.5)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 0.500000
    new_nodes["Vector Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeTexNoise")
    node.location = (760, 140)
    node.noise_dimensions = "4D"
    node.inputs[2].default_value = 1.000000
    node.inputs[3].default_value = 0.000000
    node.inputs[4].default_value = 0.400000
    node.inputs[5].default_value = 0.300000
    new_nodes["Noise Texture"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (760, -120)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = -1.000000
    node.inputs[2].default_value = 1.000000
    node.inputs[3].default_value = 0.900000
    node.inputs[4].default_value = 0.100000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (940, -120)
    node.inputs[0].default_value = 0.000000
    node.inputs[2].default_value = 0.000000
    new_nodes["Combine XYZ"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (580, -120)
    new_nodes["Separate XYZ"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (1300, 140)
    node.operation = "SCALE"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    new_nodes["Vector Math.002"] = node

    node = tree_nodes.new(type="GeometryNodeJoinGeometry")
    node.location = (1120, 420)
    new_nodes["Join Geometry"] = node

    node = tree_nodes.new(type="GeometryNodeMeshCylinder")
    node.location = (940, 420)
    node.fill_type = "NONE"
    node.inputs[2].default_value = 1
    node.inputs[3].default_value = 1.000000
    node.inputs[4].default_value = 2.000000
    new_nodes["Cylinder"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (220, 680)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = 0.500000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math"] = node

    node = tree_nodes.new(type="GeometryNodeMeshUVSphere")
    node.location = (400, 680)
    node.inputs[2].default_value = 1.000000
    new_nodes["UV Sphere"] = node

    node = tree_nodes.new(type="GeometryNodeDeleteGeometry")
    node.location = (580, 680)
    node.domain = "POINT"
    node.mode = "ALL"
    new_nodes["Delete Geometry"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (220, 500)
    new_nodes["Separate XYZ.001"] = node

    node = tree_nodes.new(type="FunctionNodeCompare")
    node.location = (400, 500)
    node.data_type = "FLOAT"
    node.mode = "ELEMENT"
    node.operation = "GREATER_THAN"
    node.inputs[1].default_value = 0.000100
    node.inputs[2].default_value = 0
    node.inputs[3].default_value = 0
    node.inputs[4].default_value = (0.0, 0.0, 0.0)
    node.inputs[5].default_value = (0.0, 0.0, 0.0)
    node.inputs[6].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[7].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[8].default_value = ""
    node.inputs[9].default_value = ""
    node.inputs[10].default_value = 0.900000
    node.inputs[11].default_value = 0.087266
    node.inputs[12].default_value = 0.001000
    new_nodes["Compare"] = node

    node = tree_nodes.new(type="ShaderNodeVectorRotate")
    node.location = (400, 340)
    node.invert = False
    node.rotation_type = "EULER_XYZ"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 1.0)
    node.inputs[3].default_value = 0.000000
    node.inputs[4].default_value = (3.1415927410125732, 0.0, 0.0)
    new_nodes["Vector Rotate"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (40, 500)
    new_nodes["Position"] = node

    node = tree_nodes.new(type="GeometryNodeSetPosition")
    node.location = (760, 680)
    node.inputs[3].default_value = (0.0, 0.0, 1.0)
    new_nodes["Set Position.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (760, 420)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = 0.250000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-220, 440)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = 4.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="GeometryNodeMergeByDistance")
    node.location = (1300, 420)
    node.inputs[2].default_value = 0.000100
    new_nodes["Merge by Distance"] = node

    node = tree_nodes.new(type="GeometryNodeSetPosition")
    node.location = (1480, 300)
    new_nodes["Set Position"] = node

    node = tree_nodes.new(type="GeometryNodeSetPosition")
    node.location = (2020, 300)
    node.inputs[3].default_value = (0.0, 0.0, 0.0)
    new_nodes["Set Position.002"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (400, -120)
    new_nodes["Position.001"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (1840, 160)
    node.operation = "SCALE"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 0.300000
    new_nodes["Vector Math.003"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (1660, 160)
    new_nodes["Position.002"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-400, 320)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (2200, 300)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Set Material"].inputs[2])
    tree_links.new(new_nodes["Cylinder"].outputs[0], new_nodes["Join Geometry"].inputs[0])
    tree_links.new(new_nodes["Set Position.001"].outputs[0], new_nodes["Join Geometry"].inputs[0])
    tree_links.new(new_nodes["Delete Geometry"].outputs[0], new_nodes["Set Position.001"].inputs[0])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["UV Sphere"].inputs[1])
    tree_links.new(new_nodes["UV Sphere"].outputs[0], new_nodes["Delete Geometry"].inputs[0])
    tree_links.new(new_nodes["Position"].outputs[0], new_nodes["Separate XYZ.001"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[2], new_nodes["Compare"].inputs[0])
    tree_links.new(new_nodes["Compare"].outputs[0], new_nodes["Delete Geometry"].inputs[1])
    tree_links.new(new_nodes["Position"].outputs[0], new_nodes["Vector Rotate"].inputs[0])
    tree_links.new(new_nodes["Vector Rotate"].outputs[0], new_nodes["Set Position.001"].inputs[2])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Cylinder"].inputs[1])
    tree_links.new(new_nodes["Join Geometry"].outputs[0], new_nodes["Merge by Distance"].inputs[0])
    tree_links.new(new_nodes["Set Position"].outputs[0], new_nodes["Set Shade Smooth"].inputs[0])
    tree_links.new(new_nodes["Set Shade Smooth"].outputs[0], new_nodes["Set Material"].inputs[0])
    tree_links.new(new_nodes["Merge by Distance"].outputs[0], new_nodes["Set Position"].inputs[0])
    tree_links.new(new_nodes["Position.001"].outputs[0], new_nodes["Noise Texture"].inputs[0])
    tree_links.new(new_nodes["Vector Math.002"].outputs[0], new_nodes["Set Position"].inputs[3])
    tree_links.new(new_nodes["Vector Math"].outputs[0], new_nodes["Vector Math.002"].inputs[0])
    tree_links.new(new_nodes["Position.001"].outputs[0], new_nodes["Separate XYZ"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ"].outputs[2], new_nodes["Map Range"].inputs[0])
    tree_links.new(new_nodes["Map Range"].outputs[0], new_nodes["Vector Math.002"].inputs[3])
    tree_links.new(new_nodes["Noise Texture"].outputs[1], new_nodes["Vector Math.001"].inputs[0])
    tree_links.new(new_nodes["Vector Math.001"].outputs[0], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Combine XYZ"].outputs[0], new_nodes["Vector Math"].inputs[1])
    tree_links.new(new_nodes["Map Range"].outputs[0], new_nodes["Combine XYZ"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Noise Texture"].inputs[1])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["UV Sphere"].inputs[0])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Math.001"].inputs[0])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Cylinder"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Math.002"].inputs[0])
    tree_links.new(new_nodes["Set Position.002"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Set Material"].outputs[0], new_nodes["Set Position.002"].inputs[0])
    tree_links.new(new_nodes["Position.002"].outputs[0], new_nodes["Vector Math.003"].inputs[0])
    tree_links.new(new_nodes["Vector Math.003"].outputs[0], new_nodes["Set Position.002"].inputs[2])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group

def create_apply_ghost_geo_nodes(tree_nodes, tree_links):
    new_nodes = {}

    # delete old nodes before adding new nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="GeometryNodeGroup")
    node.label = "Ghost"
    node.location = (0, 0)
    node.node_tree = bpy.data.node_groups.get(GHOST_GEO_NG_NAME)
    node.inputs[0].default_value = 8
    node.inputs[1].default_value = bpy.data.materials.get(GHOST_MAT_NAME)
    node.inputs[2].default_value = 0.0
    new_nodes["Ghost.Group"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-200, 0)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (220, 0)
    new_nodes["Group Output"] = node

    # create links
    tree_links.new(new_nodes["Ghost.Group"].outputs[0], new_nodes["Group Output"].inputs[0])

    return new_nodes["Ghost.Group"]

def create_ghost_materials(override_create, ghost_obj):
    ensure_materials(override_create, [GHOST_MAT_NAME], create_prereq_material)
    ghost_mat = bpy.data.materials.get(GHOST_MAT_NAME)
    ghost_obj.data.materials.append(ghost_mat)

def create_ghost_individual_geo_ng(new_node_group, override_create, ghost_obj):
    # initialize variables
    tree_nodes = new_node_group.nodes
    tree_links = new_node_group.links

    create_ghost_materials(override_create, ghost_obj)
    ensure_node_groups(override_create, [GHOST_GEO_NG_NAME], 'GeometryNodeTree', create_prereq_node_group)
    create_apply_ghost_geo_nodes(tree_nodes, tree_links)

    return new_node_group

def add_ghost_geo_nodes_to_object(ghost_obj, override_create):
    geo_nodes_mod = ghost_obj.modifiers.new(name="Ghost.GeometryNodes", type='NODES')
    create_ghost_individual_geo_ng(geo_nodes_mod.node_group, override_create, ghost_obj)

def pot_create_ghost(override_create):
    ghost_ob = create_mesh_obj_from_pydata(obj_name=GHOST_OBJNAME)
    add_ghost_geo_nodes_to_object(ghost_ob, override_create)

class BSR_PotCreateGhost(bpy.types.Operator):
    bl_description = "Create a Ghost character with Geometry Nodes mesh and Shader Nodes material"
    bl_idname = "big_space_rig.pot_create_character_ghost"
    bl_label = "Ghost"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scn = context.scene
        pot_create_ghost(scn.BSR_NodesOverrideCreate)
        return {'FINISHED'}
