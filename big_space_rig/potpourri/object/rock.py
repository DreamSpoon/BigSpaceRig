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

ROCK_OBJNAME = "Rock"
ROCK_MAT_NAME = "Rock.Potpourri.BSR.Material"
ROCK_GEO_NG_NAME = "Rock.Potpourri.BSR.GeoNG"

def create_prereq_material(material_name, material):
    if material_name == ROCK_MAT_NAME:
        return create_mat_rock(material)

    # error
    print("Unknown name passed to create_prereq_material: " + str(material_name))
    return None

def create_prereq_node_group(node_group_name, node_tree_type):
    if node_tree_type == 'GeometryNodeTree':
        if node_group_name == ROCK_GEO_NG_NAME:
            return create_geo_ng_rock()

    # error
    print("Unknown name passed to create_prereq_node_group: " + str(node_group_name))
    return None

def create_mat_rock(material):
    # initialize variables
    new_nodes = {}
    tree_nodes = material.node_tree.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeTexCoord")
    node.location = (1120, -860)
    node.from_instancer = False
    new_nodes["Texture Coordinate"] = node

    node = tree_nodes.new(type="ShaderNodeTexNoise")
    node.location = (1120, -620)
    node.noise_dimensions = "3D"
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 40.000000
    node.inputs[3].default_value = 5.000000
    node.inputs[4].default_value = 0.400000
    node.inputs[5].default_value = 0.300000
    new_nodes["Noise Texture"] = node

    node = tree_nodes.new(type="ShaderNodeBump")
    node.location = (1120, -440)
    node.invert = False
    node.inputs[0].default_value = 0.250000
    node.inputs[1].default_value = 1.000000
    node.inputs[3].default_value = 1.000000
    node.inputs[4].default_value = 1.000000
    new_nodes["Bump.002"] = node

    node = tree_nodes.new(type="ShaderNodeBsdfPrincipled")
    node.location = (1320, 60)
    node.distribution = "GGX"
    node.subsurface_method = "RANDOM_WALK"
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = (1.0, 0.20000000298023224, 0.10000000149011612)
    node.inputs[3].default_value = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
    node.inputs[4].default_value = 1.400000
    node.inputs[5].default_value = 0.000000
    node.inputs[6].default_value = 0.000000
    node.inputs[7].default_value = 0.010000
    node.inputs[8].default_value = 0.000000
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
    new_nodes["Principled BSDF.002"] = node

    node = tree_nodes.new(type="ShaderNodeMixShader")
    node.location = (1680, 200)
    new_nodes["Mix Shader.001"] = node

    node = tree_nodes.new(type="ShaderNodeTexVoronoi")
    node.location = (1240, 340)
    node.distance = "EUCLIDEAN"
    node.feature = "F1"
    node.voronoi_dimensions = "3D"
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 5.000000
    node.inputs[3].default_value = 1.000000
    node.inputs[4].default_value = 0.500000
    node.inputs[5].default_value = 1.000000
    new_nodes["Voronoi Texture.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1420, 340)
    node.operation = "GREATER_THAN"
    node.use_clamp = False
    node.inputs[1].default_value = 0.600000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1420, 520)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeTexVoronoi")
    node.location = (1240, 520)
    node.distance = "EUCLIDEAN"
    node.feature = "DISTANCE_TO_EDGE"
    node.voronoi_dimensions = "3D"
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 5.000000
    node.inputs[3].default_value = 1.000000
    node.inputs[4].default_value = 0.500000
    node.inputs[5].default_value = 1.000000
    new_nodes["Voronoi Texture"] = node

    node = tree_nodes.new(type="ShaderNodeMixRGB")
    node.location = (1040, 520)
    node.blend_type = "MIX"
    node.use_alpha = False
    node.use_clamp = False
    node.inputs[0].default_value = 0.230000
    new_nodes["Mix"] = node

    node = tree_nodes.new(type="ShaderNodeTexNoise")
    node.location = (1040, 340)
    node.noise_dimensions = "3D"
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 5.000000
    node.inputs[3].default_value = 5.000000
    node.inputs[4].default_value = 0.600000
    node.inputs[5].default_value = 0.100000
    new_nodes["Noise Texture.001"] = node

    node = tree_nodes.new(type="ShaderNodeTexCoord")
    node.location = (860, 520)
    node.from_instancer = False
    new_nodes["Texture Coordinate.001"] = node

    node = tree_nodes.new(type="ShaderNodeValToRGB")
    node.location = (1320, 740)
    node.color_ramp.color_mode = "RGB"
    node.color_ramp.interpolation = "EASE"
    node.color_ramp.elements.remove(node.color_ramp.elements[0])
    elem = node.color_ramp.elements[0]
    elem.position = 0.000000
    elem.color = (0.000000, 0.000000, 0.000000, 1.000000)
    elem = node.color_ramp.elements.new(0.022727)
    elem.color = (1.000000, 1.000000, 1.000000, 1.000000)
    elem = node.color_ramp.elements.new(0.080000)
    elem.color = (1.000000, 1.000000, 1.000000, 1.000000)
    elem = node.color_ramp.elements.new(0.095455)
    elem.color = (0.000000, 0.000000, 0.000000, 1.000000)
    new_nodes["ColorRamp"] = node

    node = tree_nodes.new(type="ShaderNodeBsdfPrincipled")
    node.location = (400, 60)
    node.distribution = "GGX"
    node.subsurface_method = "RANDOM_WALK"
    node.inputs[0].default_value = (0.02397070825099945, 0.019894273951649666, 0.021996021270751953, 1.0)
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = (1.0, 0.20000000298023224, 0.10000000149011612)
    node.inputs[3].default_value = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
    node.inputs[4].default_value = 1.400000
    node.inputs[5].default_value = 0.000000
    node.inputs[6].default_value = 0.000000
    node.inputs[7].default_value = 0.005000
    node.inputs[8].default_value = 0.000000
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

    node = tree_nodes.new(type="ShaderNodeMixShader")
    node.location = (680, 200)
    new_nodes["Mix Shader"] = node

    node = tree_nodes.new(type="ShaderNodeBsdfPrincipled")
    node.location = (400, 740)
    node.distribution = "GGX"
    node.subsurface_method = "RANDOM_WALK"
    node.inputs[0].default_value = (0.06584875285625458, 0.06793149560689926, 0.08381790667772293, 1.0)
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = (1.0, 0.20000000298023224, 0.10000000149011612)
    node.inputs[3].default_value = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
    node.inputs[4].default_value = 1.400000
    node.inputs[5].default_value = 0.000000
    node.inputs[6].default_value = 0.000000
    node.inputs[7].default_value = 0.005000
    node.inputs[8].default_value = 0.000000
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
    new_nodes["Principled BSDF.001"] = node

    node = tree_nodes.new(type="ShaderNodeNewGeometry")
    node.location = (20, -260)
    new_nodes["Geometry"] = node

    node = tree_nodes.new(type="ShaderNodeValToRGB")
    node.location = (-80, -40)
    node.color_ramp.color_mode = "RGB"
    node.color_ramp.interpolation = "EASE"
    node.color_ramp.elements.remove(node.color_ramp.elements[0])
    elem = node.color_ramp.elements[0]
    elem.position = 0.295000
    elem.color = (0.408455, 0.408455, 0.408455, 1.000000)
    elem = node.color_ramp.elements.new(0.700000)
    elem.color = (1.000000, 1.000000, 1.000000, 1.000000)
    new_nodes["ColorRamp.002"] = node

    node = tree_nodes.new(type="ShaderNodeBump")
    node.location = (220, -440)
    node.invert = False
    node.inputs[0].default_value = 0.100000
    node.inputs[1].default_value = 1.000000
    node.inputs[3].default_value = 1.000000
    node.inputs[4].default_value = 1.000000
    new_nodes["Bump"] = node

    node = tree_nodes.new(type="ShaderNodeTexNoise")
    node.location = (220, -620)
    node.noise_dimensions = "3D"
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 15.000000
    node.inputs[3].default_value = 5.000000
    node.inputs[4].default_value = 0.800000
    node.inputs[5].default_value = 0.300000
    new_nodes["Noise Texture.002"] = node

    node = tree_nodes.new(type="ShaderNodeTexCoord")
    node.location = (220, -860)
    node.from_instancer = False
    new_nodes["Texture Coordinate.003"] = node

    node = tree_nodes.new(type="ShaderNodeBump")
    node.location = (220, 240)
    node.invert = False
    node.inputs[0].default_value = 0.200000
    node.inputs[1].default_value = 1.000000
    node.inputs[3].default_value = 1.000000
    node.inputs[4].default_value = 1.000000
    new_nodes["Bump.001"] = node

    node = tree_nodes.new(type="ShaderNodeTexCoord")
    node.location = (-660, 320)
    node.from_instancer = False
    new_nodes["Texture Coordinate.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-300, 320)
    node.operation = "MULTIPLY_ADD"
    node.use_clamp = False
    node.inputs[1].default_value = 0.250000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeValToRGB")
    node.location = (-120, 320)
    node.color_ramp.color_mode = "RGB"
    node.color_ramp.interpolation = "EASE"
    node.color_ramp.elements.remove(node.color_ramp.elements[0])
    elem = node.color_ramp.elements[0]
    elem.position = 0.312727
    elem.color = (0.000000, 0.000000, 0.000000, 1.000000)
    elem = node.color_ramp.elements.new(0.890909)
    elem.color = (1.000000, 1.000000, 1.000000, 1.000000)
    new_nodes["ColorRamp.003"] = node

    node = tree_nodes.new(type="ShaderNodeTexMusgrave")
    node.location = (-480, 320)
    node.musgrave_dimensions = "3D"
    node.musgrave_type = "HETERO_TERRAIN"
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 30.000000
    node.inputs[3].default_value = 6.000000
    node.inputs[4].default_value = 0.200000
    node.inputs[5].default_value = 2.000000
    node.inputs[6].default_value = 0.000000
    node.inputs[7].default_value = 1.000000
    new_nodes["Musgrave Texture"] = node

    node = tree_nodes.new(type="ShaderNodeOutputMaterial")
    node.location = (1860, 200)
    node.target = "ALL"
    new_nodes["Material Output"] = node

    node = tree_nodes.new(type="ShaderNodeValToRGB")
    node.location = (1020, -40)
    node.color_ramp.color_mode = "RGB"
    node.color_ramp.interpolation = "EASE"
    node.color_ramp.elements.remove(node.color_ramp.elements[0])
    elem = node.color_ramp.elements[0]
    elem.position = 0.209091
    elem.color = (0.050623, 0.049308, 0.069333, 1.000000)
    elem = node.color_ramp.elements.new(0.796364)
    elem.color = (0.056807, 0.049266, 0.045800, 1.000000)
    new_nodes["ColorRamp.001"] = node

    # create links
    tree_links = material.node_tree.links
    tree_links.new(new_nodes["Geometry"].outputs[7], new_nodes["ColorRamp.002"].inputs[0])
    tree_links.new(new_nodes["ColorRamp.002"].outputs[0], new_nodes["Principled BSDF"].inputs[9])
    tree_links.new(new_nodes["Principled BSDF"].outputs[0], new_nodes["Mix Shader"].inputs[2])
    tree_links.new(new_nodes["Principled BSDF.001"].outputs[0], new_nodes["Mix Shader"].inputs[1])
    tree_links.new(new_nodes["Mix Shader"].outputs[0], new_nodes["Mix Shader.001"].inputs[1])
    tree_links.new(new_nodes["Voronoi Texture.001"].outputs[1], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Mix"].outputs[0], new_nodes["Voronoi Texture.001"].inputs[0])
    tree_links.new(new_nodes["Voronoi Texture"].outputs[0], new_nodes["Math.001"].inputs[0])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Math.001"].inputs[1])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["ColorRamp"].inputs[0])
    tree_links.new(new_nodes["ColorRamp"].outputs[0], new_nodes["Mix Shader.001"].inputs[0])
    tree_links.new(new_nodes["Principled BSDF.002"].outputs[0], new_nodes["Mix Shader.001"].inputs[2])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["ColorRamp.003"].inputs[0])
    tree_links.new(new_nodes["Musgrave Texture"].outputs[0], new_nodes["Math.002"].inputs[0])
    tree_links.new(new_nodes["Texture Coordinate.002"].outputs[3], new_nodes["Musgrave Texture"].inputs[0])
    tree_links.new(new_nodes["ColorRamp.003"].outputs[0], new_nodes["Mix Shader"].inputs[0])
    tree_links.new(new_nodes["Noise Texture"].outputs[0], new_nodes["ColorRamp.001"].inputs[0])
    tree_links.new(new_nodes["ColorRamp.001"].outputs[0], new_nodes["Principled BSDF.002"].inputs[0])
    tree_links.new(new_nodes["Texture Coordinate"].outputs[3], new_nodes["Noise Texture"].inputs[0])
    tree_links.new(new_nodes["Texture Coordinate.001"].outputs[3], new_nodes["Mix"].inputs[1])
    tree_links.new(new_nodes["Mix"].outputs[0], new_nodes["Voronoi Texture"].inputs[0])
    tree_links.new(new_nodes["Noise Texture.001"].outputs[0], new_nodes["Mix"].inputs[2])
    tree_links.new(new_nodes["Texture Coordinate.001"].outputs[3], new_nodes["Noise Texture.001"].inputs[0])
    tree_links.new(new_nodes["ColorRamp.002"].outputs[0], new_nodes["Principled BSDF.002"].inputs[9])
    tree_links.new(new_nodes["ColorRamp.002"].outputs[0], new_nodes["Principled BSDF.001"].inputs[9])
    tree_links.new(new_nodes["Texture Coordinate.003"].outputs[3], new_nodes["Noise Texture.002"].inputs[0])
    tree_links.new(new_nodes["Noise Texture.002"].outputs[0], new_nodes["Bump"].inputs[2])
    tree_links.new(new_nodes["Bump"].outputs[0], new_nodes["Principled BSDF"].inputs[22])
    tree_links.new(new_nodes["Musgrave Texture"].outputs[0], new_nodes["Bump.001"].inputs[2])
    tree_links.new(new_nodes["Bump.001"].outputs[0], new_nodes["Principled BSDF.001"].inputs[22])
    tree_links.new(new_nodes["Bump.002"].outputs[0], new_nodes["Principled BSDF.002"].inputs[22])
    tree_links.new(new_nodes["Noise Texture"].outputs[0], new_nodes["Bump.002"].inputs[2])
    tree_links.new(new_nodes["Mix Shader.001"].outputs[0], new_nodes["Material Output"].inputs[0])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_nodes

def create_geo_ng_rock():
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=ROCK_GEO_NG_NAME, type='GeometryNodeTree')
    new_node_group.inputs.new(type='NodeSocketInt', name="Detail")
    new_node_group.inputs.new(type='NodeSocketGeometry', name="Base Geometry")
    new_node_group.inputs.new(type='NodeSocketMaterial', name="Material")
    new_node_group.inputs.new(type='NodeSocketMaterial', name="Point Material")
    new_node_group.inputs.new(type='NodeSocketVector', name="Scale")
    new_node_group.inputs.new(type='NodeSocketInt', name="Seed")
    new_node_group.outputs.new(type='NodeSocketGeometry', name="Geometry")
    tree_nodes = new_node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (-90, 140)
    new_nodes["Position.001"] = node

    node = tree_nodes.new(type="GeometryNodeSetPosition")
    node.location = (-90, 800)
    new_nodes["Set Position.001"] = node

    node = tree_nodes.new(type="ShaderNodeTexNoise")
    node.location = (-90, 360)
    node.noise_dimensions = "3D"
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 2.000000
    node.inputs[3].default_value = 2.000000
    node.inputs[4].default_value = 0.500000
    node.inputs[5].default_value = 0.200000
    new_nodes["Noise Texture.001"] = node

    node = tree_nodes.new(type="GeometryNodeExtrudeMesh")
    node.location = (-430, 220)
    node.mode = "FACES"
    node.inputs[4].default_value = False
    new_nodes["Extrude Mesh"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-90, 640)
    node.operation = "MULTIPLY_ADD"
    node.inputs[1].default_value = (0.25, 0.25, 0.25)
    node.inputs[2].default_value = (-0.125, -0.125, -0.125)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.002"] = node

    node = tree_nodes.new(type="FunctionNodeRandomValue")
    node.location = (-430, -40)
    node.data_type = "FLOAT"
    node.inputs[0].default_value = (0.0, 0.0, 0.0)
    node.inputs[1].default_value = (0.0, 0.0, 1.0)
    node.inputs[2].default_value = 0.500000
    node.inputs[3].default_value = 1.000000
    node.inputs[4].default_value = 0
    node.inputs[5].default_value = 100
    node.inputs[6].default_value = 0.500000
    new_nodes["Random Value.001"] = node

    node = tree_nodes.new(type="FunctionNodeBooleanMath")
    node.location = (-190, 40)
    node.operation = "AND"
    new_nodes["Boolean Math.001"] = node

    node = tree_nodes.new(type="FunctionNodeRandomValue")
    node.location = (-10, -100)
    node.data_type = "BOOLEAN"
    node.inputs[0].default_value = (0.0, 0.0, 0.0)
    node.inputs[1].default_value = (0.0, 0.0, 1.0)
    node.inputs[2].default_value = 0.500000
    node.inputs[3].default_value = 1.000000
    node.inputs[4].default_value = 0
    node.inputs[5].default_value = 100
    node.inputs[6].default_value = 0.500000
    new_nodes["Random Value.003"] = node

    node = tree_nodes.new(type="FunctionNodeBooleanMath")
    node.location = (-10, 40)
    node.operation = "AND"
    new_nodes["Boolean Math.002"] = node

    node = tree_nodes.new(type="FunctionNodeRandomValue")
    node.location = (-190, -240)
    node.data_type = "BOOLEAN"
    node.inputs[0].default_value = (0.0, 0.0, 0.0)
    node.inputs[1].default_value = (1.0, 1.0, 1.0)
    node.inputs[2].default_value = 0.000000
    node.inputs[3].default_value = 1.000000
    node.inputs[4].default_value = 0
    node.inputs[5].default_value = 100
    node.inputs[6].default_value = 0.500000
    new_nodes["Random Value.004"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-10, -260)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[1].default_value = -42.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="FunctionNodeRandomValue")
    node.location = (190, -40)
    node.data_type = "FLOAT"
    node.inputs[0].default_value = (0.0, 0.0, 0.0)
    node.inputs[1].default_value = (0.0, 0.0, 1.0)
    node.inputs[2].default_value = 0.500000
    node.inputs[3].default_value = 1.000000
    node.inputs[4].default_value = 0
    node.inputs[5].default_value = 100
    node.inputs[6].default_value = 0.500000
    new_nodes["Random Value.002"] = node

    node = tree_nodes.new(type="GeometryNodeExtrudeMesh")
    node.location = (190, 220)
    node.mode = "FACES"
    node.inputs[4].default_value = False
    new_nodes["Extrude Mesh.001"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-190, -580)
    node.operation = "DOT_PRODUCT"
    node.inputs[1].default_value = (0.0, 0.0, 1.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.004"] = node

    node = tree_nodes.new(type="GeometryNodeInputNormal")
    node.location = (-190, -780)
    new_nodes["Normal.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-190, -400)
    node.operation = "GREATER_THAN"
    node.use_clamp = False
    node.inputs[1].default_value = -0.500000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.003"] = node

    node = tree_nodes.new(type="FunctionNodeBooleanMath")
    node.location = (-190, -100)
    node.operation = "AND"
    new_nodes["Boolean Math.003"] = node

    node = tree_nodes.new(type="FunctionNodeBooleanMath")
    node.location = (610, 20)
    node.operation = "AND"
    new_nodes["Boolean Math.004"] = node

    node = tree_nodes.new(type="FunctionNodeRandomValue")
    node.location = (790, -120)
    node.data_type = "BOOLEAN"
    node.inputs[0].default_value = (0.0, 0.0, 0.0)
    node.inputs[1].default_value = (0.0, 0.0, 1.0)
    node.inputs[2].default_value = 0.500000
    node.inputs[3].default_value = 1.000000
    node.inputs[4].default_value = 0
    node.inputs[5].default_value = 100
    node.inputs[6].default_value = 0.250000
    new_nodes["Random Value.005"] = node

    node = tree_nodes.new(type="FunctionNodeBooleanMath")
    node.location = (790, 20)
    node.operation = "AND"
    new_nodes["Boolean Math.005"] = node

    node = tree_nodes.new(type="FunctionNodeRandomValue")
    node.location = (610, -260)
    node.data_type = "BOOLEAN"
    node.inputs[0].default_value = (0.0, 0.0, 0.0)
    node.inputs[1].default_value = (1.0, 1.0, 1.0)
    node.inputs[2].default_value = 0.000000
    node.inputs[3].default_value = 1.000000
    node.inputs[4].default_value = 0
    node.inputs[5].default_value = 100
    node.inputs[6].default_value = 0.500000
    new_nodes["Random Value.006"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (610, -600)
    node.operation = "DOT_PRODUCT"
    node.inputs[1].default_value = (0.0, 0.0, 1.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.005"] = node

    node = tree_nodes.new(type="GeometryNodeInputNormal")
    node.location = (610, -800)
    new_nodes["Normal.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (610, -420)
    node.operation = "GREATER_THAN"
    node.use_clamp = False
    node.inputs[1].default_value = -0.500000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.007"] = node

    node = tree_nodes.new(type="FunctionNodeBooleanMath")
    node.location = (610, -120)
    node.operation = "AND"
    new_nodes["Boolean Math.006"] = node

    node = tree_nodes.new(type="GeometryNodeSetPosition")
    node.location = (450, 800)
    new_nodes["Set Position.002"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (450, 640)
    node.operation = "MULTIPLY_ADD"
    node.inputs[1].default_value = (0.25, 0.25, 0.25)
    node.inputs[2].default_value = (-0.125, -0.125, -0.125)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.003"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (450, 140)
    new_nodes["Position.002"] = node

    node = tree_nodes.new(type="ShaderNodeTexNoise")
    node.location = (450, 360)
    node.noise_dimensions = "3D"
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 2.000000
    node.inputs[3].default_value = 2.000000
    node.inputs[4].default_value = 0.500000
    node.inputs[5].default_value = 0.200000
    new_nodes["Noise Texture.002"] = node

    node = tree_nodes.new(type="GeometryNodeInputNormal")
    node.location = (-820, -560)
    new_nodes["Normal"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-820, -360)
    node.operation = "DOT_PRODUCT"
    node.inputs[1].default_value = (0.0, 0.0, 1.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (-620, 140)
    new_nodes["Position"] = node

    node = tree_nodes.new(type="GeometryNodeSetPosition")
    node.location = (-620, 800)
    new_nodes["Set Position"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-620, 640)
    node.operation = "MULTIPLY_ADD"
    node.inputs[1].default_value = (0.25, 0.25, 0.25)
    node.inputs[2].default_value = (-0.125, -0.125, -0.125)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-820, -200)
    node.operation = "GREATER_THAN"
    node.use_clamp = False
    node.inputs[1].default_value = -0.500000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math"] = node

    node = tree_nodes.new(type="FunctionNodeRandomValue")
    node.location = (-820, -40)
    node.data_type = "BOOLEAN"
    node.inputs[0].default_value = (0.0, 0.0, 0.0)
    node.inputs[1].default_value = (1.0, 1.0, 1.0)
    node.inputs[2].default_value = 0.000000
    node.inputs[3].default_value = 1.000000
    node.inputs[4].default_value = 0
    node.inputs[5].default_value = 100
    node.inputs[6].default_value = 0.500000
    new_nodes["Random Value"] = node

    node = tree_nodes.new(type="FunctionNodeBooleanMath")
    node.location = (-820, 100)
    node.operation = "AND"
    new_nodes["Boolean Math"] = node

    node = tree_nodes.new(type="ShaderNodeTexNoise")
    node.location = (-620, 360)
    node.noise_dimensions = "3D"
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 1.600000
    node.inputs[3].default_value = 2.000000
    node.inputs[4].default_value = 0.500000
    node.inputs[5].default_value = 0.200000
    new_nodes["Noise Texture"] = node

    node = tree_nodes.new(type="GeometryNodeExtrudeMesh")
    node.location = (980, 160)
    node.mode = "FACES"
    node.inputs[4].default_value = False
    new_nodes["Extrude Mesh.002"] = node

    node = tree_nodes.new(type="FunctionNodeRandomValue")
    node.location = (980, -100)
    node.data_type = "FLOAT"
    node.inputs[0].default_value = (0.0, 0.0, 0.0)
    node.inputs[1].default_value = (0.0, 0.0, 1.0)
    node.inputs[2].default_value = 0.500000
    node.inputs[3].default_value = 1.000000
    node.inputs[4].default_value = 0
    node.inputs[5].default_value = 100
    node.inputs[6].default_value = 0.500000
    new_nodes["Random Value.007"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (980, -280)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[1].default_value = 23.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.006"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (1380, -460)
    new_nodes["Position.003"] = node

    node = tree_nodes.new(type="ShaderNodeValToRGB")
    node.location = (1280, -20)
    node.color_ramp.color_mode = "RGB"
    node.color_ramp.interpolation = "EASE"
    node.color_ramp.elements.remove(node.color_ramp.elements[0])
    elem = node.color_ramp.elements[0]
    elem.position = 0.201818
    elem.color = (0.000000, 0.000000, 0.000000, 1.000000)
    elem = node.color_ramp.elements.new(0.967273)
    elem.color = (1.000000, 1.000000, 1.000000, 1.000000)
    new_nodes["ColorRamp"] = node

    node = tree_nodes.new(type="GeometryNodeSubdivisionSurface")
    node.location = (1380, 160)
    node.boundary_smooth = "ALL"
    node.uv_smooth = "PRESERVE_BOUNDARIES"
    new_nodes["Subdivision Surface"] = node

    node = tree_nodes.new(type="ShaderNodeTexNoise")
    node.location = (1380, -240)
    node.noise_dimensions = "3D"
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 1.000000
    node.inputs[3].default_value = 3.000000
    node.inputs[4].default_value = 0.500000
    node.inputs[5].default_value = 0.100000
    new_nodes["Noise Texture.004"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (1200, 160)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = 1.000000
    node.inputs[2].default_value = 3.000000
    node.inputs[3].default_value = 0.000000
    node.inputs[4].default_value = 2.000000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (2000, -780)
    new_nodes["Position.006"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (1760, -460)
    new_nodes["Position.004"] = node

    node = tree_nodes.new(type="ShaderNodeTexNoise")
    node.location = (1760, -240)
    node.noise_dimensions = "3D"
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 1.000000
    node.inputs[3].default_value = 3.000000
    node.inputs[4].default_value = 0.500000
    node.inputs[5].default_value = 0.100000
    new_nodes["Noise Texture.005"] = node

    node = tree_nodes.new(type="ShaderNodeValToRGB")
    node.location = (1660, -20)
    node.color_ramp.color_mode = "RGB"
    node.color_ramp.interpolation = "EASE"
    node.color_ramp.elements.remove(node.color_ramp.elements[0])
    elem = node.color_ramp.elements[0]
    elem.position = 0.323636
    elem.color = (0.000000, 0.000000, 0.000000, 1.000000)
    elem = node.color_ramp.elements.new(0.909091)
    elem.color = (1.000000, 1.000000, 1.000000, 1.000000)
    new_nodes["ColorRamp.001"] = node

    node = tree_nodes.new(type="GeometryNodeSetPosition")
    node.location = (2180, 160)
    new_nodes["Set Position.003"] = node

    node = tree_nodes.new(type="ShaderNodeMixRGB")
    node.location = (2180, -500)
    node.blend_type = "MIX"
    node.use_alpha = False
    node.use_clamp = False
    node.inputs[0].default_value = 0.750000
    new_nodes["Mix"] = node

    node = tree_nodes.new(type="ShaderNodeTexVoronoi")
    node.location = (2000, -500)
    node.distance = "EUCLIDEAN"
    node.feature = "SMOOTH_F1"
    node.voronoi_dimensions = "3D"
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 2.000000
    node.inputs[3].default_value = 0.500000
    node.inputs[4].default_value = 0.500000
    node.inputs[5].default_value = 1.000000
    new_nodes["Voronoi Texture"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (2180, 0)
    node.operation = "MULTIPLY_ADD"
    node.inputs[1].default_value = (0.25, 0.25, 0.25)
    node.inputs[2].default_value = (-0.125, -0.125, -0.125)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.006"] = node

    node = tree_nodes.new(type="ShaderNodeTexNoise")
    node.location = (2180, -280)
    node.noise_dimensions = "3D"
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 1.000000
    node.inputs[3].default_value = 3.000000
    node.inputs[4].default_value = 0.500000
    node.inputs[5].default_value = 0.300000
    new_nodes["Noise Texture.006"] = node

    node = tree_nodes.new(type="GeometryNodeSetShadeSmooth")
    node.location = (2360, 200)
    node.inputs[2].default_value = True
    new_nodes["Set Shade Smooth"] = node

    node = tree_nodes.new(type="GeometryNodeSetMaterial")
    node.location = (2540, 320)
    new_nodes["Set Material"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (2720, -20)
    new_nodes["Position.005"] = node

    node = tree_nodes.new(type="GeometryNodeSetPosition")
    node.location = (2720, 320)
    node.inputs[3].default_value = (0.0, 0.0, 0.0)
    new_nodes["Set Position.004"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (2720, 120)
    node.operation = "MULTIPLY"
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.007"] = node

    node = tree_nodes.new(type="GeometryNodeSubdivisionSurface")
    node.location = (1760, 160)
    node.boundary_smooth = "ALL"
    node.uv_smooth = "PRESERVE_BOUNDARIES"
    new_nodes["Subdivision Surface.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1600, 160)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[1].default_value = 3.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.008"] = node

    node = tree_nodes.new(type="GeometryNodeSwitch")
    node.location = (2960, 320)
    node.input_type = "GEOMETRY"
    node.inputs[0].default_value = False
    node.inputs[2].default_value = 0.000000
    node.inputs[3].default_value = 0.000000
    node.inputs[4].default_value = 0
    node.inputs[5].default_value = 0
    node.inputs[8].default_value = (0.0, 0.0, 0.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
    node.inputs[11].default_value = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
    node.inputs[12].default_value = ""
    node.inputs[13].default_value = ""
    new_nodes["Switch"] = node

    node = tree_nodes.new(type="FunctionNodeCompare")
    node.location = (2960, 160)
    node.data_type = "INT"
    node.mode = "ELEMENT"
    node.operation = "LESS_THAN"
    node.inputs[0].default_value = 0.000000
    node.inputs[1].default_value = 0.000000
    node.inputs[3].default_value = 1
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

    node = tree_nodes.new(type="GeometryNodeSetMaterial")
    node.location = (2960, 0)
    new_nodes["Set Material.001"] = node

    node = tree_nodes.new(type="GeometryNodeMeshToPoints")
    node.location = (2960, -120)
    node.mode = "VERTICES"
    new_nodes["Mesh to Points"] = node

    node = tree_nodes.new(type="GeometryNodeMeshLine")
    node.location = (2960, -300)
    node.count_mode = "TOTAL"
    node.mode = "OFFSET"
    node.inputs[0].default_value = 1
    node.inputs[1].default_value = 1.000000
    node.inputs[2].default_value = (0.0, 0.0, 0.029999999329447746)
    node.inputs[3].default_value = (0.0, 0.0, 1.0)
    new_nodes["Mesh Line"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (2960, -580)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = 0.500000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.009"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (2960, -740)
    node.operation = "LENGTH"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.008"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (3180, 320)
    new_nodes["Group Output"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (790, -280)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[1].default_value = 19.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (190, -220)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[1].default_value = 64.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-1020, 280)
    new_nodes["Group Input"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Set Position"].inputs[0])
    tree_links.new(new_nodes["Boolean Math"].outputs[0], new_nodes["Extrude Mesh"].inputs[1])
    tree_links.new(new_nodes["Random Value.001"].outputs[1], new_nodes["Extrude Mesh"].inputs[3])
    tree_links.new(new_nodes["Normal"].outputs[0], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Vector Math"].outputs[1], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Random Value"].outputs[3], new_nodes["Boolean Math"].inputs[0])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Boolean Math"].inputs[1])
    tree_links.new(new_nodes["Extrude Mesh"].outputs[1], new_nodes["Boolean Math.001"].inputs[0])
    tree_links.new(new_nodes["Boolean Math.002"].outputs[0], new_nodes["Extrude Mesh.001"].inputs[1])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Random Value.002"].inputs[8])
    tree_links.new(new_nodes["Random Value.002"].outputs[1], new_nodes["Extrude Mesh.001"].inputs[3])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Random Value.003"].inputs[8])
    tree_links.new(new_nodes["Boolean Math.001"].outputs[0], new_nodes["Boolean Math.002"].inputs[0])
    tree_links.new(new_nodes["Random Value.003"].outputs[3], new_nodes["Boolean Math.002"].inputs[1])
    tree_links.new(new_nodes["Set Position"].outputs[0], new_nodes["Extrude Mesh"].inputs[0])
    tree_links.new(new_nodes["Position"].outputs[0], new_nodes["Noise Texture"].inputs[0])
    tree_links.new(new_nodes["Vector Math.001"].outputs[0], new_nodes["Set Position"].inputs[3])
    tree_links.new(new_nodes["Noise Texture"].outputs[1], new_nodes["Vector Math.001"].inputs[0])
    tree_links.new(new_nodes["Position.001"].outputs[0], new_nodes["Noise Texture.001"].inputs[0])
    tree_links.new(new_nodes["Vector Math.002"].outputs[0], new_nodes["Set Position.001"].inputs[3])
    tree_links.new(new_nodes["Noise Texture.001"].outputs[1], new_nodes["Vector Math.002"].inputs[0])
    tree_links.new(new_nodes["Extrude Mesh"].outputs[0], new_nodes["Set Position.001"].inputs[0])
    tree_links.new(new_nodes["Set Position.001"].outputs[0], new_nodes["Extrude Mesh.001"].inputs[0])
    tree_links.new(new_nodes["Position.002"].outputs[0], new_nodes["Noise Texture.002"].inputs[0])
    tree_links.new(new_nodes["Vector Math.003"].outputs[0], new_nodes["Set Position.002"].inputs[3])
    tree_links.new(new_nodes["Noise Texture.002"].outputs[1], new_nodes["Vector Math.003"].inputs[0])
    tree_links.new(new_nodes["Extrude Mesh.001"].outputs[0], new_nodes["Set Position.002"].inputs[0])
    tree_links.new(new_nodes["Normal.001"].outputs[0], new_nodes["Vector Math.004"].inputs[0])
    tree_links.new(new_nodes["Vector Math.004"].outputs[1], new_nodes["Math.003"].inputs[0])
    tree_links.new(new_nodes["Random Value.004"].outputs[3], new_nodes["Boolean Math.003"].inputs[0])
    tree_links.new(new_nodes["Math.003"].outputs[0], new_nodes["Boolean Math.003"].inputs[1])
    tree_links.new(new_nodes["Boolean Math.003"].outputs[0], new_nodes["Boolean Math.001"].inputs[1])
    tree_links.new(new_nodes["Extrude Mesh"].outputs[1], new_nodes["Boolean Math.004"].inputs[0])
    tree_links.new(new_nodes["Boolean Math.005"].outputs[0], new_nodes["Extrude Mesh.002"].inputs[1])
    tree_links.new(new_nodes["Math.006"].outputs[0], new_nodes["Random Value.007"].inputs[8])
    tree_links.new(new_nodes["Random Value.007"].outputs[1], new_nodes["Extrude Mesh.002"].inputs[3])
    tree_links.new(new_nodes["Math.005"].outputs[0], new_nodes["Random Value.005"].inputs[8])
    tree_links.new(new_nodes["Boolean Math.004"].outputs[0], new_nodes["Boolean Math.005"].inputs[0])
    tree_links.new(new_nodes["Random Value.005"].outputs[3], new_nodes["Boolean Math.005"].inputs[1])
    tree_links.new(new_nodes["Normal.002"].outputs[0], new_nodes["Vector Math.005"].inputs[0])
    tree_links.new(new_nodes["Vector Math.005"].outputs[1], new_nodes["Math.007"].inputs[0])
    tree_links.new(new_nodes["Random Value.006"].outputs[3], new_nodes["Boolean Math.006"].inputs[0])
    tree_links.new(new_nodes["Math.007"].outputs[0], new_nodes["Boolean Math.006"].inputs[1])
    tree_links.new(new_nodes["Boolean Math.006"].outputs[0], new_nodes["Boolean Math.004"].inputs[1])
    tree_links.new(new_nodes["Set Position.002"].outputs[0], new_nodes["Extrude Mesh.002"].inputs[0])
    tree_links.new(new_nodes["Extrude Mesh.002"].outputs[0], new_nodes["Subdivision Surface"].inputs[0])
    tree_links.new(new_nodes["Position.003"].outputs[0], new_nodes["Noise Texture.004"].inputs[0])
    tree_links.new(new_nodes["Noise Texture.004"].outputs[0], new_nodes["ColorRamp"].inputs[0])
    tree_links.new(new_nodes["ColorRamp"].outputs[0], new_nodes["Subdivision Surface"].inputs[2])
    tree_links.new(new_nodes["Position.004"].outputs[0], new_nodes["Noise Texture.005"].inputs[0])
    tree_links.new(new_nodes["Noise Texture.005"].outputs[0], new_nodes["ColorRamp.001"].inputs[0])
    tree_links.new(new_nodes["ColorRamp.001"].outputs[0], new_nodes["Subdivision Surface.001"].inputs[2])
    tree_links.new(new_nodes["Subdivision Surface"].outputs[0], new_nodes["Subdivision Surface.001"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Set Material"].inputs[2])
    tree_links.new(new_nodes["Set Shade Smooth"].outputs[0], new_nodes["Set Material"].inputs[0])
    tree_links.new(new_nodes["Switch"].outputs[6], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Subdivision Surface.001"].outputs[0], new_nodes["Set Position.003"].inputs[0])
    tree_links.new(new_nodes["Noise Texture.006"].outputs[1], new_nodes["Vector Math.006"].inputs[0])
    tree_links.new(new_nodes["Vector Math.006"].outputs[0], new_nodes["Set Position.003"].inputs[3])
    tree_links.new(new_nodes["Mix"].outputs[0], new_nodes["Noise Texture.006"].inputs[0])
    tree_links.new(new_nodes["Voronoi Texture"].outputs[2], new_nodes["Mix"].inputs[1])
    tree_links.new(new_nodes["Position.006"].outputs[0], new_nodes["Voronoi Texture"].inputs[0])
    tree_links.new(new_nodes["Position.006"].outputs[0], new_nodes["Mix"].inputs[2])
    tree_links.new(new_nodes["Set Material"].outputs[0], new_nodes["Set Position.004"].inputs[0])
    tree_links.new(new_nodes["Vector Math.007"].outputs[0], new_nodes["Set Position.004"].inputs[2])
    tree_links.new(new_nodes["Position.005"].outputs[0], new_nodes["Vector Math.007"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Vector Math.007"].inputs[0])
    tree_links.new(new_nodes["Set Position.003"].outputs[0], new_nodes["Set Shade Smooth"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Map Range"].inputs[0])
    tree_links.new(new_nodes["Map Range"].outputs[0], new_nodes["Subdivision Surface"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Math.008"].inputs[0])
    tree_links.new(new_nodes["Math.008"].outputs[0], new_nodes["Subdivision Surface.001"].inputs[1])
    tree_links.new(new_nodes["Set Position.004"].outputs[0], new_nodes["Switch"].inputs[14])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Compare"].inputs[2])
    tree_links.new(new_nodes["Compare"].outputs[0], new_nodes["Switch"].inputs[1])
    tree_links.new(new_nodes["Set Material.001"].outputs[0], new_nodes["Switch"].inputs[15])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Set Material.001"].inputs[2])
    tree_links.new(new_nodes["Mesh to Points"].outputs[0], new_nodes["Set Material.001"].inputs[0])
    tree_links.new(new_nodes["Mesh Line"].outputs[0], new_nodes["Mesh to Points"].inputs[0])
    tree_links.new(new_nodes["Math.009"].outputs[0], new_nodes["Mesh to Points"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Vector Math.008"].inputs[0])
    tree_links.new(new_nodes["Vector Math.008"].outputs[1], new_nodes["Math.009"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Random Value"].inputs[8])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Random Value.001"].inputs[8])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Random Value.004"].inputs[8])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Math.002"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Random Value.006"].inputs[8])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Math.005"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Math.006"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Math.001"].inputs[0])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group

def create_apply_rock_geo_nodes(new_node_group, tree_nodes, tree_links, rock_obj):
    # initialize variables
    new_nodes = {}

    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="GeometryNodeMeshCube")
    node.location = (1160, 120)
    node.inputs[0].default_value = (1.0, 1.0, 1.0)
    node.inputs[1].default_value = 2
    node.inputs[2].default_value = 2
    node.inputs[3].default_value = 2
    new_nodes["Cube"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (1560, 120)
    new_nodes["Group Output"] = node

    node = tree_nodes.new(type="ShaderNodeTexNoise")
    node.location = (1160, -260)
    node.noise_dimensions = "3D"
    node.inputs[1].default_value = 0.0
    node.inputs[2].default_value = 1.0
    node.inputs[3].default_value = 2.0
    node.inputs[4].default_value = 0.5
    node.inputs[5].default_value = 0.0
    new_nodes["Noise Texture.003"] = node

    node = tree_nodes.new(type="GeometryNodeObjectInfo")
    node.location = (1160, -500)
    node.transform_space = "ORIGINAL"
    node.inputs[0].default_value = rock_obj
    node.inputs[1].default_value = False
    new_nodes["Object Info"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1160, -100)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = 100.0
    node.inputs[2].default_value = 0.5
    new_nodes["Math.004"] = node

    node = tree_nodes.new(type="GeometryNodeGroup")
    node.location = (1340, 120)
    node.node_tree = bpy.data.node_groups.get(ROCK_GEO_NG_NAME)
    node.inputs[0].default_value = 5
    node.inputs[2].default_value = bpy.data.materials.get(ROCK_MAT_NAME)
    node.inputs[3].default_value = bpy.data.materials.get(ROCK_MAT_NAME)
    node.inputs[4].default_value = (0.1, 0.1, 0.1)
    new_nodes["Group"] = node

    # create links
    tree_links.new(new_nodes["Cube"].outputs[0], new_nodes["Group"].inputs[1])
    tree_links.new(new_nodes["Group"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Object Info"].outputs[0], new_nodes["Noise Texture.003"].inputs[0])
    tree_links.new(new_nodes["Noise Texture.003"].outputs[0], new_nodes["Math.004"].inputs[0])
    tree_links.new(new_nodes["Math.004"].outputs[0], new_nodes["Group"].inputs[5])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group

def create_rock_individual_geo_ng(rock_obj, obj_geo_node_group, override_create):
    # initialize variables
    tree_nodes = obj_geo_node_group.nodes
    tree_links = obj_geo_node_group.links

    ensure_node_groups(override_create, [ROCK_GEO_NG_NAME], 'GeometryNodeTree', create_prereq_node_group)
    create_apply_rock_geo_nodes(obj_geo_node_group, tree_nodes, tree_links, rock_obj)

    return obj_geo_node_group

def create_rock_materials(rock_obj, override_create):
    ensure_materials(override_create, [ROCK_MAT_NAME], create_prereq_material)
    rock_mat = bpy.data.materials.get(ROCK_MAT_NAME)
    rock_obj.data.materials.append(rock_mat)

def add_rock_geo_nodes_to_object(rock_obj, override_create):
    geo_nodes_mod = rock_obj.modifiers.new(name="Rock.GeometryNodes", type='NODES')
    create_rock_materials(rock_obj, override_create)
    create_rock_individual_geo_ng(rock_obj, geo_nodes_mod.node_group, override_create)

def pot_create_rock(override_create):
    rock_obj = create_mesh_obj_from_pydata(obj_name=ROCK_OBJNAME)
    add_rock_geo_nodes_to_object(rock_obj, override_create)

class BSR_PotCreateRock(bpy.types.Operator):
    bl_description = "Create a Rock with Geometry Nodes mesh and Shader Nodes material"
    bl_idname = "big_space_rig.pot_create_character_rock"
    bl_label = "Rock"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        s = context.space_data
        return s.type == 'NODE_EDITOR' and s.node_tree != None and s.tree_type == 'GeometryNodeTree'

    def execute(self, context):
        scn = context.scene
        pot_create_rock(scn.BSR_NodesOverrideCreate)
        return {'FINISHED'}
