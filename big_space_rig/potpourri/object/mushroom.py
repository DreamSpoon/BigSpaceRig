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

MUSHROOM_OBJNAME = "Mushroom"
MUSHROOM_STEM_MAT_NAME = "MushroomStem.Potpourri.BSR.Material"
MUSHROOM_CAP_MAT_NAME = "MushroomCap.Potpourri.BSR.Material"
MUSHROOM_GILL_MAT_NAME = "MushroomGill.Potpourri.BSR.Material"
MUSHROOM_POINT_MAT_NAME = "MushroomPoint.Potpourri.BSR.Material"
MUSHROOM_GEO_NG_NAME = "Mushroom.Potpourri.BSR.GeoNG"

def create_prereq_material(material_name, material):
    if material_name == MUSHROOM_STEM_MAT_NAME:
        return create_mat_mushroom_stem(material)
    elif material_name == MUSHROOM_CAP_MAT_NAME:
        return create_mat_mushroom_cap(material)
    elif material_name == MUSHROOM_GILL_MAT_NAME:
        return create_mat_mushroom_gill(material)
    elif material_name == MUSHROOM_POINT_MAT_NAME:
        return create_mat_mushroom_point(material)

    # error
    print("Unknown name passed to create_prereq_material: " + str(material_name))
    return None

def create_prereq_node_group(node_group_name, node_tree_type):
    if node_tree_type == 'GeometryNodeTree':
        if node_group_name == MUSHROOM_GEO_NG_NAME:
            return create_geo_ng_mushroom()

    # error
    print("Unknown name passed to create_prereq_node_group: " + str(node_group_name))
    return None

def create_geo_ng_mushroom():
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=MUSHROOM_GEO_NG_NAME, type='GeometryNodeTree')
    new_node_group.inputs.new(type='NodeSocketInt', name="Detail")
    new_node_group.inputs.new(type='NodeSocketMaterial', name="Stem Material")
    new_node_group.inputs.new(type='NodeSocketMaterial', name="Cap Material")
    new_node_group.inputs.new(type='NodeSocketMaterial', name="Gill Material")
    new_node_group.inputs.new(type='NodeSocketMaterial', name="Point Material")
    new_node_group.inputs.new(type='NodeSocketFloatDistance', name="Stem Radius")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Stem Height")
    new_node_group.inputs.new(type='NodeSocketVector', name="Stem Top Offset")
    new_node_group.inputs.new(type='NodeSocketFloatDistance', name="Cap Radius")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Cap Height")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Cap Yaw")
    new_node_group.inputs.new(type='NodeSocketFloatAngle', name="Cap Pitch")
    new_node_group.outputs.new(type='NodeSocketGeometry', name="Mesh")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Vertical Factor")
    new_node_group.outputs.new(type='NodeSocketVector', name="Radial Vector")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Is Cap")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Cap Inside")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Cap Outside")
    new_node_group.outputs.new(type='NodeSocketVector', name="Cap Origin")
    new_node_group.outputs.new(type='NodeSocketVector', name="Cap Vertical Vector")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Cap Radial Factor")
    tree_nodes = new_node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (900, -1100)
    new_nodes["Position.009"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (900, -960)
    new_nodes["Separate XYZ.009"] = node

    node = tree_nodes.new(type="GeometryNodeDeleteGeometry")
    node.location = (540, 0)
    node.domain = "POINT"
    node.mode = "ALL"
    new_nodes["Delete Geometry"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (720, -420)
    new_nodes["Position.005"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (720, -220)
    node.operation = "MULTIPLY"
    node.inputs[0].default_value = (-1.0, 1.0, -1.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (540, -300)
    node.operation = "GREATER_THAN"
    node.use_clamp = False
    node.inputs[1].default_value = 0.000100
    node.inputs[2].default_value = 0.500100
    new_nodes["Math.020"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (540, -460)
    new_nodes["Separate XYZ.006"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (540, -600)
    new_nodes["Position.004"] = node

    node = tree_nodes.new(type="GeometryNodeSetPosition")
    node.location = (720, 0)
    node.inputs[3].default_value = (0.0, 0.0, 0.0)
    new_nodes["Set Position.003"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (360, -160)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = 2.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.062"] = node

    node = tree_nodes.new(type="GeometryNodeMeshUVSphere")
    node.location = (540, -160)
    node.inputs[2].default_value = 1.000000
    new_nodes["UV Sphere"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (360, -340)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = 1.000000
    node.inputs[2].default_value = 32.000000
    node.inputs[3].default_value = 2.000000
    node.inputs[4].default_value = 64.000000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range.004"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (900, -600)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.042"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (900, -760)
    node.operation = "MULTIPLY_ADD"
    node.use_clamp = False
    node.inputs[1].default_value = 0.300000
    node.inputs[2].default_value = 1.000000
    new_nodes["Math.039"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1080, -600)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.041"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1080, -760)
    node.operation = "MULTIPLY_ADD"
    node.use_clamp = False
    node.inputs[1].default_value = 0.300000
    node.inputs[2].default_value = 1.000000
    new_nodes["Math.038"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (1260, -460)
    new_nodes["Combine XYZ.008"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1260, -600)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = -0.900000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.040"] = node

    node = tree_nodes.new(type="GeometryNodeSetPosition")
    node.location = (1260, -240)
    node.inputs[3].default_value = (0.0, 0.0, 0.0)
    new_nodes["Set Position.007"] = node

    node = tree_nodes.new(type="GeometryNodeJoinGeometry")
    node.location = (1260, 40)
    new_nodes["Join Geometry.003"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.label = "Capture cap outside"
    node.location = (720, 200)
    node.data_type = "FLOAT"
    node.domain = "FACE"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = 1.000000
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute.010"] = node

    node = tree_nodes.new(type="GeometryNodeMergeByDistance")
    node.location = (1260, 180)
    node.inputs[2].default_value = 0.001000
    new_nodes["Merge by Distance.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-140, -60)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.067"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (40, -60)
    node.operation = "ADD"
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.008"] = node

    node = tree_nodes.new(type="GeometryNodeJoinGeometry")
    node.location = (-320, 40)
    new_nodes["Join Geometry"] = node

    node = tree_nodes.new(type="GeometryNodeSetMaterial")
    node.location = (40, 280)
    new_nodes["Set Material"] = node

    node = tree_nodes.new(type="GeometryNodeCurveToMesh")
    node.location = (-2900, -240)
    node.inputs[2].default_value = False
    new_nodes["Curve to Mesh"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.location = (-2900, -40)
    node.data_type = "FLOAT"
    node.domain = "POINT"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-3080, -960)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.008"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-3080, -800)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = 0.600000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math"] = node

    node = tree_nodes.new(type="GeometryNodeSplineParameter")
    node.location = (-2900, -1020)
    new_nodes["Spline Parameter"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-2900, -840)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[0].default_value = -1.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.064"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.label = "Start Handle"
    node.location = (-3080, -660)
    node.inputs[0].default_value = 0.000000
    node.inputs[1].default_value = 0.000000
    new_nodes["Combine XYZ.001"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.label = "Capture stem radial vec"
    node.location = (-2900, 140)
    node.data_type = "FLOAT_VECTOR"
    node.domain = "POINT"
    node.inputs[2].default_value = 0.000000
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute.006"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.label = "Capture stem radial vec"
    node.location = (-3080, -240)
    node.data_type = "FLOAT_VECTOR"
    node.domain = "POINT"
    node.inputs[2].default_value = 0.000000
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute.005"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (-3080, -560)
    new_nodes["Position.013"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-3080, -440)
    node.operation = "NORMALIZE"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (-3260, 120)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = 1.000000
    node.inputs[2].default_value = 32.000000
    node.inputs[3].default_value = 2.000000
    node.inputs[4].default_value = 64.000000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range.002"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (-3260, -140)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = 1.000000
    node.inputs[2].default_value = 32.000000
    node.inputs[3].default_value = 4.000000
    node.inputs[4].default_value = 64.000000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range.003"] = node

    node = tree_nodes.new(type="GeometryNodeCurvePrimitiveCircle")
    node.location = (-3080, 120)
    node.mode = "RADIUS"
    node.inputs[1].default_value = (-1.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 1.0, 0.0)
    node.inputs[3].default_value = (1.0, 0.0, 0.0)
    new_nodes["Curve Circle"] = node

    node = tree_nodes.new(type="GeometryNodeCurvePrimitiveBezierSegment")
    node.location = (-2900, -580)
    node.mode = "POSITION"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    new_nodes["Bezier Segment"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-3560, -840)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[1].default_value = 0.060000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-3560, -1000)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.label = "End Handle"
    node.location = (-3560, -700)
    new_nodes["Combine XYZ.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-3560, -1320)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.009"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (-3800, -1100)
    new_nodes["Separate XYZ.001"] = node

    node = tree_nodes.new(type="ShaderNodeVectorRotate")
    node.location = (-3360, -920)
    node.invert = False
    node.rotation_type = "AXIS_ANGLE"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 1.0)
    node.inputs[4].default_value = (0.0, 0.0, 0.0)
    new_nodes["Vector Rotate"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (-3360, -1260)
    node.inputs[0].default_value = 1.000000
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 0.000000
    new_nodes["Combine XYZ.012"] = node

    node = tree_nodes.new(type="GeometryNodeSetShadeSmooth")
    node.location = (-2900, 260)
    node.inputs[2].default_value = True
    new_nodes["Set Shade Smooth"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-2340, -100)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.014"] = node

    node = tree_nodes.new(type="GeometryNodeInputNormal")
    node.location = (-2340, -40)
    new_nodes["Normal"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-2340, 100)
    node.operation = "SCALE"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    new_nodes["Vector Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (-1820, -320)
    new_nodes["Combine XYZ.004"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (-1820, -780)
    new_nodes["Separate XYZ.004"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1820, -920)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.010"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1820, -1080)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = 0.500000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.011"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1820, -620)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.015"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1820, -460)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.018"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-2000, -460)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = 0.100000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.019"] = node

    node = tree_nodes.new(type="GeometryNodeMeshCylinder")
    node.location = (-1820, -80)
    node.fill_type = "NONE"
    node.inputs[1].default_value = 1
    node.inputs[2].default_value = 1
    new_nodes["Cylinder"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (-1500, -400)
    new_nodes["Position.014"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-1500, -200)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = (1.0, 1.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.006"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-1500, -80)
    node.operation = "NORMALIZE"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.007"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (-1500, -460)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[3].default_value = -1.000000
    node.inputs[4].default_value = 1.000000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range.008"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.location = (-1320, -80)
    node.data_type = "FLOAT_VECTOR"
    node.domain = "POINT"
    node.inputs[2].default_value = 0.000000
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute.007"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (-660, -900)
    node.inputs[0].default_value = 1.000000
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 0.000000
    new_nodes["Combine XYZ.013"] = node

    node = tree_nodes.new(type="ShaderNodeVectorRotate")
    node.location = (-660, -560)
    node.invert = False
    node.rotation_type = "AXIS_ANGLE"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 1.0)
    node.inputs[4].default_value = (0.0, 0.0, 0.0)
    new_nodes["Vector Rotate.003"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (-660, -500)
    new_nodes["Position.017"] = node

    node = tree_nodes.new(type="ShaderNodeVectorRotate")
    node.location = (-660, -240)
    node.invert = False
    node.rotation_type = "AXIS_ANGLE"
    node.inputs[1].default_value = (0.0, 0.0, -0.019999999552965164)
    node.inputs[4].default_value = (0.0, 0.0, 0.0)
    new_nodes["Vector Rotate.002"] = node

    node = tree_nodes.new(type="GeometryNodeSetPosition")
    node.location = (-660, -80)
    new_nodes["Set Position.001"] = node

    node = tree_nodes.new(type="GeometryNodeSetPosition")
    node.location = (-880, -100)
    node.inputs[3].default_value = (0.0, 0.0, 0.0)
    new_nodes["Set Position.012"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-880, -320)
    node.operation = "MULTIPLY"
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.012"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (-880, -460)
    new_nodes["Position.003"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (-880, -520)
    node.inputs[2].default_value = 1.000000
    new_nodes["Combine XYZ.015"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-2000, -80)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = 0.800000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.017"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (-880, -1160)
    new_nodes["Separate XYZ.014"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (-880, -1300)
    new_nodes["Position.019"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-880, -980)
    node.operation = "DIVIDE"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.066"] = node

    node = tree_nodes.new(type="ShaderNodeFloatCurve")
    node.location = (-980, -660)
    node.mapping.use_clip = True
    node.mapping.clip_min_x = -1.000000
    node.mapping.clip_min_y = -1.000000
    node.mapping.clip_max_x = 1.000000
    node.mapping.clip_max_y = 1.000000
    node.mapping.extend = "EXTRAPOLATED"
    point = node.mapping.curves[0].points[0]
    point.location = (-0.500000, 0.380000)
    point.handle_type = "AUTO"
    point = node.mapping.curves[0].points[1]
    point.location = (0.500000, 0.200000)
    point.handle_type = "AUTO"
    node.mapping.update()
    node.inputs[0].default_value = 1.000000
    new_nodes["Float Curve.001"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.location = (-2900, -380)
    node.data_type = "FLOAT"
    node.domain = "POINT"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute.002"] = node

    node = tree_nodes.new(type="GeometryNodeSetPosition")
    node.location = (-2340, 260)
    new_nodes["Set Position"] = node

    node = tree_nodes.new(type="ShaderNodeFloatCurve")
    node.location = (-2440, -280)
    node.mapping.use_clip = True
    node.mapping.clip_min_x = -1.000000
    node.mapping.clip_min_y = -1.000000
    node.mapping.clip_max_x = 0.000000
    node.mapping.clip_max_y = 1.000000
    node.mapping.extend = "EXTRAPOLATED"
    point = node.mapping.curves[0].points[0]
    point.location = (-1.000000, 0.000000)
    point.handle_type = "AUTO"
    point = node.mapping.curves[0].points[1]
    point.location = (-0.192727, -0.510000)
    point.handle_type = "AUTO"
    point = node.mapping.curves[0].points.new(-0.105455, -0.110000)
    point.handle_type = "AUTO"
    point = node.mapping.curves[0].points.new(-0.050909, -0.555000)
    point.handle_type = "AUTO"
    point = node.mapping.curves[0].points.new(0.000000, -0.600000)
    point.handle_type = "AUTO"
    node.mapping.reset_view()
    node.mapping.update()
    node.inputs[0].default_value = 1.000000
    new_nodes["Float Curve"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.location = (-1320, -260)
    node.data_type = "FLOAT"
    node.domain = "POINT"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute.003"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (-1500, -1200)
    new_nodes["Position.012"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (-1500, -1060)
    new_nodes["Separate XYZ.012"] = node

    node = tree_nodes.new(type="GeometryNodeAttributeStatistic")
    node.location = (-1500, -720)
    node.data_type = "FLOAT"
    node.domain = "POINT"
    new_nodes["Attribute Statistic"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.label = "End"
    node.location = (-3560, -1180)
    new_nodes["Combine XYZ.003"] = node

    node = tree_nodes.new(type="ShaderNodeVectorRotate")
    node.location = (-3360, -700)
    node.invert = False
    node.rotation_type = "AXIS_ANGLE"
    node.inputs[4].default_value = (0.0, 0.0, 0.0)
    new_nodes["Vector Rotate.001"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-3080, 540)
    node.operation = "SUBTRACT"
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.013"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-2900, 540)
    node.operation = "NORMALIZE"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.014"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.location = (40, 140)
    node.data_type = "FLOAT_VECTOR"
    node.domain = "POINT"
    node.inputs[2].default_value = 0.000000
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute.008"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.location = (-140, 140)
    node.data_type = "FLOAT"
    node.domain = "POINT"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute.004"] = node

    node = tree_nodes.new(type="GeometryNodeSetMaterial")
    node.location = (1260, 320)
    new_nodes["Set Material.001"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.label = "Capture cap inside"
    node.location = (1260, -40)
    node.data_type = "FLOAT"
    node.domain = "FACE"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = 1.000000
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute.009"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (1180, -1200)
    new_nodes["Separate XYZ.008"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (1180, -1340)
    new_nodes["Position.008"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (2000, -600)
    new_nodes["Combine XYZ.006"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1820, -760)
    node.operation = "SINE"
    node.use_clamp = False
    node.inputs[1].default_value = 0.500000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.028"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (2000, -760)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.030"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (2540, -600)
    new_nodes["Combine XYZ.007"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (2360, -760)
    node.operation = "SINE"
    node.use_clamp = False
    node.inputs[1].default_value = 0.500000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.033"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (2360, -600)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = -1.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.036"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (2540, -760)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.035"] = node

    node = tree_nodes.new(type="ShaderNodeValue")
    node.location = (1640, -920)
    node.outputs[0].default_value = -0.031416
    new_nodes["Value"] = node

    node = tree_nodes.new(type="GeometryNodeJoinGeometry")
    node.location = (2540, -280)
    new_nodes["Join Geometry.002"] = node

    node = tree_nodes.new(type="GeometryNodeSetPosition")
    node.location = (2000, -220)
    node.inputs[3].default_value = (0.0, 0.0, 0.0)
    new_nodes["Set Position.005"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1640, -1480)
    node.operation = "SQRT"
    node.use_clamp = False
    node.inputs[1].default_value = 0.500000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.024"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1640, -1620)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[0].default_value = 1.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.025"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1640, -1780)
    node.operation = "POWER"
    node.use_clamp = False
    node.inputs[1].default_value = 2.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.026"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1640, -1320)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.022"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1460, -1320)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[1].default_value = 0.500000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.021"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1640, -1160)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = 0.800000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.027"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1820, -920)
    node.operation = "COSINE"
    node.use_clamp = False
    node.inputs[1].default_value = 0.500000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.029"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (2000, -920)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.031"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (2360, -920)
    node.operation = "COSINE"
    node.use_clamp = False
    node.inputs[1].default_value = 0.500000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.032"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (2540, -920)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.034"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (2180, -920)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = -1.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.037"] = node

    node = tree_nodes.new(type="GeometryNodeSetPosition")
    node.location = (2540, -380)
    node.inputs[3].default_value = (0.0, 0.0, 0.0)
    new_nodes["Set Position.006"] = node

    node = tree_nodes.new(type="GeometryNodeMergeByDistance")
    node.location = (2540, -140)
    node.inputs[2].default_value = 0.001000
    new_nodes["Merge by Distance.002"] = node

    node = tree_nodes.new(type="GeometryNodeSetPosition")
    node.location = (3900, -440)
    node.inputs[3].default_value = (0.0, 0.0, 0.0)
    new_nodes["Set Position.008"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (3900, -660)
    new_nodes["Combine XYZ.009"] = node

    node = tree_nodes.new(type="GeometryNodeGeometryToInstance")
    node.location = (3900, -300)
    new_nodes["Geometry to Instance"] = node

    node = tree_nodes.new(type="GeometryNodeInstanceOnPoints")
    node.location = (3900, -20)
    node.inputs[3].default_value = False
    node.inputs[6].default_value = (1.0, 1.0, 1.0)
    new_nodes["Instance on Points"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (3160, -20)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = -0.500000
    node.inputs[2].default_value = 0.500000
    node.inputs[3].default_value = 0.000000
    node.inputs[4].default_value = 1.000000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range.001"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (3160, -280)
    new_nodes["Separate XYZ.011"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (3160, 140)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.061"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (2980, 140)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[0].default_value = 3.141593
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.052"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (3160, -420)
    new_nodes["Position.011"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (2980, -20)
    node.operation = "DIVIDE"
    node.use_clamp = False
    node.inputs[0].default_value = 3.141593
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.054"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.location = (3520, 140)
    node.data_type = "FLOAT_VECTOR"
    node.domain = "POINT"
    node.inputs[2].default_value = 0.000000
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute"] = node

    node = tree_nodes.new(type="GeometryNodeSetPosition")
    node.location = (3700, 140)
    node.inputs[3].default_value = (0.0, 0.0, 0.0)
    new_nodes["Set Position.009"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (3340, -20)
    node.inputs[0].default_value = 0.000000
    node.inputs[1].default_value = 0.000000
    new_nodes["Combine XYZ.011"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.label = "Zero position"
    node.location = (3700, -80)
    node.inputs[0].default_value = 0.000000
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 0.000000
    new_nodes["Combine XYZ.010"] = node

    node = tree_nodes.new(type="GeometryNodeMeshGrid")
    node.location = (3340, 140)
    node.inputs[0].default_value = 1.000000
    node.inputs[1].default_value = 1.000000
    node.inputs[3].default_value = 1
    new_nodes["Grid.001"] = node

    node = tree_nodes.new(type="GeometryNodeRealizeInstances")
    node.location = (3900, 80)
    node.legacy_behavior = False
    new_nodes["Realize Instances"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (3900, -800)
    node.operation = "MULTIPLY_ADD"
    node.use_clamp = False
    new_nodes["Math.050"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (3900, -1000)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = -1.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.051"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (3900, -1160)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.049"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (3680, -540)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.057"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (3680, -720)
    node.operation = "SIGN"
    node.use_clamp = False
    node.inputs[1].default_value = 0.500000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.056"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (3500, -540)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[0].default_value = 1.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.060"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (3500, -720)
    node.operation = "POWER"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.055"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (3500, -900)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 0.800000
    node.inputs[3].default_value = 0.500000
    node.inputs[4].default_value = 1.000000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (3320, -720)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[0].default_value = 1.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.059"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (3140, -1240)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.048"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (3140, -1060)
    node.operation = "MULTIPLY_ADD"
    node.use_clamp = False
    new_nodes["Math.047"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (2960, -1380)
    node.operation = "COSINE"
    node.use_clamp = False
    node.inputs[1].default_value = 0.500000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.046"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (2960, -1240)
    node.operation = "SINE"
    node.use_clamp = False
    node.inputs[1].default_value = 0.500000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.045"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (2420, -1360)
    node.operation = "SINE"
    node.use_clamp = False
    node.inputs[1].default_value = 0.500000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.043"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (2600, -1360)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = 0.300000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.044"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (2780, -1360)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.053"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (2220, -1160)
    new_nodes["Separate XYZ.010"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (2220, -1300)
    new_nodes["Position.010"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (3320, -900)
    node.operation = "ABSOLUTE"
    node.use_clamp = False
    node.inputs[1].default_value = 0.500000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.058"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (1640, -480)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = 5.000000
    node.inputs[2].default_value = 32.000000
    node.inputs[3].default_value = 2.000000
    node.inputs[4].default_value = 11.000000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range.006"] = node

    node = tree_nodes.new(type="GeometryNodeMeshGrid")
    node.location = (2000, -440)
    node.inputs[0].default_value = 2.000000
    node.inputs[1].default_value = 1.000000
    new_nodes["Grid"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1820, -300)
    node.operation = "MULTIPLY_ADD"
    node.use_clamp = False
    node.inputs[1].default_value = 2.000000
    node.inputs[2].default_value = 1.000000
    new_nodes["Math.063"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (1640, -220)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = 4.000000
    node.inputs[2].default_value = 32.000000
    node.inputs[3].default_value = 1.000000
    node.inputs[4].default_value = 16.000000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range.005"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (2800, 140)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = 3.000000
    node.inputs[2].default_value = 9.000000
    node.inputs[3].default_value = 2.000000
    node.inputs[4].default_value = 32.000000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range.007"] = node

    node = tree_nodes.new(type="GeometryNodeSetMaterial")
    node.location = (3900, 220)
    new_nodes["Set Material.002"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (4380, -680)
    new_nodes["Position.006"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (4380, -540)
    new_nodes["Separate XYZ.007"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (4200, 120)
    node.operation = "NORMALIZE"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.004"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (4200, 0)
    new_nodes["Position.007"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (4380, -20)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.023"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (4380, 120)
    node.operation = "SCALE"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    new_nodes["Vector Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeFloatCurve")
    node.location = (4280, -200)
    node.mapping.use_clip = True
    node.mapping.clip_min_x = 0.000000
    node.mapping.clip_min_y = -10.000000
    node.mapping.clip_max_x = 1.000000
    node.mapping.clip_max_y = 10.000000
    node.mapping.extend = "EXTRAPOLATED"
    point = node.mapping.curves[0].points[0]
    point.location = (0.000000, -1.240003)
    point.handle_type = "AUTO_CLAMPED"
    point = node.mapping.curves[0].points[1]
    point.location = (0.227273, 0.999998)
    point.handle_type = "AUTO_CLAMPED"
    point = node.mapping.curves[0].points.new(0.687273, -1.845001)
    point.handle_type = "AUTO_CLAMPED"
    point = node.mapping.curves[0].points.new(1.000000, -0.000000)
    point.handle_type = "AUTO_CLAMPED"
    node.mapping.reset_view()
    node.mapping.update()
    node.inputs[0].default_value = 1.000000
    new_nodes["Float Curve.002"] = node

    node = tree_nodes.new(type="GeometryNodeSetPosition")
    node.location = (4580, 340)
    new_nodes["Set Position.010"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (4780, -140)
    new_nodes["Position.015"] = node

    node = tree_nodes.new(type="GeometryNodeAttributeStatistic")
    node.location = (4780, 340)
    node.data_type = "FLOAT"
    node.domain = "POINT"
    new_nodes["Attribute Statistic.001"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (4780, 0)
    new_nodes["Separate XYZ.013"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (4960, 340)
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
    new_nodes["Map Range.009"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (5160, 340)
    node.operation = "NORMALIZE"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.009"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (5160, 220)
    node.operation = "MULTIPLY"
    node.inputs[0].default_value = (1.0, 1.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.010"] = node

    node = tree_nodes.new(type="GeometryNodeSetPosition")
    node.location = (4380, 280)
    new_nodes["Set Position.004"] = node

    node = tree_nodes.new(type="GeometryNodeJoinGeometry")
    node.location = (4580, 440)
    new_nodes["Join Geometry.004"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (5160, 20)
    new_nodes["Position.016"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (5640, 40)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = (1.0, 1.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.017"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (5640, -160)
    new_nodes["Position.020"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (5460, 180)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = (1.0, 1.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.016"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (5640, 180)
    node.operation = "DISTANCE"
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.015"] = node

    node = tree_nodes.new(type="GeometryNodeAttributeStatistic")
    node.location = (5820, 180)
    node.data_type = "FLOAT"
    node.domain = "POINT"
    new_nodes["Attribute Statistic.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (5820, 340)
    node.operation = "DIVIDE"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.location = (5160, 540)
    node.data_type = "FLOAT_VECTOR"
    node.domain = "FACE"
    node.inputs[2].default_value = 1.000000
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute.012"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.location = (4960, 540)
    node.data_type = "FLOAT"
    node.domain = "FACE"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute.011"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.location = (5820, 540)
    node.data_type = "FLOAT"
    node.domain = "POINT"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute.015"] = node

    node = tree_nodes.new(type="ShaderNodeVectorRotate")
    node.location = (6360, 320)
    node.invert = False
    node.rotation_type = "AXIS_ANGLE"
    node.inputs[4].default_value = (0.0, 0.0, 0.0)
    new_nodes["Vector Rotate.005"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (6360, 120)
    new_nodes["Position.018"] = node

    node = tree_nodes.new(type="ShaderNodeVectorRotate")
    node.location = (6360, 60)
    node.invert = False
    node.rotation_type = "AXIS_ANGLE"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 1.0)
    node.inputs[4].default_value = (0.0, 0.0, 0.0)
    new_nodes["Vector Rotate.004"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (6360, -260)
    node.inputs[0].default_value = 1.000000
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 0.000000
    new_nodes["Combine XYZ.014"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (6680, 380)
    node.operation = "MULTIPLY"
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (6680, 220)
    new_nodes["Position"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (6680, 160)
    new_nodes["Combine XYZ.005"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (6680, -160)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.016"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (6680, -320)
    new_nodes["Separate XYZ.005"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (6680, -20)
    new_nodes["Combine XYZ"] = node

    node = tree_nodes.new(type="GeometryNodeSetPosition")
    node.location = (6680, 540)
    new_nodes["Set Position.002"] = node

    node = tree_nodes.new(type="GeometryNodeJoinGeometry")
    node.location = (6680, 640)
    new_nodes["Join Geometry.001"] = node

    node = tree_nodes.new(type="GeometryNodeSetPosition")
    node.location = (6360, 540)
    node.inputs[3].default_value = (0.0, 0.0, 0.0)
    new_nodes["Set Position.011"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.location = (6080, 540)
    node.data_type = "FLOAT"
    node.domain = "POINT"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = 1.000000
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute.016"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (6960, -20)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.065"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.label = "Capture cap height factor"
    node.location = (6960, 180)
    node.data_type = "FLOAT"
    node.domain = "FACE"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute.013"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.label = "Capture cap height factor"
    node.location = (6960, 500)
    node.data_type = "FLOAT_VECTOR"
    node.domain = "FACE"
    node.inputs[2].default_value = 1.000000
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute.014"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (6960, 320)
    node.operation = "ADD"
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.011"] = node

    node = tree_nodes.new(type="GeometryNodeSetShadeSmooth")
    node.location = (6960, 640)
    node.inputs[2].default_value = True
    new_nodes["Set Shade Smooth.001"] = node

    node = tree_nodes.new(type="FunctionNodeCompare")
    node.location = (7680, 480)
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
    node.location = (7680, 640)
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

    node = tree_nodes.new(type="GeometryNodeSetMaterial")
    node.location = (7680, 320)
    new_nodes["Set Material.003"] = node

    node = tree_nodes.new(type="GeometryNodeMeshToPoints")
    node.location = (7680, 200)
    node.mode = "VERTICES"
    node.inputs[3].default_value = 0.050000
    new_nodes["Mesh to Points"] = node

    node = tree_nodes.new(type="GeometryNodeMeshLine")
    node.location = (7680, 20)
    node.count_mode = "TOTAL"
    node.mode = "OFFSET"
    node.inputs[0].default_value = 1
    node.inputs[1].default_value = 1.000000
    node.inputs[2].default_value = (0.0, 0.0, 0.05000000074505806)
    node.inputs[3].default_value = (0.0, 0.0, 1.0)
    new_nodes["Mesh Line"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-4360, -400)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (8000, 900)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Capture Attribute.005"].outputs[0], new_nodes["Curve to Mesh"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Set Material"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Curve Circle"].inputs[4])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Combine XYZ.001"].inputs[2])
    tree_links.new(new_nodes["Combine XYZ.001"].outputs[0], new_nodes["Bezier Segment"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[7], new_nodes["Separate XYZ.001"].inputs[0])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Combine XYZ.002"].inputs[2])
    tree_links.new(new_nodes["Math.003"].outputs[0], new_nodes["Math.001"].inputs[0])
    tree_links.new(new_nodes["Math.009"].outputs[0], new_nodes["Combine XYZ.003"].inputs[2])
    tree_links.new(new_nodes["Math.008"].outputs[0], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[0], new_nodes["Combine XYZ.002"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[1], new_nodes["Combine XYZ.002"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[2], new_nodes["Math.003"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Math.008"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[2], new_nodes["Math.008"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[1], new_nodes["Combine XYZ.003"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Math.009"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[2], new_nodes["Math.009"].inputs[0])
    tree_links.new(new_nodes["Combine XYZ.003"].outputs[0], new_nodes["Bezier Segment"].inputs[4])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[0], new_nodes["Combine XYZ.003"].inputs[0])
    tree_links.new(new_nodes["Set Position.001"].outputs[0], new_nodes["Join Geometry"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Cylinder"].inputs[3])
    tree_links.new(new_nodes["Math.017"].outputs[0], new_nodes["Cylinder"].inputs[4])
    tree_links.new(new_nodes["Combine XYZ.004"].outputs[0], new_nodes["Set Position.001"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Math.010"].inputs[0])
    tree_links.new(new_nodes["Math.011"].outputs[0], new_nodes["Math.010"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[9], new_nodes["Math.011"].inputs[0])
    tree_links.new(new_nodes["Normal"].outputs[0], new_nodes["Vector Math.003"].inputs[0])
    tree_links.new(new_nodes["Math.014"].outputs[0], new_nodes["Vector Math.003"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Math.014"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[7], new_nodes["Separate XYZ.004"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.004"].outputs[0], new_nodes["Combine XYZ.004"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.004"].outputs[1], new_nodes["Combine XYZ.004"].inputs[1])
    tree_links.new(new_nodes["Math.010"].outputs[0], new_nodes["Math.015"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.004"].outputs[2], new_nodes["Math.015"].inputs[0])
    tree_links.new(new_nodes["Set Material"].outputs[0], new_nodes["Join Geometry.001"].inputs[0])
    tree_links.new(new_nodes["Set Position.002"].outputs[0], new_nodes["Join Geometry.001"].inputs[0])
    tree_links.new(new_nodes["Vector Math"].outputs[0], new_nodes["Set Position.002"].inputs[2])
    tree_links.new(new_nodes["Position"].outputs[0], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Combine XYZ"].outputs[0], new_nodes["Set Position.002"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[7], new_nodes["Separate XYZ.005"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.005"].outputs[0], new_nodes["Combine XYZ"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.005"].outputs[1], new_nodes["Combine XYZ"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.005"].outputs[2], new_nodes["Math.016"].inputs[0])
    tree_links.new(new_nodes["Math.016"].outputs[0], new_nodes["Combine XYZ"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Math.016"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[8], new_nodes["Combine XYZ.005"].inputs[0])
    tree_links.new(new_nodes["Combine XYZ.005"].outputs[0], new_nodes["Vector Math"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[8], new_nodes["Combine XYZ.005"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[9], new_nodes["Math.017"].inputs[0])
    tree_links.new(new_nodes["Math.015"].outputs[0], new_nodes["Math.018"].inputs[0])
    tree_links.new(new_nodes["Math.018"].outputs[0], new_nodes["Combine XYZ.004"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[9], new_nodes["Math.019"].inputs[0])
    tree_links.new(new_nodes["Math.019"].outputs[0], new_nodes["Math.018"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[9], new_nodes["Combine XYZ.005"].inputs[2])
    tree_links.new(new_nodes["UV Sphere"].outputs[0], new_nodes["Delete Geometry"].inputs[0])
    tree_links.new(new_nodes["Math.020"].outputs[0], new_nodes["Delete Geometry"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.006"].outputs[2], new_nodes["Math.020"].inputs[0])
    tree_links.new(new_nodes["Position.004"].outputs[0], new_nodes["Separate XYZ.006"].inputs[0])
    tree_links.new(new_nodes["Delete Geometry"].outputs[0], new_nodes["Set Position.003"].inputs[0])
    tree_links.new(new_nodes["Vector Math.001"].outputs[0], new_nodes["Set Position.003"].inputs[2])
    tree_links.new(new_nodes["Position.005"].outputs[0], new_nodes["Vector Math.001"].inputs[1])
    tree_links.new(new_nodes["Position.006"].outputs[0], new_nodes["Separate XYZ.007"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.007"].outputs[2], new_nodes["Float Curve.002"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[9], new_nodes["Math.023"].inputs[1])
    tree_links.new(new_nodes["Vector Math.002"].outputs[0], new_nodes["Set Position.004"].inputs[3])
    tree_links.new(new_nodes["Float Curve.002"].outputs[0], new_nodes["Math.023"].inputs[0])
    tree_links.new(new_nodes["Position.007"].outputs[0], new_nodes["Vector Math.004"].inputs[0])
    tree_links.new(new_nodes["Vector Math.004"].outputs[0], new_nodes["Vector Math.002"].inputs[0])
    tree_links.new(new_nodes["Set Position.005"].outputs[0], new_nodes["Join Geometry.002"].inputs[0])
    tree_links.new(new_nodes["Grid"].outputs[0], new_nodes["Set Position.005"].inputs[0])
    tree_links.new(new_nodes["Position.008"].outputs[0], new_nodes["Separate XYZ.008"].inputs[0])
    tree_links.new(new_nodes["Combine XYZ.006"].outputs[0], new_nodes["Set Position.005"].inputs[2])
    tree_links.new(new_nodes["Separate XYZ.008"].outputs[0], new_nodes["Combine XYZ.006"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.008"].outputs[1], new_nodes["Math.021"].inputs[0])
    tree_links.new(new_nodes["Math.021"].outputs[0], new_nodes["Math.022"].inputs[0])
    tree_links.new(new_nodes["Math.025"].outputs[0], new_nodes["Math.024"].inputs[0])
    tree_links.new(new_nodes["Math.026"].outputs[0], new_nodes["Math.025"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.008"].outputs[0], new_nodes["Math.026"].inputs[0])
    tree_links.new(new_nodes["Math.024"].outputs[0], new_nodes["Math.022"].inputs[1])
    tree_links.new(new_nodes["Math.022"].outputs[0], new_nodes["Math.027"].inputs[0])
    tree_links.new(new_nodes["Value"].outputs[0], new_nodes["Math.028"].inputs[0])
    tree_links.new(new_nodes["Value"].outputs[0], new_nodes["Math.029"].inputs[0])
    tree_links.new(new_nodes["Math.028"].outputs[0], new_nodes["Math.030"].inputs[1])
    tree_links.new(new_nodes["Math.027"].outputs[0], new_nodes["Math.030"].inputs[0])
    tree_links.new(new_nodes["Math.027"].outputs[0], new_nodes["Math.031"].inputs[0])
    tree_links.new(new_nodes["Math.029"].outputs[0], new_nodes["Math.031"].inputs[1])
    tree_links.new(new_nodes["Math.031"].outputs[0], new_nodes["Combine XYZ.006"].inputs[2])
    tree_links.new(new_nodes["Math.030"].outputs[0], new_nodes["Combine XYZ.006"].inputs[1])
    tree_links.new(new_nodes["Combine XYZ.007"].outputs[0], new_nodes["Set Position.006"].inputs[2])
    tree_links.new(new_nodes["Math.036"].outputs[0], new_nodes["Combine XYZ.007"].inputs[0])
    tree_links.new(new_nodes["Math.033"].outputs[0], new_nodes["Math.035"].inputs[1])
    tree_links.new(new_nodes["Math.027"].outputs[0], new_nodes["Math.035"].inputs[0])
    tree_links.new(new_nodes["Math.027"].outputs[0], new_nodes["Math.034"].inputs[0])
    tree_links.new(new_nodes["Math.032"].outputs[0], new_nodes["Math.034"].inputs[1])
    tree_links.new(new_nodes["Math.034"].outputs[0], new_nodes["Combine XYZ.007"].inputs[2])
    tree_links.new(new_nodes["Math.035"].outputs[0], new_nodes["Combine XYZ.007"].inputs[1])
    tree_links.new(new_nodes["Set Position.006"].outputs[0], new_nodes["Join Geometry.002"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.008"].outputs[0], new_nodes["Math.036"].inputs[0])
    tree_links.new(new_nodes["Grid"].outputs[0], new_nodes["Set Position.006"].inputs[0])
    tree_links.new(new_nodes["Value"].outputs[0], new_nodes["Math.037"].inputs[0])
    tree_links.new(new_nodes["Math.037"].outputs[0], new_nodes["Math.032"].inputs[0])
    tree_links.new(new_nodes["Math.037"].outputs[0], new_nodes["Math.033"].inputs[0])
    tree_links.new(new_nodes["Delete Geometry"].outputs[0], new_nodes["Set Position.007"].inputs[0])
    tree_links.new(new_nodes["Join Geometry.003"].outputs[0], new_nodes["Merge by Distance.001"].inputs[0])
    tree_links.new(new_nodes["Join Geometry.002"].outputs[0], new_nodes["Merge by Distance.002"].inputs[0])
    tree_links.new(new_nodes["Position.009"].outputs[0], new_nodes["Separate XYZ.009"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.009"].outputs[2], new_nodes["Math.038"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.009"].outputs[2], new_nodes["Math.039"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.009"].outputs[2], new_nodes["Math.040"].inputs[0])
    tree_links.new(new_nodes["Math.040"].outputs[0], new_nodes["Combine XYZ.008"].inputs[2])
    tree_links.new(new_nodes["Combine XYZ.008"].outputs[0], new_nodes["Set Position.007"].inputs[2])
    tree_links.new(new_nodes["Math.038"].outputs[0], new_nodes["Math.041"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.009"].outputs[0], new_nodes["Math.041"].inputs[1])
    tree_links.new(new_nodes["Math.041"].outputs[0], new_nodes["Combine XYZ.008"].inputs[0])
    tree_links.new(new_nodes["Math.039"].outputs[0], new_nodes["Math.042"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.009"].outputs[1], new_nodes["Math.042"].inputs[1])
    tree_links.new(new_nodes["Math.042"].outputs[0], new_nodes["Combine XYZ.008"].inputs[1])
    tree_links.new(new_nodes["Math.023"].outputs[0], new_nodes["Vector Math.002"].inputs[3])
    tree_links.new(new_nodes["Merge by Distance.002"].outputs[0], new_nodes["Set Position.008"].inputs[0])
    tree_links.new(new_nodes["Position.010"].outputs[0], new_nodes["Separate XYZ.010"].inputs[0])
    tree_links.new(new_nodes["Combine XYZ.009"].outputs[0], new_nodes["Set Position.008"].inputs[2])
    tree_links.new(new_nodes["Separate XYZ.010"].outputs[1], new_nodes["Combine XYZ.009"].inputs[1])
    tree_links.new(new_nodes["Math.043"].outputs[0], new_nodes["Math.044"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.010"].outputs[0], new_nodes["Math.043"].inputs[0])
    tree_links.new(new_nodes["Math.044"].outputs[0], new_nodes["Math.053"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.010"].outputs[2], new_nodes["Math.053"].inputs[1])
    tree_links.new(new_nodes["Math.053"].outputs[0], new_nodes["Math.045"].inputs[0])
    tree_links.new(new_nodes["Math.053"].outputs[0], new_nodes["Math.046"].inputs[0])
    tree_links.new(new_nodes["Math.045"].outputs[0], new_nodes["Math.047"].inputs[0])
    tree_links.new(new_nodes["Math.046"].outputs[0], new_nodes["Math.048"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.010"].outputs[0], new_nodes["Math.048"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.010"].outputs[1], new_nodes["Math.047"].inputs[1])
    tree_links.new(new_nodes["Math.048"].outputs[0], new_nodes["Math.047"].inputs[2])
    tree_links.new(new_nodes["Math.045"].outputs[0], new_nodes["Math.050"].inputs[0])
    tree_links.new(new_nodes["Math.046"].outputs[0], new_nodes["Math.049"].inputs[0])
    tree_links.new(new_nodes["Math.049"].outputs[0], new_nodes["Math.050"].inputs[2])
    tree_links.new(new_nodes["Separate XYZ.010"].outputs[2], new_nodes["Math.049"].inputs[1])
    tree_links.new(new_nodes["Math.051"].outputs[0], new_nodes["Math.050"].inputs[1])
    tree_links.new(new_nodes["Math.050"].outputs[0], new_nodes["Combine XYZ.009"].inputs[2])
    tree_links.new(new_nodes["Separate XYZ.010"].outputs[0], new_nodes["Math.051"].inputs[0])
    tree_links.new(new_nodes["Math.059"].outputs[0], new_nodes["Math.055"].inputs[0])
    tree_links.new(new_nodes["Math.047"].outputs[0], new_nodes["Math.056"].inputs[0])
    tree_links.new(new_nodes["Math.060"].outputs[0], new_nodes["Math.057"].inputs[0])
    tree_links.new(new_nodes["Math.056"].outputs[0], new_nodes["Math.057"].inputs[1])
    tree_links.new(new_nodes["Math.047"].outputs[0], new_nodes["Math.058"].inputs[0])
    tree_links.new(new_nodes["Math.057"].outputs[0], new_nodes["Combine XYZ.009"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.010"].outputs[2], new_nodes["Map Range"].inputs[0])
    tree_links.new(new_nodes["Map Range"].outputs[0], new_nodes["Math.055"].inputs[1])
    tree_links.new(new_nodes["Math.058"].outputs[0], new_nodes["Math.059"].inputs[1])
    tree_links.new(new_nodes["Math.055"].outputs[0], new_nodes["Math.060"].inputs[1])
    tree_links.new(new_nodes["Set Position.008"].outputs[0], new_nodes["Geometry to Instance"].inputs[0])
    tree_links.new(new_nodes["Geometry to Instance"].outputs[0], new_nodes["Instance on Points"].inputs[2])
    tree_links.new(new_nodes["Set Position.009"].outputs[0], new_nodes["Instance on Points"].inputs[0])
    tree_links.new(new_nodes["Grid.001"].outputs[0], new_nodes["Capture Attribute"].inputs[0])
    tree_links.new(new_nodes["Position.011"].outputs[0], new_nodes["Separate XYZ.011"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute"].outputs[0], new_nodes["Set Position.009"].inputs[0])
    tree_links.new(new_nodes["Combine XYZ.010"].outputs[0], new_nodes["Set Position.009"].inputs[2])
    tree_links.new(new_nodes["Capture Attribute"].outputs[1], new_nodes["Instance on Points"].inputs[5])
    tree_links.new(new_nodes["Combine XYZ.011"].outputs[0], new_nodes["Capture Attribute"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.011"].outputs[0], new_nodes["Map Range.001"].inputs[0])
    tree_links.new(new_nodes["Math.054"].outputs[0], new_nodes["Math.052"].inputs[1])
    tree_links.new(new_nodes["Math.052"].outputs[0], new_nodes["Math.061"].inputs[0])
    tree_links.new(new_nodes["Math.061"].outputs[0], new_nodes["Combine XYZ.011"].inputs[2])
    tree_links.new(new_nodes["Map Range.001"].outputs[0], new_nodes["Math.061"].inputs[1])
    tree_links.new(new_nodes["Instance on Points"].outputs[0], new_nodes["Realize Instances"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Map Range.002"].inputs[0])
    tree_links.new(new_nodes["Map Range.002"].outputs[0], new_nodes["Bezier Segment"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Map Range.003"].inputs[0])
    tree_links.new(new_nodes["Map Range.003"].outputs[0], new_nodes["Curve Circle"].inputs[0])
    tree_links.new(new_nodes["Map Range.003"].outputs[0], new_nodes["Cylinder"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Map Range.004"].inputs[0])
    tree_links.new(new_nodes["Map Range.004"].outputs[0], new_nodes["Math.062"].inputs[0])
    tree_links.new(new_nodes["Math.062"].outputs[0], new_nodes["UV Sphere"].inputs[0])
    tree_links.new(new_nodes["Math.062"].outputs[0], new_nodes["UV Sphere"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Map Range.005"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Map Range.006"].inputs[0])
    tree_links.new(new_nodes["Map Range.006"].outputs[0], new_nodes["Grid"].inputs[3])
    tree_links.new(new_nodes["Map Range.005"].outputs[0], new_nodes["Math.063"].inputs[0])
    tree_links.new(new_nodes["Math.063"].outputs[0], new_nodes["Grid"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Map Range.007"].inputs[0])
    tree_links.new(new_nodes["Map Range.007"].outputs[0], new_nodes["Math.054"].inputs[1])
    tree_links.new(new_nodes["Map Range.007"].outputs[0], new_nodes["Grid.001"].inputs[2])
    tree_links.new(new_nodes["Capture Attribute.002"].outputs[2], new_nodes["Capture Attribute.001"].inputs[2])
    tree_links.new(new_nodes["Math.064"].outputs[0], new_nodes["Capture Attribute.002"].inputs[2])
    tree_links.new(new_nodes["Bezier Segment"].outputs[0], new_nodes["Capture Attribute.002"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.002"].outputs[0], new_nodes["Curve to Mesh"].inputs[0])
    tree_links.new(new_nodes["Curve to Mesh"].outputs[0], new_nodes["Capture Attribute.001"].inputs[0])
    tree_links.new(new_nodes["Cylinder"].outputs[0], new_nodes["Capture Attribute.003"].inputs[0])
    tree_links.new(new_nodes["Map Range.008"].outputs[0], new_nodes["Capture Attribute.003"].inputs[2])
    tree_links.new(new_nodes["Separate XYZ.012"].outputs[2], new_nodes["Map Range.008"].inputs[0])
    tree_links.new(new_nodes["Position.012"].outputs[0], new_nodes["Separate XYZ.012"].inputs[0])
    tree_links.new(new_nodes["Join Geometry"].outputs[0], new_nodes["Capture Attribute.004"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.001"].outputs[2], new_nodes["Math.067"].inputs[0])
    tree_links.new(new_nodes["Math.067"].outputs[0], new_nodes["Capture Attribute.004"].inputs[2])
    tree_links.new(new_nodes["Cylinder"].outputs[0], new_nodes["Attribute Statistic"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.012"].outputs[2], new_nodes["Attribute Statistic"].inputs[2])
    tree_links.new(new_nodes["Attribute Statistic"].outputs[3], new_nodes["Map Range.008"].inputs[1])
    tree_links.new(new_nodes["Attribute Statistic"].outputs[4], new_nodes["Map Range.008"].inputs[2])
    tree_links.new(new_nodes["Capture Attribute.003"].outputs[2], new_nodes["Math.067"].inputs[1])
    tree_links.new(new_nodes["Spline Parameter"].outputs[0], new_nodes["Math.064"].inputs[1])
    tree_links.new(new_nodes["Capture Attribute.008"].outputs[0], new_nodes["Set Material"].inputs[0])
    tree_links.new(new_nodes["Curve Circle"].outputs[0], new_nodes["Capture Attribute.005"].inputs[0])
    tree_links.new(new_nodes["Vector Math.005"].outputs[0], new_nodes["Capture Attribute.005"].inputs[1])
    tree_links.new(new_nodes["Position.013"].outputs[0], new_nodes["Vector Math.005"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.001"].outputs[0], new_nodes["Capture Attribute.006"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.006"].outputs[0], new_nodes["Set Shade Smooth"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.005"].outputs[1], new_nodes["Capture Attribute.006"].inputs[1])
    tree_links.new(new_nodes["Capture Attribute.003"].outputs[0], new_nodes["Capture Attribute.007"].inputs[0])
    tree_links.new(new_nodes["Set Position.012"].outputs[0], new_nodes["Set Position.001"].inputs[0])
    tree_links.new(new_nodes["Position.014"].outputs[0], new_nodes["Vector Math.006"].inputs[0])
    tree_links.new(new_nodes["Vector Math.006"].outputs[0], new_nodes["Vector Math.007"].inputs[0])
    tree_links.new(new_nodes["Vector Math.007"].outputs[0], new_nodes["Capture Attribute.007"].inputs[1])
    tree_links.new(new_nodes["Capture Attribute.004"].outputs[0], new_nodes["Capture Attribute.008"].inputs[0])
    tree_links.new(new_nodes["Vector Math.008"].outputs[0], new_nodes["Capture Attribute.008"].inputs[1])
    tree_links.new(new_nodes["Capture Attribute.007"].outputs[1], new_nodes["Vector Math.008"].inputs[1])
    tree_links.new(new_nodes["Capture Attribute.006"].outputs[1], new_nodes["Vector Math.008"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Set Material.001"].inputs[2])
    tree_links.new(new_nodes["Set Position.007"].outputs[0], new_nodes["Capture Attribute.009"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.009"].outputs[0], new_nodes["Join Geometry.003"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.009"].outputs[2], new_nodes["Group Output"].inputs[4])
    tree_links.new(new_nodes["Set Position.003"].outputs[0], new_nodes["Capture Attribute.010"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.010"].outputs[0], new_nodes["Join Geometry.003"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.010"].outputs[2], new_nodes["Group Output"].inputs[5])
    tree_links.new(new_nodes["Attribute Statistic.001"].outputs[3], new_nodes["Map Range.009"].inputs[1])
    tree_links.new(new_nodes["Attribute Statistic.001"].outputs[4], new_nodes["Map Range.009"].inputs[2])
    tree_links.new(new_nodes["Map Range.009"].outputs[0], new_nodes["Capture Attribute.011"].inputs[2])
    tree_links.new(new_nodes["Separate XYZ.013"].outputs[2], new_nodes["Attribute Statistic.001"].inputs[2])
    tree_links.new(new_nodes["Separate XYZ.013"].outputs[2], new_nodes["Map Range.009"].inputs[0])
    tree_links.new(new_nodes["Position.015"].outputs[0], new_nodes["Separate XYZ.013"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.011"].outputs[0], new_nodes["Capture Attribute.012"].inputs[0])
    tree_links.new(new_nodes["Vector Math.009"].outputs[0], new_nodes["Capture Attribute.012"].inputs[1])
    tree_links.new(new_nodes["Vector Math.010"].outputs[0], new_nodes["Vector Math.009"].inputs[0])
    tree_links.new(new_nodes["Position.016"].outputs[0], new_nodes["Vector Math.010"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Set Material.002"].inputs[2])
    tree_links.new(new_nodes["Realize Instances"].outputs[0], new_nodes["Set Material.002"].inputs[0])
    tree_links.new(new_nodes["Vector Math.002"].outputs[0], new_nodes["Set Position.010"].inputs[3])
    tree_links.new(new_nodes["Set Material.002"].outputs[0], new_nodes["Set Position.004"].inputs[0])
    tree_links.new(new_nodes["Set Position.004"].outputs[0], new_nodes["Join Geometry.004"].inputs[0])
    tree_links.new(new_nodes["Set Material.001"].outputs[0], new_nodes["Set Position.010"].inputs[0])
    tree_links.new(new_nodes["Merge by Distance.001"].outputs[0], new_nodes["Set Material.001"].inputs[0])
    tree_links.new(new_nodes["Set Position.010"].outputs[0], new_nodes["Join Geometry.004"].inputs[0])
    tree_links.new(new_nodes["Join Geometry.004"].outputs[0], new_nodes["Attribute Statistic.001"].inputs[0])
    tree_links.new(new_nodes["Join Geometry.004"].outputs[0], new_nodes["Capture Attribute.011"].inputs[0])
    tree_links.new(new_nodes["Set Position.011"].outputs[0], new_nodes["Set Position.002"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.013"].outputs[0], new_nodes["Capture Attribute.014"].inputs[0])
    tree_links.new(new_nodes["Join Geometry.001"].outputs[0], new_nodes["Capture Attribute.013"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.014"].outputs[0], new_nodes["Set Shade Smooth.001"].inputs[0])
    tree_links.new(new_nodes["Math.065"].outputs[0], new_nodes["Capture Attribute.013"].inputs[2])
    tree_links.new(new_nodes["Capture Attribute.004"].outputs[2], new_nodes["Math.065"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.011"].outputs[2], new_nodes["Math.065"].inputs[1])
    tree_links.new(new_nodes["Capture Attribute.013"].outputs[2], new_nodes["Group Output"].inputs[1])
    tree_links.new(new_nodes["Vector Math.011"].outputs[0], new_nodes["Capture Attribute.014"].inputs[1])
    tree_links.new(new_nodes["Capture Attribute.012"].outputs[1], new_nodes["Vector Math.011"].inputs[1])
    tree_links.new(new_nodes["Capture Attribute.008"].outputs[1], new_nodes["Vector Math.011"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.014"].outputs[1], new_nodes["Group Output"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Math.003"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[10], new_nodes["Vector Rotate"].inputs[3])
    tree_links.new(new_nodes["Vector Rotate"].outputs[0], new_nodes["Vector Rotate.001"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[11], new_nodes["Vector Rotate.001"].inputs[3])
    tree_links.new(new_nodes["Combine XYZ.003"].outputs[0], new_nodes["Vector Rotate.001"].inputs[1])
    tree_links.new(new_nodes["Combine XYZ.002"].outputs[0], new_nodes["Vector Rotate.001"].inputs[0])
    tree_links.new(new_nodes["Vector Rotate.001"].outputs[0], new_nodes["Bezier Segment"].inputs[3])
    tree_links.new(new_nodes["Combine XYZ.012"].outputs[0], new_nodes["Vector Rotate"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[10], new_nodes["Vector Rotate.003"].inputs[3])
    tree_links.new(new_nodes["Vector Rotate.003"].outputs[0], new_nodes["Vector Rotate.002"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[11], new_nodes["Vector Rotate.002"].inputs[3])
    tree_links.new(new_nodes["Combine XYZ.013"].outputs[0], new_nodes["Vector Rotate.003"].inputs[0])
    tree_links.new(new_nodes["Position.017"].outputs[0], new_nodes["Vector Rotate.002"].inputs[0])
    tree_links.new(new_nodes["Vector Rotate.002"].outputs[0], new_nodes["Set Position.001"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[10], new_nodes["Vector Rotate.004"].inputs[3])
    tree_links.new(new_nodes["Vector Rotate.004"].outputs[0], new_nodes["Vector Rotate.005"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[11], new_nodes["Vector Rotate.005"].inputs[3])
    tree_links.new(new_nodes["Combine XYZ.014"].outputs[0], new_nodes["Vector Rotate.004"].inputs[0])
    tree_links.new(new_nodes["Position.018"].outputs[0], new_nodes["Vector Rotate.005"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.016"].outputs[0], new_nodes["Set Position.011"].inputs[0])
    tree_links.new(new_nodes["Combine XYZ.003"].outputs[0], new_nodes["Vector Rotate.005"].inputs[1])
    tree_links.new(new_nodes["Vector Rotate.005"].outputs[0], new_nodes["Set Position.011"].inputs[2])
    tree_links.new(new_nodes["Float Curve"].outputs[0], new_nodes["Math.014"].inputs[1])
    tree_links.new(new_nodes["Vector Math.003"].outputs[0], new_nodes["Set Position"].inputs[3])
    tree_links.new(new_nodes["Set Shade Smooth"].outputs[0], new_nodes["Set Position"].inputs[0])
    tree_links.new(new_nodes["Set Position"].outputs[0], new_nodes["Join Geometry"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.007"].outputs[0], new_nodes["Set Position.012"].inputs[0])
    tree_links.new(new_nodes["Vector Math.012"].outputs[0], new_nodes["Set Position.012"].inputs[2])
    tree_links.new(new_nodes["Position.003"].outputs[0], new_nodes["Vector Math.012"].inputs[0])
    tree_links.new(new_nodes["Combine XYZ.015"].outputs[0], new_nodes["Vector Math.012"].inputs[1])
    tree_links.new(new_nodes["Position.019"].outputs[0], new_nodes["Separate XYZ.014"].inputs[0])
    tree_links.new(new_nodes["Float Curve.001"].outputs[0], new_nodes["Combine XYZ.015"].inputs[0])
    tree_links.new(new_nodes["Float Curve.001"].outputs[0], new_nodes["Combine XYZ.015"].inputs[1])
    tree_links.new(new_nodes["Math.017"].outputs[0], new_nodes["Math.066"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.014"].outputs[2], new_nodes["Math.066"].inputs[0])
    tree_links.new(new_nodes["Math.066"].outputs[0], new_nodes["Float Curve.001"].inputs[1])
    tree_links.new(new_nodes["Capture Attribute.001"].outputs[2], new_nodes["Float Curve"].inputs[1])
    tree_links.new(new_nodes["Combine XYZ.003"].outputs[0], new_nodes["Group Output"].inputs[6])
    tree_links.new(new_nodes["Combine XYZ.003"].outputs[0], new_nodes["Vector Math.013"].inputs[0])
    tree_links.new(new_nodes["Vector Rotate.001"].outputs[0], new_nodes["Vector Math.013"].inputs[1])
    tree_links.new(new_nodes["Vector Math.013"].outputs[0], new_nodes["Vector Math.014"].inputs[0])
    tree_links.new(new_nodes["Vector Math.014"].outputs[0], new_nodes["Group Output"].inputs[7])
    tree_links.new(new_nodes["Capture Attribute.012"].outputs[0], new_nodes["Capture Attribute.015"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.015"].outputs[2], new_nodes["Group Output"].inputs[8])
    tree_links.new(new_nodes["Combine XYZ.003"].outputs[0], new_nodes["Vector Math.016"].inputs[0])
    tree_links.new(new_nodes["Position.020"].outputs[0], new_nodes["Vector Math.017"].inputs[0])
    tree_links.new(new_nodes["Vector Math.017"].outputs[0], new_nodes["Vector Math.015"].inputs[1])
    tree_links.new(new_nodes["Vector Math.016"].outputs[0], new_nodes["Vector Math.015"].inputs[0])
    tree_links.new(new_nodes["Vector Math.015"].outputs[1], new_nodes["Attribute Statistic.002"].inputs[2])
    tree_links.new(new_nodes["Vector Math.015"].outputs[1], new_nodes["Math.002"].inputs[0])
    tree_links.new(new_nodes["Attribute Statistic.002"].outputs[4], new_nodes["Math.002"].inputs[1])
    tree_links.new(new_nodes["Capture Attribute.012"].outputs[0], new_nodes["Attribute Statistic.002"].inputs[0])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Capture Attribute.015"].inputs[2])
    tree_links.new(new_nodes["Capture Attribute.015"].outputs[0], new_nodes["Capture Attribute.016"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.016"].outputs[2], new_nodes["Group Output"].inputs[3])
    tree_links.new(new_nodes["Set Shade Smooth.001"].outputs[0], new_nodes["Switch"].inputs[14])
    tree_links.new(new_nodes["Switch"].outputs[6], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Compare"].outputs[0], new_nodes["Switch"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Compare"].inputs[2])
    tree_links.new(new_nodes["Set Material.003"].outputs[0], new_nodes["Switch"].inputs[15])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Set Material.003"].inputs[2])
    tree_links.new(new_nodes["Mesh to Points"].outputs[0], new_nodes["Set Material.003"].inputs[0])
    tree_links.new(new_nodes["Mesh Line"].outputs[0], new_nodes["Mesh to Points"].inputs[0])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group

def create_apply_mushroom_geo_nodes(new_node_group, tree_nodes, tree_links, mushroom_obj):
    new_node_group.outputs.new(type='NodeSocketFloat', name="Vertical Factor")
    new_node_group.outputs.new(type='NodeSocketVector', name="Radial Vector")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Cap Inside")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Cap Outside")
    new_node_group.outputs.new(type='NodeSocketVector', name="Cap Origin")
    new_node_group.outputs.new(type='NodeSocketVector', name="Cap Vertical Vector")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Cap Radial Factor")

    # initialize variables
    new_nodes = {}

    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="GeometryNodeGroup")
    node.location = (-240, 40)
    node.node_tree = bpy.data.node_groups.get(MUSHROOM_GEO_NG_NAME)
    node.inputs[0].default_value = 7
    node.inputs[1].default_value = bpy.data.materials.get(MUSHROOM_STEM_MAT_NAME)
    node.inputs[2].default_value = bpy.data.materials.get(MUSHROOM_CAP_MAT_NAME)
    node.inputs[3].default_value = bpy.data.materials.get(MUSHROOM_GILL_MAT_NAME)
    node.inputs[4].default_value = bpy.data.materials.get(MUSHROOM_POINT_MAT_NAME)
    new_nodes["Group"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-440, -940)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = 6.283185
    node.inputs[2].default_value = 0.500000
    new_nodes["Math"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (-440, -1100)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 1.000000
    node.inputs[3].default_value = -3.141593
    node.inputs[4].default_value = 3.141593
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (-440, -680)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 1.000000
    node.inputs[3].default_value = 0.030000
    node.inputs[4].default_value = 0.050000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range.004"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (-440, -420)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 1.000000
    node.inputs[3].default_value = 0.035000
    node.inputs[4].default_value = 0.050000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range.002"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-440, -140)
    node.operation = "MULTIPLY_ADD"
    node.inputs[1].default_value = (0.20000000298023224, 0.20000000298023224, 0.05000000074505806)
    node.inputs[2].default_value = (-0.10000000149011612, -0.10000000149011612, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (-440, 120)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 1.000000
    node.inputs[3].default_value = 0.040000
    node.inputs[4].default_value = 0.080000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range.003"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (-440, 380)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 1.000000
    node.inputs[3].default_value = 0.010000
    node.inputs[4].default_value = 0.018000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range.001"] = node

    node = tree_nodes.new(type="GeometryNodeObjectInfo")
    node.location = (-840, -540)
    node.transform_space = "ORIGINAL"
    node.inputs[0].default_value = mushroom_obj
    node.inputs[1].default_value = False
    new_nodes["Object Info"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateRGB")
    node.location = (-660, -320)
    new_nodes["Separate RGB"] = node

    node = tree_nodes.new(type="ShaderNodeTexNoise")
    node.location = (-840, -320)
    node.noise_dimensions = "3D"
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 3.000000
    node.inputs[3].default_value = 1.000000
    node.inputs[4].default_value = 0.500000
    node.inputs[5].default_value = 0.000000
    new_nodes["Noise Texture.001"] = node

    node = tree_nodes.new(type="ShaderNodeVectorRotate")
    node.location = (424, -120)
    node.invert = False
    node.rotation_type = "AXIS_ANGLE"
    node.inputs[4].default_value = (0.0, 0.0, 0.0)
    new_nodes["Vector Rotate"] = node

    node = tree_nodes.new(type="GeometryNodeSetPosition")
    node.location = (424, 100)
    node.inputs[3].default_value = (0.0, 0.0, 0.0)
    new_nodes["Set Position.001"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (420, -340)
    new_nodes["Position.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (240, -540)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (240, -720)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (240, -1480)
    new_nodes["Position.002"] = node

    node = tree_nodes.new(type="ShaderNodeValToRGB")
    node.location = (140, -1040)
    node.color_ramp.color_mode = "RGB"
    node.color_ramp.interpolation = "EASE"
    node.color_ramp.elements.remove(node.color_ramp.elements[0])
    elem = node.color_ramp.elements[0]
    elem.position = 0.125000
    elem.color = (0.043564, 0.043564, 0.043564, 1.000000)
    elem = node.color_ramp.elements.new(0.333000)
    elem.color = (0.521782, 0.521782, 0.521782, 1.000000)
    elem = node.color_ramp.elements.new(0.900000)
    elem.color = (1.000000, 1.000000, 1.000000, 1.000000)
    new_nodes["ColorRamp"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (240, -880)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[1].default_value = -0.500000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (60, -380)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[0].default_value = 1.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (240, -380)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeValToRGB")
    node.location = (-40, -720)
    node.color_ramp.color_mode = "RGB"
    node.color_ramp.interpolation = "EASE"
    node.color_ramp.elements.remove(node.color_ramp.elements[0])
    elem = node.color_ramp.elements[0]
    elem.position = 0.500000
    elem.color = (1.000000, 1.000000, 1.000000, 1.000000)
    elem = node.color_ramp.elements.new(0.900000)
    elem.color = (0.000000, 0.000000, 0.000000, 1.000000)
    new_nodes["ColorRamp.001"] = node

    node = tree_nodes.new(type="ShaderNodeTexNoise")
    node.location = (240, -1260)
    node.noise_dimensions = "3D"
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 60.000000
    node.inputs[3].default_value = 1.000000
    node.inputs[4].default_value = 0.600000
    node.inputs[5].default_value = 0.000000
    new_nodes["Noise Texture.002"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (660, -60)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = (0.009999999776482582, 0.009999999776482582, 0.009999999776482582)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (660, -500)
    new_nodes["Position"] = node

    node = tree_nodes.new(type="ShaderNodeTexNoise")
    node.location = (660, -260)
    node.noise_dimensions = "3D"
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 25.000000
    node.inputs[3].default_value = 1.000000
    node.inputs[4].default_value = 0.500000
    node.inputs[5].default_value = 0.000000
    new_nodes["Noise Texture"] = node

    node = tree_nodes.new(type="GeometryNodeSetPosition")
    node.location = (660, 100)
    new_nodes["Set Position"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-960, 80)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (860, 100)
    new_nodes["Group Output"] = node

    # create links
    tree_links.new(new_nodes["Set Position"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Group"].outputs[1], new_nodes["Group Output"].inputs[1])
    tree_links.new(new_nodes["Group"].outputs[2], new_nodes["Group Output"].inputs[2])
    tree_links.new(new_nodes["Group"].outputs[4], new_nodes["Group Output"].inputs[3])
    tree_links.new(new_nodes["Group"].outputs[5], new_nodes["Group Output"].inputs[4])
    tree_links.new(new_nodes["Set Position.001"].outputs[0], new_nodes["Set Position"].inputs[0])
    tree_links.new(new_nodes["Vector Math"].outputs[0], new_nodes["Set Position"].inputs[3])
    tree_links.new(new_nodes["Noise Texture"].outputs[1], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Position"].outputs[0], new_nodes["Noise Texture"].inputs[0])
    tree_links.new(new_nodes["Noise Texture.001"].outputs[1], new_nodes["Separate RGB"].inputs[0])
    tree_links.new(new_nodes["Object Info"].outputs[0], new_nodes["Noise Texture.001"].inputs[0])
    tree_links.new(new_nodes["Separate RGB"].outputs[0], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Group"].inputs[10])
    tree_links.new(new_nodes["Separate RGB"].outputs[1], new_nodes["Map Range"].inputs[0])
    tree_links.new(new_nodes["Map Range"].outputs[0], new_nodes["Group"].inputs[11])
    tree_links.new(new_nodes["Vector Math.001"].outputs[0], new_nodes["Group"].inputs[7])
    tree_links.new(new_nodes["Noise Texture.001"].outputs[1], new_nodes["Vector Math.001"].inputs[0])
    tree_links.new(new_nodes["Separate RGB"].outputs[2], new_nodes["Map Range.001"].inputs[0])
    tree_links.new(new_nodes["Separate RGB"].outputs[2], new_nodes["Map Range.002"].inputs[0])
    tree_links.new(new_nodes["Map Range.001"].outputs[0], new_nodes["Group"].inputs[5])
    tree_links.new(new_nodes["Map Range.002"].outputs[0], new_nodes["Group"].inputs[8])
    tree_links.new(new_nodes["Separate RGB"].outputs[0], new_nodes["Map Range.003"].inputs[0])
    tree_links.new(new_nodes["Map Range.003"].outputs[0], new_nodes["Group"].inputs[6])
    tree_links.new(new_nodes["Separate RGB"].outputs[0], new_nodes["Map Range.004"].inputs[0])
    tree_links.new(new_nodes["Map Range.004"].outputs[0], new_nodes["Group"].inputs[9])
    tree_links.new(new_nodes["Group"].outputs[6], new_nodes["Group Output"].inputs[5])
    tree_links.new(new_nodes["Group"].outputs[7], new_nodes["Group Output"].inputs[6])
    tree_links.new(new_nodes["Group"].outputs[8], new_nodes["Group Output"].inputs[7])
    tree_links.new(new_nodes["Group"].outputs[0], new_nodes["Set Position.001"].inputs[0])
    tree_links.new(new_nodes["Group"].outputs[3], new_nodes["Math.001"].inputs[0])
    tree_links.new(new_nodes["Vector Rotate"].outputs[0], new_nodes["Set Position.001"].inputs[2])
    tree_links.new(new_nodes["Group"].outputs[6], new_nodes["Vector Rotate"].inputs[1])
    tree_links.new(new_nodes["Group"].outputs[7], new_nodes["Vector Rotate"].inputs[2])
    tree_links.new(new_nodes["Position.001"].outputs[0], new_nodes["Vector Rotate"].inputs[0])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Math.001"].inputs[1])
    tree_links.new(new_nodes["Position.002"].outputs[0], new_nodes["Noise Texture.002"].inputs[0])
    tree_links.new(new_nodes["Noise Texture.002"].outputs[0], new_nodes["ColorRamp"].inputs[0])
    tree_links.new(new_nodes["ColorRamp"].outputs[0], new_nodes["Math.004"].inputs[0])
    tree_links.new(new_nodes["Math.004"].outputs[0], new_nodes["Math.002"].inputs[1])
    tree_links.new(new_nodes["Group"].outputs[8], new_nodes["ColorRamp.001"].inputs[0])
    tree_links.new(new_nodes["ColorRamp.001"].outputs[0], new_nodes["Math.002"].inputs[0])
    tree_links.new(new_nodes["Group"].outputs[1], new_nodes["Math.003"].inputs[1])
    tree_links.new(new_nodes["Math.003"].outputs[0], new_nodes["Math.005"].inputs[0])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Math.005"].inputs[1])
    tree_links.new(new_nodes["Math.005"].outputs[0], new_nodes["Vector Rotate"].inputs[3])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group

def create_mat_mushroom_stem(material):
    # initialize variables
    new_nodes = {}
    tree_nodes = material.node_tree.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeBsdfPrincipled")
    node.location = (380, 460)
    node.distribution = "GGX"
    node.subsurface_method = "RANDOM_WALK"
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = (1.0, 0.20000000298023224, 0.10000000149011612)
    node.inputs[3].default_value = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
    node.inputs[4].default_value = 1.400000
    node.inputs[5].default_value = 0.000000
    node.inputs[6].default_value = 0.000000
    node.inputs[7].default_value = 0.020000
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

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-80, 120)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[0].default_value = -1.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-80, 520)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math"] = node

    node = tree_nodes.new(type="ShaderNodeValToRGB")
    node.location = (-180, 340)
    node.color_ramp.color_mode = "RGB"
    node.color_ramp.interpolation = "EASE"
    node.color_ramp.elements.remove(node.color_ramp.elements[0])
    elem = node.color_ramp.elements[0]
    elem.position = 0.000000
    elem.color = (1.000000, 1.000000, 1.000000, 1.000000)
    elem = node.color_ramp.elements.new(0.327273)
    elem.color = (0.000000, 0.000000, 0.000000, 1.000000)
    elem = node.color_ramp.elements.new(0.816364)
    elem.color = (0.000000, 0.000000, 0.000000, 1.000000)
    elem = node.color_ramp.elements.new(1.000000)
    elem.color = (1.000000, 1.000000, 1.000000, 1.000000)
    new_nodes["ColorRamp.003"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-360, 260)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = (0.10000000149011612, 0.10000000149011612, 1.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="ShaderNodeTexVoronoi")
    node.location = (-360, 520)
    node.distance = "EUCLIDEAN"
    node.feature = "F1"
    node.voronoi_dimensions = "3D"
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 3.000000
    node.inputs[3].default_value = 1.000000
    node.inputs[4].default_value = 0.500000
    node.inputs[5].default_value = 1.000000
    new_nodes["Voronoi Texture"] = node

    node = tree_nodes.new(type="ShaderNodeBump")
    node.location = (200, -100)
    node.invert = True
    node.inputs[0].default_value = 0.110000
    node.inputs[1].default_value = 1.000000
    node.inputs[3].default_value = 1.000000
    node.inputs[4].default_value = 1.000000
    new_nodes["Bump"] = node

    node = tree_nodes.new(type="ShaderNodeValToRGB")
    node.location = (100, 120)
    node.color_ramp.color_mode = "RGB"
    node.color_ramp.interpolation = "EASE"
    node.color_ramp.elements.remove(node.color_ramp.elements[0])
    elem = node.color_ramp.elements[0]
    elem.position = 0.087273
    elem.color = (0.120196, 0.120196, 0.120196, 1.000000)
    elem = node.color_ramp.elements.new(0.905455)
    elem.color = (0.092644, 0.092644, 0.092644, 1.000000)
    new_nodes["ColorRamp"] = node

    node = tree_nodes.new(type="ShaderNodeValToRGB")
    node.location = (100, -280)
    node.color_ramp.color_mode = "RGB"
    node.color_ramp.interpolation = "EASE"
    node.color_ramp.elements.remove(node.color_ramp.elements[0])
    elem = node.color_ramp.elements[0]
    elem.position = 0.178182
    elem.color = (0.000000, 0.000000, 0.000000, 1.000000)
    elem = node.color_ramp.elements.new(0.769091)
    elem.color = (1.000000, 1.000000, 1.000000, 1.000000)
    new_nodes["ColorRamp.001"] = node

    node = tree_nodes.new(type="ShaderNodeTexNoise")
    node.location = (-100, -100)
    node.noise_dimensions = "3D"
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 2.000000
    node.inputs[3].default_value = 2.000000
    node.inputs[4].default_value = 0.500000
    node.inputs[5].default_value = 0.000000
    new_nodes["Noise Texture"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (-540, 100)
    new_nodes["Combine XYZ"] = node

    node = tree_nodes.new(type="ShaderNodeAttribute")
    node.location = (-720, 100)
    node.attribute_name = "h_fac"
    node.attribute_type = "GEOMETRY"
    new_nodes["Attribute"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (-540, -40)
    new_nodes["Separate XYZ"] = node

    node = tree_nodes.new(type="ShaderNodeAttribute")
    node.location = (-540, -180)
    node.attribute_name = "radial_v"
    node.attribute_type = "GEOMETRY"
    new_nodes["Attribute.001"] = node

    node = tree_nodes.new(type="ShaderNodeValToRGB")
    node.location = (100, 520)
    node.color_ramp.color_mode = "RGB"
    node.color_ramp.interpolation = "EASE"
    node.color_ramp.elements.remove(node.color_ramp.elements[0])
    elem = node.color_ramp.elements[0]
    elem.position = 0.060000
    elem.color = (0.342760, 0.243750, 0.142594, 1.000000)
    elem = node.color_ramp.elements.new(0.601818)
    elem.color = (0.449549, 0.429702, 0.386943, 1.000000)
    new_nodes["ColorRamp.002"] = node

    node = tree_nodes.new(type="ShaderNodeOutputMaterial")
    node.location = (660, 460)
    node.target = "ALL"
    new_nodes["Material Output"] = node

    # create links
    tree_links = material.node_tree.links
    tree_links.new(new_nodes["Attribute.001"].outputs[1], new_nodes["Separate XYZ"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ"].outputs[0], new_nodes["Combine XYZ"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ"].outputs[1], new_nodes["Combine XYZ"].inputs[1])
    tree_links.new(new_nodes["Attribute"].outputs[2], new_nodes["Combine XYZ"].inputs[2])
    tree_links.new(new_nodes["Bump"].outputs[0], new_nodes["Principled BSDF"].inputs[22])
    tree_links.new(new_nodes["ColorRamp.001"].outputs[0], new_nodes["Bump"].inputs[2])
    tree_links.new(new_nodes["Noise Texture"].outputs[0], new_nodes["ColorRamp.001"].inputs[0])
    tree_links.new(new_nodes["Combine XYZ"].outputs[0], new_nodes["Noise Texture"].inputs[0])
    tree_links.new(new_nodes["Noise Texture"].outputs[0], new_nodes["ColorRamp"].inputs[0])
    tree_links.new(new_nodes["ColorRamp"].outputs[0], new_nodes["Principled BSDF"].inputs[9])
    tree_links.new(new_nodes["Vector Math"].outputs[0], new_nodes["Voronoi Texture"].inputs[0])
    tree_links.new(new_nodes["Combine XYZ"].outputs[0], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Attribute"].outputs[2], new_nodes["Math.001"].inputs[1])
    tree_links.new(new_nodes["ColorRamp.002"].outputs[0], new_nodes["Principled BSDF"].inputs[0])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["ColorRamp.002"].inputs[0])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["ColorRamp.003"].inputs[0])
    tree_links.new(new_nodes["Voronoi Texture"].outputs[0], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["ColorRamp.003"].outputs[0], new_nodes["Math"].inputs[1])
    tree_links.new(new_nodes["Principled BSDF"].outputs[0], new_nodes["Material Output"].inputs[0])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_nodes

def create_mat_mushroom_cap(material):
    # initialize variables
    new_nodes = {}
    tree_nodes = material.node_tree.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeBump")
    node.location = (860, -840)
    node.invert = False
    node.inputs[0].default_value = 0.030000
    node.inputs[1].default_value = 1.000000
    node.inputs[3].default_value = 1.000000
    node.inputs[4].default_value = 1.000000
    new_nodes["Bump"] = node

    node = tree_nodes.new(type="ShaderNodeBsdfPrincipled")
    node.location = (1140, -260)
    node.distribution = "GGX"
    node.subsurface_method = "RANDOM_WALK"
    node.inputs[0].default_value = (0.1716674268245697, 0.10746203362941742, 0.048559579998254776, 1.0)
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = (1.0, 0.20000000298023224, 0.10000000149011612)
    node.inputs[3].default_value = (0.2361498475074768, 0.2361498475074768, 0.2361498475074768, 1.0)
    node.inputs[4].default_value = 1.400000
    node.inputs[5].default_value = 0.000000
    node.inputs[6].default_value = 0.000000
    node.inputs[7].default_value = 0.030000
    node.inputs[8].default_value = 0.000000
    node.inputs[9].default_value = 0.600000
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

    node = tree_nodes.new(type="ShaderNodeAttribute")
    node.location = (1220, 120)
    node.attribute_name = "cap_outside"
    node.attribute_type = "GEOMETRY"
    new_nodes["Attribute.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1220, 280)
    node.operation = "GREATER_THAN"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math"] = node

    node = tree_nodes.new(type="ShaderNodeAttribute")
    node.location = (1220, -60)
    node.attribute_name = "cap_inside"
    node.attribute_type = "GEOMETRY"
    new_nodes["Attribute"] = node

    node = tree_nodes.new(type="ShaderNodeAttribute")
    node.location = (-820, -840)
    node.attribute_name = "radial_v"
    node.attribute_type = "GEOMETRY"
    new_nodes["Attribute.003"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (-640, -840)
    new_nodes["Separate XYZ"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (-640, -700)
    new_nodes["Combine XYZ"] = node

    node = tree_nodes.new(type="ShaderNodeValToRGB")
    node.location = (-300, -580)
    node.color_ramp.color_mode = "RGB"
    node.color_ramp.interpolation = "EASE"
    node.color_ramp.elements.remove(node.color_ramp.elements[0])
    elem = node.color_ramp.elements[0]
    elem.position = 0.065455
    elem.color = (1.000000, 1.000000, 1.000000, 1.000000)
    elem = node.color_ramp.elements.new(0.649091)
    elem.color = (0.000000, 0.000000, 0.000000, 1.000000)
    new_nodes["ColorRamp.001"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-200, -1020)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = (8.0, 8.0, 0.20000000298023224)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-200, -420)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeMixRGB")
    node.location = (-200, -240)
    node.blend_type = "MIX"
    node.use_alpha = False
    node.use_clamp = False
    node.inputs[2].default_value = (0.7454043626785278, 0.0802198275923729, 0.02121901698410511, 1.0)
    new_nodes["Mix"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (660, -700)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateHSV")
    node.location = (180, -640)
    new_nodes["Separate HSV"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (360, -640)
    node.operation = "COMPARE"
    node.use_clamp = False
    node.inputs[1].default_value = 0.500000
    node.inputs[2].default_value = 0.250000
    new_nodes["Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (360, -480)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[0].default_value = 1.000000
    node.inputs[2].default_value = 0.050000
    new_nodes["Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeTexCoord")
    node.location = (0, -900)
    node.from_instancer = False
    new_nodes["Texture Coordinate"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (660, -320)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (660, -160)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.006"] = node

    node = tree_nodes.new(type="ShaderNodeMixRGB")
    node.location = (660, 20)
    node.blend_type = "MIX"
    node.use_alpha = False
    node.use_clamp = True
    node.inputs[1].default_value = (0.5739970207214355, 0.5548160076141357, 0.45310500264167786, 1.0)
    new_nodes["Mix.001"] = node

    node = tree_nodes.new(type="ShaderNodeValToRGB")
    node.location = (-640, -240)
    node.color_ramp.color_mode = "RGB"
    node.color_ramp.interpolation = "EASE"
    node.color_ramp.elements.remove(node.color_ramp.elements[0])
    elem = node.color_ramp.elements[0]
    elem.position = 0.034545
    elem.color = (0.303399, 0.234665, 0.154681, 1.000000)
    elem = node.color_ramp.elements.new(0.060000)
    elem.color = (0.377462, 0.057935, 0.011966, 1.000000)
    elem = node.color_ramp.elements.new(0.117727)
    elem.color = (0.344431, 0.020243, 0.008554, 1.000000)
    elem = node.color_ramp.elements.new(0.299773)
    elem.color = (0.317241, 0.012954, 0.007466, 1.000000)
    elem = node.color_ramp.elements.new(0.914546)
    elem.color = (0.349023, 0.007742, 0.007742, 1.000000)
    new_nodes["ColorRamp"] = node

    node = tree_nodes.new(type="ShaderNodeTexNoise")
    node.location = (-200, -800)
    node.noise_dimensions = "3D"
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 3.000000
    node.inputs[3].default_value = 1.000000
    node.inputs[4].default_value = 0.500000
    node.inputs[5].default_value = 0.000000
    new_nodes["Noise Texture"] = node

    node = tree_nodes.new(type="ShaderNodeTexVoronoi")
    node.location = (0, -640)
    node.distance = "EUCLIDEAN"
    node.feature = "F1"
    node.voronoi_dimensions = "3D"
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 8.000000
    node.inputs[3].default_value = 0.500000
    node.inputs[4].default_value = 0.500000
    node.inputs[5].default_value = 1.000000
    new_nodes["Voronoi Texture"] = node

    node = tree_nodes.new(type="ShaderNodeValToRGB")
    node.location = (560, -480)
    node.color_ramp.color_mode = "RGB"
    node.color_ramp.interpolation = "EASE"
    node.color_ramp.elements.remove(node.color_ramp.elements[0])
    elem = node.color_ramp.elements[0]
    elem.position = 0.083636
    elem.color = (0.000000, 0.000000, 0.000000, 1.000000)
    elem = node.color_ramp.elements.new(0.396364)
    elem.color = (1.000000, 1.000000, 1.000000, 1.000000)
    new_nodes["ColorRamp.002"] = node

    node = tree_nodes.new(type="ShaderNodeValToRGB")
    node.location = (260, -160)
    node.color_ramp.color_mode = "RGB"
    node.color_ramp.interpolation = "EASE"
    node.color_ramp.elements.remove(node.color_ramp.elements[0])
    elem = node.color_ramp.elements[0]
    elem.position = 0.307273
    elem.color = (1.000000, 1.000000, 1.000000, 1.000000)
    elem = node.color_ramp.elements.new(0.492727)
    elem.color = (0.000000, 0.000000, 0.000000, 1.000000)
    new_nodes["ColorRamp.003"] = node

    node = tree_nodes.new(type="ShaderNodeValToRGB")
    node.location = (560, -880)
    node.color_ramp.color_mode = "RGB"
    node.color_ramp.interpolation = "EASE"
    node.color_ramp.elements.remove(node.color_ramp.elements[0])
    elem = node.color_ramp.elements[0]
    elem.position = 0.152727
    elem.color = (0.017358, 0.017358, 0.017358, 1.000000)
    elem = node.color_ramp.elements.new(0.840000)
    elem.color = (0.412924, 0.412924, 0.412924, 1.000000)
    new_nodes["ColorRamp.004"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (660, -1120)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = 0.250000
    node.inputs[2].default_value = 0.650000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range"] = node

    node = tree_nodes.new(type="ShaderNodeBsdfPrincipled")
    node.location = (860, -160)
    node.distribution = "GGX"
    node.subsurface_method = "RANDOM_WALK"
    node.inputs[2].default_value = (1.0, 0.5, 0.5)
    node.inputs[3].default_value = (0.296821266412735, 0.0015710798325017095, 0.0, 1.0)
    node.inputs[4].default_value = 1.400000
    node.inputs[5].default_value = 0.000000
    node.inputs[6].default_value = 0.000000
    node.inputs[7].default_value = 0.030000
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
    node.location = (1420, -100)
    new_nodes["Mix Shader"] = node

    node = tree_nodes.new(type="ShaderNodeAttribute")
    node.location = (-820, -260)
    node.attribute_name = "h_fac"
    node.attribute_type = "GEOMETRY"
    new_nodes["Attribute.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (280, 60)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = 0.010000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.007"] = node

    node = tree_nodes.new(type="ShaderNodeValToRGB")
    node.location = (-80, 60)
    node.color_ramp.color_mode = "RGB"
    node.color_ramp.interpolation = "EASE"
    node.color_ramp.elements.remove(node.color_ramp.elements[0])
    elem = node.color_ramp.elements[0]
    elem.position = 0.010000
    elem.color = (0.000000, 0.000000, 0.000000, 1.000000)
    elem = node.color_ramp.elements.new(0.500000)
    elem.color = (1.000000, 1.000000, 1.000000, 1.000000)
    new_nodes["ColorRamp.005"] = node

    node = tree_nodes.new(type="ShaderNodeOutputMaterial")
    node.location = (1600, -100)
    node.target = "ALL"
    new_nodes["Material Output"] = node

    # create links
    tree_links = material.node_tree.links
    tree_links.new(new_nodes["Attribute"].outputs[2], new_nodes["Math"].inputs[1])
    tree_links.new(new_nodes["Attribute.001"].outputs[2], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Mix Shader"].inputs[0])
    tree_links.new(new_nodes["Principled BSDF"].outputs[0], new_nodes["Mix Shader"].inputs[2])
    tree_links.new(new_nodes["Principled BSDF.001"].outputs[0], new_nodes["Mix Shader"].inputs[1])
    tree_links.new(new_nodes["Attribute.002"].outputs[2], new_nodes["ColorRamp"].inputs[0])
    tree_links.new(new_nodes["Mix.001"].outputs[0], new_nodes["Principled BSDF"].inputs[0])
    tree_links.new(new_nodes["ColorRamp"].outputs[0], new_nodes["Mix"].inputs[1])
    tree_links.new(new_nodes["Attribute.002"].outputs[2], new_nodes["Combine XYZ"].inputs[2])
    tree_links.new(new_nodes["Attribute.003"].outputs[1], new_nodes["Separate XYZ"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ"].outputs[0], new_nodes["Combine XYZ"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ"].outputs[1], new_nodes["Combine XYZ"].inputs[1])
    tree_links.new(new_nodes["Combine XYZ"].outputs[0], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Vector Math"].outputs[0], new_nodes["Noise Texture"].inputs[0])
    tree_links.new(new_nodes["Attribute.002"].outputs[2], new_nodes["ColorRamp.001"].inputs[0])
    tree_links.new(new_nodes["Noise Texture"].outputs[0], new_nodes["Math.001"].inputs[0])
    tree_links.new(new_nodes["ColorRamp.001"].outputs[0], new_nodes["Math.001"].inputs[1])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Mix"].inputs[0])
    tree_links.new(new_nodes["Mix"].outputs[0], new_nodes["Mix.001"].inputs[2])
    tree_links.new(new_nodes["Voronoi Texture"].outputs[0], new_nodes["Math.003"].inputs[1])
    tree_links.new(new_nodes["Voronoi Texture"].outputs[1], new_nodes["Separate HSV"].inputs[0])
    tree_links.new(new_nodes["Separate HSV"].outputs[0], new_nodes["Math.004"].inputs[0])
    tree_links.new(new_nodes["Math.003"].outputs[0], new_nodes["ColorRamp.002"].inputs[0])
    tree_links.new(new_nodes["Math.004"].outputs[0], new_nodes["Math.005"].inputs[1])
    tree_links.new(new_nodes["Math.004"].outputs[0], new_nodes["Math.003"].inputs[0])
    tree_links.new(new_nodes["Math.005"].outputs[0], new_nodes["Math.002"].inputs[0])
    tree_links.new(new_nodes["ColorRamp.002"].outputs[0], new_nodes["Math.002"].inputs[1])
    tree_links.new(new_nodes["Texture Coordinate"].outputs[0], new_nodes["Voronoi Texture"].inputs[0])
    tree_links.new(new_nodes["ColorRamp.003"].outputs[0], new_nodes["Math.006"].inputs[1])
    tree_links.new(new_nodes["Math.006"].outputs[0], new_nodes["Mix.001"].inputs[0])
    tree_links.new(new_nodes["Attribute.002"].outputs[2], new_nodes["ColorRamp.003"].inputs[0])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Math.006"].inputs[0])
    tree_links.new(new_nodes["Bump"].outputs[0], new_nodes["Principled BSDF"].inputs[22])
    tree_links.new(new_nodes["Attribute.002"].outputs[2], new_nodes["Map Range"].inputs[0])
    tree_links.new(new_nodes["Noise Texture"].outputs[0], new_nodes["Map Range"].inputs[3])
    tree_links.new(new_nodes["Voronoi Texture"].outputs[0], new_nodes["Map Range"].inputs[4])
    tree_links.new(new_nodes["Map Range"].outputs[0], new_nodes["Bump"].inputs[2])
    tree_links.new(new_nodes["Map Range"].outputs[0], new_nodes["ColorRamp.004"].inputs[0])
    tree_links.new(new_nodes["ColorRamp.004"].outputs[0], new_nodes["Principled BSDF"].inputs[9])
    tree_links.new(new_nodes["Mix Shader"].outputs[0], new_nodes["Material Output"].inputs[0])
    tree_links.new(new_nodes["Attribute.002"].outputs[2], new_nodes["ColorRamp.005"].inputs[0])
    tree_links.new(new_nodes["ColorRamp.005"].outputs[0], new_nodes["Math.007"].inputs[0])
    tree_links.new(new_nodes["Math.007"].outputs[0], new_nodes["Principled BSDF"].inputs[1])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_nodes

def create_mat_mushroom_gill(material):
    # initialize variables
    new_nodes = {}
    tree_nodes = material.node_tree.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeBsdfTransparent")
    node.location = (120, 400)
    node.inputs[0].default_value = (1.0, 1.0, 1.0, 1.0)
    new_nodes["Transparent BSDF"] = node

    node = tree_nodes.new(type="ShaderNodeValToRGB")
    node.location = (20, 760)
    node.color_ramp.color_mode = "RGB"
    node.color_ramp.interpolation = "EASE"
    node.color_ramp.elements.remove(node.color_ramp.elements[0])
    elem = node.color_ramp.elements[0]
    elem.position = 0.254546
    elem.color = (0.010000, 0.010000, 0.010000, 1.000000)
    elem = node.color_ramp.elements.new(0.814546)
    elem.color = (0.750000, 0.750000, 0.750000, 1.000000)
    new_nodes["ColorRamp.001"] = node

    node = tree_nodes.new(type="ShaderNodeTexNoise")
    node.location = (-160, 760)
    node.noise_dimensions = "3D"
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 10.000000
    node.inputs[3].default_value = 1.000000
    node.inputs[4].default_value = 0.500000
    node.inputs[5].default_value = 0.000000
    new_nodes["Noise Texture"] = node

    node = tree_nodes.new(type="ShaderNodeTexCoord")
    node.location = (-160, 540)
    node.from_instancer = False
    new_nodes["Texture Coordinate"] = node

    node = tree_nodes.new(type="ShaderNodeValToRGB")
    node.location = (-260, 280)
    node.color_ramp.color_mode = "RGB"
    node.color_ramp.interpolation = "EASE"
    node.color_ramp.elements.remove(node.color_ramp.elements[0])
    elem = node.color_ramp.elements[0]
    elem.position = 0.120000
    elem.color = (0.606348, 0.531464, 0.369917, 1.000000)
    elem = node.color_ramp.elements.new(0.260000)
    elem.color = (0.114697, 0.074364, 0.035514, 1.000000)
    new_nodes["ColorRamp"] = node

    node = tree_nodes.new(type="ShaderNodeBsdfPrincipled")
    node.location = (20, 280)
    node.distribution = "GGX"
    node.subsurface_method = "RANDOM_WALK"
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = (1.0, 0.20000000298023224, 0.10000000149011612)
    node.inputs[3].default_value = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
    node.inputs[4].default_value = 1.400000
    node.inputs[5].default_value = 0.000000
    node.inputs[6].default_value = 0.000000
    node.inputs[7].default_value = 0.100000
    node.inputs[8].default_value = 0.000000
    node.inputs[9].default_value = 0.500000
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
    node.location = (120, 540)
    new_nodes["Mix Shader"] = node

    node = tree_nodes.new(type="ShaderNodeAttribute")
    node.location = (-440, 280)
    node.attribute_name = "h_fac"
    node.attribute_type = "GEOMETRY"
    new_nodes["Attribute"] = node

    node = tree_nodes.new(type="ShaderNodeOutputMaterial")
    node.location = (300, 540)
    node.target = "ALL"
    new_nodes["Material Output"] = node

    # create links
    tree_links = material.node_tree.links
    tree_links.new(new_nodes["Attribute"].outputs[2], new_nodes["ColorRamp"].inputs[0])
    tree_links.new(new_nodes["ColorRamp"].outputs[0], new_nodes["Principled BSDF"].inputs[0])
    tree_links.new(new_nodes["Principled BSDF"].outputs[0], new_nodes["Mix Shader"].inputs[2])
    tree_links.new(new_nodes["Transparent BSDF"].outputs[0], new_nodes["Mix Shader"].inputs[1])
    tree_links.new(new_nodes["Texture Coordinate"].outputs[0], new_nodes["Noise Texture"].inputs[0])
    tree_links.new(new_nodes["Noise Texture"].outputs[0], new_nodes["ColorRamp.001"].inputs[0])
    tree_links.new(new_nodes["ColorRamp.001"].outputs[0], new_nodes["Mix Shader"].inputs[0])
    tree_links.new(new_nodes["Mix Shader"].outputs[0], new_nodes["Material Output"].inputs[0])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_nodes

def create_mat_mushroom_point(material):
    # initialize variables
    new_nodes = {}
    tree_nodes = material.node_tree.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (1620, 560)
    new_nodes["Separate XYZ.002"] = node

    node = tree_nodes.new(type="ShaderNodeNewGeometry")
    node.location = (1620, 420)
    new_nodes["Geometry.004"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1620, 740)
    node.operation = "MULTIPLY_ADD"
    node.use_clamp = False
    node.inputs[1].default_value = 0.500000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeValToRGB")
    node.location = (1520, 960)
    node.color_ramp.color_mode = "RGB"
    node.color_ramp.interpolation = "EASE"
    node.color_ramp.elements.remove(node.color_ramp.elements[0])
    elem = node.color_ramp.elements[0]
    elem.position = 0.618182
    elem.color = (0.000000, 0.000000, 0.000000, 1.000000)
    elem = node.color_ramp.elements.new(0.658182)
    elem.color = (1.000000, 1.000000, 1.000000, 1.000000)
    new_nodes["ColorRamp.001"] = node

    node = tree_nodes.new(type="ShaderNodeMixShader")
    node.location = (1800, 180)
    new_nodes["Mix Shader"] = node

    node = tree_nodes.new(type="ShaderNodeBsdfPrincipled")
    node.location = (1700, 40)
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
    node.inputs[9].default_value = 0.300000
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

    node = tree_nodes.new(type="ShaderNodeTexVoronoi")
    node.location = (1520, -200)
    node.distance = "EUCLIDEAN"
    node.feature = "F1"
    node.voronoi_dimensions = "3D"
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 75.000000
    node.inputs[3].default_value = 1.000000
    node.inputs[4].default_value = 0.500000
    node.inputs[5].default_value = 1.000000
    new_nodes["Voronoi Texture"] = node

    node = tree_nodes.new(type="ShaderNodeMixShader")
    node.location = (1240, 180)
    new_nodes["Mix Shader.001"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (1060, 1060)
    node.operation = "NORMALIZE"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (1060, 940)
    node.operation = "NORMALIZE"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.006"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (1060, 1200)
    node.operation = "DOT_PRODUCT"
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeValToRGB")
    node.location = (960, 1420)
    node.color_ramp.color_mode = "RGB"
    node.color_ramp.interpolation = "EASE"
    node.color_ramp.elements.remove(node.color_ramp.elements[0])
    elem = node.color_ramp.elements[0]
    elem.position = 0.990000
    elem.color = (0.000000, 0.000000, 0.000000, 1.000000)
    elem = node.color_ramp.elements.new(0.995000)
    elem.color = (1.000000, 1.000000, 1.000000, 1.000000)
    new_nodes["ColorRamp.002"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (1060, 620)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = (1.0, 1.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (1060, 820)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = (1.0, 1.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeBsdfTransparent")
    node.location = (1060, 180)
    node.inputs[0].default_value = (1.0, 1.0, 1.0, 1.0)
    new_nodes["Transparent BSDF"] = node

    node = tree_nodes.new(type="ShaderNodeNewGeometry")
    node.location = (1060, 420)
    new_nodes["Geometry.003"] = node

    node = tree_nodes.new(type="ShaderNodeValToRGB")
    node.location = (1420, 40)
    node.color_ramp.color_mode = "RGB"
    node.color_ramp.interpolation = "EASE"
    node.color_ramp.elements.remove(node.color_ramp.elements[0])
    elem = node.color_ramp.elements[0]
    elem.position = 0.125455
    elem.color = (0.520426, 0.520426, 0.520426, 1.000000)
    elem = node.color_ramp.elements.new(0.229091)
    elem.color = (0.387974, 0.005456, 0.008666, 1.000000)
    new_nodes["ColorRamp"] = node

    node = tree_nodes.new(type="ShaderNodeBsdfPrincipled")
    node.location = (960, 40)
    node.distribution = "GGX"
    node.subsurface_method = "RANDOM_WALK"
    node.inputs[0].default_value = (0.6206883192062378, 0.5830996632575989, 0.5567834377288818, 1.0)
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = (1.0, 0.20000000298023224, 0.10000000149011612)
    node.inputs[3].default_value = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
    node.inputs[4].default_value = 1.400000
    node.inputs[5].default_value = 0.000000
    node.inputs[6].default_value = 0.000000
    node.inputs[7].default_value = 0.010000
    node.inputs[8].default_value = 0.000000
    node.inputs[9].default_value = 0.300000
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

    node = tree_nodes.new(type="ShaderNodeOutputMaterial")
    node.location = (1980, 180)
    node.target = "ALL"
    new_nodes["Material Output"] = node

    # create links
    tree_links = material.node_tree.links
    tree_links.new(new_nodes["Principled BSDF"].outputs[0], new_nodes["Mix Shader"].inputs[2])
    tree_links.new(new_nodes["Mix Shader.001"].outputs[0], new_nodes["Mix Shader"].inputs[1])
    tree_links.new(new_nodes["Transparent BSDF"].outputs[0], new_nodes["Mix Shader.001"].inputs[1])
    tree_links.new(new_nodes["Principled BSDF.001"].outputs[0], new_nodes["Mix Shader.001"].inputs[2])
    tree_links.new(new_nodes["Geometry.003"].outputs[1], new_nodes["Vector Math.003"].inputs[0])
    tree_links.new(new_nodes["Geometry.003"].outputs[4], new_nodes["Vector Math.002"].inputs[0])
    tree_links.new(new_nodes["Vector Math.006"].outputs[0], new_nodes["Vector Math.004"].inputs[1])
    tree_links.new(new_nodes["Vector Math.003"].outputs[0], new_nodes["Vector Math.005"].inputs[0])
    tree_links.new(new_nodes["Vector Math.002"].outputs[0], new_nodes["Vector Math.006"].inputs[0])
    tree_links.new(new_nodes["Vector Math.005"].outputs[0], new_nodes["Vector Math.004"].inputs[0])
    tree_links.new(new_nodes["Vector Math.004"].outputs[1], new_nodes["ColorRamp.002"].inputs[0])
    tree_links.new(new_nodes["ColorRamp.002"].outputs[0], new_nodes["Mix Shader.001"].inputs[0])
    tree_links.new(new_nodes["Geometry.004"].outputs[1], new_nodes["Separate XYZ.002"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.002"].outputs[2], new_nodes["Math.003"].inputs[0])
    tree_links.new(new_nodes["Math.003"].outputs[0], new_nodes["ColorRamp.001"].inputs[0])
    tree_links.new(new_nodes["ColorRamp.001"].outputs[0], new_nodes["Mix Shader"].inputs[0])
    tree_links.new(new_nodes["Mix Shader"].outputs[0], new_nodes["Material Output"].inputs[0])
    tree_links.new(new_nodes["Voronoi Texture"].outputs[0], new_nodes["ColorRamp"].inputs[0])
    tree_links.new(new_nodes["ColorRamp"].outputs[0], new_nodes["Principled BSDF"].inputs[0])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_nodes

def create_mushroom_materials(mushroom_obj, override_create):
    ensure_materials(override_create, [MUSHROOM_STEM_MAT_NAME, MUSHROOM_CAP_MAT_NAME, MUSHROOM_GILL_MAT_NAME,
                                       MUSHROOM_POINT_MAT_NAME], create_prereq_material)
    stem_mat = bpy.data.materials.get(MUSHROOM_STEM_MAT_NAME)
    cap_mat = bpy.data.materials.get(MUSHROOM_CAP_MAT_NAME)
    gill_mat = bpy.data.materials.get(MUSHROOM_GILL_MAT_NAME)
    point_mat = bpy.data.materials.get(MUSHROOM_POINT_MAT_NAME)
    mushroom_obj.data.materials.append(stem_mat)
    mushroom_obj.data.materials.append(cap_mat)
    mushroom_obj.data.materials.append(gill_mat)
    mushroom_obj.data.materials.append(point_mat)

def create_mushroom_individual_geo_ng(mushroom_obj, obj_geo_node_group, override_create):
    # initialize variables
    tree_nodes = obj_geo_node_group.nodes
    tree_links = obj_geo_node_group.links

    ensure_node_groups(override_create, [MUSHROOM_GEO_NG_NAME], 'GeometryNodeTree',
                       create_prereq_node_group)
    create_apply_mushroom_geo_nodes(obj_geo_node_group, tree_nodes, tree_links, mushroom_obj)

    return obj_geo_node_group

def add_mushroom_geo_nodes_to_object(mushroom_obj, override_create):
    geo_nodes_mod = mushroom_obj.modifiers.new(name="Mushroom.GeometryNodes", type='NODES')
    create_mushroom_materials(mushroom_obj, override_create)
    create_mushroom_individual_geo_ng(mushroom_obj, geo_nodes_mod.node_group, override_create)
    geo_nodes_mod["Output_2_attribute_name"] = "h_fac"
    geo_nodes_mod["Output_3_attribute_name"] = "radial_v"
    geo_nodes_mod["Output_4_attribute_name"] = "cap_inside"
    geo_nodes_mod["Output_5_attribute_name"] = "cap_outside"
    geo_nodes_mod["Output_6_attribute_name"] = "cap_origin"
    geo_nodes_mod["Output_7_attribute_name"] = "cap_vert"
    geo_nodes_mod["Output_8_attribute_name"] = "cap_rad_f"

def pot_create_mushroom(override_create):
    mushroom_obj = create_mesh_obj_from_pydata(obj_name=MUSHROOM_OBJNAME)
    add_mushroom_geo_nodes_to_object(mushroom_obj, override_create)

class BSR_PotCreateMushroom(bpy.types.Operator):
    bl_description = "Create a Mushroom with Geometry Nodes mesh and Shader Nodes material"
    bl_idname = "big_space_rig.pot_create_character_mushroom"
    bl_label = "Mushroom"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        s = context.space_data
        return s.type == 'NODE_EDITOR' and s.node_tree != None and s.tree_type == 'GeometryNodeTree'

    def execute(self, context):
        scn = context.scene
        pot_create_mushroom(scn.BSR_NodesOverrideCreate)
        return {'FINISHED'}
