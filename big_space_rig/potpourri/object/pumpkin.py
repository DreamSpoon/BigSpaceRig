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

PUMPKIN_OBJNAME = "Pumpkin"
PUMPKIN_SURFACE_MAT_NG_NAME = "PumpkinSurface.Potpourri.BSR.MatNG"
PUMPKIN_SKIN_MAT_NAME = "PumpkinSkin.Potpourri.BSR.Material"
PUMPKIN_STEM_MAT_NAME = "PumpkinStem.Potpourri.BSR.Material"
PUMPKIN_POINT_MAT_NAME = "PumpkinPoint.Potpourri.BSR.Material"
PUMPKIN_GEO_NG_NAME = "Pumpkin.Potpourri.BSR.GeoNG"
PUMPKIN_DEFORM_GEO_NG_NAME = "PumpkinDeform.Potpourri.BSR.GeoNG"

def create_prereq_material(material_name, material):
    if material_name == PUMPKIN_SKIN_MAT_NAME:
        return create_mat_pumpkin_skin(material)
    elif material_name == PUMPKIN_STEM_MAT_NAME:
        return create_mat_pumpkin_stem(material)
    elif material_name == PUMPKIN_POINT_MAT_NAME:
        return create_mat_pumpkin_point(material)

    # error
    print("Unknown name passed to create_prereq_material: " + str(material_name))
    return None

def create_prereq_node_group(node_group_name, node_tree_type):
    if node_tree_type == 'GeometryNodeTree':
        if node_group_name == PUMPKIN_DEFORM_GEO_NG_NAME:
            return create_geo_ng_pumpkin_deform()
        elif node_group_name == PUMPKIN_GEO_NG_NAME:
            return create_geo_ng_pumpkin()

    if node_tree_type == 'ShaderNodeTree':
        if node_group_name == PUMPKIN_SURFACE_MAT_NG_NAME:
            return create_mat_ng_pumpkin_surface()

    # error
    print("Unknown name passed to create_prereq_node_group: " + str(node_group_name))
    return None

def create_mat_ng_pumpkin_surface():
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=PUMPKIN_SURFACE_MAT_NG_NAME, type='ShaderNodeTree')
    new_node_group.inputs.new(type='NodeSocketFloat', name="Body Radial Percent")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Body Height Percent")
    new_node_group.inputs.new(type='NodeSocketVector', name="Body Radial Vector")
    new_node_group.inputs.new(type='NodeSocketFloatFactor', name="Inside Pumpkin")
    new_node_group.inputs.new(type='NodeSocketFloatFactor', name="Top/Bottom Nub")
    new_node_group.outputs.new(type='NodeSocketShader', name="Shader")
    new_node_group.outputs.new(type='NodeSocketVector', name="Displacement")
    tree_nodes = new_node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-400, 360)
    node.operation = "POWER"
    node.use_clamp = False
    node.inputs[1].default_value = 0.125000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.014"] = node

    node = tree_nodes.new(type="ShaderNodeValToRGB")
    node.location = (-220, 360)
    node.color_ramp.color_mode = "RGB"
    node.color_ramp.interpolation = "EASE"
    node.color_ramp.elements.remove(node.color_ramp.elements[0])
    elem = node.color_ramp.elements[0]
    elem.position = 0.000000
    elem.color = (0.030000, 0.030000, 0.030000, 1.000000)
    elem = node.color_ramp.elements.new(0.100000)
    elem.color = (0.020000, 0.020000, 0.020000, 1.000000)
    elem = node.color_ramp.elements.new(0.900000)
    elem.color = (0.000000, 0.000000, 0.000000, 1.000000)
    new_nodes["ColorRamp.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-480, 80)
    node.operation = "POWER"
    node.use_clamp = False
    node.inputs[1].default_value = 10.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.012"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-300, 80)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[0].default_value = 1.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.011"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (-660, 80)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 1.000000
    node.inputs[3].default_value = 1.000000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range.001"] = node

    node = tree_nodes.new(type="ShaderNodeTexVoronoi")
    node.location = (-1020, 80)
    node.distance = "EUCLIDEAN"
    node.feature = "SMOOTH_F1"
    node.voronoi_dimensions = "3D"
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 800.000000
    node.inputs[3].default_value = 1.000000
    node.inputs[4].default_value = 0.500000
    node.inputs[5].default_value = 1.000000
    new_nodes["Voronoi Texture.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-840, 80)
    node.operation = "GREATER_THAN"
    node.use_clamp = False
    node.inputs[1].default_value = 0.850000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.008"] = node

    node = tree_nodes.new(type="ShaderNodeTexMusgrave")
    node.location = (-820, 540)
    node.musgrave_dimensions = "3D"
    node.musgrave_type = "FBM"
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 23.000000
    node.inputs[3].default_value = 3.000000
    node.inputs[4].default_value = 1.000000
    node.inputs[5].default_value = 3.000000
    node.inputs[6].default_value = 0.000000
    node.inputs[7].default_value = 1.000000
    new_nodes["Musgrave Texture"] = node

    node = tree_nodes.new(type="ShaderNodeTexCoord")
    node.location = (-1200, 80)
    node.from_instancer = False
    new_nodes["Texture Coordinate.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-400, 660)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.025"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (-640, 540)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 0.900000
    node.inputs[3].default_value = -0.200000
    node.inputs[4].default_value = 0.500000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range.009"] = node

    node = tree_nodes.new(type="ShaderNodeValToRGB")
    node.location = (-220, 620)
    node.color_ramp.color_mode = "RGB"
    node.color_ramp.interpolation = "EASE"
    node.color_ramp.elements.remove(node.color_ramp.elements[0])
    elem = node.color_ramp.elements[0]
    elem.position = 0.000000
    elem.color = (0.323955, 0.117949, 0.004471, 1.000000)
    elem = node.color_ramp.elements.new(0.185455)
    elem.color = (0.350000, 0.092400, 0.000000, 1.000000)
    elem = node.color_ramp.elements.new(0.923636)
    elem.color = (0.420000, 0.075961, 0.000000, 1.000000)
    new_nodes["ColorRamp.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1060, 580)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = 2.382000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.007"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1240, 580)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeTexGradient")
    node.location = (-2080, 680)
    node.gradient_type = "RADIAL"
    new_nodes["Gradient Texture.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1900, 680)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = 20.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1720, 680)
    node.operation = "PINGPONG"
    node.use_clamp = False
    node.inputs[1].default_value = 1.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.006"] = node

    node = tree_nodes.new(type="ShaderNodeFloatCurve")
    node.location = (-1540, 680)
    node.mapping.use_clip = True
    node.mapping.clip_min_x = 0.000000
    node.mapping.clip_min_y = 0.000000
    node.mapping.clip_max_x = 1.000000
    node.mapping.clip_max_y = 1.000000
    node.mapping.extend = "EXTRAPOLATED"
    point = node.mapping.curves[0].points[0]
    point.location = (0.000000, 0.000000)
    point.handle_type = "AUTO"
    point = node.mapping.curves[0].points[1]
    point.location = (0.110000, 0.110000)
    point.handle_type = "AUTO"
    point = node.mapping.curves[0].points.new(0.500000, 0.210000)
    point.handle_type = "AUTO"
    point = node.mapping.curves[0].points.new(0.890000, 0.110000)
    point.handle_type = "AUTO"
    point = node.mapping.curves[0].points.new(1.000000, 0.000000)
    point.handle_type = "AUTO"
    node.mapping.update()
    node.inputs[0].default_value = 1.000000
    new_nodes["Float Curve.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1900, 360)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = 42.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1720, 360)
    node.operation = "PINGPONG"
    node.use_clamp = False
    node.inputs[1].default_value = 1.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeFloatCurve")
    node.location = (-1540, 360)
    node.mapping.use_clip = True
    node.mapping.clip_min_x = 0.000000
    node.mapping.clip_min_y = 0.000000
    node.mapping.clip_max_x = 1.000000
    node.mapping.clip_max_y = 1.000000
    node.mapping.extend = "EXTRAPOLATED"
    point = node.mapping.curves[0].points[0]
    point.location = (0.000000, 0.000000)
    point.handle_type = "AUTO"
    point = node.mapping.curves[0].points[1]
    point.location = (0.110000, 0.110000)
    point.handle_type = "AUTO"
    point = node.mapping.curves[0].points.new(0.500000, 0.210000)
    point.handle_type = "AUTO"
    point = node.mapping.curves[0].points.new(0.890000, 0.110000)
    point.handle_type = "AUTO"
    point = node.mapping.curves[0].points.new(1.000000, 0.000000)
    point.handle_type = "AUTO"
    node.mapping.update()
    node.inputs[0].default_value = 1.000000
    new_nodes["Float Curve"] = node

    node = tree_nodes.new(type="ShaderNodeTexGradient")
    node.location = (-2080, 360)
    node.gradient_type = "RADIAL"
    new_nodes["Gradient Texture"] = node

    node = tree_nodes.new(type="ShaderNodeMixRGB")
    node.location = (80, 620)
    node.blend_type = "LIGHTEN"
    node.use_alpha = False
    node.use_clamp = False
    node.inputs[2].default_value = (1.0, 1.0, 1.0, 1.0)
    new_nodes["Mix"] = node

    node = tree_nodes.new(type="ShaderNodeBsdfPrincipled")
    node.location = (260, 620)
    node.distribution = "GGX"
    node.subsurface_method = "RANDOM_WALK"
    node.inputs[1].default_value = 0.000500
    node.inputs[2].default_value = (1.0, 1.0, 0.5)
    node.inputs[3].default_value = (0.6190975904464722, 0.22791600227355957, 0.017799995839595795, 1.0)
    node.inputs[4].default_value = 1.400000
    node.inputs[5].default_value = 0.000000
    node.inputs[6].default_value = 0.000000
    node.inputs[7].default_value = 0.005000
    node.inputs[8].default_value = 0.000000
    node.inputs[9].default_value = 0.400000
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

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-120, 80)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.010"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-1300, -240)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = (1.0, 1.0, 50.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeTexVoronoi")
    node.location = (-1120, -240)
    node.distance = "EUCLIDEAN"
    node.feature = "SMOOTH_F1"
    node.voronoi_dimensions = "3D"
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 1.618030
    node.inputs[3].default_value = 1.000000
    node.inputs[4].default_value = 0.500000
    node.inputs[5].default_value = 1.000000
    new_nodes["Voronoi Texture"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-940, -240)
    node.operation = "GREATER_THAN"
    node.use_clamp = False
    node.inputs[1].default_value = 0.700000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.013"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (-760, -240)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 1.000000
    node.inputs[3].default_value = 1.000000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range.002"] = node

    node = tree_nodes.new(type="ShaderNodeValToRGB")
    node.location = (-580, -240)
    node.color_ramp.color_mode = "RGB"
    node.color_ramp.interpolation = "LINEAR"
    node.color_ramp.elements.remove(node.color_ramp.elements[0])
    elem = node.color_ramp.elements[0]
    elem.position = 0.000000
    elem.color = (0.000000, 0.000000, 0.000000, 1.000000)
    elem = node.color_ramp.elements.new(0.307273)
    elem.color = (1.000000, 1.000000, 1.000000, 1.000000)
    new_nodes["ColorRamp"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-300, -240)
    node.operation = "POWER"
    node.use_clamp = False
    node.inputs[1].default_value = 0.007000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.009"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1660, -340)
    node.operation = "PINGPONG"
    node.use_clamp = False
    node.inputs[1].default_value = 3.141590
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeBump")
    node.location = (60, 80)
    node.invert = False
    node.inputs[0].default_value = 0.200000
    node.inputs[1].default_value = 1.000000
    node.inputs[3].default_value = 1.000000
    node.inputs[4].default_value = 1.000000
    new_nodes["Bump"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (240, -260)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = (1.0, 1.0, 0.20000000298023224)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeTexNoise")
    node.location = (420, -260)
    node.noise_dimensions = "3D"
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 12.000000
    node.inputs[3].default_value = 1.500000
    node.inputs[4].default_value = 0.500000
    node.inputs[5].default_value = 0.000000
    new_nodes["Noise Texture"] = node

    node = tree_nodes.new(type="ShaderNodeMixRGB")
    node.location = (600, -260)
    node.blend_type = "MIX"
    node.use_alpha = False
    node.use_clamp = False
    node.inputs[0].default_value = 0.110000
    new_nodes["Mix.003"] = node

    node = tree_nodes.new(type="ShaderNodeFloatCurve")
    node.location = (1320, -300)
    node.mapping.use_clip = True
    node.mapping.clip_min_x = 0.000000
    node.mapping.clip_min_y = 0.000000
    node.mapping.clip_max_x = 1.000000
    node.mapping.clip_max_y = 1.000000
    node.mapping.extend = "EXTRAPOLATED"
    point = node.mapping.curves[0].points[0]
    point.location = (0.000000, 0.000000)
    point.handle_type = "AUTO"
    point = node.mapping.curves[0].points[1]
    point.location = (0.110000, 0.110000)
    point.handle_type = "AUTO"
    point = node.mapping.curves[0].points.new(0.500000, 0.210000)
    point.handle_type = "AUTO"
    point = node.mapping.curves[0].points.new(0.890000, 0.110000)
    point.handle_type = "AUTO"
    point = node.mapping.curves[0].points.new(1.000000, 0.000000)
    point.handle_type = "AUTO"
    node.mapping.update()
    node.inputs[0].default_value = 1.000000
    new_nodes["Float Curve.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (960, -300)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = 42.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.026"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1140, -300)
    node.operation = "PINGPONG"
    node.use_clamp = False
    node.inputs[1].default_value = 1.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.028"] = node

    node = tree_nodes.new(type="ShaderNodeTexGradient")
    node.location = (780, -300)
    node.gradient_type = "RADIAL"
    new_nodes["Gradient Texture.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1620, -300)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = 0.002000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.027"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (1800, -300)
    node.operation = "SCALE"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1800, -440)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[0].default_value = 1.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.019"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (1980, -300)
    node.operation = "SCALE"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    new_nodes["Vector Math.008"] = node

    node = tree_nodes.new(type="ShaderNodeTexCoord")
    node.location = (60, -180)
    node.from_instancer = False
    new_nodes["Texture Coordinate"] = node

    node = tree_nodes.new(type="ShaderNodeBsdfPrincipled")
    node.location = (1420, 560)
    node.distribution = "GGX"
    node.subsurface_method = "RANDOM_WALK"
    node.inputs[1].default_value = 0.005000
    node.inputs[2].default_value = (1.0, 1.0, 1.0)
    node.inputs[3].default_value = (0.45329198241233826, 0.22898271679878235, 0.014534974470734596, 1.0)
    node.inputs[4].default_value = 1.400000
    node.inputs[5].default_value = 0.000000
    node.inputs[6].default_value = 0.000000
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

    node = tree_nodes.new(type="ShaderNodeTexNoise")
    node.location = (780, 220)
    node.noise_dimensions = "3D"
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 9.000000
    node.inputs[3].default_value = 3.000000
    node.inputs[4].default_value = 0.500000
    node.inputs[5].default_value = 0.000000
    new_nodes["Noise Texture.001"] = node

    node = tree_nodes.new(type="ShaderNodeValToRGB")
    node.location = (960, 260)
    node.color_ramp.color_mode = "RGB"
    node.color_ramp.interpolation = "EASE"
    node.color_ramp.elements.remove(node.color_ramp.elements[0])
    elem = node.color_ramp.elements[0]
    elem.position = 0.167273
    elem.color = (0.761362, 0.306311, 0.000000, 1.000000)
    elem = node.color_ramp.elements.new(0.707273)
    elem.color = (0.564689, 0.119660, 0.000000, 1.000000)
    new_nodes["ColorRamp.004"] = node

    node = tree_nodes.new(type="ShaderNodeTexCoord")
    node.location = (600, 220)
    node.from_instancer = False
    new_nodes["Texture Coordinate.002"] = node

    node = tree_nodes.new(type="ShaderNodeMixRGB")
    node.location = (1240, 560)
    node.blend_type = "MIX"
    node.use_alpha = False
    node.use_clamp = False
    node.inputs[2].default_value = (0.1313672512769699, 0.04885357618331909, 0.007897761650383472, 1.0)
    new_nodes["Mix.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1240, 380)
    node.operation = "MULTIPLY_ADD"
    node.use_clamp = True
    node.inputs[1].default_value = -0.300000
    node.inputs[2].default_value = 0.300000
    new_nodes["Math.024"] = node

    node = tree_nodes.new(type="ShaderNodeValToRGB")
    node.location = (960, 40)
    node.color_ramp.color_mode = "RGB"
    node.color_ramp.interpolation = "EASE"
    node.color_ramp.elements.remove(node.color_ramp.elements[0])
    elem = node.color_ramp.elements[0]
    elem.position = 0.201818
    elem.color = (0.812106, 0.812106, 0.812106, 1.000000)
    elem = node.color_ramp.elements.new(0.899999)
    elem.color = (0.521110, 0.521110, 0.521110, 1.000000)
    elem = node.color_ramp.elements.new(0.970909)
    elem.color = (0.000000, 0.000000, 0.000000, 1.000000)
    new_nodes["ColorRamp.003"] = node

    node = tree_nodes.new(type="ShaderNodeNewGeometry")
    node.location = (1040, 500)
    new_nodes["Geometry"] = node

    node = tree_nodes.new(type="ShaderNodeMixShader")
    node.location = (1700, 660)
    new_nodes["Mix Shader.003"] = node

    node = tree_nodes.new(type="ShaderNodeMixShader")
    node.location = (820, 780)
    new_nodes["Mix Shader.004"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (-1480, -240)
    new_nodes["Combine XYZ"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1840, -340)
    node.operation = "ARCTAN2"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (-2020, -340)
    new_nodes["Separate XYZ"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (2160, -180)
    node.operation = "SCALE"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    new_nodes["Vector Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeBump")
    node.location = (1240, 20)
    node.invert = False
    node.inputs[0].default_value = 0.070000
    node.inputs[1].default_value = 1.000000
    node.inputs[3].default_value = 1.000000
    node.inputs[4].default_value = 1.000000
    new_nodes["Bump.001"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-620, 1300)
    node.operation = "ADD"
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (-800, 1140)
    node.inputs[0].default_value = 0.000000
    node.inputs[1].default_value = 0.000000
    new_nodes["Combine XYZ.001"] = node

    node = tree_nodes.new(type="ShaderNodeTexCoord")
    node.location = (-800, 1380)
    node.from_instancer = False
    new_nodes["Texture Coordinate.003"] = node

    node = tree_nodes.new(type="ShaderNodeBsdfPrincipled")
    node.location = (260, 1480)
    node.distribution = "GGX"
    node.subsurface_method = "RANDOM_WALK"
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = (1.0, 0.20000000298023224, 0.10000000149011612)
    node.inputs[3].default_value = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
    node.inputs[4].default_value = 1.400000
    node.inputs[5].default_value = 0.000000
    node.inputs[6].default_value = 0.000000
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

    node = tree_nodes.new(type="ShaderNodeValToRGB")
    node.location = (-20, 1480)
    node.color_ramp.color_mode = "RGB"
    node.color_ramp.interpolation = "EASE"
    node.color_ramp.elements.remove(node.color_ramp.elements[0])
    elem = node.color_ramp.elements[0]
    elem.position = 0.376364
    elem.color = (0.027828, 0.023845, 0.009577, 1.000000)
    elem = node.color_ramp.elements.new(0.841818)
    elem.color = (0.054239, 0.045318, 0.020162, 1.000000)
    new_nodes["ColorRamp.005"] = node

    node = tree_nodes.new(type="ShaderNodeTexNoise")
    node.location = (-440, 1300)
    node.noise_dimensions = "3D"
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 100.000000
    node.inputs[3].default_value = 3.000000
    node.inputs[4].default_value = 0.500000
    node.inputs[5].default_value = 6.000000
    new_nodes["Noise Texture.002"] = node

    node = tree_nodes.new(type="ShaderNodeBump")
    node.location = (60, 820)
    node.invert = False
    node.inputs[0].default_value = 0.100000
    node.inputs[1].default_value = 1.000000
    node.inputs[3].default_value = 1.000000
    node.inputs[4].default_value = 1.000000
    new_nodes["Bump.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (460, 780)
    node.operation = "ABSOLUTE"
    node.use_clamp = False
    node.inputs[1].default_value = 0.500000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.015"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (640, 780)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = 0.850000
    node.inputs[2].default_value = 1.000000
    node.inputs[3].default_value = 1.000000
    node.inputs[4].default_value = 0.000000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1700, 140)
    node.operation = "ABSOLUTE"
    node.use_clamp = False
    node.inputs[1].default_value = 0.500000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.017"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (1880, 140)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = 0.850000
    node.inputs[2].default_value = 1.000000
    node.inputs[3].default_value = 1.000000
    node.inputs[4].default_value = 0.000000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range.003"] = node

    node = tree_nodes.new(type="ShaderNodeValToRGB")
    node.location = (-20, 1040)
    node.color_ramp.color_mode = "RGB"
    node.color_ramp.interpolation = "EASE"
    node.color_ramp.elements.remove(node.color_ramp.elements[0])
    elem = node.color_ramp.elements[0]
    elem.position = 0.050909
    elem.color = (0.350000, 0.350000, 0.350000, 1.000000)
    elem = node.color_ramp.elements.new(0.647273)
    elem.color = (0.650000, 0.650000, 0.650000, 1.000000)
    new_nodes["ColorRamp.006"] = node

    node = tree_nodes.new(type="ShaderNodeValToRGB")
    node.location = (-20, 1260)
    node.color_ramp.color_mode = "RGB"
    node.color_ramp.interpolation = "EASE"
    node.color_ramp.elements.remove(node.color_ramp.elements[0])
    elem = node.color_ramp.elements[0]
    elem.position = 0.129091
    elem.color = (0.100000, 0.100000, 0.100000, 1.000000)
    elem = node.color_ramp.elements.new(0.778182)
    elem.color = (0.005000, 0.005000, 0.005000, 1.000000)
    new_nodes["ColorRamp.007"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-2440, -100)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (2340, -20)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Combine XYZ"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Combine XYZ"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Separate XYZ"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Mix Shader.003"].inputs[0])
    tree_links.new(new_nodes["Vector Math.002"].outputs[0], new_nodes["Noise Texture"].inputs[0])
    tree_links.new(new_nodes["Texture Coordinate"].outputs[3], new_nodes["Vector Math.002"].inputs[0])
    tree_links.new(new_nodes["Combine XYZ"].outputs[0], new_nodes["Vector Math.003"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ"].outputs[0], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ"].outputs[1], new_nodes["Math"].inputs[1])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Combine XYZ"].inputs[2])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Math.001"].inputs[0])
    tree_links.new(new_nodes["Math.003"].outputs[0], new_nodes["Math.004"].inputs[0])
    tree_links.new(new_nodes["Gradient Texture"].outputs[1], new_nodes["Math.003"].inputs[0])
    tree_links.new(new_nodes["Math.004"].outputs[0], new_nodes["Float Curve"].inputs[1])
    tree_links.new(new_nodes["Math.005"].outputs[0], new_nodes["Math.006"].inputs[0])
    tree_links.new(new_nodes["Gradient Texture.001"].outputs[1], new_nodes["Math.005"].inputs[0])
    tree_links.new(new_nodes["Math.006"].outputs[0], new_nodes["Float Curve.001"].inputs[1])
    tree_links.new(new_nodes["Float Curve.001"].outputs[0], new_nodes["Math.002"].inputs[0])
    tree_links.new(new_nodes["Float Curve"].outputs[0], new_nodes["Math.002"].inputs[1])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Math.007"].inputs[0])
    tree_links.new(new_nodes["Mix"].outputs[0], new_nodes["Principled BSDF"].inputs[0])
    tree_links.new(new_nodes["Vector Math.003"].outputs[0], new_nodes["Voronoi Texture"].inputs[0])
    tree_links.new(new_nodes["ColorRamp"].outputs[0], new_nodes["Math.009"].inputs[0])
    tree_links.new(new_nodes["Texture Coordinate.001"].outputs[3], new_nodes["Voronoi Texture.002"].inputs[0])
    tree_links.new(new_nodes["Voronoi Texture.002"].outputs[1], new_nodes["Math.008"].inputs[0])
    tree_links.new(new_nodes["Math.008"].outputs[0], new_nodes["Map Range.001"].inputs[0])
    tree_links.new(new_nodes["ColorRamp.001"].outputs[0], new_nodes["Mix"].inputs[1])
    tree_links.new(new_nodes["Math.009"].outputs[0], new_nodes["Math.010"].inputs[1])
    tree_links.new(new_nodes["Math.012"].outputs[0], new_nodes["Math.011"].inputs[1])
    tree_links.new(new_nodes["Map Range.001"].outputs[0], new_nodes["Math.012"].inputs[0])
    tree_links.new(new_nodes["Math.011"].outputs[0], new_nodes["Math.010"].inputs[0])
    tree_links.new(new_nodes["Voronoi Texture.002"].outputs[0], new_nodes["Math.014"].inputs[0])
    tree_links.new(new_nodes["Math.014"].outputs[0], new_nodes["ColorRamp.002"].inputs[0])
    tree_links.new(new_nodes["ColorRamp.002"].outputs[0], new_nodes["Mix"].inputs[0])
    tree_links.new(new_nodes["Bump"].outputs[0], new_nodes["Principled BSDF"].inputs[22])
    tree_links.new(new_nodes["Math.010"].outputs[0], new_nodes["Bump"].inputs[2])
    tree_links.new(new_nodes["Voronoi Texture.002"].outputs[0], new_nodes["Map Range.001"].inputs[4])
    tree_links.new(new_nodes["Math.013"].outputs[0], new_nodes["Map Range.002"].inputs[0])
    tree_links.new(new_nodes["Voronoi Texture"].outputs[1], new_nodes["Math.013"].inputs[0])
    tree_links.new(new_nodes["Voronoi Texture"].outputs[0], new_nodes["Map Range.002"].inputs[4])
    tree_links.new(new_nodes["Map Range.002"].outputs[0], new_nodes["ColorRamp"].inputs[0])
    tree_links.new(new_nodes["Mix.001"].outputs[0], new_nodes["Principled BSDF.001"].inputs[0])
    tree_links.new(new_nodes["Noise Texture.001"].outputs[0], new_nodes["ColorRamp.004"].inputs[0])
    tree_links.new(new_nodes["ColorRamp.003"].outputs[0], new_nodes["Principled BSDF.001"].inputs[9])
    tree_links.new(new_nodes["Noise Texture.001"].outputs[0], new_nodes["ColorRamp.003"].inputs[0])
    tree_links.new(new_nodes["Bump.001"].outputs[0], new_nodes["Principled BSDF.001"].inputs[22])
    tree_links.new(new_nodes["Noise Texture.001"].outputs[0], new_nodes["Bump.001"].inputs[2])
    tree_links.new(new_nodes["Principled BSDF.001"].outputs[0], new_nodes["Mix Shader.003"].inputs[2])
    tree_links.new(new_nodes["Math.019"].outputs[0], new_nodes["Vector Math.008"].inputs[3])
    tree_links.new(new_nodes["Mix Shader.004"].outputs[0], new_nodes["Mix Shader.003"].inputs[1])
    tree_links.new(new_nodes["Texture Coordinate.002"].outputs[3], new_nodes["Noise Texture.001"].inputs[0])
    tree_links.new(new_nodes["ColorRamp.004"].outputs[0], new_nodes["Mix.001"].inputs[1])
    tree_links.new(new_nodes["Geometry"].outputs[6], new_nodes["Mix.001"].inputs[0])
    tree_links.new(new_nodes["Geometry"].outputs[6], new_nodes["Math.024"].inputs[0])
    tree_links.new(new_nodes["Math.024"].outputs[0], new_nodes["Principled BSDF.001"].inputs[7])
    tree_links.new(new_nodes["Math.007"].outputs[0], new_nodes["Math.025"].inputs[0])
    tree_links.new(new_nodes["Math.025"].outputs[0], new_nodes["ColorRamp.001"].inputs[0])
    tree_links.new(new_nodes["Texture Coordinate.001"].outputs[3], new_nodes["Musgrave Texture"].inputs[0])
    tree_links.new(new_nodes["Musgrave Texture"].outputs[0], new_nodes["Map Range.009"].inputs[0])
    tree_links.new(new_nodes["Map Range.009"].outputs[0], new_nodes["Math.025"].inputs[1])
    tree_links.new(new_nodes["Math.026"].outputs[0], new_nodes["Math.028"].inputs[0])
    tree_links.new(new_nodes["Gradient Texture.002"].outputs[1], new_nodes["Math.026"].inputs[0])
    tree_links.new(new_nodes["Math.028"].outputs[0], new_nodes["Float Curve.002"].inputs[1])
    tree_links.new(new_nodes["Float Curve.002"].outputs[0], new_nodes["Math.027"].inputs[0])
    tree_links.new(new_nodes["Math.027"].outputs[0], new_nodes["Vector Math"].inputs[3])
    tree_links.new(new_nodes["Mix.003"].outputs[0], new_nodes["Gradient Texture.002"].inputs[0])
    tree_links.new(new_nodes["Noise Texture"].outputs[1], new_nodes["Mix.003"].inputs[2])
    tree_links.new(new_nodes["Texture Coordinate"].outputs[1], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Vector Math"].outputs[0], new_nodes["Vector Math.008"].inputs[0])
    tree_links.new(new_nodes["Mix Shader.003"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Gradient Texture"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Gradient Texture.001"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Mix.003"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Math.019"].inputs[1])
    tree_links.new(new_nodes["Principled BSDF"].outputs[0], new_nodes["Mix Shader.004"].inputs[2])
    tree_links.new(new_nodes["Principled BSDF.002"].outputs[0], new_nodes["Mix Shader.004"].inputs[1])
    tree_links.new(new_nodes["ColorRamp.005"].outputs[0], new_nodes["Principled BSDF.002"].inputs[0])
    tree_links.new(new_nodes["Noise Texture.002"].outputs[0], new_nodes["ColorRamp.005"].inputs[0])
    tree_links.new(new_nodes["Vector Math.004"].outputs[0], new_nodes["Noise Texture.002"].inputs[0])
    tree_links.new(new_nodes["Vector Math.008"].outputs[0], new_nodes["Vector Math.001"].inputs[0])
    tree_links.new(new_nodes["Vector Math.001"].outputs[0], new_nodes["Group Output"].inputs[1])
    tree_links.new(new_nodes["Texture Coordinate.003"].outputs[3], new_nodes["Vector Math.004"].inputs[0])
    tree_links.new(new_nodes["Combine XYZ.001"].outputs[0], new_nodes["Vector Math.004"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Combine XYZ.001"].inputs[2])
    tree_links.new(new_nodes["Noise Texture.002"].outputs[0], new_nodes["ColorRamp.006"].inputs[0])
    tree_links.new(new_nodes["ColorRamp.006"].outputs[0], new_nodes["Principled BSDF.002"].inputs[9])
    tree_links.new(new_nodes["Noise Texture.002"].outputs[0], new_nodes["ColorRamp.007"].inputs[0])
    tree_links.new(new_nodes["ColorRamp.007"].outputs[0], new_nodes["Principled BSDF.002"].inputs[7])
    tree_links.new(new_nodes["Bump.002"].outputs[0], new_nodes["Principled BSDF.002"].inputs[22])
    tree_links.new(new_nodes["Noise Texture.002"].outputs[0], new_nodes["Bump.002"].inputs[2])
    tree_links.new(new_nodes["Math.015"].outputs[0], new_nodes["Map Range"].inputs[0])
    tree_links.new(new_nodes["Map Range"].outputs[0], new_nodes["Mix Shader.004"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Math.015"].inputs[0])
    tree_links.new(new_nodes["Math.017"].outputs[0], new_nodes["Map Range.003"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Math.017"].inputs[0])
    tree_links.new(new_nodes["Map Range.003"].outputs[0], new_nodes["Vector Math.001"].inputs[3])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False
    return new_node_group

def create_mat_pumpkin_skin(material):
    # initialize variables
    new_nodes = {}
    tree_nodes = material.node_tree.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (4960, 260)
    node.node_tree = bpy.data.node_groups.get(PUMPKIN_SURFACE_MAT_NG_NAME)
    new_nodes["Group"] = node

    node = tree_nodes.new(type="ShaderNodeValToRGB")
    node.location = (4440, 740)
    node.color_ramp.color_mode = "RGB"
    node.color_ramp.interpolation = "EASE"
    node.color_ramp.elements.remove(node.color_ramp.elements[0])
    elem = node.color_ramp.elements[0]
    elem.position = 0.100000
    elem.color = (0.000000, 0.000000, 0.000000, 1.000000)
    elem = node.color_ramp.elements.new(0.534546)
    elem.color = (1.000000, 1.000000, 1.000000, 1.000000)
    new_nodes["ColorRamp"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (4540, 900)
    node.operation = "LESS_THAN"
    node.use_clamp = False
    node.inputs[1].default_value = 0.500000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeTexNoise")
    node.location = (4540, 360)
    node.noise_dimensions = "2D"
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 8.000000
    node.inputs[3].default_value = 1.618034
    node.inputs[4].default_value = 0.618034
    node.inputs[5].default_value = 0.166667
    new_nodes["Noise Texture"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (4540, 520)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (3460, 320)
    node.inputs[2].default_value = 0.000000
    new_nodes["Combine XYZ"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (3460, 520)
    node.operation = "SUBTRACT"
    node.inputs[1].default_value = (0.5, 0.5, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.010"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (3820, 520)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (3820, -20)
    node.operation = "SUBTRACT"
    node.inputs[1].default_value = (0.15000000596046448, -0.20000000298023224, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (3820, 100)
    node.operation = "LENGTH"
    node.inputs[1].default_value = (0.05000000074505806, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.006"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (3640, 260)
    node.operation = "LENGTH"
    node.inputs[1].default_value = (0.05000000074505806, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.008"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (3640, 140)
    node.operation = "SUBTRACT"
    node.inputs[1].default_value = (-0.15000000596046448, -0.20000000298023224, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.007"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (3820, 360)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = 0.030000
    node.inputs[2].default_value = 0.130000
    node.inputs[3].default_value = 1.000000
    node.inputs[4].default_value = 0.000000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range.003"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (4000, 100)
    node.operation = "LENGTH"
    node.inputs[1].default_value = (0.05000000074505806, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (4000, -20)
    node.operation = "SUBTRACT"
    node.inputs[1].default_value = (0.0, -0.25, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (4000, 360)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = 0.030000
    node.inputs[2].default_value = 0.130000
    node.inputs[3].default_value = 1.000000
    node.inputs[4].default_value = 0.000000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (4000, 520)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (4180, -20)
    node.operation = "SUBTRACT"
    node.inputs[1].default_value = (-0.20000000298023224, 0.07999999821186066, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (4180, 100)
    node.operation = "LENGTH"
    node.inputs[1].default_value = (0.05000000074505806, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (4180, 360)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = 0.040000
    node.inputs[2].default_value = 0.250000
    node.inputs[3].default_value = 1.000000
    node.inputs[4].default_value = 0.000000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (4180, 520)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (4360, -20)
    node.operation = "SUBTRACT"
    node.inputs[1].default_value = (0.20000000298023224, 0.07999999821186066, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (4360, 100)
    node.operation = "LENGTH"
    node.inputs[1].default_value = (0.05000000074505806, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.009"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (4360, 360)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = 0.040000
    node.inputs[2].default_value = 0.250000
    node.inputs[3].default_value = 1.000000
    node.inputs[4].default_value = 0.000000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (4360, 520)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (3280, 520)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = -1.047200
    node.inputs[2].default_value = 1.047197
    node.inputs[3].default_value = 0.000000
    node.inputs[4].default_value = 1.000000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range.005"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (3280, 100)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = -0.800000
    node.inputs[2].default_value = 0.800000
    node.inputs[3].default_value = 0.000000
    node.inputs[4].default_value = 1.000000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range.006"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (3280, 260)
    node.operation = "ARCTAN2"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.006"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (3280, -160)
    node.operation = "ARCTAN2"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.007"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (3280, -320)
    node.operation = "LENGTH"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.012"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (3100, -120)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = (1.0, 1.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.011"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (3100, 20)
    new_nodes["Separate XYZ"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (3100, -320)
    node.operation = "ADD"
    node.inputs[1].default_value = (0.0, 0.0, -0.09000000357627869)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.013"] = node

    node = tree_nodes.new(type="ShaderNodeTexCoord")
    node.location = (3100, -520)
    node.from_instancer = False
    new_nodes["Texture Coordinate"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (3640, 520)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = 0.030000
    node.inputs[2].default_value = 0.130000
    node.inputs[3].default_value = 1.000000
    node.inputs[4].default_value = 0.000000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range.004"] = node

    node = tree_nodes.new(type="ShaderNodeVolumeScatter")
    node.location = (4960, 620)
    node.inputs[0].default_value = (1.0, 0.0020000000949949026, 0.0, 1.0)
    node.inputs[1].default_value = 1000000.000000
    node.inputs[2].default_value = 0.010000
    new_nodes["Volume Scatter"] = node

    node = tree_nodes.new(type="ShaderNodeVolumeAbsorption")
    node.location = (4960, 720)
    node.inputs[0].default_value = (0.9990000128746033, 0.9900000095367432, 0.0, 1.0)
    node.inputs[1].default_value = 100000.000000
    new_nodes["Volume Absorption"] = node

    node = tree_nodes.new(type="ShaderNodeMixShader")
    node.location = (4960, 860)
    node.inputs[0].default_value = 0.100000
    new_nodes["Mix Shader.001"] = node

    node = tree_nodes.new(type="ShaderNodeMixShader")
    node.location = (4960, 1000)
    new_nodes["Mix Shader"] = node

    node = tree_nodes.new(type="ShaderNodeBsdfTransparent")
    node.location = (4960, 340)
    node.inputs[0].default_value = (1.0, 1.0, 1.0, 1.0)
    new_nodes["Transparent BSDF"] = node

    node = tree_nodes.new(type="ShaderNodeMixShader")
    node.location = (4960, 460)
    new_nodes["Mix Shader.002"] = node

    node = tree_nodes.new(type="ShaderNodeAttribute")
    node.location = (4780, 100)
    node.attribute_name = "body_radial_vec"
    node.attribute_type = "GEOMETRY"
    new_nodes["Attribute"] = node

    node = tree_nodes.new(type="ShaderNodeAttribute")
    node.location = (4780, 460)
    node.attribute_name = "body_radial_pct"
    node.attribute_type = "GEOMETRY"
    new_nodes["Attribute.001"] = node

    node = tree_nodes.new(type="ShaderNodeAttribute")
    node.location = (4780, 280)
    node.attribute_name = "body_h_pct"
    node.attribute_type = "GEOMETRY"
    new_nodes["Attribute.002"] = node

    node = tree_nodes.new(type="ShaderNodeAttribute")
    node.location = (4780, -80)
    node.attribute_name = "inside_pumpkin"
    node.attribute_type = "GEOMETRY"
    new_nodes["Attribute.003"] = node

    node = tree_nodes.new(type="ShaderNodeAttribute")
    node.location = (4780, -260)
    node.attribute_name = "top_bot_nub"
    node.attribute_type = "GEOMETRY"
    new_nodes["Attribute.004"] = node

    node = tree_nodes.new(type="ShaderNodeOutputMaterial")
    node.location = (5240, 480)
    node.target = "ALL"
    new_nodes["Material Output"] = node

    # create links
    tree_links = material.node_tree.links
    tree_links.new(new_nodes["Group"].outputs[1], new_nodes["Material Output"].inputs[2])
    tree_links.new(new_nodes["Attribute.001"].outputs[2], new_nodes["Group"].inputs[0])
    tree_links.new(new_nodes["Attribute.002"].outputs[2], new_nodes["Group"].inputs[1])
    tree_links.new(new_nodes["Attribute"].outputs[1], new_nodes["Group"].inputs[2])
    tree_links.new(new_nodes["Mix Shader.001"].outputs[0], new_nodes["Mix Shader"].inputs[2])
    tree_links.new(new_nodes["Volume Absorption"].outputs[0], new_nodes["Mix Shader.001"].inputs[1])
    tree_links.new(new_nodes["Volume Scatter"].outputs[0], new_nodes["Mix Shader.001"].inputs[2])
    tree_links.new(new_nodes["Vector Math.013"].outputs[0], new_nodes["Separate XYZ"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ"].outputs[0], new_nodes["Math.006"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ"].outputs[1], new_nodes["Math.006"].inputs[1])
    tree_links.new(new_nodes["Vector Math.011"].outputs[0], new_nodes["Vector Math.012"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ"].outputs[2], new_nodes["Math.007"].inputs[0])
    tree_links.new(new_nodes["Vector Math.012"].outputs[1], new_nodes["Math.007"].inputs[1])
    tree_links.new(new_nodes["Math.007"].outputs[0], new_nodes["Map Range.006"].inputs[0])
    tree_links.new(new_nodes["Math.006"].outputs[0], new_nodes["Map Range.005"].inputs[0])
    tree_links.new(new_nodes["Map Range.005"].outputs[0], new_nodes["Combine XYZ"].inputs[0])
    tree_links.new(new_nodes["Map Range.006"].outputs[0], new_nodes["Combine XYZ"].inputs[1])
    tree_links.new(new_nodes["Math.005"].outputs[0], new_nodes["Mix Shader"].inputs[0])
    tree_links.new(new_nodes["Texture Coordinate"].outputs[3], new_nodes["Vector Math.013"].inputs[0])
    tree_links.new(new_nodes["Vector Math.013"].outputs[0], new_nodes["Vector Math.011"].inputs[0])
    tree_links.new(new_nodes["Attribute.003"].outputs[2], new_nodes["Group"].inputs[3])
    tree_links.new(new_nodes["Mix Shader"].outputs[0], new_nodes["Material Output"].inputs[1])
    tree_links.new(new_nodes["Vector Math.002"].outputs[0], new_nodes["Vector Math.009"].inputs[0])
    tree_links.new(new_nodes["Vector Math.009"].outputs[1], new_nodes["Map Range.001"].inputs[0])
    tree_links.new(new_nodes["Noise Texture"].outputs[0], new_nodes["Math"].inputs[1])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["ColorRamp"].inputs[0])
    tree_links.new(new_nodes["Combine XYZ"].outputs[0], new_nodes["Vector Math.010"].inputs[0])
    tree_links.new(new_nodes["Vector Math.003"].outputs[0], new_nodes["Vector Math.004"].inputs[0])
    tree_links.new(new_nodes["Vector Math.004"].outputs[1], new_nodes["Map Range.002"].inputs[0])
    tree_links.new(new_nodes["Math.003"].outputs[0], new_nodes["Math.004"].inputs[1])
    tree_links.new(new_nodes["Math.004"].outputs[0], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Map Range.001"].outputs[0], new_nodes["Math.004"].inputs[0])
    tree_links.new(new_nodes["Vector Math.010"].outputs[0], new_nodes["Vector Math.002"].inputs[0])
    tree_links.new(new_nodes["Vector Math.010"].outputs[0], new_nodes["Vector Math.003"].inputs[0])
    tree_links.new(new_nodes["Vector Math"].outputs[0], new_nodes["Vector Math.001"].inputs[0])
    tree_links.new(new_nodes["Vector Math.001"].outputs[1], new_nodes["Map Range"].inputs[0])
    tree_links.new(new_nodes["Vector Math.010"].outputs[0], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Map Range.002"].outputs[0], new_nodes["Math.003"].inputs[0])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Math.003"].inputs[1])
    tree_links.new(new_nodes["Vector Math.007"].outputs[0], new_nodes["Vector Math.008"].inputs[0])
    tree_links.new(new_nodes["Vector Math.008"].outputs[1], new_nodes["Map Range.004"].inputs[0])
    tree_links.new(new_nodes["Vector Math.010"].outputs[0], new_nodes["Vector Math.007"].inputs[0])
    tree_links.new(new_nodes["Map Range"].outputs[0], new_nodes["Math.002"].inputs[0])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Math.002"].inputs[1])
    tree_links.new(new_nodes["Vector Math.005"].outputs[0], new_nodes["Vector Math.006"].inputs[0])
    tree_links.new(new_nodes["Vector Math.006"].outputs[1], new_nodes["Map Range.003"].inputs[0])
    tree_links.new(new_nodes["Vector Math.010"].outputs[0], new_nodes["Vector Math.005"].inputs[0])
    tree_links.new(new_nodes["Map Range.004"].outputs[0], new_nodes["Math.001"].inputs[0])
    tree_links.new(new_nodes["Map Range.003"].outputs[0], new_nodes["Math.001"].inputs[1])
    tree_links.new(new_nodes["Combine XYZ"].outputs[0], new_nodes["Noise Texture"].inputs[0])
    tree_links.new(new_nodes["Transparent BSDF"].outputs[0], new_nodes["Mix Shader.002"].inputs[1])
    tree_links.new(new_nodes["Group"].outputs[0], new_nodes["Mix Shader.002"].inputs[2])
    tree_links.new(new_nodes["Math.005"].outputs[0], new_nodes["Mix Shader.002"].inputs[0])
    tree_links.new(new_nodes["Attribute.004"].outputs[2], new_nodes["Group"].inputs[4])
    tree_links.new(new_nodes["Mix Shader.002"].outputs[0], new_nodes["Material Output"].inputs[0])
    tree_links.new(new_nodes["ColorRamp"].outputs[0], new_nodes["Math.005"].inputs[0])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_nodes

def create_mat_pumpkin_stem(material):
    # initialize variables
    new_nodes = {}
    tree_nodes = material.node_tree.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeValToRGB")
    node.location = (-280, 300)
    node.color_ramp.color_mode = "RGB"
    node.color_ramp.interpolation = "LINEAR"
    node.color_ramp.elements.remove(node.color_ramp.elements[0])
    elem = node.color_ramp.elements[0]
    elem.position = 0.000000
    elem.color = (0.000905, 0.005000, 0.000513, 1.000000)
    elem = node.color_ramp.elements.new(1.000000)
    elem.color = (0.114386, 0.102213, 0.075504, 1.000000)
    new_nodes["ColorRamp.001"] = node

    node = tree_nodes.new(type="ShaderNodeBsdfPrincipled")
    node.location = (20, 300)
    node.distribution = "GGX"
    node.subsurface_method = "RANDOM_WALK"
    node.inputs[1].default_value = 0.000300
    node.inputs[2].default_value = (1.0, 1.0, 1.0)
    node.inputs[3].default_value = (0.10461650043725967, 0.09530749171972275, 0.07036010175943375, 1.0)
    node.inputs[4].default_value = 1.400000
    node.inputs[5].default_value = 0.000000
    node.inputs[6].default_value = 0.000000
    node.inputs[7].default_value = 0.030000
    node.inputs[8].default_value = 0.000000
    node.inputs[9].default_value = 0.750000
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

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-460, 300)
    node.operation = "ADD"
    node.use_clamp = True
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (480, 300)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = 0.998000
    node.inputs[2].default_value = 1.000000
    node.inputs[3].default_value = 1.000000
    node.inputs[4].default_value = 0.000000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range"] = node

    node = tree_nodes.new(type="ShaderNodeAttribute")
    node.location = (300, 300)
    node.attribute_name = "stem_height_pct"
    node.attribute_type = "GEOMETRY"
    new_nodes["Attribute.004"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (-1280, 300)
    new_nodes["Separate XYZ"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (-1100, 300)
    new_nodes["Combine XYZ"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1280, 120)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = 0.300000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math"] = node

    node = tree_nodes.new(type="ShaderNodeAttribute")
    node.location = (-1460, 120)
    node.attribute_name = "stem_height_pct"
    node.attribute_type = "GEOMETRY"
    new_nodes["Attribute"] = node

    node = tree_nodes.new(type="ShaderNodeAttribute")
    node.location = (-1460, 300)
    node.attribute_name = "stem_radial_vec"
    node.attribute_type = "GEOMETRY"
    new_nodes["Attribute.001"] = node

    node = tree_nodes.new(type="ShaderNodeValToRGB")
    node.location = (-740, 300)
    node.color_ramp.color_mode = "RGB"
    node.color_ramp.interpolation = "EASE"
    node.color_ramp.elements.remove(node.color_ramp.elements[0])
    elem = node.color_ramp.elements[0]
    elem.position = 0.629091
    elem.color = (0.000000, 0.000000, 0.000000, 1.000000)
    elem = node.color_ramp.elements.new(0.738182)
    elem.color = (0.680157, 0.680157, 0.680157, 1.000000)
    elem = node.color_ramp.elements.new(1.000000)
    elem.color = (1.000000, 1.000000, 1.000000, 1.000000)
    new_nodes["ColorRamp"] = node

    node = tree_nodes.new(type="ShaderNodeTexNoise")
    node.location = (-920, 300)
    node.noise_dimensions = "3D"
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 60.000000
    node.inputs[3].default_value = 3.000000
    node.inputs[4].default_value = 1.000000
    node.inputs[5].default_value = 0.000000
    new_nodes["Noise Texture"] = node

    node = tree_nodes.new(type="ShaderNodeTexCoord")
    node.location = (-1100, -100)
    node.from_instancer = False
    new_nodes["Texture Coordinate"] = node

    node = tree_nodes.new(type="ShaderNodeTexVoronoi")
    node.location = (-920, -100)
    node.distance = "EUCLIDEAN"
    node.feature = "F1"
    node.voronoi_dimensions = "3D"
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 800.000000
    node.inputs[3].default_value = 1.000000
    node.inputs[4].default_value = 0.500000
    node.inputs[5].default_value = 1.000000
    new_nodes["Voronoi Texture"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-340, -180)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeBump")
    node.location = (-160, -180)
    node.invert = False
    node.inputs[0].default_value = 0.250000
    node.inputs[1].default_value = 1.000000
    node.inputs[3].default_value = 1.000000
    node.inputs[4].default_value = 1.000000
    new_nodes["Bump"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (660, -180)
    node.operation = "SCALE"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="ShaderNodeTexGradient")
    node.location = (-540, -420)
    node.gradient_type = "RADIAL"
    new_nodes["Gradient Texture"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-180, -420)
    node.operation = "PINGPONG"
    node.use_clamp = False
    node.inputs[1].default_value = 1.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-360, -420)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = 10.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (480, -420)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.006"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (300, -420)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeFloatCurve")
    node.location = (0, -420)
    node.mapping.use_clip = True
    node.mapping.clip_min_x = 0.000000
    node.mapping.clip_min_y = 0.000000
    node.mapping.clip_max_x = 1.000000
    node.mapping.clip_max_y = 1.000000
    node.mapping.extend = "EXTRAPOLATED"
    point = node.mapping.curves[0].points[0]
    point.location = (0.000000, 0.000000)
    point.handle_type = "AUTO"
    point = node.mapping.curves[0].points[1]
    point.location = (0.125000, 0.030000)
    point.handle_type = "AUTO"
    point = node.mapping.curves[0].points.new(0.499126, 0.502500)
    point.handle_type = "AUTO"
    point = node.mapping.curves[0].points.new(0.875000, 0.030000)
    point.handle_type = "AUTO"
    point = node.mapping.curves[0].points.new(1.000000, 0.000000)
    point.handle_type = "AUTO"
    node.mapping.update()
    node.inputs[0].default_value = 1.000000
    new_nodes["Float Curve"] = node

    node = tree_nodes.new(type="ShaderNodeAttribute")
    node.location = (-720, -420)
    node.attribute_name = "stem_radial_vec"
    node.attribute_type = "GEOMETRY"
    new_nodes["Attribute.002"] = node

    node = tree_nodes.new(type="ShaderNodeAttribute")
    node.location = (-360, -600)
    node.attribute_name = "stem_height"
    node.attribute_type = "GEOMETRY"
    new_nodes["Attribute.006"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-180, -600)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = -0.080000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.007"] = node

    node = tree_nodes.new(type="ShaderNodeAttribute")
    node.location = (-180, -780)
    node.attribute_name = "stem_height_pct"
    node.attribute_type = "GEOMETRY"
    new_nodes["Attribute.003"] = node

    node = tree_nodes.new(type="ShaderNodeValToRGB")
    node.location = (0, -780)
    node.color_ramp.color_mode = "RGB"
    node.color_ramp.interpolation = "LINEAR"
    node.color_ramp.elements.remove(node.color_ramp.elements[0])
    elem = node.color_ramp.elements[0]
    elem.position = 0.643636
    elem.color = (1.000000, 1.000000, 1.000000, 1.000000)
    elem = node.color_ramp.elements.new(0.967273)
    elem.color = (0.006062, 0.006062, 0.006062, 1.000000)
    new_nodes["ColorRamp.003"] = node

    node = tree_nodes.new(type="ShaderNodeTexCoord")
    node.location = (480, -180)
    node.from_instancer = False
    new_nodes["Texture Coordinate.001"] = node

    node = tree_nodes.new(type="ShaderNodeValToRGB")
    node.location = (-740, -100)
    node.color_ramp.color_mode = "RGB"
    node.color_ramp.interpolation = "EASE"
    node.color_ramp.elements.remove(node.color_ramp.elements[0])
    elem = node.color_ramp.elements[0]
    elem.position = 0.000000
    elem.color = (1.000000, 1.000000, 1.000000, 1.000000)
    elem = node.color_ramp.elements.new(0.176364)
    elem.color = (0.000000, 0.000000, 0.000000, 1.000000)
    new_nodes["ColorRamp.002"] = node

    node = tree_nodes.new(type="ShaderNodeValToRGB")
    node.location = (-280, 740)
    node.color_ramp.color_mode = "RGB"
    node.color_ramp.interpolation = "EASE"
    node.color_ramp.elements.remove(node.color_ramp.elements[0])
    elem = node.color_ramp.elements[0]
    elem.position = 0.050909
    elem.color = (0.350000, 0.350000, 0.350000, 1.000000)
    elem = node.color_ramp.elements.new(0.647273)
    elem.color = (0.650000, 0.650000, 0.650000, 1.000000)
    new_nodes["ColorRamp.006"] = node

    node = tree_nodes.new(type="ShaderNodeValToRGB")
    node.location = (-280, 960)
    node.color_ramp.color_mode = "RGB"
    node.color_ramp.interpolation = "EASE"
    node.color_ramp.elements.remove(node.color_ramp.elements[0])
    elem = node.color_ramp.elements[0]
    elem.position = 0.129091
    elem.color = (0.007000, 0.007000, 0.007000, 1.000000)
    elem = node.color_ramp.elements.new(0.778182)
    elem.color = (0.002000, 0.002000, 0.002000, 1.000000)
    new_nodes["ColorRamp.007"] = node

    node = tree_nodes.new(type="ShaderNodeBump")
    node.location = (-180, 520)
    node.invert = False
    node.inputs[0].default_value = 0.400000
    node.inputs[1].default_value = 1.000000
    node.inputs[3].default_value = 1.000000
    node.inputs[4].default_value = 1.000000
    new_nodes["Bump.001"] = node

    node = tree_nodes.new(type="ShaderNodeValToRGB")
    node.location = (-280, 1180)
    node.color_ramp.color_mode = "RGB"
    node.color_ramp.interpolation = "EASE"
    node.color_ramp.elements.remove(node.color_ramp.elements[0])
    elem = node.color_ramp.elements[0]
    elem.position = 0.247273
    elem.color = (0.140476, 0.080072, 0.027312, 1.000000)
    elem = node.color_ramp.elements.new(0.687273)
    elem.color = (0.286793, 0.150956, 0.041281, 1.000000)
    new_nodes["ColorRamp.004"] = node

    node = tree_nodes.new(type="ShaderNodeBsdfPrincipled")
    node.location = (0, 1060)
    node.distribution = "GGX"
    node.subsurface_method = "RANDOM_WALK"
    node.inputs[1].default_value = 0.000300
    node.inputs[2].default_value = (1.0, 1.0, 1.0)
    node.inputs[3].default_value = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
    node.inputs[4].default_value = 1.400000
    node.inputs[5].default_value = 0.000000
    node.inputs[6].default_value = 0.000000
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

    node = tree_nodes.new(type="ShaderNodeTexCoord")
    node.location = (-700, 620)
    node.from_instancer = False
    new_nodes["Texture Coordinate.002"] = node

    node = tree_nodes.new(type="ShaderNodeTexNoise")
    node.location = (-520, 620)
    node.noise_dimensions = "3D"
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 250.000000
    node.inputs[3].default_value = 2.000000
    node.inputs[4].default_value = 1.000000
    node.inputs[5].default_value = 0.500000
    new_nodes["Noise Texture.001"] = node

    node = tree_nodes.new(type="ShaderNodeMixShader")
    node.location = (660, 300)
    new_nodes["Mix Shader"] = node

    node = tree_nodes.new(type="ShaderNodeOutputMaterial")
    node.location = (860, 60)
    node.target = "ALL"
    new_nodes["Material Output"] = node

    # create links
    tree_links = material.node_tree.links
    tree_links.new(new_nodes["Attribute.001"].outputs[1], new_nodes["Separate XYZ"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ"].outputs[0], new_nodes["Combine XYZ"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ"].outputs[1], new_nodes["Combine XYZ"].inputs[1])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Combine XYZ"].inputs[2])
    tree_links.new(new_nodes["Combine XYZ"].outputs[0], new_nodes["Noise Texture"].inputs[0])
    tree_links.new(new_nodes["Noise Texture"].outputs[0], new_nodes["ColorRamp"].inputs[0])
    tree_links.new(new_nodes["Attribute"].outputs[2], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Voronoi Texture"].outputs[0], new_nodes["ColorRamp.002"].inputs[0])
    tree_links.new(new_nodes["Texture Coordinate"].outputs[3], new_nodes["Voronoi Texture"].inputs[0])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["ColorRamp.001"].inputs[0])
    tree_links.new(new_nodes["ColorRamp"].outputs[0], new_nodes["Math.001"].inputs[0])
    tree_links.new(new_nodes["ColorRamp.002"].outputs[0], new_nodes["Math.001"].inputs[1])
    tree_links.new(new_nodes["Noise Texture"].outputs[0], new_nodes["Math.002"].inputs[0])
    tree_links.new(new_nodes["ColorRamp.002"].outputs[0], new_nodes["Math.002"].inputs[1])
    tree_links.new(new_nodes["Principled BSDF.001"].outputs[0], new_nodes["Mix Shader"].inputs[1])
    tree_links.new(new_nodes["Attribute.004"].outputs[2], new_nodes["Map Range"].inputs[0])
    tree_links.new(new_nodes["ColorRamp.004"].outputs[0], new_nodes["Principled BSDF.001"].inputs[0])
    tree_links.new(new_nodes["Map Range"].outputs[0], new_nodes["Mix Shader"].inputs[0])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Bump"].inputs[2])
    tree_links.new(new_nodes["Bump.001"].outputs[0], new_nodes["Principled BSDF.001"].inputs[22])
    tree_links.new(new_nodes["Bump"].outputs[0], new_nodes["Principled BSDF.002"].inputs[22])
    tree_links.new(new_nodes["ColorRamp.001"].outputs[0], new_nodes["Principled BSDF.002"].inputs[0])
    tree_links.new(new_nodes["Principled BSDF.002"].outputs[0], new_nodes["Mix Shader"].inputs[2])
    tree_links.new(new_nodes["Math.004"].outputs[0], new_nodes["Math.003"].inputs[0])
    tree_links.new(new_nodes["Gradient Texture"].outputs[0], new_nodes["Math.004"].inputs[0])
    tree_links.new(new_nodes["Math.003"].outputs[0], new_nodes["Float Curve"].inputs[1])
    tree_links.new(new_nodes["Math.006"].outputs[0], new_nodes["Vector Math"].inputs[3])
    tree_links.new(new_nodes["Float Curve"].outputs[0], new_nodes["Math.005"].inputs[0])
    tree_links.new(new_nodes["Math.005"].outputs[0], new_nodes["Math.006"].inputs[0])
    tree_links.new(new_nodes["ColorRamp.003"].outputs[0], new_nodes["Math.006"].inputs[1])
    tree_links.new(new_nodes["Math.007"].outputs[0], new_nodes["Math.005"].inputs[1])
    tree_links.new(new_nodes["Attribute.002"].outputs[1], new_nodes["Gradient Texture"].inputs[0])
    tree_links.new(new_nodes["Attribute.003"].outputs[2], new_nodes["ColorRamp.003"].inputs[0])
    tree_links.new(new_nodes["Attribute.006"].outputs[2], new_nodes["Math.007"].inputs[0])
    tree_links.new(new_nodes["Vector Math"].outputs[0], new_nodes["Material Output"].inputs[2])
    tree_links.new(new_nodes["Texture Coordinate.001"].outputs[1], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["ColorRamp.007"].outputs[0], new_nodes["Principled BSDF.001"].inputs[7])
    tree_links.new(new_nodes["ColorRamp.006"].outputs[0], new_nodes["Principled BSDF.001"].inputs[9])
    tree_links.new(new_nodes["Texture Coordinate.002"].outputs[3], new_nodes["Noise Texture.001"].inputs[0])
    tree_links.new(new_nodes["Noise Texture.001"].outputs[0], new_nodes["ColorRamp.004"].inputs[0])
    tree_links.new(new_nodes["Noise Texture.001"].outputs[0], new_nodes["ColorRamp.007"].inputs[0])
    tree_links.new(new_nodes["Noise Texture.001"].outputs[0], new_nodes["ColorRamp.006"].inputs[0])
    tree_links.new(new_nodes["Noise Texture.001"].outputs[0], new_nodes["Bump.001"].inputs[2])
    tree_links.new(new_nodes["Mix Shader"].outputs[0], new_nodes["Material Output"].inputs[0])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False
    return new_nodes

def create_mat_pumpkin_point(material):
    # initialize variables
    new_nodes = {}
    tree_nodes = material.node_tree.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-480, 740)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-660, 320)
    node.operation = "LENGTH"
    node.inputs[1].default_value = (0.05000000074505806, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-1380, 740)
    node.operation = "SUBTRACT"
    node.inputs[1].default_value = (0.5, 0.5, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-840, 320)
    node.operation = "LENGTH"
    node.inputs[1].default_value = (0.05000000074505806, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-840, 740)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (-1560, 320)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = -0.800000
    node.inputs[2].default_value = 0.800000
    node.inputs[3].default_value = 0.000000
    node.inputs[4].default_value = 1.000000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-1560, -100)
    node.operation = "LENGTH"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-480, 320)
    node.operation = "LENGTH"
    node.inputs[1].default_value = (0.05000000074505806, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-300, 740)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (-1560, 740)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = -1.047200
    node.inputs[2].default_value = 1.047197
    node.inputs[3].default_value = 0.000000
    node.inputs[4].default_value = 1.000000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1560, 480)
    node.operation = "ARCTAN2"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-840, 200)
    node.operation = "SUBTRACT"
    node.inputs[1].default_value = (0.0, -0.25, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-1740, -100)
    node.operation = "ADD"
    node.inputs[1].default_value = (0.0, 0.0, -0.09000000357627869)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.006"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (-1380, 540)
    node.inputs[2].default_value = 0.000000
    new_nodes["Combine XYZ"] = node

    node = tree_nodes.new(type="ShaderNodeTexNoise")
    node.location = (-300, 580)
    node.noise_dimensions = "2D"
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 8.000000
    node.inputs[3].default_value = 1.618034
    node.inputs[4].default_value = 0.618034
    node.inputs[5].default_value = 0.166667
    new_nodes["Noise Texture"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-1740, 100)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = (1.0, 1.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.007"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (-1740, 240)
    new_nodes["Separate XYZ"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (-1200, 740)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = 0.030000
    node.inputs[2].default_value = 0.130000
    node.inputs[3].default_value = 1.000000
    node.inputs[4].default_value = 0.000000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range.002"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (-480, 580)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = 0.040000
    node.inputs[2].default_value = 0.250000
    node.inputs[3].default_value = 1.000000
    node.inputs[4].default_value = 0.000000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range.003"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-1020, 200)
    node.operation = "SUBTRACT"
    node.inputs[1].default_value = (0.15000000596046448, -0.20000000298023224, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.008"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (-660, 580)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = 0.040000
    node.inputs[2].default_value = 0.250000
    node.inputs[3].default_value = 1.000000
    node.inputs[4].default_value = 0.000000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range.004"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1560, 60)
    node.operation = "ARCTAN2"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-1200, 480)
    node.operation = "LENGTH"
    node.inputs[1].default_value = (0.05000000074505806, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.009"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-660, 740)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-1020, 320)
    node.operation = "LENGTH"
    node.inputs[1].default_value = (0.05000000074505806, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.010"] = node

    node = tree_nodes.new(type="ShaderNodeValToRGB")
    node.location = (-400, 960)
    node.color_ramp.color_mode = "RGB"
    node.color_ramp.interpolation = "EASE"
    node.color_ramp.elements.remove(node.color_ramp.elements[0])
    elem = node.color_ramp.elements[0]
    elem.position = 0.100000
    elem.color = (0.000000, 0.000000, 0.000000, 1.000000)
    elem = node.color_ramp.elements.new(0.534546)
    elem.color = (1.000000, 1.000000, 1.000000, 1.000000)
    new_nodes["ColorRamp"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1020, 740)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.006"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-1200, 360)
    node.operation = "SUBTRACT"
    node.inputs[1].default_value = (-0.15000000596046448, -0.20000000298023224, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.011"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-660, 200)
    node.operation = "SUBTRACT"
    node.inputs[1].default_value = (-0.20000000298023224, 0.07999999821186066, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.012"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (-1020, 580)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = 0.030000
    node.inputs[2].default_value = 0.130000
    node.inputs[3].default_value = 1.000000
    node.inputs[4].default_value = 0.000000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range.005"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (-840, 580)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = 0.030000
    node.inputs[2].default_value = 0.130000
    node.inputs[3].default_value = 1.000000
    node.inputs[4].default_value = 0.000000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range.006"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-480, 200)
    node.operation = "SUBTRACT"
    node.inputs[1].default_value = (0.20000000298023224, 0.07999999821186066, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.013"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-300, 1120)
    node.operation = "LESS_THAN"
    node.use_clamp = False
    node.inputs[1].default_value = 0.500000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.007"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-700, -700)
    node.operation = "PINGPONG"
    node.use_clamp = False
    node.inputs[1].default_value = 1.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.008"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-700, -860)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = 42.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.009"] = node

    node = tree_nodes.new(type="ShaderNodeTexGradient")
    node.location = (-700, -1020)
    node.gradient_type = "RADIAL"
    new_nodes["Gradient Texture"] = node

    node = tree_nodes.new(type="ShaderNodeFloatCurve")
    node.location = (-800, -380)
    node.mapping.use_clip = True
    node.mapping.clip_min_x = 0.000000
    node.mapping.clip_min_y = 0.000000
    node.mapping.clip_max_x = 1.000000
    node.mapping.clip_max_y = 1.000000
    node.mapping.extend = "EXTRAPOLATED"
    point = node.mapping.curves[0].points[0]
    point.location = (0.000000, 0.000000)
    point.handle_type = "AUTO"
    point = node.mapping.curves[0].points[1]
    point.location = (0.110000, 0.110000)
    point.handle_type = "AUTO"
    point = node.mapping.curves[0].points.new(0.500000, 0.210000)
    point.handle_type = "AUTO"
    point = node.mapping.curves[0].points.new(0.890000, 0.110000)
    point.handle_type = "AUTO"
    point = node.mapping.curves[0].points.new(1.000000, 0.000000)
    point.handle_type = "AUTO"
    node.mapping.update()
    node.inputs[0].default_value = 1.000000
    new_nodes["Float Curve"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-700, -220)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.010"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-700, -60)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = 2.382000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.011"] = node

    node = tree_nodes.new(type="ShaderNodeValToRGB")
    node.location = (-480, -60)
    node.color_ramp.color_mode = "RGB"
    node.color_ramp.interpolation = "EASE"
    node.color_ramp.elements.remove(node.color_ramp.elements[0])
    elem = node.color_ramp.elements[0]
    elem.position = 0.000000
    elem.color = (0.323955, 0.117949, 0.004471, 1.000000)
    elem = node.color_ramp.elements.new(0.185455)
    elem.color = (0.350000, 0.092400, 0.000000, 1.000000)
    elem = node.color_ramp.elements.new(0.923636)
    elem.color = (0.420000, 0.075961, 0.000000, 1.000000)
    new_nodes["ColorRamp.001"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (-480, -440)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 0.900000
    node.inputs[3].default_value = -0.200000
    node.inputs[4].default_value = 0.500000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range.007"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-480, -280)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.012"] = node

    node = tree_nodes.new(type="ShaderNodeTexGradient")
    node.location = (-1020, -860)
    node.gradient_type = "RADIAL"
    new_nodes["Gradient Texture.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1020, -700)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = 20.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.013"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1020, -540)
    node.operation = "PINGPONG"
    node.use_clamp = False
    node.inputs[1].default_value = 1.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.014"] = node

    node = tree_nodes.new(type="ShaderNodeFloatCurve")
    node.location = (-1120, -220)
    node.mapping.use_clip = True
    node.mapping.clip_min_x = 0.000000
    node.mapping.clip_min_y = 0.000000
    node.mapping.clip_max_x = 1.000000
    node.mapping.clip_max_y = 1.000000
    node.mapping.extend = "EXTRAPOLATED"
    point = node.mapping.curves[0].points[0]
    point.location = (0.000000, 0.000000)
    point.handle_type = "AUTO"
    point = node.mapping.curves[0].points[1]
    point.location = (0.110000, 0.110000)
    point.handle_type = "AUTO"
    point = node.mapping.curves[0].points.new(0.500000, 0.210000)
    point.handle_type = "AUTO"
    point = node.mapping.curves[0].points.new(0.890000, 0.110000)
    point.handle_type = "AUTO"
    point = node.mapping.curves[0].points.new(1.000000, 0.000000)
    point.handle_type = "AUTO"
    node.mapping.update()
    node.inputs[0].default_value = 1.000000
    new_nodes["Float Curve.001"] = node

    node = tree_nodes.new(type="ShaderNodeTexMusgrave")
    node.location = (-480, -700)
    node.musgrave_dimensions = "3D"
    node.musgrave_type = "FBM"
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 23.000000
    node.inputs[3].default_value = 3.000000
    node.inputs[4].default_value = 1.000000
    node.inputs[5].default_value = 3.000000
    node.inputs[6].default_value = 0.000000
    node.inputs[7].default_value = 1.000000
    new_nodes["Musgrave Texture"] = node

    node = tree_nodes.new(type="ShaderNodeTexCoord")
    node.location = (-1740, -300)
    node.from_instancer = False
    new_nodes["Texture Coordinate"] = node

    node = tree_nodes.new(type="ShaderNodeValToRGB")
    node.location = (-300, -280)
    node.color_ramp.color_mode = "RGB"
    node.color_ramp.interpolation = "EASE"
    node.color_ramp.elements.remove(node.color_ramp.elements[0])
    elem = node.color_ramp.elements[0]
    elem.position = 0.320000
    elem.color = (0.468672, 0.468672, 0.468672, 1.000000)
    elem = node.color_ramp.elements.new(0.910909)
    elem.color = (0.086398, 0.086398, 0.086398, 1.000000)
    new_nodes["ColorRamp.003"] = node

    node = tree_nodes.new(type="ShaderNodeEmission")
    node.location = (80, 240)
    node.inputs[0].default_value = (1.0, 0.5592027902603149, 0.33316874504089355, 1.0)
    node.inputs[1].default_value = 2.000000
    new_nodes["Emission"] = node

    node = tree_nodes.new(type="ShaderNodeBsdfDiffuse")
    node.location = (80, 120)
    node.inputs[0].default_value = (0.047191448509693146, 0.015317324548959732, 0.005014140624552965, 1.0)
    node.inputs[1].default_value = 0.000000
    new_nodes["Diffuse BSDF"] = node

    node = tree_nodes.new(type="ShaderNodeMixShader")
    node.location = (80, 380)
    node.inputs[0].default_value = 1.000000
    new_nodes["Mix Shader"] = node

    node = tree_nodes.new(type="ShaderNodeMixShader")
    node.location = (280, 240)
    new_nodes["Mix Shader.001"] = node

    node = tree_nodes.new(type="ShaderNodeOutputMaterial")
    node.location = (1200, 260)
    node.target = "ALL"
    new_nodes["Material Output"] = node

    node = tree_nodes.new(type="ShaderNodeValToRGB")
    node.location = (660, 80)
    node.color_ramp.color_mode = "RGB"
    node.color_ramp.interpolation = "EASE"
    node.color_ramp.elements.remove(node.color_ramp.elements[0])
    elem = node.color_ramp.elements[0]
    elem.position = 0.950000
    elem.color = (0.000000, 0.000000, 0.000000, 1.000000)
    elem = node.color_ramp.elements.new(0.960000)
    elem.color = (1.000000, 1.000000, 1.000000, 1.000000)
    new_nodes["ColorRamp.002"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (440, 100)
    new_nodes["Separate XYZ.001"] = node

    node = tree_nodes.new(type="ShaderNodeBsdfDiffuse")
    node.location = (1000, 120)
    node.inputs[0].default_value = (0.02718264050781727, 0.02510812133550644, 0.006872729863971472, 1.0)
    node.inputs[1].default_value = 0.000000
    new_nodes["Diffuse BSDF.001"] = node

    node = tree_nodes.new(type="ShaderNodeMixShader")
    node.location = (980, 260)
    new_nodes["Mix Shader.002"] = node

    node = tree_nodes.new(type="ShaderNodeBsdfPrincipled")
    node.location = (-20, -60)
    node.distribution = "GGX"
    node.subsurface_method = "RANDOM_WALK"
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

    # create links
    tree_links = material.node_tree.links
    tree_links.new(new_nodes["Vector Math.006"].outputs[0], new_nodes["Separate XYZ"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ"].outputs[0], new_nodes["Math.003"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ"].outputs[1], new_nodes["Math.003"].inputs[1])
    tree_links.new(new_nodes["Vector Math.007"].outputs[0], new_nodes["Vector Math.003"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ"].outputs[2], new_nodes["Math.004"].inputs[0])
    tree_links.new(new_nodes["Vector Math.003"].outputs[1], new_nodes["Math.004"].inputs[1])
    tree_links.new(new_nodes["Math.004"].outputs[0], new_nodes["Map Range"].inputs[0])
    tree_links.new(new_nodes["Math.003"].outputs[0], new_nodes["Map Range.001"].inputs[0])
    tree_links.new(new_nodes["Map Range.001"].outputs[0], new_nodes["Combine XYZ"].inputs[0])
    tree_links.new(new_nodes["Map Range"].outputs[0], new_nodes["Combine XYZ"].inputs[1])
    tree_links.new(new_nodes["Texture Coordinate"].outputs[3], new_nodes["Vector Math.006"].inputs[0])
    tree_links.new(new_nodes["Vector Math.006"].outputs[0], new_nodes["Vector Math.007"].inputs[0])
    tree_links.new(new_nodes["Vector Math.013"].outputs[0], new_nodes["Vector Math.004"].inputs[0])
    tree_links.new(new_nodes["Vector Math.004"].outputs[1], new_nodes["Map Range.003"].inputs[0])
    tree_links.new(new_nodes["Noise Texture"].outputs[0], new_nodes["Math.002"].inputs[1])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["ColorRamp"].inputs[0])
    tree_links.new(new_nodes["Combine XYZ"].outputs[0], new_nodes["Vector Math.001"].inputs[0])
    tree_links.new(new_nodes["Vector Math.012"].outputs[0], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Vector Math"].outputs[1], new_nodes["Map Range.004"].inputs[0])
    tree_links.new(new_nodes["Math.005"].outputs[0], new_nodes["Math"].inputs[1])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Math.002"].inputs[0])
    tree_links.new(new_nodes["Map Range.003"].outputs[0], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Vector Math.001"].outputs[0], new_nodes["Vector Math.013"].inputs[0])
    tree_links.new(new_nodes["Vector Math.001"].outputs[0], new_nodes["Vector Math.012"].inputs[0])
    tree_links.new(new_nodes["Vector Math.005"].outputs[0], new_nodes["Vector Math.002"].inputs[0])
    tree_links.new(new_nodes["Vector Math.002"].outputs[1], new_nodes["Map Range.006"].inputs[0])
    tree_links.new(new_nodes["Vector Math.001"].outputs[0], new_nodes["Vector Math.005"].inputs[0])
    tree_links.new(new_nodes["Map Range.004"].outputs[0], new_nodes["Math.005"].inputs[0])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Math.005"].inputs[1])
    tree_links.new(new_nodes["Vector Math.011"].outputs[0], new_nodes["Vector Math.009"].inputs[0])
    tree_links.new(new_nodes["Vector Math.009"].outputs[1], new_nodes["Map Range.002"].inputs[0])
    tree_links.new(new_nodes["Vector Math.001"].outputs[0], new_nodes["Vector Math.011"].inputs[0])
    tree_links.new(new_nodes["Map Range.006"].outputs[0], new_nodes["Math.001"].inputs[0])
    tree_links.new(new_nodes["Math.006"].outputs[0], new_nodes["Math.001"].inputs[1])
    tree_links.new(new_nodes["Vector Math.008"].outputs[0], new_nodes["Vector Math.010"].inputs[0])
    tree_links.new(new_nodes["Vector Math.010"].outputs[1], new_nodes["Map Range.005"].inputs[0])
    tree_links.new(new_nodes["Vector Math.001"].outputs[0], new_nodes["Vector Math.008"].inputs[0])
    tree_links.new(new_nodes["Map Range.002"].outputs[0], new_nodes["Math.006"].inputs[0])
    tree_links.new(new_nodes["Map Range.005"].outputs[0], new_nodes["Math.006"].inputs[1])
    tree_links.new(new_nodes["Combine XYZ"].outputs[0], new_nodes["Noise Texture"].inputs[0])
    tree_links.new(new_nodes["ColorRamp"].outputs[0], new_nodes["Math.007"].inputs[0])
    tree_links.new(new_nodes["Math.007"].outputs[0], new_nodes["Mix Shader.001"].inputs[0])
    tree_links.new(new_nodes["Principled BSDF"].outputs[0], new_nodes["Mix Shader.001"].inputs[2])
    tree_links.new(new_nodes["Emission"].outputs[0], new_nodes["Mix Shader"].inputs[1])
    tree_links.new(new_nodes["Mix Shader"].outputs[0], new_nodes["Mix Shader.001"].inputs[1])
    tree_links.new(new_nodes["Diffuse BSDF"].outputs[0], new_nodes["Mix Shader"].inputs[2])
    tree_links.new(new_nodes["Math.009"].outputs[0], new_nodes["Math.008"].inputs[0])
    tree_links.new(new_nodes["Gradient Texture"].outputs[1], new_nodes["Math.009"].inputs[0])
    tree_links.new(new_nodes["Math.008"].outputs[0], new_nodes["Float Curve"].inputs[1])
    tree_links.new(new_nodes["Math.013"].outputs[0], new_nodes["Math.014"].inputs[0])
    tree_links.new(new_nodes["Gradient Texture.001"].outputs[1], new_nodes["Math.013"].inputs[0])
    tree_links.new(new_nodes["Math.014"].outputs[0], new_nodes["Float Curve.001"].inputs[1])
    tree_links.new(new_nodes["Float Curve.001"].outputs[0], new_nodes["Math.010"].inputs[0])
    tree_links.new(new_nodes["Float Curve"].outputs[0], new_nodes["Math.010"].inputs[1])
    tree_links.new(new_nodes["Math.010"].outputs[0], new_nodes["Math.011"].inputs[0])
    tree_links.new(new_nodes["Math.011"].outputs[0], new_nodes["Math.012"].inputs[0])
    tree_links.new(new_nodes["Math.012"].outputs[0], new_nodes["ColorRamp.001"].inputs[0])
    tree_links.new(new_nodes["Musgrave Texture"].outputs[0], new_nodes["Map Range.007"].inputs[0])
    tree_links.new(new_nodes["Map Range.007"].outputs[0], new_nodes["Math.012"].inputs[1])
    tree_links.new(new_nodes["ColorRamp.001"].outputs[0], new_nodes["Principled BSDF"].inputs[0])
    tree_links.new(new_nodes["Texture Coordinate"].outputs[3], new_nodes["Gradient Texture"].inputs[0])
    tree_links.new(new_nodes["Texture Coordinate"].outputs[3], new_nodes["Musgrave Texture"].inputs[0])
    tree_links.new(new_nodes["Texture Coordinate"].outputs[3], new_nodes["Gradient Texture.001"].inputs[0])
    tree_links.new(new_nodes["Mix Shader.001"].outputs[0], new_nodes["Mix Shader.002"].inputs[1])
    tree_links.new(new_nodes["ColorRamp.002"].outputs[0], new_nodes["Mix Shader.002"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[2], new_nodes["ColorRamp.002"].inputs[0])
    tree_links.new(new_nodes["Texture Coordinate"].outputs[1], new_nodes["Separate XYZ.001"].inputs[0])
    tree_links.new(new_nodes["Diffuse BSDF.001"].outputs[0], new_nodes["Mix Shader.002"].inputs[2])
    tree_links.new(new_nodes["Math.012"].outputs[0], new_nodes["ColorRamp.003"].inputs[0])
    tree_links.new(new_nodes["ColorRamp.003"].outputs[0], new_nodes["Principled BSDF"].inputs[9])
    tree_links.new(new_nodes["Mix Shader.002"].outputs[0], new_nodes["Material Output"].inputs[0])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_nodes

def create_geo_ng_pumpkin():
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=PUMPKIN_GEO_NG_NAME, type='GeometryNodeTree')
    new_node_group.inputs.new(type='NodeSocketInt', name="Detail")
    new_node_group.inputs.new(type='NodeSocketBool', name="Make Inside")
    new_node_group.inputs.new(type='NodeSocketVector', name="Scale")
    new_node_group.inputs.new(type='NodeSocketMaterial', name="Skin Material")
    new_node_group.inputs.new(type='NodeSocketMaterial', name="Stem Material")
    new_node_group.inputs.new(type='NodeSocketMaterial', name="Point Material")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Stem Top Radius")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Stem Height")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Stem Bottom Radius")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Stem Yaw")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Stem Pitch")
    new_node_group.inputs.new(type='NodeSocketFloatDistance', name="Top Nub Radius")
    new_node_group.inputs.new(type='NodeSocketFloatDistance', name="Bottom Nub Radius")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Body Top Offset")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Body Top Outer Offset")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Body Outer Offset")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Body Bottom Outer Offset")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Body Bottom Offset")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Indent Factor")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Wall Depth")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Height Offset")
    new_node_group.outputs.new(type='NodeSocketGeometry', name="Stem Geometry")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Stem Height")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Stem Height Pct")
    new_node_group.outputs.new(type='NodeSocketVector', name="Stem Radial Vector")
    new_node_group.outputs.new(type='NodeSocketGeometry', name="Body Geometry")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Pumpkin Indent")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Top/Bottom Nub")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Body Height Pct")
    new_node_group.outputs.new(type='NodeSocketVector', name="Body Radial Vector")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Body Radial Pct")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Body Height")
    new_node_group.outputs.new(type='NodeSocketGeometry', name="Inside Geometry")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Inside Pumpkin")
    tree_nodes = new_node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="GeometryNodeMeshCircle")
    node.location = (780, 180)
    node.fill_type = "TRIANGLE_FAN"
    node.inputs[0].default_value = 50
    node.inputs[1].default_value = 1.350000
    new_nodes["Mesh Circle"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (600, 40)
    new_nodes["Position"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (780, 40)
    node.operation = "SCALE"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (1140, -100)
    new_nodes["Position.001"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (1320, -100)
    node.operation = "SCALE"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    new_nodes["Vector Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1140, -240)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[0].default_value = -0.500000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (1320, -240)
    node.inputs[0].default_value = 0.000000
    node.inputs[1].default_value = 0.000000
    new_nodes["Combine XYZ"] = node

    node = tree_nodes.new(type="GeometryNodeFlipFaces")
    node.location = (1320, 40)
    new_nodes["Flip Faces"] = node

    node = tree_nodes.new(type="GeometryNodeSetPosition")
    node.location = (1140, 200)
    new_nodes["Set Position"] = node

    node = tree_nodes.new(type="GeometryNodeSetPosition")
    node.location = (1680, 60)
    new_nodes["Set Position.001"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.label = "Capture bottom"
    node.location = (1500, 40)
    node.data_type = "FLOAT"
    node.domain = "FACE"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = 1.000000
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.label = "Capture top"
    node.location = (960, 180)
    node.data_type = "FLOAT"
    node.domain = "FACE"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = 1.000000
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute.001"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (2080, -620)
    node.operation = "SCALE"
    node.inputs[0].default_value = (0.0, 0.0, 0.07000000029802322)
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    new_nodes["Vector Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1900, -620)
    node.operation = "COMPARE"
    node.use_clamp = False
    node.inputs[1].default_value = 0.062832
    node.inputs[2].default_value = 0.050000
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (2260, -680)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (2080, -420)
    node.operation = "SCALE"
    node.inputs[0].default_value = (0.0, 0.0, -0.07000000029802322)
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    new_nodes["Vector Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (2260, -420)
    node.operation = "ADD"
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeVectorRotate")
    node.location = (2440, -420)
    node.invert = False
    node.rotation_type = "EULER_XYZ"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 1.0)
    node.inputs[3].default_value = 0.000000
    new_nodes["Vector Rotate"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1900, -420)
    node.operation = "COMPARE"
    node.use_clamp = False
    node.inputs[1].default_value = 0.062832
    node.inputs[2].default_value = 0.001000
    new_nodes["Math.003"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.label = "Capture indent"
    node.location = (2620, -340)
    node.data_type = "FLOAT"
    node.domain = "POINT"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute.002"] = node

    node = tree_nodes.new(type="GeometryNodeSetPosition")
    node.location = (2800, -320)
    node.inputs[3].default_value = (0.0, 0.0, 0.0)
    new_nodes["Set Position.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1360, -620)
    node.operation = "LESS_THAN"
    node.use_clamp = False
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 0.080000
    new_nodes["Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1180, -620)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[1].default_value = -0.125664
    node.inputs[2].default_value = 0.080000
    new_nodes["Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1720, -620)
    node.operation = "MODULO"
    node.use_clamp = False
    node.inputs[1].default_value = 0.628319
    node.inputs[2].default_value = 0.080000
    new_nodes["Math.006"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1540, -620)
    node.operation = "MULTIPLY_ADD"
    node.use_clamp = False
    node.inputs[1].default_value = 3.141593
    new_nodes["Math.007"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (640, -620)
    new_nodes["Position.002"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (820, -620)
    new_nodes["Separate XYZ"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1000, -620)
    node.operation = "ARCTAN2"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.008"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1360, -420)
    node.operation = "LESS_THAN"
    node.use_clamp = False
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 0.080000
    new_nodes["Math.009"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1540, -420)
    node.operation = "MULTIPLY_ADD"
    node.use_clamp = False
    node.inputs[1].default_value = 3.141593
    new_nodes["Math.010"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1720, -420)
    node.operation = "MODULO"
    node.use_clamp = False
    node.inputs[1].default_value = 0.628319
    node.inputs[2].default_value = 0.080000
    new_nodes["Math.011"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (600, -100)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[1].default_value = 0.500000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.012"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (780, -100)
    node.inputs[0].default_value = 0.000000
    node.inputs[1].default_value = 0.000000
    new_nodes["Combine XYZ.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (2620, -880)
    node.operation = "DIVIDE"
    node.use_clamp = False
    node.inputs[2].default_value = 0.080000
    new_nodes["Math.013"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (2440, -880)
    node.operation = "PINGPONG"
    node.use_clamp = False
    node.inputs[2].default_value = 0.080000
    new_nodes["Math.014"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (2260, -1040)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = 3.141593
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.015"] = node

    node = tree_nodes.new(type="ShaderNodeValue")
    node.location = (2080, -1040)
    node.outputs[0].default_value = 0.100000
    new_nodes["Value"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (3080, -880)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.080000
    new_nodes["Math.016"] = node

    node = tree_nodes.new(type="ShaderNodeFloatCurve")
    node.location = (2800, -880)
    node.mapping.use_clip = True
    node.mapping.clip_min_x = 0.000000
    node.mapping.clip_min_y = 0.000000
    node.mapping.clip_max_x = 1.000000
    node.mapping.clip_max_y = 1.000000
    node.mapping.extend = "EXTRAPOLATED"
    point = node.mapping.curves[0].points[0]
    point.location = (0.000000, 0.000000)
    point.handle_type = "AUTO"
    point = node.mapping.curves[0].points[1]
    point.location = (0.075482, 0.192500)
    point.handle_type = "AUTO"
    point = node.mapping.curves[0].points.new(0.541825, 0.445000)
    point.handle_type = "AUTO"
    point = node.mapping.curves[0].points.new(1.000000, 0.510000)
    point.handle_type = "AUTO"
    node.mapping.update()
    node.inputs[0].default_value = 1.000000
    new_nodes["Float Curve"] = node

    node = tree_nodes.new(type="GeometryNodeInputNormal")
    node.location = (3260, -800)
    new_nodes["Normal"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (3440, -800)
    node.operation = "SCALE"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    new_nodes["Vector Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (3260, -880)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.017"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Subtract bottom nub"
    node.location = (2120, -1740)
    node.operation = "SUBTRACT"
    node.use_clamp = True
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.018"] = node

    node = tree_nodes.new(type="ShaderNodeFloatCurve")
    node.location = (2300, -1740)
    node.mapping.use_clip = True
    node.mapping.clip_min_x = 0.000000
    node.mapping.clip_min_y = 0.000000
    node.mapping.clip_max_x = 1.000000
    node.mapping.clip_max_y = 1.000000
    node.mapping.extend = "EXTRAPOLATED"
    point = node.mapping.curves[0].points[0]
    point.location = (0.000000, 0.000000)
    point.handle_type = "AUTO"
    point = node.mapping.curves[0].points[1]
    point.location = (0.055133, 0.022500)
    point.handle_type = "AUTO"
    point = node.mapping.curves[0].points.new(0.275665, 0.780000)
    point.handle_type = "AUTO"
    point = node.mapping.curves[0].points.new(1.000000, 1.000000)
    point.handle_type = "AUTO"
    node.mapping.update()
    node.inputs[0].default_value = 1.000000
    new_nodes["Float Curve.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (2580, -1740)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.019"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (1540, -1400)
    new_nodes["Position.003"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (1720, -1400)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = (1.0, 1.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.006"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (1900, -1400)
    node.operation = "LENGTH"
    node.inputs[1].default_value = (1.0, 1.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.007"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Subtract top stem"
    node.location = (2080, -1400)
    node.operation = "SUBTRACT"
    node.use_clamp = True
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.020"] = node

    node = tree_nodes.new(type="ShaderNodeFloatCurve")
    node.location = (2300, -1400)
    node.mapping.use_clip = True
    node.mapping.clip_min_x = 0.000000
    node.mapping.clip_min_y = 0.000000
    node.mapping.clip_max_x = 1.000000
    node.mapping.clip_max_y = 1.000000
    node.mapping.extend = "EXTRAPOLATED"
    point = node.mapping.curves[0].points[0]
    point.location = (0.000000, 0.000000)
    point.handle_type = "AUTO"
    point = node.mapping.curves[0].points[1]
    point.location = (0.230038, 0.717500)
    point.handle_type = "AUTO"
    point = node.mapping.curves[0].points.new(0.633080, 1.000000)
    point.handle_type = "AUTO"
    point = node.mapping.curves[0].points.new(1.000000, 1.000000)
    point.handle_type = "AUTO"
    node.mapping.update()
    node.inputs[0].default_value = 1.000000
    new_nodes["Float Curve.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (2580, -1400)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.021"] = node

    node = tree_nodes.new(type="FunctionNodeBooleanMath")
    node.location = (2260, -1220)
    node.operation = "NOT"
    node.inputs[1].default_value = False
    new_nodes["Boolean Math"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (2080, -1220)
    node.operation = "GREATER_THAN"
    node.use_clamp = False
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.022"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (1900, -1220)
    new_nodes["Separate XYZ.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (2760, -1400)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.023"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (2260, -880)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[1].default_value = -0.125664
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.024"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (2080, -880)
    node.operation = "ARCTAN2"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.025"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (1900, -880)
    new_nodes["Separate XYZ.002"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (1720, -880)
    new_nodes["Position.004"] = node

    node = tree_nodes.new(type="GeometryNodeMeshCircle")
    node.location = (1140, 40)
    node.fill_type = "TRIANGLE_FAN"
    node.inputs[0].default_value = 50
    node.inputs[1].default_value = 1.000000
    new_nodes["Mesh Circle.001"] = node

    node = tree_nodes.new(type="GeometryNodeJoinGeometry")
    node.location = (1880, 40)
    new_nodes["Join Geometry"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1880, -60)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.026"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.label = "Capture top/bottom +-"
    node.location = (2060, 0)
    node.data_type = "FLOAT"
    node.domain = "FACE"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute.003"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-880, -860)
    node.operation = "COMPARE"
    node.use_clamp = False
    node.inputs[1].default_value = 0.500000
    node.inputs[2].default_value = 0.010000
    new_nodes["Math.027"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-700, -860)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.100000
    new_nodes["Math.028"] = node

    node = tree_nodes.new(type="GeometryNodeSetPosition")
    node.location = (420, 220)
    new_nodes["Set Position.003"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (-300, 100)
    node.inputs[1].default_value = -0.500000
    node.inputs[2].default_value = 0.000000
    new_nodes["Combine XYZ.002"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (-300, 220)
    node.inputs[1].default_value = -0.500000
    node.inputs[2].default_value = 0.000000
    new_nodes["Combine XYZ.003"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-700, -520)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.100000
    new_nodes["Math.029"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-880, -500)
    node.operation = "COMPARE"
    node.use_clamp = False
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 0.010000
    new_nodes["Math.030"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-880, -320)
    node.operation = "COMPARE"
    node.use_clamp = False
    node.inputs[1].default_value = -0.343000
    node.inputs[2].default_value = 0.010000
    new_nodes["Math.031"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-700, -680)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.100000
    new_nodes["Math.032"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-700, -320)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.100000
    new_nodes["Math.033"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-700, -140)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.100000
    new_nodes["Math.034"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-300, -140)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.035"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-480, -140)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.036"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-120, -140)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.037"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (60, -140)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.038"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-880, -680)
    node.operation = "COMPARE"
    node.use_clamp = False
    node.inputs[1].default_value = 0.343000
    node.inputs[2].default_value = 0.010000
    new_nodes["Math.039"] = node

    node = tree_nodes.new(type="GeometryNodeCurveSetHandles")
    node.location = (240, 220)
    node.handle_type = "AUTO"
    node.mode = {"LEFT", "RIGHT"}
    new_nodes["Set Handle Type"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (-1240, -140)
    new_nodes["Position.005"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (-1060, -140)
    new_nodes["Separate XYZ.003"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-880, -140)
    node.operation = "COMPARE"
    node.use_clamp = False
    node.inputs[1].default_value = -0.500000
    node.inputs[2].default_value = 0.010000
    new_nodes["Math.040"] = node

    node = tree_nodes.new(type="GeometryNodeSubdivideCurve")
    node.location = (60, 220)
    node.inputs[1].default_value = 3
    new_nodes["Subdivide Curve"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (240, -140)
    node.operation = "MULTIPLY"
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.008"] = node

    node = tree_nodes.new(type="GeometryNodeInputNormal")
    node.location = (60, -300)
    new_nodes["Normal.001"] = node

    node = tree_nodes.new(type="GeometryNodeCurvePrimitiveBezierSegment")
    node.location = (-120, 220)
    node.mode = "POSITION"
    node.inputs[3].default_value = (0.7071070075035095, 0.5, 0.0)
    node.inputs[4].default_value = (0.0, 0.5, 0.0)
    new_nodes["Bezier Segment"] = node

    node = tree_nodes.new(type="GeometryNodeCurveToMesh")
    node.location = (600, 380)
    node.inputs[2].default_value = False
    new_nodes["Curve to Mesh"] = node

    node = tree_nodes.new(type="GeometryNodeCurvePrimitiveCircle")
    node.location = (420, 380)
    node.mode = "RADIUS"
    node.inputs[0].default_value = 50
    node.inputs[1].default_value = (-1.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 1.0, 0.0)
    node.inputs[3].default_value = (1.0, 0.0, 0.0)
    new_nodes["Curve Circle"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (-680, 420)
    new_nodes["Position.006"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (-500, 420)
    new_nodes["Separate XYZ.004"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-320, 420)
    node.operation = "ABSOLUTE"
    node.use_clamp = False
    node.inputs[1].default_value = -0.500000
    node.inputs[2].default_value = 0.010000
    new_nodes["Math.041"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-140, 420)
    node.operation = "LESS_THAN"
    node.use_clamp = False
    node.inputs[1].default_value = 0.490000
    node.inputs[2].default_value = 0.010000
    new_nodes["Math.042"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (-920, 380)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = 1.000000
    node.inputs[2].default_value = 6.000000
    node.inputs[3].default_value = 1.000000
    node.inputs[4].default_value = 6.000000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range"] = node

    node = tree_nodes.new(type="GeometryNodeSubdivisionSurface")
    node.location = (3440, -540)
    node.boundary_smooth = "ALL"
    node.uv_smooth = "PRESERVE_BOUNDARIES"
    node.inputs[2].default_value = 0.000000
    new_nodes["Subdivision Surface"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (3260, -540)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = 6.000000
    node.inputs[2].default_value = 20.000000
    node.inputs[3].default_value = 0.000000
    node.inputs[4].default_value = 14.000000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range.001"] = node

    node = tree_nodes.new(type="GeometryNodeMergeByDistance")
    node.location = (2240, -80)
    node.inputs[2].default_value = 0.001000
    new_nodes["Merge by Distance"] = node

    node = tree_nodes.new(type="GeometryNodeSetMaterial")
    node.location = (2980, -200)
    new_nodes["Set Material"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (3980, -1260)
    node.operation = "SCALE"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    new_nodes["Vector Math.009"] = node

    node = tree_nodes.new(type="GeometryNodeInputNormal")
    node.location = (3800, -1260)
    new_nodes["Normal.002"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (4360, -1880)
    new_nodes["Position.007"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (4540, -1880)
    new_nodes["Separate XYZ.005"] = node

    node = tree_nodes.new(type="GeometryNodeAttributeStatistic")
    node.location = (4720, -1660)
    node.data_type = "FLOAT"
    node.domain = "POINT"
    new_nodes["Attribute Statistic"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (4900, -1540)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[3].default_value = 0.000000
    node.inputs[4].default_value = 1.000000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range.002"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (4720, -1540)
    new_nodes["Separate XYZ.006"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (4540, -1540)
    new_nodes["Position.008"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (4900, -720)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = 0.000000
    node.inputs[3].default_value = 0.000000
    node.inputs[4].default_value = 1.000000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range.003"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (4720, -720)
    node.operation = "LENGTH"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.010"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (4180, -920)
    new_nodes["Position.009"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (4360, -920)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = (1.0, 1.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.011"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (4540, -920)
    node.operation = "LENGTH"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.012"] = node

    node = tree_nodes.new(type="GeometryNodeAttributeStatistic")
    node.location = (4720, -920)
    node.data_type = "FLOAT"
    node.domain = "POINT"
    new_nodes["Attribute Statistic.001"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (4540, -720)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = (1.0, 1.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.013"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (4360, -720)
    new_nodes["Position.010"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (2800, 480)
    node.inputs[2].default_value = 0.000000
    new_nodes["Combine XYZ.004"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (2260, 540)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = 1.200000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.043"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (2620, 480)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = -1.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.044"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (2440, 480)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.045"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (2620, 320)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = -1.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.046"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (2800, 140)
    node.inputs[0].default_value = -0.030000
    node.inputs[2].default_value = 0.000000
    new_nodes["Combine XYZ.005"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (2620, 140)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = 0.833333
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.047"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (2980, 480)
    node.operation = "ADD"
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.014"] = node

    node = tree_nodes.new(type="GeometryNodeCurveToMesh")
    node.location = (3540, 400)
    node.inputs[2].default_value = False
    new_nodes["Curve to Mesh.001"] = node

    node = tree_nodes.new(type="GeometryNodeFlipFaces")
    node.location = (3540, 260)
    new_nodes["Flip Faces.001"] = node

    node = tree_nodes.new(type="GeometryNodeCurvePrimitiveCircle")
    node.location = (3360, 400)
    node.mode = "RADIUS"
    node.inputs[0].default_value = 5
    node.inputs[1].default_value = (-1.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 1.0, 0.0)
    node.inputs[3].default_value = (1.0, 0.0, 0.0)
    new_nodes["Curve Circle.001"] = node

    node = tree_nodes.new(type="GeometryNodeCurvePrimitiveBezierSegment")
    node.location = (3180, 400)
    node.mode = "POSITION"
    node.inputs[0].default_value = 8
    node.inputs[3].default_value = (0.03999999910593033, -0.009999999776482582, 0.0)
    node.inputs[4].default_value = (0.0, 0.0, 0.0)
    new_nodes["Bezier Segment.001"] = node

    node = tree_nodes.new(type="GeometryNodeMeshCircle")
    node.location = (3360, 140)
    node.fill_type = "TRIANGLE_FAN"
    node.inputs[0].default_value = 5
    new_nodes["Mesh Circle.002"] = node

    node = tree_nodes.new(type="GeometryNodeSetPosition")
    node.location = (3540, 140)
    new_nodes["Set Position.004"] = node

    node = tree_nodes.new(type="GeometryNodeMergeByDistance")
    node.location = (3900, 400)
    node.inputs[2].default_value = 0.000100
    new_nodes["Merge by Distance.001"] = node

    node = tree_nodes.new(type="GeometryNodeSetPosition")
    node.location = (4080, 400)
    new_nodes["Set Position.005"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (3720, 260)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[1].default_value = -0.007000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.048"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (3900, 260)
    node.inputs[0].default_value = 0.000000
    node.inputs[1].default_value = 0.000000
    new_nodes["Combine XYZ.006"] = node

    node = tree_nodes.new(type="GeometryNodeJoinGeometry")
    node.location = (3720, 400)
    new_nodes["Join Geometry.001"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (3360, -20)
    node.inputs[0].default_value = 0.000000
    node.inputs[1].default_value = 0.000000
    new_nodes["Combine XYZ.007"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (4260, 200)
    new_nodes["Position.011"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (4440, 200)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = (1.0, 1.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.015"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (4620, 200)
    node.operation = "NORMALIZE"
    node.inputs[1].default_value = (1.0, 1.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.016"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (4440, 0)
    new_nodes["Position.012"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (4620, 0)
    new_nodes["Separate XYZ.007"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (4800, 0)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[3].default_value = 0.000000
    node.inputs[4].default_value = 1.000000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range.004"] = node

    node = tree_nodes.new(type="GeometryNodeAttributeStatistic")
    node.location = (4620, -120)
    node.data_type = "FLOAT"
    node.domain = "POINT"
    new_nodes["Attribute Statistic.002"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (4440, -340)
    new_nodes["Separate XYZ.008"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (4260, -340)
    new_nodes["Position.013"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.label = "Capture stem radial vec"
    node.location = (4800, 200)
    node.data_type = "FLOAT_VECTOR"
    node.domain = "POINT"
    node.inputs[2].default_value = 0.000000
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute.004"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.label = "Capture stem height pct"
    node.location = (5000, 160)
    node.data_type = "FLOAT"
    node.domain = "POINT"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute.005"] = node

    node = tree_nodes.new(type="GeometryNodeSetPosition")
    node.location = (5960, -40)
    node.inputs[3].default_value = (0.0, 0.0, 0.0)
    new_nodes["Set Position.006"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (5600, -120)
    new_nodes["Position.014"] = node

    node = tree_nodes.new(type="GeometryNodeSetMaterial")
    node.location = (6140, 80)
    new_nodes["Set Material.001"] = node

    node = tree_nodes.new(type="ShaderNodeVectorRotate")
    node.location = (5780, -120)
    node.invert = False
    node.rotation_type = "EULER_XYZ"
    node.inputs[2].default_value = (0.0, 0.0, 1.0)
    node.inputs[3].default_value = 0.000000
    new_nodes["Vector Rotate.001"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (5600, -200)
    node.inputs[0].default_value = 0.000000
    new_nodes["Combine XYZ.008"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (5420, -380)
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 0.000000
    new_nodes["Combine XYZ.009"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (5240, -380)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.049"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (5420, -200)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = -0.250000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.050"] = node

    node = tree_nodes.new(type="ShaderNodeVectorRotate")
    node.location = (5600, -380)
    node.invert = False
    node.rotation_type = "EULER_XYZ"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 1.0)
    node.inputs[3].default_value = 0.000000
    new_nodes["Vector Rotate.002"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (5420, -520)
    node.inputs[0].default_value = 0.000000
    node.inputs[1].default_value = 0.000000
    new_nodes["Combine XYZ.010"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (5280, -1440)
    new_nodes["Position.015"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (5460, -1440)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = (1.0, 1.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.017"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (5640, -1440)
    node.operation = "NORMALIZE"
    node.inputs[1].default_value = (1.0, 1.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.018"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.label = "Capture body radial vec"
    node.location = (5820, -1440)
    node.data_type = "FLOAT_VECTOR"
    node.domain = "POINT"
    node.inputs[2].default_value = 0.000000
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute.006"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.label = "Capture body height pct"
    node.location = (5080, -1340)
    node.data_type = "FLOAT"
    node.domain = "POINT"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute.007"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.label = "Capture body radial pct"
    node.location = (5260, -1200)
    node.data_type = "FLOAT"
    node.domain = "POINT"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute.008"] = node

    node = tree_nodes.new(type="GeometryNodeSetPosition")
    node.location = (3620, -540)
    new_nodes["Set Position.007"] = node

    node = tree_nodes.new(type="GeometryNodeSetPosition")
    node.location = (4160, -1120)
    new_nodes["Set Position.008"] = node

    node = tree_nodes.new(type="GeometryNodeSetPosition")
    node.location = (7060, -1280)
    new_nodes["Set Position.009"] = node

    node = tree_nodes.new(type="GeometryNodeSetPosition")
    node.location = (7060, -1120)
    new_nodes["Set Position.010"] = node

    node = tree_nodes.new(type="GeometryNodeSetPosition")
    node.location = (7060, -960)
    new_nodes["Set Position.011"] = node

    node = tree_nodes.new(type="GeometryNodeSetPosition")
    node.location = (7300, -1140)
    node.inputs[3].default_value = (0.0, 0.0, 0.0)
    new_nodes["Set Position.013"] = node

    node = tree_nodes.new(type="GeometryNodeSetPosition")
    node.location = (7300, -920)
    node.inputs[3].default_value = (0.0, 0.0, 0.0)
    new_nodes["Set Position.014"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (7060, -1500)
    node.operation = "MULTIPLY"
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 0.500000
    new_nodes["Vector Math.019"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.location = (7480, -1360)
    node.data_type = "FLOAT"
    node.domain = "POINT"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = 1.000000
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute.009"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (5700, -1160)
    new_nodes["Position.017"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (5880, -1160)
    new_nodes["Separate XYZ.009"] = node

    node = tree_nodes.new(type="GeometryNodeAttributeStatistic")
    node.location = (6060, -940)
    node.data_type = "FLOAT"
    node.domain = "POINT"
    new_nodes["Attribute Statistic.003"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (6240, -940)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.000000
    new_nodes["Math.051"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (6420, -940)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.052"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (6600, -940)
    node.inputs[0].default_value = 0.000000
    node.inputs[1].default_value = 0.000000
    new_nodes["Combine XYZ.011"] = node

    node = tree_nodes.new(type="GeometryNodeFlipFaces")
    node.location = (3620, -1120)
    new_nodes["Flip Faces.002"] = node

    node = tree_nodes.new(type="GeometryNodeSwitch")
    node.location = (3440, -1120)
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

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (6320, -60)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = 6.000000
    node.inputs[2].default_value = 26.000000
    node.inputs[3].default_value = 0.000000
    node.inputs[4].default_value = 20.000000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range.005"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (6320, -320)
    node.operation = "GREATER_THAN"
    node.use_clamp = False
    node.inputs[1].default_value = 0.990000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.053"] = node

    node = tree_nodes.new(type="GeometryNodeSubdivisionSurface")
    node.location = (6500, 40)
    node.boundary_smooth = "ALL"
    node.uv_smooth = "PRESERVE_BOUNDARIES"
    new_nodes["Subdivision Surface.001"] = node

    node = tree_nodes.new(type="GeometryNodeSetShadeSmooth")
    node.location = (3980, -1120)
    node.inputs[2].default_value = True
    new_nodes["Set Shade Smooth"] = node

    node = tree_nodes.new(type="GeometryNodeSetShadeSmooth")
    node.location = (6320, 80)
    node.inputs[2].default_value = True
    new_nodes["Set Shade Smooth.001"] = node

    node = tree_nodes.new(type="GeometryNodeSetShadeSmooth")
    node.location = (3160, -200)
    node.inputs[2].default_value = True
    new_nodes["Set Shade Smooth.002"] = node

    node = tree_nodes.new(type="GeometryNodeSetMaterial")
    node.location = (3800, -1120)
    new_nodes["Set Material.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-480, 100)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[1].default_value = 0.707107
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.054"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-1720, 120)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="GeometryNodeSwitch")
    node.location = (8120, -1080)
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
    new_nodes["Switch.002"] = node

    node = tree_nodes.new(type="GeometryNodeSwitch")
    node.location = (8120, -920)
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
    new_nodes["Switch.001"] = node

    node = tree_nodes.new(type="FunctionNodeCompare")
    node.location = (8120, -1400)
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

    node = tree_nodes.new(type="GeometryNodeSwitch")
    node.location = (8120, -1240)
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
    new_nodes["Switch.003"] = node

    node = tree_nodes.new(type="GeometryNodeSetMaterial")
    node.location = (8120, -1560)
    new_nodes["Set Material.003"] = node

    node = tree_nodes.new(type="GeometryNodeMeshToPoints")
    node.location = (8120, -1680)
    node.mode = "VERTICES"
    new_nodes["Mesh to Points"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (8340, -660)
    new_nodes["Group Output"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (8120, -1860)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = 0.050000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.055"] = node

    node = tree_nodes.new(type="GeometryNodeMeshLine")
    node.location = (8120, -2020)
    node.count_mode = "TOTAL"
    node.mode = "OFFSET"
    node.inputs[0].default_value = 1
    node.inputs[1].default_value = 1.000000
    node.inputs[3].default_value = (0.0, 0.0, 1.0)
    new_nodes["Mesh Line"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (8120, -2240)
    node.inputs[0].default_value = 0.000000
    node.inputs[1].default_value = 0.000000
    new_nodes["Combine XYZ.012"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (8120, -2380)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = 0.063333
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.056"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (7920, -2020)
    node.operation = "LENGTH"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.021"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (7060, -1640)
    node.operation = "SCALE"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 0.250000
    new_nodes["Vector Math.020"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (7060, -1780)
    new_nodes["Position.016"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.location = (7760, -800)
    node.data_type = "FLOAT"
    node.domain = "POINT"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute.010"] = node

    node = tree_nodes.new(type="GeometryNodeAttributeStatistic")
    node.location = (7760, -1000)
    node.data_type = "FLOAT"
    node.domain = "POINT"
    new_nodes["Attribute Statistic.004"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (7760, -1340)
    new_nodes["Separate XYZ.010"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (7760, -1480)
    new_nodes["Position.018"] = node

    node = tree_nodes.new(type="GeometryNodeSetPosition")
    node.location = (7300, -1360)
    node.inputs[3].default_value = (0.0, 0.0, 0.0)
    new_nodes["Set Position.012"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Group Input"].outputs[15], new_nodes["Math.029"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[16], new_nodes["Math.032"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[12], new_nodes["Curve Circle"].inputs[4])
    tree_links.new(new_nodes["Group Input"].outputs[13], new_nodes["Math.034"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[14], new_nodes["Math.033"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[17], new_nodes["Math.028"].inputs[1])
    tree_links.new(new_nodes["Curve Circle"].outputs[0], new_nodes["Curve to Mesh"].inputs[0])
    tree_links.new(new_nodes["Bezier Segment"].outputs[0], new_nodes["Subdivide Curve"].inputs[0])
    tree_links.new(new_nodes["Set Handle Type"].outputs[0], new_nodes["Set Position.003"].inputs[0])
    tree_links.new(new_nodes["Math.031"].outputs[0], new_nodes["Math.033"].inputs[1])
    tree_links.new(new_nodes["Math.030"].outputs[0], new_nodes["Math.029"].inputs[0])
    tree_links.new(new_nodes["Position.005"].outputs[0], new_nodes["Separate XYZ.003"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.003"].outputs[1], new_nodes["Math.039"].inputs[0])
    tree_links.new(new_nodes["Math.039"].outputs[0], new_nodes["Math.032"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.003"].outputs[1], new_nodes["Math.031"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.003"].outputs[1], new_nodes["Math.030"].inputs[0])
    tree_links.new(new_nodes["Combine XYZ.003"].outputs[0], new_nodes["Bezier Segment"].inputs[1])
    tree_links.new(new_nodes["Combine XYZ.002"].outputs[0], new_nodes["Bezier Segment"].inputs[2])
    tree_links.new(new_nodes["Math.054"].outputs[0], new_nodes["Combine XYZ.002"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.003"].outputs[1], new_nodes["Math.040"].inputs[0])
    tree_links.new(new_nodes["Math.040"].outputs[0], new_nodes["Math.034"].inputs[0])
    tree_links.new(new_nodes["Math.027"].outputs[0], new_nodes["Math.028"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.003"].outputs[1], new_nodes["Math.027"].inputs[0])
    tree_links.new(new_nodes["Subdivide Curve"].outputs[0], new_nodes["Set Handle Type"].inputs[0])
    tree_links.new(new_nodes["Set Position.003"].outputs[0], new_nodes["Curve to Mesh"].inputs[1])
    tree_links.new(new_nodes["Math.036"].outputs[0], new_nodes["Math.037"].inputs[0])
    tree_links.new(new_nodes["Math.035"].outputs[0], new_nodes["Math.037"].inputs[1])
    tree_links.new(new_nodes["Math.032"].outputs[0], new_nodes["Math.036"].inputs[1])
    tree_links.new(new_nodes["Math.028"].outputs[0], new_nodes["Math.035"].inputs[0])
    tree_links.new(new_nodes["Math.033"].outputs[0], new_nodes["Math.035"].inputs[1])
    tree_links.new(new_nodes["Normal.001"].outputs[0], new_nodes["Vector Math.008"].inputs[1])
    tree_links.new(new_nodes["Math.037"].outputs[0], new_nodes["Math.038"].inputs[0])
    tree_links.new(new_nodes["Math.029"].outputs[0], new_nodes["Math.038"].inputs[1])
    tree_links.new(new_nodes["Math.038"].outputs[0], new_nodes["Vector Math.008"].inputs[0])
    tree_links.new(new_nodes["Vector Math.008"].outputs[0], new_nodes["Set Position.003"].inputs[3])
    tree_links.new(new_nodes["Math.034"].outputs[0], new_nodes["Math.036"].inputs[0])
    tree_links.new(new_nodes["Position.006"].outputs[0], new_nodes["Separate XYZ.004"].inputs[0])
    tree_links.new(new_nodes["Math.041"].outputs[0], new_nodes["Math.042"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.004"].outputs[1], new_nodes["Math.041"].inputs[0])
    tree_links.new(new_nodes["Math.042"].outputs[0], new_nodes["Set Handle Type"].inputs[1])
    tree_links.new(new_nodes["Curve to Mesh"].outputs[0], new_nodes["Join Geometry"].inputs[0])
    tree_links.new(new_nodes["Set Position"].outputs[0], new_nodes["Join Geometry"].inputs[0])
    tree_links.new(new_nodes["Combine XYZ.001"].outputs[0], new_nodes["Set Position"].inputs[3])
    tree_links.new(new_nodes["Math.012"].outputs[0], new_nodes["Combine XYZ.001"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[13], new_nodes["Math.012"].inputs[0])
    tree_links.new(new_nodes["Position"].outputs[0], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Vector Math"].outputs[0], new_nodes["Set Position"].inputs[2])
    tree_links.new(new_nodes["Combine XYZ"].outputs[0], new_nodes["Set Position.001"].inputs[3])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Combine XYZ"].inputs[2])
    tree_links.new(new_nodes["Position.001"].outputs[0], new_nodes["Vector Math.001"].inputs[0])
    tree_links.new(new_nodes["Vector Math.001"].outputs[0], new_nodes["Set Position.001"].inputs[2])
    tree_links.new(new_nodes["Set Position.001"].outputs[0], new_nodes["Join Geometry"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[12], new_nodes["Vector Math.001"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[17], new_nodes["Math"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ"].outputs[0], new_nodes["Math.008"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ"].outputs[1], new_nodes["Math.008"].inputs[1])
    tree_links.new(new_nodes["Math.003"].outputs[0], new_nodes["Vector Math.003"].inputs[3])
    tree_links.new(new_nodes["Math.011"].outputs[0], new_nodes["Math.003"].inputs[0])
    tree_links.new(new_nodes["Math.008"].outputs[0], new_nodes["Math.009"].inputs[0])
    tree_links.new(new_nodes["Math.009"].outputs[0], new_nodes["Math.010"].inputs[0])
    tree_links.new(new_nodes["Math.008"].outputs[0], new_nodes["Math.010"].inputs[2])
    tree_links.new(new_nodes["Math.010"].outputs[0], new_nodes["Math.011"].inputs[0])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Vector Math.002"].inputs[3])
    tree_links.new(new_nodes["Math.006"].outputs[0], new_nodes["Math.001"].inputs[0])
    tree_links.new(new_nodes["Math.005"].outputs[0], new_nodes["Math.004"].inputs[0])
    tree_links.new(new_nodes["Math.004"].outputs[0], new_nodes["Math.007"].inputs[0])
    tree_links.new(new_nodes["Math.007"].outputs[0], new_nodes["Math.006"].inputs[0])
    tree_links.new(new_nodes["Position.002"].outputs[0], new_nodes["Vector Rotate"].inputs[0])
    tree_links.new(new_nodes["Math.005"].outputs[0], new_nodes["Math.007"].inputs[2])
    tree_links.new(new_nodes["Vector Rotate"].outputs[0], new_nodes["Set Position.002"].inputs[2])
    tree_links.new(new_nodes["Vector Math.003"].outputs[0], new_nodes["Vector Math.004"].inputs[0])
    tree_links.new(new_nodes["Vector Math.002"].outputs[0], new_nodes["Vector Math.004"].inputs[1])
    tree_links.new(new_nodes["Vector Math.004"].outputs[0], new_nodes["Vector Rotate"].inputs[4])
    tree_links.new(new_nodes["Position.002"].outputs[0], new_nodes["Separate XYZ"].inputs[0])
    tree_links.new(new_nodes["Math.008"].outputs[0], new_nodes["Math.005"].inputs[0])
    tree_links.new(new_nodes["Mesh Circle.001"].outputs[0], new_nodes["Flip Faces"].inputs[0])
    tree_links.new(new_nodes["Math.003"].outputs[0], new_nodes["Math.002"].inputs[0])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Math.002"].inputs[1])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Capture Attribute.002"].inputs[2])
    tree_links.new(new_nodes["Capture Attribute.002"].outputs[2], new_nodes["Group Output"].inputs[5])
    tree_links.new(new_nodes["Merge by Distance"].outputs[0], new_nodes["Capture Attribute.002"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.002"].outputs[0], new_nodes["Set Position.002"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.002"].outputs[0], new_nodes["Math.025"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.002"].outputs[1], new_nodes["Math.025"].inputs[1])
    tree_links.new(new_nodes["Position.004"].outputs[0], new_nodes["Separate XYZ.002"].inputs[0])
    tree_links.new(new_nodes["Normal"].outputs[0], new_nodes["Vector Math.005"].inputs[0])
    tree_links.new(new_nodes["Subdivision Surface"].outputs[0], new_nodes["Set Position.007"].inputs[0])
    tree_links.new(new_nodes["Vector Math.005"].outputs[0], new_nodes["Set Position.007"].inputs[3])
    tree_links.new(new_nodes["Math.013"].outputs[0], new_nodes["Float Curve"].inputs[1])
    tree_links.new(new_nodes["Math.014"].outputs[0], new_nodes["Math.013"].inputs[0])
    tree_links.new(new_nodes["Value"].outputs[0], new_nodes["Math.015"].inputs[0])
    tree_links.new(new_nodes["Math.024"].outputs[0], new_nodes["Math.014"].inputs[0])
    tree_links.new(new_nodes["Math.015"].outputs[0], new_nodes["Math.014"].inputs[1])
    tree_links.new(new_nodes["Math.015"].outputs[0], new_nodes["Math.013"].inputs[1])
    tree_links.new(new_nodes["Float Curve"].outputs[0], new_nodes["Math.016"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[18], new_nodes["Math.016"].inputs[1])
    tree_links.new(new_nodes["Position.003"].outputs[0], new_nodes["Vector Math.006"].inputs[0])
    tree_links.new(new_nodes["Vector Math.006"].outputs[0], new_nodes["Vector Math.007"].inputs[0])
    tree_links.new(new_nodes["Vector Math.007"].outputs[1], new_nodes["Math.020"].inputs[0])
    tree_links.new(new_nodes["Vector Math.007"].outputs[1], new_nodes["Math.018"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[12], new_nodes["Math.018"].inputs[1])
    tree_links.new(new_nodes["Math.018"].outputs[0], new_nodes["Float Curve.001"].inputs[1])
    tree_links.new(new_nodes["Position.003"].outputs[0], new_nodes["Separate XYZ.001"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[2], new_nodes["Math.022"].inputs[0])
    tree_links.new(new_nodes["Math.022"].outputs[0], new_nodes["Math.021"].inputs[0])
    tree_links.new(new_nodes["Float Curve.002"].outputs[0], new_nodes["Math.021"].inputs[1])
    tree_links.new(new_nodes["Math.022"].outputs[0], new_nodes["Boolean Math"].inputs[0])
    tree_links.new(new_nodes["Boolean Math"].outputs[0], new_nodes["Math.019"].inputs[0])
    tree_links.new(new_nodes["Float Curve.001"].outputs[0], new_nodes["Math.019"].inputs[1])
    tree_links.new(new_nodes["Math.019"].outputs[0], new_nodes["Math.023"].inputs[1])
    tree_links.new(new_nodes["Math.021"].outputs[0], new_nodes["Math.023"].inputs[0])
    tree_links.new(new_nodes["Math.023"].outputs[0], new_nodes["Math.017"].inputs[1])
    tree_links.new(new_nodes["Math.016"].outputs[0], new_nodes["Math.017"].inputs[0])
    tree_links.new(new_nodes["Math.017"].outputs[0], new_nodes["Vector Math.005"].inputs[3])
    tree_links.new(new_nodes["Math.020"].outputs[0], new_nodes["Float Curve.002"].inputs[1])
    tree_links.new(new_nodes["Join Geometry"].outputs[0], new_nodes["Capture Attribute.003"].inputs[0])
    tree_links.new(new_nodes["Math.026"].outputs[0], new_nodes["Capture Attribute.003"].inputs[2])
    tree_links.new(new_nodes["Capture Attribute.001"].outputs[2], new_nodes["Math.026"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute"].outputs[2], new_nodes["Math.026"].inputs[1])
    tree_links.new(new_nodes["Mesh Circle"].outputs[0], new_nodes["Capture Attribute.001"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.001"].outputs[0], new_nodes["Set Position"].inputs[0])
    tree_links.new(new_nodes["Flip Faces"].outputs[0], new_nodes["Capture Attribute"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute"].outputs[0], new_nodes["Set Position.001"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.003"].outputs[0], new_nodes["Merge by Distance"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.003"].outputs[2], new_nodes["Group Output"].inputs[6])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Set Material"].inputs[2])
    tree_links.new(new_nodes["Curve Circle.001"].outputs[0], new_nodes["Curve to Mesh.001"].inputs[0])
    tree_links.new(new_nodes["Bezier Segment.001"].outputs[0], new_nodes["Curve to Mesh.001"].inputs[1])
    tree_links.new(new_nodes["Math.046"].outputs[0], new_nodes["Combine XYZ.004"].inputs[1])
    tree_links.new(new_nodes["Math.044"].outputs[0], new_nodes["Combine XYZ.004"].inputs[0])
    tree_links.new(new_nodes["Math.045"].outputs[0], new_nodes["Math.044"].inputs[0])
    tree_links.new(new_nodes["Combine XYZ.004"].outputs[0], new_nodes["Vector Math.014"].inputs[0])
    tree_links.new(new_nodes["Curve to Mesh.001"].outputs[0], new_nodes["Join Geometry.001"].inputs[0])
    tree_links.new(new_nodes["Set Position.004"].outputs[0], new_nodes["Join Geometry.001"].inputs[0])
    tree_links.new(new_nodes["Flip Faces.001"].outputs[0], new_nodes["Join Geometry.001"].inputs[0])
    tree_links.new(new_nodes["Combine XYZ.007"].outputs[0], new_nodes["Set Position.004"].inputs[3])
    tree_links.new(new_nodes["Vector Math.014"].outputs[0], new_nodes["Bezier Segment.001"].inputs[2])
    tree_links.new(new_nodes["Combine XYZ.004"].outputs[0], new_nodes["Bezier Segment.001"].inputs[1])
    tree_links.new(new_nodes["Merge by Distance.001"].outputs[0], new_nodes["Set Position.005"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[8], new_nodes["Math.043"].inputs[0])
    tree_links.new(new_nodes["Math.043"].outputs[0], new_nodes["Math.045"].inputs[0])
    tree_links.new(new_nodes["Math.043"].outputs[0], new_nodes["Curve Circle.001"].inputs[4])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Math.045"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Mesh Circle.002"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[7], new_nodes["Math.046"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[7], new_nodes["Combine XYZ.007"].inputs[2])
    tree_links.new(new_nodes["Combine XYZ.005"].outputs[0], new_nodes["Vector Math.014"].inputs[1])
    tree_links.new(new_nodes["Math.047"].outputs[0], new_nodes["Combine XYZ.005"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[7], new_nodes["Math.047"].inputs[0])
    tree_links.new(new_nodes["Mesh Circle.002"].outputs[0], new_nodes["Flip Faces.001"].inputs[0])
    tree_links.new(new_nodes["Position.013"].outputs[0], new_nodes["Separate XYZ.008"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.008"].outputs[2], new_nodes["Attribute Statistic.002"].inputs[2])
    tree_links.new(new_nodes["Set Position.005"].outputs[0], new_nodes["Attribute Statistic.002"].inputs[0])
    tree_links.new(new_nodes["Position.012"].outputs[0], new_nodes["Separate XYZ.007"].inputs[0])
    tree_links.new(new_nodes["Attribute Statistic.002"].outputs[3], new_nodes["Map Range.004"].inputs[1])
    tree_links.new(new_nodes["Attribute Statistic.002"].outputs[4], new_nodes["Map Range.004"].inputs[2])
    tree_links.new(new_nodes["Separate XYZ.007"].outputs[2], new_nodes["Map Range.004"].inputs[0])
    tree_links.new(new_nodes["Map Range.004"].outputs[0], new_nodes["Capture Attribute.005"].inputs[2])
    tree_links.new(new_nodes["Capture Attribute.005"].outputs[2], new_nodes["Group Output"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Set Material.001"].inputs[2])
    tree_links.new(new_nodes["Position.011"].outputs[0], new_nodes["Vector Math.015"].inputs[0])
    tree_links.new(new_nodes["Vector Math.015"].outputs[0], new_nodes["Vector Math.016"].inputs[0])
    tree_links.new(new_nodes["Vector Math.016"].outputs[0], new_nodes["Capture Attribute.004"].inputs[1])
    tree_links.new(new_nodes["Capture Attribute.004"].outputs[1], new_nodes["Group Output"].inputs[3])
    tree_links.new(new_nodes["Set Position.005"].outputs[0], new_nodes["Capture Attribute.004"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.004"].outputs[0], new_nodes["Capture Attribute.005"].inputs[0])
    tree_links.new(new_nodes["Set Position.006"].outputs[0], new_nodes["Set Material.001"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.005"].outputs[0], new_nodes["Set Position.006"].inputs[0])
    tree_links.new(new_nodes["Position.014"].outputs[0], new_nodes["Vector Rotate.001"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.005"].outputs[2], new_nodes["Math.049"].inputs[0])
    tree_links.new(new_nodes["Combine XYZ.008"].outputs[0], new_nodes["Vector Rotate.001"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[7], new_nodes["Math.050"].inputs[0])
    tree_links.new(new_nodes["Math.048"].outputs[0], new_nodes["Combine XYZ.006"].inputs[2])
    tree_links.new(new_nodes["Combine XYZ.006"].outputs[0], new_nodes["Set Position.005"].inputs[3])
    tree_links.new(new_nodes["Math.012"].outputs[0], new_nodes["Math.048"].inputs[0])
    tree_links.new(new_nodes["Math.012"].outputs[0], new_nodes["Combine XYZ.008"].inputs[2])
    tree_links.new(new_nodes["Math.050"].outputs[0], new_nodes["Combine XYZ.008"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[10], new_nodes["Math.049"].inputs[1])
    tree_links.new(new_nodes["Vector Rotate.001"].outputs[0], new_nodes["Set Position.006"].inputs[2])
    tree_links.new(new_nodes["Math.049"].outputs[0], new_nodes["Combine XYZ.009"].inputs[0])
    tree_links.new(new_nodes["Combine XYZ.009"].outputs[0], new_nodes["Vector Rotate.002"].inputs[0])
    tree_links.new(new_nodes["Vector Rotate.002"].outputs[0], new_nodes["Vector Rotate.001"].inputs[4])
    tree_links.new(new_nodes["Combine XYZ.010"].outputs[0], new_nodes["Vector Rotate.002"].inputs[4])
    tree_links.new(new_nodes["Group Input"].outputs[9], new_nodes["Combine XYZ.010"].inputs[2])
    tree_links.new(new_nodes["Set Position.002"].outputs[0], new_nodes["Set Material"].inputs[0])
    tree_links.new(new_nodes["Set Shade Smooth.002"].outputs[0], new_nodes["Subdivision Surface"].inputs[0])
    tree_links.new(new_nodes["Join Geometry.001"].outputs[0], new_nodes["Merge by Distance.001"].inputs[0])
    tree_links.new(new_nodes["Position.007"].outputs[0], new_nodes["Separate XYZ.005"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.005"].outputs[2], new_nodes["Attribute Statistic"].inputs[2])
    tree_links.new(new_nodes["Position.008"].outputs[0], new_nodes["Separate XYZ.006"].inputs[0])
    tree_links.new(new_nodes["Attribute Statistic"].outputs[3], new_nodes["Map Range.002"].inputs[1])
    tree_links.new(new_nodes["Attribute Statistic"].outputs[4], new_nodes["Map Range.002"].inputs[2])
    tree_links.new(new_nodes["Separate XYZ.006"].outputs[2], new_nodes["Map Range.002"].inputs[0])
    tree_links.new(new_nodes["Map Range.002"].outputs[0], new_nodes["Capture Attribute.007"].inputs[2])
    tree_links.new(new_nodes["Position.015"].outputs[0], new_nodes["Vector Math.017"].inputs[0])
    tree_links.new(new_nodes["Vector Math.017"].outputs[0], new_nodes["Vector Math.018"].inputs[0])
    tree_links.new(new_nodes["Vector Math.018"].outputs[0], new_nodes["Capture Attribute.006"].inputs[1])
    tree_links.new(new_nodes["Capture Attribute.007"].outputs[2], new_nodes["Group Output"].inputs[7])
    tree_links.new(new_nodes["Capture Attribute.006"].outputs[1], new_nodes["Group Output"].inputs[8])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Map Range"].inputs[0])
    tree_links.new(new_nodes["Map Range"].outputs[0], new_nodes["Bezier Segment"].inputs[0])
    tree_links.new(new_nodes["Math.025"].outputs[0], new_nodes["Math.024"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Map Range.001"].inputs[0])
    tree_links.new(new_nodes["Map Range.001"].outputs[0], new_nodes["Subdivision Surface"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Map Range.005"].inputs[0])
    tree_links.new(new_nodes["Map Range.005"].outputs[0], new_nodes["Subdivision Surface.001"].inputs[1])
    tree_links.new(new_nodes["Capture Attribute.005"].outputs[2], new_nodes["Math.053"].inputs[0])
    tree_links.new(new_nodes["Math.053"].outputs[0], new_nodes["Subdivision Surface.001"].inputs[2])
    tree_links.new(new_nodes["Merge by Distance"].outputs[0], new_nodes["Switch"].inputs[15])
    tree_links.new(new_nodes["Switch"].outputs[6], new_nodes["Flip Faces.002"].inputs[0])
    tree_links.new(new_nodes["Flip Faces.002"].outputs[0], new_nodes["Set Material.002"].inputs[0])
    tree_links.new(new_nodes["Normal.002"].outputs[0], new_nodes["Vector Math.009"].inputs[0])
    tree_links.new(new_nodes["Vector Math.009"].outputs[0], new_nodes["Set Position.008"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[19], new_nodes["Vector Math.009"].inputs[3])
    tree_links.new(new_nodes["Capture Attribute.008"].outputs[0], new_nodes["Capture Attribute.006"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.007"].outputs[0], new_nodes["Capture Attribute.008"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.008"].outputs[2], new_nodes["Group Output"].inputs[9])
    tree_links.new(new_nodes["Attribute Statistic.001"].outputs[4], new_nodes["Map Range.003"].inputs[2])
    tree_links.new(new_nodes["Vector Math.013"].outputs[0], new_nodes["Vector Math.010"].inputs[0])
    tree_links.new(new_nodes["Vector Math.010"].outputs[1], new_nodes["Map Range.003"].inputs[0])
    tree_links.new(new_nodes["Position.010"].outputs[0], new_nodes["Vector Math.013"].inputs[0])
    tree_links.new(new_nodes["Map Range.003"].outputs[0], new_nodes["Capture Attribute.008"].inputs[2])
    tree_links.new(new_nodes["Vector Math.011"].outputs[0], new_nodes["Vector Math.012"].inputs[0])
    tree_links.new(new_nodes["Position.009"].outputs[0], new_nodes["Vector Math.011"].inputs[0])
    tree_links.new(new_nodes["Vector Math.012"].outputs[1], new_nodes["Attribute Statistic.001"].inputs[2])
    tree_links.new(new_nodes["Mesh Circle.002"].outputs[0], new_nodes["Set Position.004"].inputs[0])
    tree_links.new(new_nodes["Position.017"].outputs[0], new_nodes["Separate XYZ.009"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.009"].outputs[2], new_nodes["Attribute Statistic.003"].inputs[2])
    tree_links.new(new_nodes["Math.052"].outputs[0], new_nodes["Combine XYZ.011"].inputs[2])
    tree_links.new(new_nodes["Combine XYZ.011"].outputs[0], new_nodes["Set Position.010"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[20], new_nodes["Math.051"].inputs[1])
    tree_links.new(new_nodes["Math.051"].outputs[0], new_nodes["Math.052"].inputs[0])
    tree_links.new(new_nodes["Attribute Statistic.003"].outputs[3], new_nodes["Math.052"].inputs[1])
    tree_links.new(new_nodes["Combine XYZ.011"].outputs[0], new_nodes["Set Position.011"].inputs[3])
    tree_links.new(new_nodes["Subdivision Surface.001"].outputs[0], new_nodes["Set Position.011"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.006"].outputs[0], new_nodes["Attribute Statistic.003"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.006"].outputs[0], new_nodes["Set Position.010"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Switch"].inputs[1])
    tree_links.new(new_nodes["Set Position.007"].outputs[0], new_nodes["Attribute Statistic.001"].inputs[0])
    tree_links.new(new_nodes["Set Position.007"].outputs[0], new_nodes["Capture Attribute.007"].inputs[0])
    tree_links.new(new_nodes["Set Position.007"].outputs[0], new_nodes["Attribute Statistic"].inputs[0])
    tree_links.new(new_nodes["Combine XYZ.011"].outputs[0], new_nodes["Set Position.009"].inputs[3])
    tree_links.new(new_nodes["Set Position.008"].outputs[0], new_nodes["Set Position.009"].inputs[0])
    tree_links.new(new_nodes["Vector Math.019"].outputs[0], new_nodes["Set Position.014"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Vector Math.019"].inputs[1])
    tree_links.new(new_nodes["Vector Math.019"].outputs[0], new_nodes["Set Position.013"].inputs[2])
    tree_links.new(new_nodes["Vector Math.019"].outputs[0], new_nodes["Set Position.012"].inputs[2])
    tree_links.new(new_nodes["Set Position.009"].outputs[0], new_nodes["Set Position.012"].inputs[0])
    tree_links.new(new_nodes["Set Position.010"].outputs[0], new_nodes["Set Position.013"].inputs[0])
    tree_links.new(new_nodes["Set Position.011"].outputs[0], new_nodes["Set Position.014"].inputs[0])
    tree_links.new(new_nodes["Switch.001"].outputs[6], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Vector Math.020"].outputs[0], new_nodes["Vector Math.019"].inputs[0])
    tree_links.new(new_nodes["Position.016"].outputs[0], new_nodes["Vector Math.020"].inputs[0])
    tree_links.new(new_nodes["Set Position.012"].outputs[0], new_nodes["Capture Attribute.009"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.009"].outputs[2], new_nodes["Group Output"].inputs[12])
    tree_links.new(new_nodes["Set Position.014"].outputs[0], new_nodes["Capture Attribute.010"].inputs[0])
    tree_links.new(new_nodes["Position.018"].outputs[0], new_nodes["Separate XYZ.010"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.010"].outputs[2], new_nodes["Attribute Statistic.004"].inputs[2])
    tree_links.new(new_nodes["Set Position.014"].outputs[0], new_nodes["Attribute Statistic.004"].inputs[0])
    tree_links.new(new_nodes["Attribute Statistic.003"].outputs[5], new_nodes["Math.051"].inputs[0])
    tree_links.new(new_nodes["Attribute Statistic.003"].outputs[5], new_nodes["Group Output"].inputs[10])
    tree_links.new(new_nodes["Attribute Statistic.004"].outputs[5], new_nodes["Capture Attribute.010"].inputs[2])
    tree_links.new(new_nodes["Capture Attribute.010"].outputs[2], new_nodes["Group Output"].inputs[1])
    tree_links.new(new_nodes["Set Material.002"].outputs[0], new_nodes["Set Shade Smooth"].inputs[0])
    tree_links.new(new_nodes["Set Shade Smooth"].outputs[0], new_nodes["Set Position.008"].inputs[0])
    tree_links.new(new_nodes["Set Material.001"].outputs[0], new_nodes["Set Shade Smooth.001"].inputs[0])
    tree_links.new(new_nodes["Set Shade Smooth.001"].outputs[0], new_nodes["Subdivision Surface.001"].inputs[0])
    tree_links.new(new_nodes["Set Material"].outputs[0], new_nodes["Set Shade Smooth.002"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Set Material.002"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[11], new_nodes["Vector Math"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[11], new_nodes["Math.020"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[12], new_nodes["Math.054"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[12], new_nodes["Combine XYZ.003"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.010"].outputs[0], new_nodes["Switch.001"].inputs[14])
    tree_links.new(new_nodes["Compare"].outputs[0], new_nodes["Switch.001"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Compare"].inputs[2])
    tree_links.new(new_nodes["Compare"].outputs[0], new_nodes["Switch.002"].inputs[1])
    tree_links.new(new_nodes["Set Position.013"].outputs[0], new_nodes["Switch.002"].inputs[14])
    tree_links.new(new_nodes["Switch.002"].outputs[6], new_nodes["Group Output"].inputs[4])
    tree_links.new(new_nodes["Compare"].outputs[0], new_nodes["Switch.003"].inputs[1])
    tree_links.new(new_nodes["Capture Attribute.009"].outputs[0], new_nodes["Switch.003"].inputs[14])
    tree_links.new(new_nodes["Switch.003"].outputs[6], new_nodes["Group Output"].inputs[11])
    tree_links.new(new_nodes["Set Material.003"].outputs[0], new_nodes["Switch.002"].inputs[15])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Set Material.003"].inputs[2])
    tree_links.new(new_nodes["Mesh to Points"].outputs[0], new_nodes["Set Material.003"].inputs[0])
    tree_links.new(new_nodes["Mesh Line"].outputs[0], new_nodes["Mesh to Points"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Vector Math.021"].inputs[0])
    tree_links.new(new_nodes["Vector Math.021"].outputs[1], new_nodes["Math.055"].inputs[0])
    tree_links.new(new_nodes["Math.055"].outputs[0], new_nodes["Mesh to Points"].inputs[3])
    tree_links.new(new_nodes["Combine XYZ.012"].outputs[0], new_nodes["Mesh Line"].inputs[2])
    tree_links.new(new_nodes["Vector Math.021"].outputs[1], new_nodes["Math.056"].inputs[0])
    tree_links.new(new_nodes["Math.056"].outputs[0], new_nodes["Combine XYZ.012"].inputs[2])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group

def create_geo_ng_pumpkin_deform():
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=PUMPKIN_DEFORM_GEO_NG_NAME, type='GeometryNodeTree')
    new_node_group.inputs.new(type='NodeSocketVector', name="Location")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Full Height")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Bend Amount")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Bend Rotation")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Twist Amount")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Pinch Amount")
    new_node_group.inputs.new(type='NodeSocketFloatAngle', name="Pinch Angle")
    new_node_group.outputs.new(type='NodeSocketVector', name="Output")
    tree_nodes = new_node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-560, -1440)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-740, -1740)
    node.operation = "LENGTH"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1820, -1440)
    node.operation = "ARCTAN2"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-560, -1600)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1640, -1440)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[1].default_value = 4.712390
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-740, -1440)
    node.operation = "SINE"
    node.use_clamp = False
    node.inputs[1].default_value = 1.000000
    node.inputs[2].default_value = 0.000000
    new_nodes["Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1460, -1440)
    node.operation = "SINE"
    node.use_clamp = False
    node.inputs[1].default_value = 1.000000
    node.inputs[2].default_value = 0.000000
    new_nodes["Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-920, -1740)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = (1.0, 1.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-740, -1580)
    node.operation = "COSINE"
    node.use_clamp = False
    node.inputs[1].default_value = 1.000000
    node.inputs[2].default_value = 0.000000
    new_nodes["Math.006"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (-380, -1320)
    new_nodes["Combine XYZ"] = node

    node = tree_nodes.new(type="ShaderNodeVectorRotate")
    node.location = (-2180, -1540)
    node.invert = False
    node.rotation_type = "Z_AXIS"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 1.0)
    node.inputs[4].default_value = (0.0, 0.0, 0.0)
    new_nodes["Vector Rotate"] = node

    node = tree_nodes.new(type="ShaderNodeVectorRotate")
    node.location = (-200, -1240)
    node.invert = True
    node.rotation_type = "Z_AXIS"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 1.0)
    node.inputs[4].default_value = (0.0, 0.0, 0.0)
    new_nodes["Vector Rotate.001"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (60, -1800)
    new_nodes["Separate XYZ"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Height Pct"
    node.location = (60, -1640)
    node.operation = "DIVIDE"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.007"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Twist * HeightPct"
    node.location = (60, -1480)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.008"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (240, -1280)
    node.operation = "ADD"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (760, -2080)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.009"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (760, -2240)
    node.operation = "COSINE"
    node.use_clamp = False
    node.inputs[1].default_value = 0.500000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.010"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (760, -1920)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.011"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (760, -1420)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = -1.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.012"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (760, -1580)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.013"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (760, -1740)
    node.operation = "SINE"
    node.use_clamp = False
    node.inputs[1].default_value = 0.500000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.014"] = node

    node = tree_nodes.new(type="ShaderNodeVectorRotate")
    node.location = (760, -960)
    node.invert = False
    node.rotation_type = "AXIS_ANGLE"
    node.inputs[4].default_value = (0.0, 0.0, 0.0)
    new_nodes["Vector Rotate.002"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (760, -820)
    node.operation = "SUBTRACT"
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (760, -1160)
    node.inputs[0].default_value = 0.000000
    node.inputs[1].default_value = 0.000000
    new_nodes["Combine XYZ.001"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (580, -1280)
    node.inputs[0].default_value = 1.000000
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 0.000000
    new_nodes["Combine XYZ.002"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (960, -1660)
    node.inputs[0].default_value = 0.000000
    new_nodes["Combine XYZ.003"] = node

    node = tree_nodes.new(type="ShaderNodeVectorRotate")
    node.location = (960, -1420)
    node.invert = False
    node.rotation_type = "EULER_XYZ"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 1.0)
    node.inputs[3].default_value = 0.000000
    new_nodes["Vector Rotate.003"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (960, -1780)
    node.inputs[0].default_value = 0.000000
    node.inputs[1].default_value = 0.000000
    new_nodes["Combine XYZ.004"] = node

    node = tree_nodes.new(type="ShaderNodeVectorRotate")
    node.location = (580, -960)
    node.invert = False
    node.rotation_type = "AXIS_ANGLE"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 1.0)
    node.inputs[4].default_value = (0.0, 0.0, 0.0)
    new_nodes["Vector Rotate.004"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Height Pct"
    node.location = (540, -1700)
    node.operation = "DIVIDE"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.015"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (540, -1860)
    new_nodes["Separate XYZ.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Bend * HeightPct"
    node.location = (540, -1540)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.016"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (960, -1280)
    node.operation = "ADD"
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (-2000, -1340)
    new_nodes["Separate XYZ.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1280, -1440)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[0].default_value = 1.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.017"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (-1100, -1440)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = -1.000000
    node.inputs[2].default_value = 1.000000
    node.inputs[4].default_value = 1.000000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-920, -1440)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.018"] = node

    node = tree_nodes.new(type="ShaderNodeVectorRotate")
    node.location = (240, -1480)
    node.invert = False
    node.rotation_type = "AXIS_ANGLE"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 1.0)
    node.inputs[4].default_value = (0.0, 0.0, 0.0)
    new_nodes["Vector Rotate.005"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-2400, -1220)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (1180, -1240)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Math.015"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[2], new_nodes["Math.015"].inputs[0])
    tree_links.new(new_nodes["Math.015"].outputs[0], new_nodes["Math.016"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Math.016"].inputs[1])
    tree_links.new(new_nodes["Math.016"].outputs[0], new_nodes["Math.014"].inputs[0])
    tree_links.new(new_nodes["Math.016"].outputs[0], new_nodes["Math.010"].inputs[0])
    tree_links.new(new_nodes["Math.014"].outputs[0], new_nodes["Math.013"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[2], new_nodes["Math.013"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[2], new_nodes["Math.009"].inputs[1])
    tree_links.new(new_nodes["Math.010"].outputs[0], new_nodes["Math.009"].inputs[0])
    tree_links.new(new_nodes["Math.011"].outputs[0], new_nodes["Combine XYZ.003"].inputs[2])
    tree_links.new(new_nodes["Math.009"].outputs[0], new_nodes["Math.011"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[2], new_nodes["Math.011"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[2], new_nodes["Combine XYZ.001"].inputs[2])
    tree_links.new(new_nodes["Combine XYZ.001"].outputs[0], new_nodes["Vector Rotate.002"].inputs[1])
    tree_links.new(new_nodes["Vector Rotate.002"].outputs[0], new_nodes["Vector Math.003"].inputs[0])
    tree_links.new(new_nodes["Vector Math.003"].outputs[0], new_nodes["Vector Math.004"].inputs[0])
    tree_links.new(new_nodes["Math.013"].outputs[0], new_nodes["Math.012"].inputs[0])
    tree_links.new(new_nodes["Math.012"].outputs[0], new_nodes["Combine XYZ.003"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Combine XYZ.004"].inputs[2])
    tree_links.new(new_nodes["Combine XYZ.004"].outputs[0], new_nodes["Vector Rotate.003"].inputs[4])
    tree_links.new(new_nodes["Combine XYZ.003"].outputs[0], new_nodes["Vector Rotate.003"].inputs[0])
    tree_links.new(new_nodes["Vector Rotate.003"].outputs[0], new_nodes["Vector Math.004"].inputs[1])
    tree_links.new(new_nodes["Math.016"].outputs[0], new_nodes["Vector Rotate.002"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Vector Rotate.004"].inputs[3])
    tree_links.new(new_nodes["Combine XYZ.002"].outputs[0], new_nodes["Vector Rotate.004"].inputs[0])
    tree_links.new(new_nodes["Vector Rotate.004"].outputs[0], new_nodes["Vector Rotate.002"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Math.007"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ"].outputs[2], new_nodes["Math.007"].inputs[0])
    tree_links.new(new_nodes["Math.007"].outputs[0], new_nodes["Math.008"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Math.008"].inputs[1])
    tree_links.new(new_nodes["Math.008"].outputs[0], new_nodes["Vector Rotate.005"].inputs[3])
    tree_links.new(new_nodes["Vector Math.002"].outputs[0], new_nodes["Vector Rotate.002"].inputs[0])
    tree_links.new(new_nodes["Vector Math.002"].outputs[0], new_nodes["Separate XYZ.001"].inputs[0])
    tree_links.new(new_nodes["Vector Rotate.005"].outputs[0], new_nodes["Vector Math.002"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Vector Math.003"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.002"].outputs[0], new_nodes["Math.001"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.002"].outputs[1], new_nodes["Math.001"].inputs[1])
    tree_links.new(new_nodes["Math.004"].outputs[0], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Vector Math"].outputs[1], new_nodes["Math"].inputs[1])
    tree_links.new(new_nodes["Vector Math"].outputs[1], new_nodes["Math.002"].inputs[1])
    tree_links.new(new_nodes["Math.006"].outputs[0], new_nodes["Math.002"].inputs[0])
    tree_links.new(new_nodes["Vector Math.001"].outputs[0], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Combine XYZ"].inputs[1])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Combine XYZ"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.002"].outputs[2], new_nodes["Combine XYZ"].inputs[2])
    tree_links.new(new_nodes["Math.003"].outputs[0], new_nodes["Math.005"].inputs[0])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Math.003"].inputs[0])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Math.018"].inputs[1])
    tree_links.new(new_nodes["Math.018"].outputs[0], new_nodes["Math.004"].inputs[0])
    tree_links.new(new_nodes["Math.018"].outputs[0], new_nodes["Math.006"].inputs[0])
    tree_links.new(new_nodes["Vector Rotate"].outputs[0], new_nodes["Separate XYZ.002"].inputs[0])
    tree_links.new(new_nodes["Combine XYZ"].outputs[0], new_nodes["Vector Rotate.001"].inputs[0])
    tree_links.new(new_nodes["Vector Rotate"].outputs[0], new_nodes["Vector Math.001"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Vector Rotate"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Vector Rotate"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Vector Rotate.001"].inputs[3])
    tree_links.new(new_nodes["Vector Math.004"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Vector Rotate.001"].outputs[0], new_nodes["Separate XYZ"].inputs[0])
    tree_links.new(new_nodes["Vector Rotate.001"].outputs[0], new_nodes["Vector Rotate.005"].inputs[0])
    tree_links.new(new_nodes["Math.005"].outputs[0], new_nodes["Map Range"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Math.017"].inputs[1])
    tree_links.new(new_nodes["Math.017"].outputs[0], new_nodes["Map Range"].inputs[3])
    tree_links.new(new_nodes["Map Range"].outputs[0], new_nodes["Math.018"].inputs[0])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group

def create_apply_pumpkin_geo_nodes(new_node_group, tree_nodes, tree_links, pumpkin_obj):
    new_node_group.outputs.new(type='NodeSocketFloat', name="Stem Height")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Stem Height Pct")
    new_node_group.outputs.new(type='NodeSocketVector', name="Stem Radial Vector")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Pumpkin Indent")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Top/Bottom Nub")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Body Height Pct")
    new_node_group.outputs.new(type='NodeSocketVector', name="Body Radial Vector")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Body Radial Pct")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Inside Pumpkin")

    # initialize variables
    new_nodes = {}

    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="GeometryNodeGroup")
    node.location = (-2160, 300)
    node.node_tree = bpy.data.node_groups.get(PUMPKIN_GEO_NG_NAME)
    node.inputs[0].default_value = 7
    node.inputs[1].default_value = True
    node.inputs[2].default_value = (1.0, 1.0, 1.0)
    node.inputs[3].default_value = bpy.data.materials.get(PUMPKIN_SKIN_MAT_NAME)
    node.inputs[4].default_value = bpy.data.materials.get(PUMPKIN_STEM_MAT_NAME)
    node.inputs[5].default_value = bpy.data.materials.get(PUMPKIN_POINT_MAT_NAME)
    node.inputs[6].default_value = 0.050000
    node.inputs[8].default_value = 0.080000
    node.inputs[11].default_value = 0.030000
    node.inputs[12].default_value = 0.020000
    node.inputs[15].default_value = 0.000000
    node.inputs[18].default_value = 0.050000
    node.inputs[19].default_value = 0.080000
    node.inputs[20].default_value = 0.000000
    new_nodes["Group"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (-2700, -900)
    new_nodes["Position"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-2520, -900)
    node.operation = "ADD"
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1880, -900)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math"] = node

    node = tree_nodes.new(type="GeometryNodeSetPosition")
    node.location = (-1440, -560)
    new_nodes["Set Position"] = node

    node = tree_nodes.new(type="ShaderNodeTexNoise")
    node.location = (-2340, -900)
    node.noise_dimensions = "3D"
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 8.000000
    node.inputs[3].default_value = 2.000000
    node.inputs[4].default_value = 0.500000
    node.inputs[5].default_value = 0.000000
    new_nodes["Noise Texture"] = node

    node = tree_nodes.new(type="ShaderNodeValToRGB")
    node.location = (-2160, -660)
    node.color_ramp.color_mode = "RGB"
    node.color_ramp.interpolation = "EASE"
    node.color_ramp.elements.remove(node.color_ramp.elements[0])
    elem = node.color_ramp.elements[0]
    elem.position = 0.120000
    elem.color = (0.000000, 0.000000, 0.000000, 1.000000)
    elem = node.color_ramp.elements.new(0.890909)
    elem.color = (0.538702, 0.538702, 0.538702, 1.000000)
    new_nodes["ColorRamp"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1880, -660)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeValToRGB")
    node.location = (-2160, -900)
    node.color_ramp.color_mode = "RGB"
    node.color_ramp.interpolation = "EASE"
    node.color_ramp.elements.remove(node.color_ramp.elements[0])
    elem = node.color_ramp.elements[0]
    elem.position = 0.080000
    elem.color = (0.005560, 0.005560, 0.005560, 1.000000)
    elem = node.color_ramp.elements.new(0.885455)
    elem.color = (0.278998, 0.278998, 0.278998, 1.000000)
    new_nodes["ColorRamp.001"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (-2160, -1140)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 1.000000
    node.inputs[3].default_value = -0.300000
    node.inputs[4].default_value = 0.300000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-2160, -1400)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = 12.566380
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-1220, -760)
    node.operation = "SCALE"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    new_nodes["Vector Math.001"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (-1220, -900)
    new_nodes["Position.001"] = node

    node = tree_nodes.new(type="GeometryNodeSetPosition")
    node.location = (-1220, -540)
    node.inputs[3].default_value = (0.0, 0.0, 0.0)
    new_nodes["Set Position.001"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (-1220, -980)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = 0.100000
    node.inputs[2].default_value = 0.900000
    node.inputs[3].default_value = 0.500000
    node.inputs[4].default_value = 1.000000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range.001"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (-2700, -180)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = 0.100000
    node.inputs[2].default_value = 0.900000
    node.inputs[3].default_value = 0.000000
    node.inputs[4].default_value = 37.699200
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range.002"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (-2880, -140)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = 0.100000
    node.inputs[2].default_value = 0.900000
    node.inputs[3].default_value = 0.050000
    node.inputs[4].default_value = 0.300000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range.003"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (-2520, -220)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = 0.100000
    node.inputs[2].default_value = 0.900000
    node.inputs[3].default_value = 0.100000
    node.inputs[4].default_value = 0.500000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range.004"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (-2880, -420)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = 0.100000
    node.inputs[2].default_value = 0.900000
    node.inputs[3].default_value = -0.250000
    node.inputs[4].default_value = 0.200000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range.005"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (-2700, -460)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = 0.100000
    node.inputs[2].default_value = 0.900000
    node.inputs[3].default_value = -0.150000
    node.inputs[4].default_value = 0.200000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range.006"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (-2520, -500)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = 0.100000
    node.inputs[2].default_value = 0.900000
    node.inputs[3].default_value = -0.200000
    node.inputs[4].default_value = 0.100000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range.007"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateRGB")
    node.location = (-3060, -660)
    new_nodes["Separate RGB"] = node

    node = tree_nodes.new(type="ShaderNodeTexNoise")
    node.location = (-3260, -560)
    node.noise_dimensions = "4D"
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 6.000000
    node.inputs[3].default_value = 2.000000
    node.inputs[4].default_value = 0.500000
    node.inputs[5].default_value = 0.000000
    new_nodes["Noise Texture.001"] = node

    node = tree_nodes.new(type="GeometryNodeObjectInfo")
    node.location = (-3440, -780)
    node.transform_space = "ORIGINAL"
    node.inputs[0].default_value = pumpkin_obj
    node.inputs[1].default_value = False
    new_nodes["Object Info"] = node

    node = tree_nodes.new(type="GeometryNodeJoinGeometry")
    node.location = (-1740, -80)
    new_nodes["Join Geometry"] = node

    node = tree_nodes.new(type="GeometryNodeGroup")
    node.location = (-1680, -660)
    node.node_tree = bpy.data.node_groups.get(PUMPKIN_DEFORM_GEO_NG_NAME)
    node.inputs[6].default_value = 0.000000
    new_nodes["Group.001"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-2720, 20)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (-1000, -320)
    new_nodes["Group Output"] = node

    # create links
    tree_links.new(new_nodes["Group"].outputs[5], new_nodes["Group Output"].inputs[4])
    tree_links.new(new_nodes["Group"].outputs[2], new_nodes["Group Output"].inputs[2])
    tree_links.new(new_nodes["Group"].outputs[3], new_nodes["Group Output"].inputs[3])
    tree_links.new(new_nodes["Group"].outputs[7], new_nodes["Group Output"].inputs[6])
    tree_links.new(new_nodes["Group"].outputs[8], new_nodes["Group Output"].inputs[7])
    tree_links.new(new_nodes["Group"].outputs[9], new_nodes["Group Output"].inputs[8])
    tree_links.new(new_nodes["Group"].outputs[6], new_nodes["Group Output"].inputs[5])
    tree_links.new(new_nodes["Group"].outputs[11], new_nodes["Join Geometry"].inputs[0])
    tree_links.new(new_nodes["Position"].outputs[0], new_nodes["Group.001"].inputs[0])
    tree_links.new(new_nodes["Noise Texture"].outputs[0], new_nodes["ColorRamp"].inputs[0])
    tree_links.new(new_nodes["Vector Math"].outputs[0], new_nodes["Noise Texture"].inputs[0])
    tree_links.new(new_nodes["Noise Texture"].outputs[0], new_nodes["ColorRamp.001"].inputs[0])
    tree_links.new(new_nodes["Group"].outputs[4], new_nodes["Join Geometry"].inputs[0])
    tree_links.new(new_nodes["Join Geometry"].outputs[0], new_nodes["Set Position"].inputs[0])
    tree_links.new(new_nodes["Group.001"].outputs[0], new_nodes["Set Position"].inputs[3])
    tree_links.new(new_nodes["Group"].outputs[10], new_nodes["Group.001"].inputs[1])
    tree_links.new(new_nodes["Object Info"].outputs[0], new_nodes["Noise Texture.001"].inputs[0])
    tree_links.new(new_nodes["Noise Texture.001"].outputs[0], new_nodes["Map Range"].inputs[0])
    tree_links.new(new_nodes["ColorRamp"].outputs[0], new_nodes["Math.001"].inputs[0])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Group.001"].inputs[2])
    tree_links.new(new_nodes["Noise Texture.001"].outputs[0], new_nodes["Math.002"].inputs[0])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Group.001"].inputs[3])
    tree_links.new(new_nodes["Map Range"].outputs[0], new_nodes["Math"].inputs[1])
    tree_links.new(new_nodes["ColorRamp.001"].outputs[0], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Group.001"].inputs[5])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Group.001"].inputs[4])
    tree_links.new(new_nodes["Map Range"].outputs[0], new_nodes["Math.001"].inputs[1])
    tree_links.new(new_nodes["Noise Texture.001"].outputs[1], new_nodes["Separate RGB"].inputs[0])
    tree_links.new(new_nodes["Separate RGB"].outputs[0], new_nodes["Map Range.005"].inputs[0])
    tree_links.new(new_nodes["Map Range.005"].outputs[0], new_nodes["Group"].inputs[13])
    tree_links.new(new_nodes["Separate RGB"].outputs[1], new_nodes["Map Range.006"].inputs[0])
    tree_links.new(new_nodes["Separate RGB"].outputs[2], new_nodes["Map Range.007"].inputs[0])
    tree_links.new(new_nodes["Map Range.007"].outputs[0], new_nodes["Group"].inputs[17])
    tree_links.new(new_nodes["Map Range.005"].outputs[0], new_nodes["Group"].inputs[14])
    tree_links.new(new_nodes["Map Range.006"].outputs[0], new_nodes["Group"].inputs[16])
    tree_links.new(new_nodes["Position"].outputs[0], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Object Info"].outputs[0], new_nodes["Vector Math"].inputs[1])
    tree_links.new(new_nodes["Noise Texture.001"].outputs[0], new_nodes["Map Range.003"].inputs[0])
    tree_links.new(new_nodes["Map Range.003"].outputs[0], new_nodes["Group"].inputs[7])
    tree_links.new(new_nodes["Set Position"].outputs[0], new_nodes["Set Position.001"].inputs[0])
    tree_links.new(new_nodes["Position.001"].outputs[0], new_nodes["Vector Math.001"].inputs[0])
    tree_links.new(new_nodes["Vector Math.001"].outputs[0], new_nodes["Set Position.001"].inputs[2])
    tree_links.new(new_nodes["Noise Texture.001"].outputs[0], new_nodes["Map Range.001"].inputs[0])
    tree_links.new(new_nodes["Map Range.001"].outputs[0], new_nodes["Vector Math.001"].inputs[3])
    tree_links.new(new_nodes["Noise Texture.001"].outputs[0], new_nodes["Map Range.002"].inputs[0])
    tree_links.new(new_nodes["Map Range.002"].outputs[0], new_nodes["Group"].inputs[9])
    tree_links.new(new_nodes["Noise Texture.001"].outputs[0], new_nodes["Map Range.004"].inputs[0])
    tree_links.new(new_nodes["Map Range.004"].outputs[0], new_nodes["Group"].inputs[10])
    tree_links.new(new_nodes["Group"].outputs[12], new_nodes["Group Output"].inputs[9])
    tree_links.new(new_nodes["Group"].outputs[1], new_nodes["Group Output"].inputs[1])
    tree_links.new(new_nodes["Set Position.001"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Group"].outputs[0], new_nodes["Join Geometry"].inputs[0])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group

def create_pumpkin_materials(override_create, pumpkin_obj):
    ensure_node_groups(override_create, [PUMPKIN_SURFACE_MAT_NG_NAME], 'ShaderNodeTree', create_prereq_node_group)
    ensure_materials(override_create, [PUMPKIN_SKIN_MAT_NAME, PUMPKIN_STEM_MAT_NAME, PUMPKIN_POINT_MAT_NAME],
                     create_prereq_material)
    skin_mat = bpy.data.materials.get(PUMPKIN_SKIN_MAT_NAME)
    skin_mat.cycles.displacement_method = 'BOTH'
    stem_mat = bpy.data.materials.get(PUMPKIN_STEM_MAT_NAME)
    stem_mat.cycles.displacement_method = 'BOTH'
    point_mat = bpy.data.materials.get(PUMPKIN_POINT_MAT_NAME)
    pumpkin_obj.data.materials.append(skin_mat)
    pumpkin_obj.data.materials.append(stem_mat)
    pumpkin_obj.data.materials.append(point_mat)

def create_pumpkin_individual_geo_ng(obj_geo_node_group, override_create, pumpkin_obj):
    # initialize variables
    tree_nodes = obj_geo_node_group.nodes
    tree_links = obj_geo_node_group.links

    ensure_node_groups(override_create, [PUMPKIN_DEFORM_GEO_NG_NAME, PUMPKIN_GEO_NG_NAME], 'GeometryNodeTree',
                       create_prereq_node_group)
    create_apply_pumpkin_geo_nodes(obj_geo_node_group, tree_nodes, tree_links, pumpkin_obj)

    return obj_geo_node_group

def add_pumpkin_geo_nodes_to_object(pumpkin_obj, override_create):
    geo_nodes_mod = pumpkin_obj.modifiers.new(name="Pumpkin.GeometryNodes", type='NODES')
    create_pumpkin_materials(override_create, pumpkin_obj)
    create_pumpkin_individual_geo_ng(geo_nodes_mod.node_group, override_create, pumpkin_obj)
    geo_nodes_mod["Output_2_attribute_name"] = "stem_height"
    geo_nodes_mod["Output_3_attribute_name"] = "stem_height_pct"
    geo_nodes_mod["Output_4_attribute_name"] = "stem_radial_vec"
    geo_nodes_mod["Output_5_attribute_name"] = "pumpkin_indent"
    geo_nodes_mod["Output_6_attribute_name"] = "top_bot_nub"
    geo_nodes_mod["Output_7_attribute_name"] = "body_h_pct"
    geo_nodes_mod["Output_8_attribute_name"] = "body_radial_vec"
    geo_nodes_mod["Output_9_attribute_name"] = "body_radial_pct"
    geo_nodes_mod["Output_10_attribute_name"] = "inside_pumpkin"

def pot_create_pumpkin(override_create):
    pumpkin_ob = create_mesh_obj_from_pydata(obj_name=PUMPKIN_OBJNAME)
    add_pumpkin_geo_nodes_to_object(pumpkin_ob, override_create)

class BSR_PotCreatePumpkin(bpy.types.Operator):
    bl_description = "Create a Pumpkin with Geometry Nodes mesh and Shader Nodes material. Use Cycles renderer, " + \
        "because EEVEE is very slow to compute Material Shaders on pumpkin skin/stem"
    bl_idname = "big_space_rig.pot_create_character_pumpkin"
    bl_label = "Pumpkin"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        s = context.space_data
        return s.type == 'NODE_EDITOR' and s.node_tree != None and s.tree_type == 'GeometryNodeTree'

    def execute(self, context):
        scn = context.scene
        pot_create_pumpkin(scn.BSR_NodesOverrideCreate)
        return {'FINISHED'}
