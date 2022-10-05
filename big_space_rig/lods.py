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

from .node_other import ensure_node_groups

GEOMETRY_LODS_GEO_NG_NAME = "GeometryLODs.BSR.GeoNG"
GEOMETRY_LODS_PROXIMITY_GEO_NG_NAME = "GeometryLODs.Proximity.BSR.GeoNG"
GEOMETRY_LODS_CHOOSE_GEO_NG_NAME = "GeometryLODs.Choose.BSR.GeoNG"

INSTANCE_LODS_GEO_NG_NAME = "InstanceLODs.BSR.GeoNG"
INSTANCE_LODS_PROXIMITY_GEO_NG_NAME = "InstanceLODs.Proximity.BSR.GeoNG"
INSTANCE_LODS_CHOOSE_GEO_NG_NAME = "InstanceLODs.Choose.BSR.GeoNG"

def create_geo_ng_geometry_lods_proximity():
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=GEOMETRY_LODS_PROXIMITY_GEO_NG_NAME, type='GeometryNodeTree')
    new_node_group.inputs.new(type='NodeSocketVector', name="Position")
    new_node_group.inputs.new(type='NodeSocketGeometry', name="Proximity Geometry")
    new_node_group.inputs.new(type='NodeSocketFloat', name="ProxGeo Test Radius")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Simple Radius")
    new_node_group.outputs.new(type='NodeSocketBool', name="Use ProxGeo")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Original Distance")
    tree_nodes = new_node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (480, -240)
    node.operation = "MULTIPLY_ADD"
    node.use_clamp = False
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="GeometryNodeProximity")
    node.location = (300, -240)
    node.target_element = "FACES"
    new_nodes["Geometry Proximity"] = node

    node = tree_nodes.new(type="FunctionNodeBooleanMath")
    node.location = (120, -400)
    node.operation = "NOT"
    node.inputs[1].default_value = False
    new_nodes["Boolean Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (300, -400)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="FunctionNodeCompare")
    node.location = (-240, -360)
    node.data_type = "FLOAT"
    node.mode = "ELEMENT"
    node.operation = "LESS_EQUAL"
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

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-240, -180)
    node.operation = "GREATER_THAN"
    node.use_clamp = False
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math"] = node

    node = tree_nodes.new(type="GeometryNodeAttributeDomainSize")
    node.location = (-420, -180)
    node.component = "MESH"
    new_nodes["Domain Size"] = node

    node = tree_nodes.new(type="FunctionNodeBooleanMath")
    node.location = (-60, -240)
    node.operation = "AND"
    new_nodes["Boolean Math"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-420, -440)
    node.operation = "LENGTH"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-240, -520)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-60, -520)
    node.operation = "GREATER_THAN"
    node.use_clamp = False
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (120, -520)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.005"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-640, -360)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (660, -240)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Geometry Proximity"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Geometry Proximity"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Domain Size"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Domain Size"].outputs[2], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Boolean Math"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Compare"].inputs[1])
    tree_links.new(new_nodes["Vector Math"].outputs[1], new_nodes["Compare"].inputs[0])
    tree_links.new(new_nodes["Compare"].outputs[0], new_nodes["Boolean Math"].inputs[1])
    tree_links.new(new_nodes["Boolean Math"].outputs[0], new_nodes["Boolean Math.001"].inputs[0])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Group Output"].inputs[1])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Math.001"].inputs[2])
    tree_links.new(new_nodes["Math.005"].outputs[0], new_nodes["Math.002"].inputs[1])
    tree_links.new(new_nodes["Geometry Proximity"].outputs[1], new_nodes["Math.001"].inputs[1])
    tree_links.new(new_nodes["Boolean Math"].outputs[0], new_nodes["Math.001"].inputs[0])
    tree_links.new(new_nodes["Boolean Math.001"].outputs[0], new_nodes["Math.002"].inputs[0])
    tree_links.new(new_nodes["Vector Math"].outputs[1], new_nodes["Math.003"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Math.003"].inputs[1])
    tree_links.new(new_nodes["Math.003"].outputs[0], new_nodes["Math.004"].inputs[0])
    tree_links.new(new_nodes["Math.004"].outputs[0], new_nodes["Math.005"].inputs[0])
    tree_links.new(new_nodes["Math.003"].outputs[0], new_nodes["Math.005"].inputs[1])
    tree_links.new(new_nodes["Boolean Math"].outputs[0], new_nodes["Group Output"].inputs[0])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False
    return new_node_group

def create_geo_ng_geometry_lods_choose():
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=GEOMETRY_LODS_CHOOSE_GEO_NG_NAME, type='GeometryNodeTree')
    new_node_group.inputs.new(type='NodeSocketGeometry', name="Prev LOD Geometry")
    new_node_group.inputs.new(type='NodeSocketInt', name="LOD Index Count")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Closest Distance")
    new_node_group.inputs.new(type='NodeSocketBool', name="Use ProxGeo")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Original Distance")
    new_node_group.inputs.new(type='NodeSocketGeometry', name="LOD Geometry")
    new_node_group.inputs.new(type='NodeSocketFloat', name="LOD Distance")
    new_node_group.inputs.new(type='NodeSocketVector', name="Camera Location")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Absolute Bias Distance")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Relative Bias Distance")
    new_node_group.inputs.new(type='NodeSocketVector', name="Relative Bias Vector")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Simple Radius")
    new_node_group.outputs.new(type='NodeSocketGeometry', name="Geometry")
    new_node_group.outputs.new(type='NodeSocketInt', name="LOD Index Count")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Closest Distance")
    tree_nodes = new_node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (320, -80)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[0].default_value = 1.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-40, -280)
    node.operation = "LESS_THAN"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (500, -80)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.004"] = node

    node = tree_nodes.new(type="GeometryNodeSwitch")
    node.location = (320, 80)
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

    node = tree_nodes.new(type="FunctionNodeBooleanMath")
    node.location = (320, -260)
    node.operation = "NOT"
    node.inputs[1].default_value = False
    new_nodes["Boolean Math"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (860, -80)
    new_nodes["Group Output"] = node

    node = tree_nodes.new(type="FunctionNodeBooleanMath")
    node.location = (140, -80)
    node.operation = "AND"
    new_nodes["Boolean Math.001"] = node

    node = tree_nodes.new(type="FunctionNodeBooleanMath")
    node.location = (-40, -80)
    node.operation = "OR"
    new_nodes["Boolean Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-220, -80)
    node.operation = "GREATER_THAN"
    node.use_clamp = False
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.007"] = node

    node = tree_nodes.new(type="GeometryNodeAttributeDomainSize")
    node.location = (-400, -80)
    node.component = "MESH"
    new_nodes["Domain Size"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-220, 80)
    node.operation = "GREATER_THAN"
    node.use_clamp = False
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.008"] = node

    node = tree_nodes.new(type="GeometryNodeAttributeDomainSize")
    node.location = (-400, 80)
    node.component = "POINTCLOUD"
    new_nodes["Domain Size.001"] = node

    node = tree_nodes.new(type="FunctionNodeBooleanMath")
    node.location = (-760, -420)
    node.operation = "NOT"
    node.inputs[1].default_value = False
    new_nodes["Boolean Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-580, -420)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.012"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-1300, -540)
    node.operation = "LENGTH"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-1480, -540)
    node.operation = "SUBTRACT"
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-220, -280)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-400, -460)
    node.operation = "MULTIPLY_ADD"
    node.use_clamp = False
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-400, -280)
    node.operation = "MULTIPLY_ADD"
    node.use_clamp = False
    new_nodes["Math.011"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (680, -80)
    node.operation = "MULTIPLY_ADD"
    node.use_clamp = False
    new_nodes["Math.006"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (500, -260)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-1660, -540)
    node.operation = "MULTIPLY"
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1120, -540)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.015"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-940, -540)
    node.operation = "GREATER_THAN"
    node.use_clamp = False
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.013"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-760, -540)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.014"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-1860, -260)
    new_nodes["Group Input"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Switch"].inputs[14])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Domain Size"].inputs[0])
    tree_links.new(new_nodes["Switch"].outputs[6], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Boolean Math.001"].inputs[1])
    tree_links.new(new_nodes["Boolean Math.001"].outputs[0], new_nodes["Switch"].inputs[1])
    tree_links.new(new_nodes["Boolean Math.001"].outputs[0], new_nodes["Math"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Switch"].inputs[15])
    tree_links.new(new_nodes["Domain Size"].outputs[0], new_nodes["Math.007"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Math.001"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[9], new_nodes["Math.001"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[8], new_nodes["Math.001"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Math.004"].inputs[1])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Math.004"].inputs[0])
    tree_links.new(new_nodes["Math.004"].outputs[0], new_nodes["Group Output"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Math.002"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Math.005"].inputs[0])
    tree_links.new(new_nodes["Boolean Math.001"].outputs[0], new_nodes["Boolean Math"].inputs[0])
    tree_links.new(new_nodes["Boolean Math"].outputs[0], new_nodes["Math.005"].inputs[1])
    tree_links.new(new_nodes["Math.005"].outputs[0], new_nodes["Math.006"].inputs[2])
    tree_links.new(new_nodes["Boolean Math.001"].outputs[0], new_nodes["Math.006"].inputs[0])
    tree_links.new(new_nodes["Math.006"].outputs[0], new_nodes["Group Output"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Domain Size.001"].inputs[0])
    tree_links.new(new_nodes["Domain Size.001"].outputs[0], new_nodes["Math.008"].inputs[0])
    tree_links.new(new_nodes["Math.008"].outputs[0], new_nodes["Boolean Math.002"].inputs[0])
    tree_links.new(new_nodes["Math.007"].outputs[0], new_nodes["Boolean Math.002"].inputs[1])
    tree_links.new(new_nodes["Boolean Math.002"].outputs[0], new_nodes["Boolean Math.001"].inputs[0])
    tree_links.new(new_nodes["Vector Math.001"].outputs[0], new_nodes["Vector Math"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[10], new_nodes["Vector Math.001"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[7], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Vector Math.001"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Math.011"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Boolean Math.003"].inputs[0])
    tree_links.new(new_nodes["Boolean Math.003"].outputs[0], new_nodes["Math.012"].inputs[0])
    tree_links.new(new_nodes["Math.012"].outputs[0], new_nodes["Math.011"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Math.011"].inputs[0])
    tree_links.new(new_nodes["Vector Math.002"].outputs[1], new_nodes["Math.015"].inputs[0])
    tree_links.new(new_nodes["Math.015"].outputs[0], new_nodes["Math.013"].inputs[0])
    tree_links.new(new_nodes["Math.013"].outputs[0], new_nodes["Math.014"].inputs[0])
    tree_links.new(new_nodes["Math.015"].outputs[0], new_nodes["Math.014"].inputs[1])
    tree_links.new(new_nodes["Vector Math"].outputs[0], new_nodes["Vector Math.002"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[11], new_nodes["Math.015"].inputs[1])
    tree_links.new(new_nodes["Math.014"].outputs[0], new_nodes["Math.012"].inputs[1])
    tree_links.new(new_nodes["Math.011"].outputs[0], new_nodes["Math.003"].inputs[0])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Math.003"].inputs[1])
    tree_links.new(new_nodes["Math.003"].outputs[0], new_nodes["Math.002"].inputs[0])
    tree_links.new(new_nodes["Math.003"].outputs[0], new_nodes["Math.006"].inputs[1])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False
    return new_node_group

def create_geo_ng_geometry_lods():
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=GEOMETRY_LODS_GEO_NG_NAME, type='GeometryNodeTree')
    new_node_group.inputs.new(type='NodeSocketVector', name="Camera Location")
    new_node_group.inputs.new(type='NodeSocketVector', name="Absolute Bias Vector")
    new_node_group.inputs.new(type='NodeSocketVector', name="Relative Bias Vector")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Absolute Bias Distance")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Relative Bias Distance")
    new_node_group.inputs.new(type='NodeSocketFloatDistance', name="Simple Radius")
    new_node_group.inputs.new(type='NodeSocketFloatDistance', name="ProxGeo Test Radius")
    new_node_group.inputs.new(type='NodeSocketGeometry', name="Proximity Geometry")
    new_node_group.inputs.new(type='NodeSocketGeometry', name="LOD 0 Geometry")
    new_node_group.inputs.new(type='NodeSocketFloat', name="LOD 1 Distance")
    new_node_group.inputs.new(type='NodeSocketGeometry', name="LOD 1 Geometry")
    new_node_group.inputs.new(type='NodeSocketFloat', name="LOD 2 Distance")
    new_node_group.inputs.new(type='NodeSocketGeometry', name="LOD 2 Geometry")
    new_node_group.inputs.new(type='NodeSocketFloat', name="LOD 3 Distance")
    new_node_group.inputs.new(type='NodeSocketGeometry', name="LOD 3 Geometry")
    new_node_group.outputs.new(type='NodeSocketGeometry', name="Geometry")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Closest Distance")
    new_node_group.outputs.new(type='NodeSocketInt', name="LOD Index")
    new_node_group.outputs.new(type='NodeSocketInt', name="Max LOD Index")
    tree_nodes = new_node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="GeometryNodeGroup")
    node.location = (180, 220)
    node.node_tree = bpy.data.node_groups.get(GEOMETRY_LODS_CHOOSE_GEO_NG_NAME)
    new_nodes["Group.001"] = node

    node = tree_nodes.new(type="GeometryNodeGroup")
    node.location = (380, 220)
    node.node_tree = bpy.data.node_groups.get(GEOMETRY_LODS_CHOOSE_GEO_NG_NAME)
    new_nodes["Group"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.label = "Capture LOD Index"
    node.location = (580, 220)
    node.data_type = "INT"
    node.domain = "POINT"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = 0.000000
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    new_nodes["Capture Attribute"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (940, 220)
    node.inputs[3].default_value = 3
    new_nodes["Group Output"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.label = "Capture Closest Distance"
    node.location = (760, 220)
    node.data_type = "FLOAT"
    node.domain = "POINT"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute.001"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-420, 220)
    node.operation = "SUBTRACT"
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-640, 220)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="GeometryNodeGroup")
    node.location = (-240, 220)
    node.node_tree = bpy.data.node_groups.get(GEOMETRY_LODS_PROXIMITY_GEO_NG_NAME)
    new_nodes["Group.003"] = node

    node = tree_nodes.new(type="GeometryNodeGroup")
    node.location = (-20, 220)
    node.node_tree = bpy.data.node_groups.get(GEOMETRY_LODS_CHOOSE_GEO_NG_NAME)
    node.inputs[1].default_value = 0
    node.inputs[2].default_value = 0.000000
    new_nodes["Group.002"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Vector Math"].outputs[0], new_nodes["Group.003"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[7], new_nodes["Group.003"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[9], new_nodes["Group"].inputs[6])
    tree_links.new(new_nodes["Group Input"].outputs[8], new_nodes["Group"].inputs[5])
    tree_links.new(new_nodes["Capture Attribute.001"].outputs[2], new_nodes["Group Output"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Group.003"].inputs[2])
    tree_links.new(new_nodes["Capture Attribute"].outputs[5], new_nodes["Group Output"].inputs[2])
    tree_links.new(new_nodes["Group"].outputs[1], new_nodes["Capture Attribute"].inputs[5])
    tree_links.new(new_nodes["Group Input"].outputs[10], new_nodes["Group.001"].inputs[5])
    tree_links.new(new_nodes["Group Input"].outputs[11], new_nodes["Group.001"].inputs[6])
    tree_links.new(new_nodes["Group.001"].outputs[0], new_nodes["Group"].inputs[0])
    tree_links.new(new_nodes["Group.001"].outputs[1], new_nodes["Group"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[13], new_nodes["Group.002"].inputs[6])
    tree_links.new(new_nodes["Group.002"].outputs[0], new_nodes["Group.001"].inputs[0])
    tree_links.new(new_nodes["Group.002"].outputs[1], new_nodes["Group.001"].inputs[1])
    tree_links.new(new_nodes["Group.003"].outputs[1], new_nodes["Group.002"].inputs[4])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Group.002"].inputs[8])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Group.002"].inputs[9])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Group.001"].inputs[8])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Group.001"].inputs[9])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Group"].inputs[8])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Group"].inputs[9])
    tree_links.new(new_nodes["Group.003"].outputs[1], new_nodes["Group.001"].inputs[4])
    tree_links.new(new_nodes["Group.003"].outputs[1], new_nodes["Group"].inputs[4])
    tree_links.new(new_nodes["Group.002"].outputs[2], new_nodes["Group.001"].inputs[2])
    tree_links.new(new_nodes["Group.001"].outputs[2], new_nodes["Group"].inputs[2])
    tree_links.new(new_nodes["Group"].outputs[2], new_nodes["Capture Attribute.001"].inputs[2])
    tree_links.new(new_nodes["Group"].outputs[0], new_nodes["Capture Attribute"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.001"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute"].outputs[0], new_nodes["Capture Attribute.001"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[12], new_nodes["Group.002"].inputs[5])
    tree_links.new(new_nodes["Group Input"].outputs[14], new_nodes["Group.002"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Group.002"].inputs[10])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Group.001"].inputs[10])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Group"].inputs[10])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Vector Math"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Group.003"].inputs[3])
    tree_links.new(new_nodes["Group.003"].outputs[0], new_nodes["Group.002"].inputs[3])
    tree_links.new(new_nodes["Group.003"].outputs[0], new_nodes["Group.001"].inputs[3])
    tree_links.new(new_nodes["Group.003"].outputs[0], new_nodes["Group"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Group.002"].inputs[11])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Group.001"].inputs[11])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Group"].inputs[11])
    tree_links.new(new_nodes["Vector Math"].outputs[0], new_nodes["Group.002"].inputs[7])
    tree_links.new(new_nodes["Vector Math"].outputs[0], new_nodes["Group.001"].inputs[7])
    tree_links.new(new_nodes["Vector Math"].outputs[0], new_nodes["Group"].inputs[7])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False
    return new_node_group

def create_geo_ng_instance_lods_proximity():
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=INSTANCE_LODS_PROXIMITY_GEO_NG_NAME, type='GeometryNodeTree')
    new_node_group.inputs.new(type='NodeSocketGeometry', name="Points")
    new_node_group.inputs.new(type='NodeSocketVector', name="Rotation")
    new_node_group.inputs.new(type='NodeSocketVector', name="Scale")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Instance Radius")
    new_node_group.inputs.new(type='NodeSocketVector', name="Camera Location")
    new_node_group.inputs.new(type='NodeSocketFloat', name="ProxGeo Test Radius")
    new_node_group.inputs.new(type='NodeSocketGeometry', name="Proximity Geometry")
    new_node_group.outputs.new(type='NodeSocketGeometry', name="Points")
    new_node_group.outputs.new(type='NodeSocketBool', name="Use ProxGeo")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Original Distance")
    tree_nodes = new_node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-240, 140)
    node.operation = "GREATER_THAN"
    node.use_clamp = False
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math"] = node

    node = tree_nodes.new(type="GeometryNodeAttributeDomainSize")
    node.location = (-420, 140)
    node.component = "MESH"
    new_nodes["Domain Size"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.location = (480, -40)
    node.data_type = "FLOAT"
    node.domain = "POINT"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (660, 40)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.006"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.location = (480, 140)
    node.data_type = "FLOAT"
    node.domain = "POINT"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (120, -180)
    node.operation = "GREATER_THAN"
    node.use_clamp = False
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.003"] = node

    node = tree_nodes.new(type="GeometryNodeJoinGeometry")
    node.location = (660, 140)
    new_nodes["Join Geometry"] = node

    node = tree_nodes.new(type="FunctionNodeBooleanMath")
    node.location = (-60, 140)
    node.operation = "AND"
    new_nodes["Boolean Math"] = node

    node = tree_nodes.new(type="GeometryNodeSeparateGeometry")
    node.location = (120, 140)
    node.domain = "POINT"
    new_nodes["Separate Geometry"] = node

    node = tree_nodes.new(type="ShaderNodeVectorRotate")
    node.location = (-960, -40)
    node.invert = True
    node.rotation_type = "EULER_XYZ"
    node.inputs[2].default_value = (0.0, 0.0, 1.0)
    node.inputs[3].default_value = 0.000000
    new_nodes["Vector Rotate"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-600, -40)
    node.operation = "DIVIDE"
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.002"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.location = (1020, 140)
    node.data_type = "BOOLEAN"
    node.domain = "POINT"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = 0.000000
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute.003"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (-1140, -240)
    new_nodes["Position.001"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-780, -40)
    node.operation = "SUBTRACT"
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-240, -40)
    node.operation = "LESS_THAN"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-420, -40)
    node.operation = "LENGTH"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-60, -180)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (300, -180)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.004"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.location = (840, 140)
    node.data_type = "FLOAT"
    node.domain = "POINT"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute.002"] = node

    node = tree_nodes.new(type="GeometryNodeProximity")
    node.location = (300, 140)
    node.target_element = "FACES"
    new_nodes["Geometry Proximity"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-1279, 160)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (1220, 100)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Domain Size"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Math.001"].inputs[1])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Boolean Math"].inputs[0])
    tree_links.new(new_nodes["Boolean Math"].outputs[0], new_nodes["Separate Geometry"].inputs[1])
    tree_links.new(new_nodes["Domain Size"].outputs[2], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Vector Math"].outputs[1], new_nodes["Math.002"].inputs[0])
    tree_links.new(new_nodes["Separate Geometry"].outputs[0], new_nodes["Capture Attribute.001"].inputs[0])
    tree_links.new(new_nodes["Geometry Proximity"].outputs[1], new_nodes["Capture Attribute.001"].inputs[2])
    tree_links.new(new_nodes["Separate Geometry"].outputs[1], new_nodes["Capture Attribute"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute"].outputs[0], new_nodes["Join Geometry"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.001"].outputs[0], new_nodes["Join Geometry"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.001"].outputs[2], new_nodes["Math.006"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute"].outputs[2], new_nodes["Math.006"].inputs[1])
    tree_links.new(new_nodes["Capture Attribute.002"].outputs[2], new_nodes["Group Output"].inputs[2])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Boolean Math"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Vector Rotate"].inputs[4])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Vector Rotate"].inputs[0])
    tree_links.new(new_nodes["Position.001"].outputs[0], new_nodes["Vector Rotate"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Geometry Proximity"].inputs[0])
    tree_links.new(new_nodes["Math.006"].outputs[0], new_nodes["Capture Attribute.002"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Separate Geometry"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Vector Math.002"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Math.002"].inputs[1])
    tree_links.new(new_nodes["Vector Math.002"].outputs[0], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Join Geometry"].outputs[0], new_nodes["Capture Attribute.002"].inputs[0])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Math.003"].inputs[0])
    tree_links.new(new_nodes["Math.003"].outputs[0], new_nodes["Math.004"].inputs[0])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Math.004"].inputs[1])
    tree_links.new(new_nodes["Math.004"].outputs[0], new_nodes["Capture Attribute"].inputs[2])
    tree_links.new(new_nodes["Vector Math"].outputs[1], new_nodes["Math.001"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.002"].outputs[0], new_nodes["Capture Attribute.003"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.003"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Boolean Math"].outputs[0], new_nodes["Capture Attribute.003"].inputs[4])
    tree_links.new(new_nodes["Capture Attribute.003"].outputs[4], new_nodes["Group Output"].inputs[1])
    tree_links.new(new_nodes["Position.001"].outputs[0], new_nodes["Vector Math.003"].inputs[1])
    tree_links.new(new_nodes["Vector Rotate"].outputs[0], new_nodes["Vector Math.003"].inputs[0])
    tree_links.new(new_nodes["Vector Math.003"].outputs[0], new_nodes["Vector Math.002"].inputs[0])
    tree_links.new(new_nodes["Vector Math.002"].outputs[0], new_nodes["Geometry Proximity"].inputs[1])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False
    return new_node_group

def create_geo_ng_instance_lods_choose():
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=INSTANCE_LODS_CHOOSE_GEO_NG_NAME, type='GeometryNodeTree')
    new_node_group.inputs.new(type='NodeSocketGeometry', name="Points")
    new_node_group.inputs.new(type='NodeSocketInt', name="LOD Index")
    new_node_group.inputs.new(type='NodeSocketBool', name="Use ProxGeo")
    new_node_group.inputs.new(type='NodeSocketVector', name="Rotation")
    new_node_group.inputs.new(type='NodeSocketVector', name="Scale")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Original Distance")
    new_node_group.inputs.new(type='NodeSocketGeometry', name="LOD Geometry")
    new_node_group.inputs.new(type='NodeSocketFloat', name="LOD Distance")
    new_node_group.inputs.new(type='NodeSocketVector', name="Camera Location")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Instance Radius")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Absolute Bias Distance")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Relative Bias Factor")
    new_node_group.inputs.new(type='NodeSocketVector', name="Relative Bias Vector")
    new_node_group.outputs.new(type='NodeSocketGeometry', name="Chosen Points")
    new_node_group.outputs.new(type='NodeSocketGeometry', name="Remaining Points")
    new_node_group.outputs.new(type='NodeSocketInt', name="LOD Index")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Closest Distance")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Remaining Closest Distance")
    new_node_group.outputs.new(type='NodeSocketBool', name="Use ProxGeo")
    tree_nodes = new_node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-1280, 540)
    node.operation = "SUBTRACT"
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-380, 480)
    node.operation = "MULTIPLY_ADD"
    node.use_clamp = False
    new_nodes["Math.007"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-200, 20)
    node.operation = "GREATER_THAN"
    node.use_clamp = False
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.011"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-200, -160)
    node.operation = "GREATER_THAN"
    node.use_clamp = False
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.012"] = node

    node = tree_nodes.new(type="FunctionNodeBooleanMath")
    node.location = (-20, 20)
    node.operation = "OR"
    new_nodes["Boolean Math.002"] = node

    node = tree_nodes.new(type="GeometryNodeAttributeDomainSize")
    node.location = (-380, -200)
    node.component = "POINTCLOUD"
    new_nodes["Domain Size"] = node

    node = tree_nodes.new(type="GeometryNodeAttributeDomainSize")
    node.location = (-380, -20)
    node.component = "MESH"
    new_nodes["Domain Size.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-560, 540)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.014"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-1460, 400)
    node.operation = "MULTIPLY"
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.002"] = node

    node = tree_nodes.new(type="FunctionNodeBooleanMath")
    node.location = (-560, 380)
    node.operation = "NOT"
    node.inputs[1].default_value = False
    new_nodes["Boolean Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-20, 340)
    node.operation = "LESS_THAN"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.006"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-380, 200)
    node.operation = "MULTIPLY_ADD"
    node.use_clamp = False
    new_nodes["Math"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-200, 340)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-560, 260)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-1460, 540)
    node.operation = "DIVIDE"
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeVectorRotate")
    node.location = (-1840, 540)
    node.invert = True
    node.rotation_type = "EULER_XYZ"
    node.inputs[2].default_value = (0.0, 0.0, 1.0)
    node.inputs[3].default_value = 0.000000
    new_nodes["Vector Rotate"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-1660, 540)
    node.operation = "SUBTRACT"
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-1100, 540)
    node.operation = "LENGTH"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-920, 540)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-740, 540)
    node.operation = "GREATER_THAN"
    node.use_clamp = False
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.013"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (-2020, 360)
    new_nodes["Position"] = node

    node = tree_nodes.new(type="FunctionNodeBooleanMath")
    node.location = (160, 320)
    node.operation = "AND"
    new_nodes["Boolean Math.001"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.location = (880, 280)
    node.data_type = "FLOAT"
    node.domain = "POINT"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute.001"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.location = (880, 100)
    node.data_type = "FLOAT"
    node.domain = "POINT"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute.002"] = node

    node = tree_nodes.new(type="GeometryNodeSeparateGeometry")
    node.location = (680, 120)
    node.domain = "POINT"
    new_nodes["Separate Geometry"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (520, 260)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.008"] = node

    node = tree_nodes.new(type="FunctionNodeBooleanMath")
    node.location = (340, 260)
    node.operation = "NOT"
    node.inputs[1].default_value = False
    new_nodes["Boolean Math"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-2200, 280)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (1080, 240)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Group Input"].outputs[7], new_nodes["Math.006"].inputs[1])
    tree_links.new(new_nodes["Math.006"].outputs[0], new_nodes["Boolean Math.001"].inputs[0])
    tree_links.new(new_nodes["Boolean Math.001"].outputs[0], new_nodes["Separate Geometry"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Math.008"].inputs[1])
    tree_links.new(new_nodes["Math.008"].outputs[0], new_nodes["Group Output"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[12], new_nodes["Vector Math.002"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[7], new_nodes["Vector Math.002"].inputs[0])
    tree_links.new(new_nodes["Vector Math"].outputs[0], new_nodes["Vector Math.001"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[7], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[11], new_nodes["Math"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[10], new_nodes["Math"].inputs[2])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Math.001"].inputs[1])
    tree_links.new(new_nodes["Math.005"].outputs[0], new_nodes["Math.007"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[9], new_nodes["Math.004"].inputs[1])
    tree_links.new(new_nodes["Boolean Math.001"].outputs[0], new_nodes["Boolean Math"].inputs[0])
    tree_links.new(new_nodes["Boolean Math"].outputs[0], new_nodes["Math.008"].inputs[0])
    tree_links.new(new_nodes["Domain Size.001"].outputs[2], new_nodes["Math.011"].inputs[0])
    tree_links.new(new_nodes["Math.011"].outputs[0], new_nodes["Boolean Math.002"].inputs[0])
    tree_links.new(new_nodes["Math.012"].outputs[0], new_nodes["Boolean Math.002"].inputs[1])
    tree_links.new(new_nodes["Domain Size"].outputs[0], new_nodes["Math.012"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Domain Size.001"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Domain Size"].inputs[0])
    tree_links.new(new_nodes["Boolean Math.002"].outputs[0], new_nodes["Boolean Math.001"].inputs[1])
    tree_links.new(new_nodes["Vector Math.002"].outputs[0], new_nodes["Vector Math"].inputs[1])
    tree_links.new(new_nodes["Math.013"].outputs[0], new_nodes["Math.014"].inputs[0])
    tree_links.new(new_nodes["Boolean Math.003"].outputs[0], new_nodes["Math.007"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Math.005"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Boolean Math.003"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Math.005"].inputs[0])
    tree_links.new(new_nodes["Math.007"].outputs[0], new_nodes["Math.001"].inputs[0])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Math.006"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Group Output"].inputs[5])
    tree_links.new(new_nodes["Group Input"].outputs[8], new_nodes["Vector Rotate"].inputs[0])
    tree_links.new(new_nodes["Position"].outputs[0], new_nodes["Vector Rotate"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Vector Rotate"].inputs[4])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Vector Math.003"].inputs[1])
    tree_links.new(new_nodes["Vector Math.003"].outputs[0], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Math.014"].outputs[0], new_nodes["Math.007"].inputs[0])
    tree_links.new(new_nodes["Vector Math.001"].outputs[1], new_nodes["Math.004"].inputs[0])
    tree_links.new(new_nodes["Math.004"].outputs[0], new_nodes["Math.014"].inputs[1])
    tree_links.new(new_nodes["Math.004"].outputs[0], new_nodes["Math.013"].inputs[0])
    tree_links.new(new_nodes["Vector Rotate"].outputs[0], new_nodes["Vector Math.004"].inputs[0])
    tree_links.new(new_nodes["Position"].outputs[0], new_nodes["Vector Math.004"].inputs[1])
    tree_links.new(new_nodes["Vector Math.004"].outputs[0], new_nodes["Vector Math.003"].inputs[0])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Capture Attribute.001"].inputs[2])
    tree_links.new(new_nodes["Separate Geometry"].outputs[0], new_nodes["Capture Attribute.001"].inputs[0])
    tree_links.new(new_nodes["Separate Geometry"].outputs[1], new_nodes["Capture Attribute.002"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.002"].outputs[2], new_nodes["Group Output"].inputs[4])
    tree_links.new(new_nodes["Capture Attribute.001"].outputs[2], new_nodes["Group Output"].inputs[3])
    tree_links.new(new_nodes["Capture Attribute.001"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.002"].outputs[0], new_nodes["Group Output"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Separate Geometry"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Capture Attribute.002"].inputs[2])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False
    return new_node_group

def create_geo_ng_instance_lods():
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=INSTANCE_LODS_GEO_NG_NAME, type='GeometryNodeTree')
    new_node_group.inputs.new(type='NodeSocketGeometry', name="Points")
    new_node_group.inputs.new(type='NodeSocketBool', name="Selection")
    new_node_group.inputs.new(type='NodeSocketBool', name="Pick Instance")
    new_node_group.inputs.new(type='NodeSocketInt', name="Instance Index")
    new_node_group.inputs.new(type='NodeSocketVectorEuler', name="Rotation")
    new_node_group.inputs.new(type='NodeSocketVectorXYZ', name="Scale")
    new_node_group.inputs.new(type='NodeSocketFloatDistance', name="Instance Radius")
    new_node_group.inputs.new(type='NodeSocketVector', name="Camera Location")
    new_node_group.inputs.new(type='NodeSocketVector', name="Absolute Bias Vector")
    new_node_group.inputs.new(type='NodeSocketVector', name="Relative Bias Vector")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Absolute Bias Distance")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Relative Bias Factor")
    new_node_group.inputs.new(type='NodeSocketFloat', name="ProxGeo Test Radius")
    new_node_group.inputs.new(type='NodeSocketGeometry', name="Proximity Geometry")
    new_node_group.inputs.new(type='NodeSocketGeometry', name="LOD 0 Geometry")
    new_node_group.inputs.new(type='NodeSocketFloat', name="LOD 1 Distance")
    new_node_group.inputs.new(type='NodeSocketGeometry', name="LOD 1 Geometry")
    new_node_group.inputs.new(type='NodeSocketFloat', name="LOD 2 Distance")
    new_node_group.inputs.new(type='NodeSocketGeometry', name="LOD 2 Geometry")
    new_node_group.inputs.new(type='NodeSocketFloat', name="LOD 3 Distance")
    new_node_group.inputs.new(type='NodeSocketGeometry', name="LOD 3 Geometry")
    new_node_group.outputs.new(type='NodeSocketGeometry', name="Instances")
    new_node_group.outputs.new(type='NodeSocketInt', name="LOD Index")
    new_node_group.outputs.new(type='NodeSocketInt', name="Max LOD Index")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Closest Distance")
    tree_nodes = new_node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="GeometryNodeGroup")
    node.location = (-380, 440)
    node.node_tree = bpy.data.node_groups.get(INSTANCE_LODS_PROXIMITY_GEO_NG_NAME)
    new_nodes["Group.003"] = node

    node = tree_nodes.new(type="GeometryNodeGroup")
    node.location = (240, 440)
    node.node_tree = bpy.data.node_groups.get(INSTANCE_LODS_CHOOSE_GEO_NG_NAME)
    new_nodes["Group.001"] = node

    node = tree_nodes.new(type="GeometryNodeGroup")
    node.location = (640, 440)
    node.node_tree = bpy.data.node_groups.get(INSTANCE_LODS_CHOOSE_GEO_NG_NAME)
    new_nodes["Group"] = node

    node = tree_nodes.new(type="GeometryNodeGroup")
    node.location = (-160, 440)
    node.node_tree = bpy.data.node_groups.get(INSTANCE_LODS_CHOOSE_GEO_NG_NAME)
    node.inputs[1].default_value = 0
    new_nodes["Group.002"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-580, 440)
    node.operation = "SUBTRACT"
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.label = "Capture Closest Distance"
    node.location = (240, 680)
    node.data_type = "FLOAT"
    node.domain = "INSTANCE"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute.002"] = node

    node = tree_nodes.new(type="GeometryNodeInstanceOnPoints")
    node.label = "Instance LOD 1"
    node.location = (460, 680)
    new_nodes["Instance on Points.002"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.label = "Capture Closest Distance"
    node.location = (640, 680)
    node.data_type = "FLOAT"
    node.domain = "INSTANCE"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute.003"] = node

    node = tree_nodes.new(type="GeometryNodeJoinGeometry")
    node.location = (1420, 440)
    new_nodes["Join Geometry"] = node

    node = tree_nodes.new(type="GeometryNodeInstanceOnPoints")
    node.label = "Instance LOD 2"
    node.location = (860, 680)
    new_nodes["Instance on Points.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (860, 880)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.label = "Capture Closest Distance"
    node.location = (1040, 440)
    node.data_type = "FLOAT"
    node.domain = "INSTANCE"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute.005"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.label = "Capture Closest Distance"
    node.location = (1040, 680)
    node.data_type = "FLOAT"
    node.domain = "INSTANCE"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute.004"] = node

    node = tree_nodes.new(type="GeometryNodeInstanceOnPoints")
    node.label = "Instance LOD 3"
    node.location = (860, 440)
    new_nodes["Instance on Points"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.label = "Capture LOD Index"
    node.location = (1780, 440)
    node.data_type = "FLOAT"
    node.domain = "INSTANCE"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute.001"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.label = "Capture Closest Distance"
    node.location = (1600, 440)
    node.data_type = "FLOAT"
    node.domain = "INSTANCE"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1420, 340)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="GeometryNodeInstanceOnPoints")
    node.label = "Instance LOD 0"
    node.location = (60, 680)
    new_nodes["Instance on Points.003"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1220, 880)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-840, 440)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (1960, 440)
    node.inputs[2].default_value = 3
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Instance on Points.003"].inputs[5])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Instance on Points.003"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Instance on Points.003"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Instance on Points.003"].inputs[4])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Instance on Points.003"].inputs[6])
    tree_links.new(new_nodes["Capture Attribute"].outputs[2], new_nodes["Group Output"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Instance on Points.002"].inputs[5])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Instance on Points.002"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Instance on Points.002"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Instance on Points.002"].inputs[4])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Instance on Points.002"].inputs[6])
    tree_links.new(new_nodes["Group Input"].outputs[16], new_nodes["Instance on Points.002"].inputs[2])
    tree_links.new(new_nodes["Group.002"].outputs[0], new_nodes["Instance on Points.003"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[14], new_nodes["Instance on Points.003"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Instance on Points.001"].inputs[5])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Instance on Points.001"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Instance on Points.001"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Instance on Points.001"].inputs[4])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Instance on Points.001"].inputs[6])
    tree_links.new(new_nodes["Capture Attribute.003"].outputs[0], new_nodes["Join Geometry"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.004"].outputs[0], new_nodes["Join Geometry"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.001"].outputs[2], new_nodes["Group Output"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[18], new_nodes["Instance on Points.001"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Instance on Points"].inputs[5])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Instance on Points"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Instance on Points"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Instance on Points"].inputs[4])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Instance on Points"].inputs[6])
    tree_links.new(new_nodes["Capture Attribute.005"].outputs[0], new_nodes["Join Geometry"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[20], new_nodes["Instance on Points"].inputs[2])
    tree_links.new(new_nodes["Group.002"].outputs[1], new_nodes["Group.001"].inputs[0])
    tree_links.new(new_nodes["Group.001"].outputs[0], new_nodes["Instance on Points.002"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[13], new_nodes["Group.003"].inputs[6])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Group.003"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[12], new_nodes["Group.003"].inputs[5])
    tree_links.new(new_nodes["Vector Math"].outputs[0], new_nodes["Group.003"].inputs[4])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Group.003"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Group.003"].inputs[1])
    tree_links.new(new_nodes["Group.003"].outputs[0], new_nodes["Group.002"].inputs[0])
    tree_links.new(new_nodes["Group.003"].outputs[2], new_nodes["Group.002"].inputs[5])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Group.003"].inputs[2])
    tree_links.new(new_nodes["Group.003"].outputs[2], new_nodes["Group.001"].inputs[5])
    tree_links.new(new_nodes["Group.003"].outputs[2], new_nodes["Group"].inputs[5])
    tree_links.new(new_nodes["Group.001"].outputs[1], new_nodes["Group"].inputs[0])
    tree_links.new(new_nodes["Group.002"].outputs[2], new_nodes["Group.001"].inputs[1])
    tree_links.new(new_nodes["Group.001"].outputs[2], new_nodes["Group"].inputs[1])
    tree_links.new(new_nodes["Group"].outputs[2], new_nodes["Capture Attribute.001"].inputs[2])
    tree_links.new(new_nodes["Group"].outputs[0], new_nodes["Instance on Points.001"].inputs[0])
    tree_links.new(new_nodes["Group"].outputs[1], new_nodes["Instance on Points"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[15], new_nodes["Group.002"].inputs[7])
    tree_links.new(new_nodes["Group Input"].outputs[17], new_nodes["Group.001"].inputs[7])
    tree_links.new(new_nodes["Group Input"].outputs[19], new_nodes["Group"].inputs[7])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Group.002"].inputs[9])
    tree_links.new(new_nodes["Group Input"].outputs[10], new_nodes["Group.002"].inputs[10])
    tree_links.new(new_nodes["Group Input"].outputs[11], new_nodes["Group.002"].inputs[11])
    tree_links.new(new_nodes["Group Input"].outputs[9], new_nodes["Group.002"].inputs[12])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Group.001"].inputs[9])
    tree_links.new(new_nodes["Group Input"].outputs[10], new_nodes["Group.001"].inputs[10])
    tree_links.new(new_nodes["Group Input"].outputs[11], new_nodes["Group.001"].inputs[11])
    tree_links.new(new_nodes["Group Input"].outputs[9], new_nodes["Group.001"].inputs[12])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Group"].inputs[9])
    tree_links.new(new_nodes["Group Input"].outputs[10], new_nodes["Group"].inputs[10])
    tree_links.new(new_nodes["Group Input"].outputs[11], new_nodes["Group"].inputs[11])
    tree_links.new(new_nodes["Group Input"].outputs[9], new_nodes["Group"].inputs[12])
    tree_links.new(new_nodes["Capture Attribute"].outputs[0], new_nodes["Capture Attribute.001"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.001"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Join Geometry"].outputs[0], new_nodes["Capture Attribute"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[14], new_nodes["Group.002"].inputs[6])
    tree_links.new(new_nodes["Group Input"].outputs[16], new_nodes["Group.001"].inputs[6])
    tree_links.new(new_nodes["Group Input"].outputs[18], new_nodes["Group"].inputs[6])
    tree_links.new(new_nodes["Group Input"].outputs[7], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[8], new_nodes["Vector Math"].inputs[1])
    tree_links.new(new_nodes["Vector Math"].outputs[0], new_nodes["Group.002"].inputs[8])
    tree_links.new(new_nodes["Vector Math"].outputs[0], new_nodes["Group.001"].inputs[8])
    tree_links.new(new_nodes["Vector Math"].outputs[0], new_nodes["Group"].inputs[8])
    tree_links.new(new_nodes["Group.002"].outputs[5], new_nodes["Group.001"].inputs[2])
    tree_links.new(new_nodes["Group.001"].outputs[5], new_nodes["Group"].inputs[2])
    tree_links.new(new_nodes["Group.003"].outputs[1], new_nodes["Group.002"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Group.002"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Group.001"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Group"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Group.002"].inputs[4])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Group.001"].inputs[4])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Group"].inputs[4])
    tree_links.new(new_nodes["Instance on Points.003"].outputs[0], new_nodes["Capture Attribute.002"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.002"].outputs[0], new_nodes["Join Geometry"].inputs[0])
    tree_links.new(new_nodes["Group.002"].outputs[3], new_nodes["Capture Attribute.002"].inputs[2])
    tree_links.new(new_nodes["Instance on Points.002"].outputs[0], new_nodes["Capture Attribute.003"].inputs[0])
    tree_links.new(new_nodes["Group.001"].outputs[3], new_nodes["Capture Attribute.003"].inputs[2])
    tree_links.new(new_nodes["Instance on Points.001"].outputs[0], new_nodes["Capture Attribute.004"].inputs[0])
    tree_links.new(new_nodes["Group"].outputs[3], new_nodes["Capture Attribute.004"].inputs[2])
    tree_links.new(new_nodes["Instance on Points"].outputs[0], new_nodes["Capture Attribute.005"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.003"].outputs[2], new_nodes["Math.001"].inputs[1])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Capture Attribute"].inputs[2])
    tree_links.new(new_nodes["Capture Attribute.002"].outputs[2], new_nodes["Math.001"].inputs[0])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Math.002"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.005"].outputs[2], new_nodes["Math.002"].inputs[1])
    tree_links.new(new_nodes["Capture Attribute.004"].outputs[2], new_nodes["Math"].inputs[1])
    tree_links.new(new_nodes["Group"].outputs[4], new_nodes["Capture Attribute.005"].inputs[2])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False
    return new_node_group

def create_prereq_util_node_group(node_group_name, node_tree_type):
    if node_group_name == GEOMETRY_LODS_PROXIMITY_GEO_NG_NAME:
        return create_geo_ng_geometry_lods_proximity()
    elif node_group_name == GEOMETRY_LODS_CHOOSE_GEO_NG_NAME:
        return create_geo_ng_geometry_lods_choose()
    elif node_group_name == GEOMETRY_LODS_GEO_NG_NAME:
        return create_geo_ng_geometry_lods()
    elif node_group_name == INSTANCE_LODS_PROXIMITY_GEO_NG_NAME:
        return create_geo_ng_instance_lods_proximity()
    elif node_group_name == INSTANCE_LODS_CHOOSE_GEO_NG_NAME:
        return create_geo_ng_instance_lods_choose()
    elif node_group_name == INSTANCE_LODS_GEO_NG_NAME:
        return create_geo_ng_instance_lods()

    # error
    print("Unknown name passed to create_prereq_util_node_group: " + str(node_group_name))
    return None

def create_input_geometry_lods_nodes(tree_nodes, tree_links, cam_obj_name, special_node):
    # initialize variables
    new_nodes = { "Group": special_node }

    # create node
    node = tree_nodes.new(type="GeometryNodeObjectInfo")
    node.location = (-330, -115)
    node.transform_space = "RELATIVE"
    node.inputs[0].default_value = bpy.data.objects.get(cam_obj_name)
    node.inputs[1].default_value = False
    new_nodes["Object Info"] = node

    # create link
    tree_links.new(new_nodes["Object Info"].outputs[0], new_nodes["Group"].inputs[0])

def create_geometry_lods_geo_nodes(context, cam_obj_name, override_create):
    ensure_node_groups(override_create, [GEOMETRY_LODS_PROXIMITY_GEO_NG_NAME,
                                         GEOMETRY_LODS_CHOOSE_GEO_NG_NAME,
                                         GEOMETRY_LODS_GEO_NG_NAME],
                                         'GeometryNodeTree', create_prereq_util_node_group)

    # create group node that will do the work
    node = context.space_data.edit_tree.nodes.new(type='GeometryNodeGroup')
    node.location = (-160, -120)
    node.node_tree = bpy.data.node_groups.get(GEOMETRY_LODS_GEO_NG_NAME)
    node.inputs[0].default_value = (0.0, 0.0, 0.0)
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 0.0
    node.inputs[4].default_value = 0.0
    node.inputs[5].default_value = 0.0
    node.inputs[9].default_value = 100.0
    node.inputs[11].default_value = 500.0
    node.inputs[13].default_value = 1000.0

    # create the 'input' nodes
    tr = context.space_data.edit_tree
    create_input_geometry_lods_nodes(tr.nodes, tr.links, cam_obj_name, node)

class BSR_GeometryLODsCreateNodes(bpy.types.Operator):
    bl_description = "Add nodes to current node tree that choose Level Of Detail geometry by distance"
    bl_idname = "big_space_rig.geometry_lods_create_geo_node"
    bl_label = "Geometry LODs"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scn = context.scene
        create_geometry_lods_geo_nodes(context, scn.BSR_LODsCamera[1:len(scn.BSR_LODsCamera)],
                                     scn.BSR_NodesOverrideCreate)
        return {'FINISHED'}

def create_input_instance_lods_nodes(tree_nodes, tree_links, cam_obj_name, special_node):
    # initialize variables
    new_nodes = { "Group": special_node }

    # create nodes
    node = tree_nodes.new(type="GeometryNodeObjectInfo")
    node.location = (-360, -450)
    node.transform_space = "RELATIVE"
    node.inputs[0].default_value = bpy.data.objects.get(cam_obj_name)
    node.inputs[1].default_value = False
    new_nodes["Object Info"] = node

    # create links
    tree_links.new(new_nodes["Object Info"].outputs[0], new_nodes["Group"].inputs[7])

def create_instance_lods_geo_nodes(context, cam_obj_name, override_create):
    ensure_node_groups(override_create, [INSTANCE_LODS_PROXIMITY_GEO_NG_NAME,
                                         INSTANCE_LODS_CHOOSE_GEO_NG_NAME,
                                         INSTANCE_LODS_GEO_NG_NAME],
                                         'GeometryNodeTree', create_prereq_util_node_group)
    # create group node that will do the work
    node = context.space_data.edit_tree.nodes.new(type='GeometryNodeGroup')
    node.location = (-160, -120)
    node.node_tree = bpy.data.node_groups.get(INSTANCE_LODS_GEO_NG_NAME)
    node.inputs[1].default_value = True
    node.inputs[2].default_value = False
    node.inputs[3].default_value = 0
    node.inputs[4].default_value = (0.0, 0.0, 0.0)
    node.inputs[5].default_value = (1.0, 1.0, 1.0)
    node.inputs[6].default_value = 0.0
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (0.0, 0.0, 0.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = 0.0
    node.inputs[11].default_value = 0.0
    node.inputs[12].default_value = 0.0
    node.inputs[15].default_value = 100.0
    node.inputs[17].default_value = 500.0
    node.inputs[19].default_value = 1000.0

    # create the 'input' nodes
    tr = context.space_data.edit_tree
    create_input_instance_lods_nodes(tr.nodes, tr.links, cam_obj_name, node)

class BSR_InstanceLODsCreateNodes(bpy.types.Operator):
    bl_description = "Add nodes to current node tree that choose Level Of Detail instance geometry by distance"
    bl_idname = "big_space_rig.instance_lods_create_geo_node"
    bl_label = "Instance LODs"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scn = context.scene
        create_instance_lods_geo_nodes(context, scn.BSR_LODsCamera[1:len(scn.BSR_LODsCamera)],
                                       scn.BSR_NodesOverrideCreate)
        return {'FINISHED'}
