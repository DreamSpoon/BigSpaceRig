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

from .rig import is_big_space_rig
from .rig import (PROXY_OBSERVER_0E_BNAME, PROXY_OBSERVER_6E_BNAME)
from .attach import (PROXY_PLACE_0E_VAR_NAME_PREPEND, PROXY_PLACE_6E_VAR_NAME_PREPEND)
from .node_other import (get_0e_6e_from_place_bone_name)

MEGASPHERE_SCALE_FOR_DIST_GEO_NG_NAME = "MegaSphere.ScaleForDist.BSR.GeoNG"
MEGASPHERE_CULL_ANGLE_GEO_NG_NAME = "MegaSphere.CullAngle.BSR.GeoNG"
MEGASPHERE_CULL_DIST_GEO_NG_NAME = "MegaSphere.CullDist.BSR.GeoNG"
MEGASPHERE_LOD_GEO_NG_NAME = "MegaSphere.LOD.BSR.GeoNG"
MEGASPHERE_SUBDIV_GEO_NG_NAME = "MegaSphere.Subdiv.BSR.GeoNG"
MEGASPHERE_ITERATE_GEO_NG_NAME = "MegaSphere.Iterate.BSR.GeoNG"
MEGASPHERE_GEO_NG_NAME = "MegaSphere.BSR.GeoNG"
MEGASPHERE_INDIVIDUAL_NG_NAME = "MegaSphereIndividual"

MEGASPHERE_OBJ_NAME = "MegaSphere"

def create_geo_ng_scale_for_dist():
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=MEGASPHERE_SCALE_FOR_DIST_GEO_NG_NAME, type='GeometryNodeTree')
    new_node_group.inputs.new(type='NodeSocketFloat', name="Subdiv Scale")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Mega Sphere Radius")
    new_node_group.inputs.new(type='NodeSocketVector', name="Observer 6e Loc")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Max Subdiv")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Scale Step")
    tree_nodes = new_node_group.nodes
    # delete old nodes before adding new nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Observer to sphere surface dist"
    node.location = (80, 100)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = 1000.0
    new_nodes["Math"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (260, 100)
    node.operation = "POWER"
    node.inputs[1].default_value = 0.125
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Check zero dist"
    node.location = (440, 100)
    node.operation = "LESS_THAN"
    node.inputs[1].default_value = 9.999999747378752e-05
    new_nodes["Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (440, -60)
    node.operation = "DIVIDE"
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Fix zero dist"
    node.location = (620, 80)
    node.operation = "MULTIPLY_ADD"
    new_nodes["Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-100, 60)
    node.operation = "MULTIPLY_ADD"
    new_nodes["Math.007"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.label = "Observer 6e less sphere surface"
    node.location = (-460, -80)
    node.operation = "SUBTRACT"
    new_nodes["Vector Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-640, -80)
    node.operation = "MULTIPLY"
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-820, -100)
    node.operation = "NORMALIZE"
    new_nodes["Vector Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-280, -80)
    node.operation = "LENGTH"
    new_nodes["Vector Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-460, -240)
    node.operation = "COMPARE"
    node.inputs[1].default_value = 0.0
    node.inputs[2].default_value = 0.0
    new_nodes["Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-640, -260)
    node.operation = "LENGTH"
    new_nodes["Vector Math.004"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-1020, 20)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (800, 80)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Vector Math"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Vector Math.002"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Math.002"].inputs[0])
    tree_links.new(new_nodes["Math.004"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Vector Math.001"].outputs[0], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Vector Math"].outputs[0], new_nodes["Vector Math.002"].inputs[1])
    tree_links.new(new_nodes["Vector Math.002"].outputs[0], new_nodes["Vector Math.003"].inputs[0])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Math.001"].inputs[0])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Math.002"].inputs[1])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Math.003"].inputs[0])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Math.004"].inputs[2])
    tree_links.new(new_nodes["Math.003"].outputs[0], new_nodes["Math.004"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Vector Math.001"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Math.004"].inputs[1])
    tree_links.new(new_nodes["Math.005"].outputs[0], new_nodes["Math.007"].inputs[1])
    tree_links.new(new_nodes["Vector Math.003"].outputs[1], new_nodes["Math.007"].inputs[2])
    tree_links.new(new_nodes["Math.007"].outputs[0], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Math.007"].inputs[0])
    tree_links.new(new_nodes["Vector Math.001"].outputs[0], new_nodes["Vector Math.004"].inputs[0])
    tree_links.new(new_nodes["Vector Math.004"].outputs[1], new_nodes["Math.005"].inputs[0])

    return new_node_group

def create_geo_ng_cull_by_angle():
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=MEGASPHERE_CULL_ANGLE_GEO_NG_NAME, type='GeometryNodeTree')
    new_node_group.inputs.new(type='NodeSocketGeometry', name="Geometry")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Mega Sphere Radius")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Vis Angle Adjust")
    new_node_group.inputs.new(type='NodeSocketVector', name="Observer 6e Loc")
    new_node_group.outputs.new(type='NodeSocketGeometry', name="Geometry")
    tree_nodes = new_node_group.nodes    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Adjust"
    node.location = (110, -160)
    node.operation = "ADD"
    new_nodes["Math.006"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Outside visible angle cull"
    node.location = (285, 15)
    node.operation = "LESS_THAN"
    new_nodes["Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-105, 0)
    node.operation = "NORMALIZE"
    new_nodes["Vector Math.008"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (-105, -120)
    new_nodes["Position.003"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.label = "cos angle observer vertice"
    node.location = (75, 10)
    node.operation = "DOT_PRODUCT"
    new_nodes["Vector Math.009"] = node

    node = tree_nodes.new(type="GeometryNodeDeleteGeometry")
    node.label = "Delete by angle cull"
    node.location = (485, 165)
    new_nodes["Delete Geometry"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (-80, -300)
    node.clamp = True
    node.inputs[1].default_value = 0.5
    node.inputs[2].default_value = 1.0
    node.inputs[3].default_value = 0.0
    node.inputs[4].default_value = 0.9975
    new_nodes["Map Range.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Cos max vis angle"
    node.location = (-255, -350)
    node.operation = "DIVIDE"
    new_nodes["Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-420, -470)
    node.operation = "LENGTH"
    new_nodes["Vector Math.010"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-655, -300)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (645, 0)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Delete Geometry"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Delete Geometry"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Vector Math.008"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Math.005"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Math.006"].inputs[0])
    tree_links.new(new_nodes["Vector Math.008"].outputs[0], new_nodes["Vector Math.009"].inputs[0])
    tree_links.new(new_nodes["Position.003"].outputs[0], new_nodes["Vector Math.009"].inputs[1])
    tree_links.new(new_nodes["Vector Math.009"].outputs[1], new_nodes["Math.003"].inputs[0])
    tree_links.new(new_nodes["Math.003"].outputs[0], new_nodes["Delete Geometry"].inputs[1])
    tree_links.new(new_nodes["Vector Math.010"].outputs[1], new_nodes["Math.005"].inputs[1])
    tree_links.new(new_nodes["Math.006"].outputs[0], new_nodes["Math.003"].inputs[1])
    tree_links.new(new_nodes["Math.005"].outputs[0], new_nodes["Map Range.001"].inputs[0])
    tree_links.new(new_nodes["Map Range.001"].outputs[0], new_nodes["Math.006"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Vector Math.010"].inputs[0])

    return new_node_group

def create_geo_ng_cull_by_dist():
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=MEGASPHERE_CULL_DIST_GEO_NG_NAME, type='GeometryNodeTree')
    new_node_group.inputs.new(type='NodeSocketGeometry', name="Geometry")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Sphere Radius")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Face Size Fix")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Desired Cull Dist")
    new_node_group.outputs.new(type='NodeSocketGeometry', name="Geometry")
    tree_nodes = new_node_group.nodes
    # delete old nodes before creating new nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-880, -645)
    node.operation = "MULTIPLY"
    new_nodes["Math"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-700, -725)
    node.operation = "GREATER_THAN"
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-510, -570)
    node.operation = "MULTIPLY"
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="FunctionNodeBooleanMath")
    node.location = (-505, -735)
    new_nodes["Boolean Math"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Greater of Cull Dist and Face Size Fix"
    node.location = (-285, -710)
    node.operation = "MULTIPLY_ADD"
    new_nodes["Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-40, -580)
    node.operation = "LENGTH"
    new_nodes["Vector Math.007"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (-205, -560)
    new_nodes["Position.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Greater than cull dist"
    node.location = (145, -580)
    node.operation = "GREATER_THAN"
    new_nodes["Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (325, -620)
    node.operation = "SUBTRACT"
    new_nodes["Math.006"] = node

    node = tree_nodes.new(type="GeometryNodeDeleteGeometry")
    node.label = "Delete by dist cull"
    node.location = (520, -440)
    node.domain = 'FACE'
    new_nodes["Delete Geometry.001"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (725, -470)
    new_nodes["Group Output"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-1150, -505)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (150, -770)
    node.operation = "COMPARE"
    node.inputs[1].default_value = 0.0
    node.inputs[2].default_value = 0.0
    new_nodes["Math.005"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Delete Geometry.001"].inputs[0])
    tree_links.new(new_nodes["Position.002"].outputs[0], new_nodes["Vector Math.007"].inputs[0])
    tree_links.new(new_nodes["Vector Math.007"].outputs[1], new_nodes["Math.004"].inputs[0])
    tree_links.new(new_nodes["Delete Geometry.001"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Math"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Math.001"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Math.001"].inputs[1])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Math.002"].inputs[0])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Math.002"].inputs[1])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Boolean Math"].inputs[0])
    tree_links.new(new_nodes["Boolean Math"].outputs[0], new_nodes["Math.003"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Math.003"].inputs[1])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Math.003"].inputs[2])
    tree_links.new(new_nodes["Math.003"].outputs[0], new_nodes["Math.004"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Math.005"].inputs[0])
    tree_links.new(new_nodes["Math.005"].outputs[0], new_nodes["Math.006"].inputs[1])
    tree_links.new(new_nodes["Math.004"].outputs[0], new_nodes["Math.006"].inputs[0])
    tree_links.new(new_nodes["Math.006"].outputs[0], new_nodes["Delete Geometry.001"].inputs[1])

    return new_node_group

def create_geo_ng_level_of_detail():
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=MEGASPHERE_LOD_GEO_NG_NAME, type='GeometryNodeTree')
    new_node_group.inputs.new(type='NodeSocketGeometry', name="Geometry")
    new_node_group.inputs.new(type='NodeSocketFloat', name="LOD Distance")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Sphere Radius")
    new_node_group.outputs.new(type='NodeSocketGeometry', name="LOD Geometry")
    new_node_group.outputs.new(type='NodeSocketGeometry', name="Geometry")
    tree_nodes = new_node_group.nodes
    # delete old nodes before adding new nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (-755, 30)
    new_nodes["Position.003"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Greater than LOD dist"
    node.location = (-420, 80)
    node.operation = "GREATER_THAN"
    new_nodes["Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-590, 70)
    node.operation = "LENGTH"
    new_nodes["Vector Math.008"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "LOD Dist > 0"
    node.location = (-425, -105)
    node.operation = "GREATER_THAN"
    node.inputs[1].default_value = 0.0
    new_nodes["Math.010"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-1035, 125)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="GeometryNodeSeparateGeometry")
    node.location = (-35, 205)
    node.domain = 'FACE'
    new_nodes["Separate Geometry"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (195, 160)
    new_nodes["Group Output"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-655, -95)
    node.operation = "MULTIPLY"
    new_nodes["Math"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "If LOD allowed"
    node.location = (-230, 50)
    node.operation = "MULTIPLY"
    new_nodes["Math.012"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Separate Geometry"].inputs[0])
    tree_links.new(new_nodes["Separate Geometry"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Math.010"].inputs[0])
    tree_links.new(new_nodes["Position.003"].outputs[0], new_nodes["Vector Math.008"].inputs[0])
    tree_links.new(new_nodes["Vector Math.008"].outputs[1], new_nodes["Math.005"].inputs[0])
    tree_links.new(new_nodes["Math.005"].outputs[0], new_nodes["Math.012"].inputs[0])
    tree_links.new(new_nodes["Math.010"].outputs[0], new_nodes["Math.012"].inputs[1])
    tree_links.new(new_nodes["Math.012"].outputs[0], new_nodes["Separate Geometry"].inputs[1])
    tree_links.new(new_nodes["Separate Geometry"].outputs[1], new_nodes["Group Output"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Math"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Math.005"].inputs[1])

    return new_node_group

def create_geo_ng_subdiv():
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=MEGASPHERE_SUBDIV_GEO_NG_NAME, type='GeometryNodeTree')
    new_node_group.inputs.new(type='NodeSocketGeometry', name="Geometry")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Subdiv")
    new_node_group.inputs.new(type='NodeSocketInt', name="Max Faces")
    new_node_group.inputs.new(type='NodeSocketInt', name="Add Faces")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Dist Subdiv Min")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Dist Subdiv Max")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Add Subdiv Min")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Add Subdiv Max")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Crease Start Dist")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Crease Delta Dist")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Sphere Radius")
    new_node_group.inputs.new(type='NodeSocketBool', name="Max FaceCount")
    new_node_group.outputs.new(type='NodeSocketGeometry', name="Mesh")
    new_node_group.outputs.new(type='NodeSocketBool', name="Max FaceCount")
    tree_nodes = new_node_group.nodes
    # delete old nodes before adding new nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-620, -665)
    node.operation = "MULTIPLY"
    new_nodes["Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-810, -800)
    node.operation = "POWER"
    node.inputs[0].default_value = 4.0
    new_nodes["Math.004"] = node

    node = tree_nodes.new(type="GeometryNodeAttributeDomainSize")
    node.location = (-810, -605)
    new_nodes["Domain Size"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-440, -540)
    node.operation = "ADD"
    new_nodes["Math.005"] = node

    node = tree_nodes.new(type="FunctionNodeBooleanMath")
    node.location = (125, -305)
    new_nodes["Boolean Math.001"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (505, -70)
    new_nodes["Group Output"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (-65, 235)
    new_nodes["Map Range.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (125, -135)
    node.operation = "DIVIDE"
    node.use_clamp = True
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Face count check"
    node.location = (130, 35)
    node.operation = "MULTIPLY"
    new_nodes["Math.011"] = node

    node = tree_nodes.new(type="GeometryNodeSubdivisionSurface")
    node.location = (320, 75)
    new_nodes["Subdivision Surface"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-65, -95)
    node.operation = "SUBTRACT"
    new_nodes["Math"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-420, -60)
    node.operation = "LENGTH"
    new_nodes["Vector Math.008"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (-580, -90)
    new_nodes["Position.003"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-240, -55)
    node.operation = "DIVIDE"
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-255, -490)
    node.operation = "LESS_THAN"
    new_nodes["Math.010"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-70, -340)
    node.operation = "SUBTRACT"
    new_nodes["Math.012"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-1185, 5)
    new_nodes["Group Input"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Subdivision Surface"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Map Range.002"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Domain Size"].inputs[0])
    tree_links.new(new_nodes["Math.005"].outputs[0], new_nodes["Math.010"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Map Range.002"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Map Range.002"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Map Range.002"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[7], new_nodes["Map Range.002"].inputs[4])
    tree_links.new(new_nodes["Math.011"].outputs[0], new_nodes["Subdivision Surface"].inputs[1])
    tree_links.new(new_nodes["Map Range.002"].outputs[0], new_nodes["Math.011"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Subdivision Surface"].inputs[0])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[8], new_nodes["Math"].inputs[1])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Subdivision Surface"].inputs[2])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Math.001"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[9], new_nodes["Math.001"].inputs[1])
    tree_links.new(new_nodes["Position.003"].outputs[0], new_nodes["Vector Math.008"].inputs[0])
    tree_links.new(new_nodes["Vector Math.008"].outputs[1], new_nodes["Math.002"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[10], new_nodes["Math.002"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[7], new_nodes["Math.004"].inputs[1])
    tree_links.new(new_nodes["Math.004"].outputs[0], new_nodes["Math.003"].inputs[1])
    tree_links.new(new_nodes["Domain Size"].outputs[2], new_nodes["Math.003"].inputs[0])
    tree_links.new(new_nodes["Math.003"].outputs[0], new_nodes["Math.005"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Math.005"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Math.010"].inputs[1])
    tree_links.new(new_nodes["Boolean Math.001"].outputs[0], new_nodes["Group Output"].inputs[1])
    tree_links.new(new_nodes["Math.010"].outputs[0], new_nodes["Math.012"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[11], new_nodes["Math.012"].inputs[1])
    tree_links.new(new_nodes["Math.012"].outputs[0], new_nodes["Boolean Math.001"].inputs[0])
    tree_links.new(new_nodes["Math.012"].outputs[0], new_nodes["Math.011"].inputs[1])

    return new_node_group

def create_geo_ng_iterate():
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=MEGASPHERE_ITERATE_GEO_NG_NAME, type='GeometryNodeTree')
    new_node_group.inputs.new(type='NodeSocketGeometry', name="LOD Geometry")
    new_node_group.inputs.new(type='NodeSocketGeometry', name="Geometry")
    new_node_group.inputs.new(type='NodeSocketInt', name="Max Faces")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Subdiv")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Sphere Radius")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Desired Cull Dist")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Dist Subdiv Min")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Crease Start Dist")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Crease Delta Dist")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Face Size Fix")
    new_node_group.inputs.new(type='NodeSocketFloat', name="LOD Distance")
    new_node_group.inputs.new(type='NodeSocketBool', name="Max FaceCount")
    new_node_group.outputs.new(type='NodeSocketGeometry', name="LOD Geometry")
    new_node_group.outputs.new(type='NodeSocketGeometry', name="Geometry")
    new_node_group.outputs.new(type='NodeSocketBool', name="Max FaceCount")
    tree_nodes = new_node_group.nodes
    # delete old nodes before creating new nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="GeometryNodeGroup")
    node.location = (-180, -300)
    node.node_tree = bpy.data.node_groups.get(MEGASPHERE_CULL_DIST_GEO_NG_NAME)
    new_nodes["Group.045"] = node

    node = tree_nodes.new(type="GeometryNodeGroup")
    node.location = (60, -400)
    node.node_tree = bpy.data.node_groups.get(MEGASPHERE_LOD_GEO_NG_NAME)
    new_nodes["Group.046"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-1040, -60)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="GeometryNodeAttributeDomainSize")
    node.location = (-860, 160)
    new_nodes["Domain Size.007"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-800, -340)
    node.operation = "ADD"
    node.inputs[1].default_value = 2.0
    new_nodes["Math"] = node

    node = tree_nodes.new(type="GeometryNodeGroup")
    node.location = (-460, 0)
    node.node_tree = bpy.data.node_groups.get(MEGASPHERE_SUBDIV_GEO_NG_NAME)
    node.inputs[6].default_value = 0.0
    node.inputs[7].default_value = 2.0
    new_nodes["Group.044"] = node

    node = tree_nodes.new(type="GeometryNodeGroup")
    node.location = (-460, 200)
    node.node_tree = bpy.data.node_groups.get(MEGASPHERE_CULL_DIST_GEO_NG_NAME)
    new_nodes["Group.043"] = node

    node = tree_nodes.new(type="GeometryNodeJoinGeometry")
    node.location = (340, -40)
    new_nodes["Join Geometry.008"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (520, -80)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Domain Size.007"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Group.044"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Group.044"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Group.045"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Group.045"].inputs[3])
    tree_links.new(new_nodes["Join Geometry.008"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[11], new_nodes["Group.044"].inputs[11])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Group.044"].inputs[0])
    tree_links.new(new_nodes["Group.044"].outputs[1], new_nodes["Group Output"].inputs[2])
    tree_links.new(new_nodes["Group.046"].outputs[1], new_nodes["Group Output"].inputs[1])
    tree_links.new(new_nodes["Group.044"].outputs[0], new_nodes["Group.045"].inputs[0])
    tree_links.new(new_nodes["Group.045"].outputs[0], new_nodes["Group.046"].inputs[0])
    tree_links.new(new_nodes["Group.046"].outputs[0], new_nodes["Join Geometry.008"].inputs[0])
    tree_links.new(new_nodes["Group.043"].outputs[0], new_nodes["Join Geometry.008"].inputs[0])
    tree_links.new(new_nodes["Domain Size.007"].outputs[2], new_nodes["Group.044"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Group.043"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Group.046"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Group.044"].inputs[10])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Group.043"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Group.044"].inputs[4])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Group.044"].inputs[5])
    tree_links.new(new_nodes["Group Input"].outputs[7], new_nodes["Group.044"].inputs[8])
    tree_links.new(new_nodes["Group Input"].outputs[8], new_nodes["Group.044"].inputs[9])
    tree_links.new(new_nodes["Group Input"].outputs[9], new_nodes["Group.045"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[10], new_nodes["Group.046"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[9], new_nodes["Group.043"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Group.043"].inputs[0])

    return new_node_group

def create_geo_ng_megasphere():
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=MEGASPHERE_GEO_NG_NAME, type='GeometryNodeTree')
    new_node_group.inputs.new(type='NodeSocketFloat', name="Subdivision Scale")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Mega Sphere Radius")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Vis Angle Adjust")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Cull Distance")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Max Subdiv")
    new_node_group.inputs.new(type='NodeSocketInt', name="Max Face Count")
    new_node_group.inputs.new(type='NodeSocketVector', name="Observer 6e Loc")
    new_node_group.inputs.new(type='NodeSocketVector', name="Observer 0e Loc")
    new_node_group.outputs.new(type='NodeSocketGeometry', name="Geometry")
    new_node_group.outputs.new(type='NodeSocketVector', name="Original Loc")
    new_node_group.outputs.new(type='NodeSocketBool', name="Max FaceCount")
    tree_nodes = new_node_group.nodes
    # delete old nodes before adding new nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="GeometryNodeGroup")
    node.location = (340, -140)
    node.node_tree = bpy.data.node_groups.get(MEGASPHERE_ITERATE_GEO_NG_NAME)
    node.inputs[6].default_value = 13.0
    node.inputs[7].default_value = 1.8
    node.inputs[8].default_value = 0.45
    node.inputs[9].default_value = 0.3703700006008148
    node.inputs[10].default_value = 0.7407400012016296
    new_nodes["Group.006"] = node

    node = tree_nodes.new(type="GeometryNodeGroup")
    node.location = (1640, -140)
    node.node_tree = bpy.data.node_groups.get(MEGASPHERE_ITERATE_GEO_NG_NAME)
    node.inputs[6].default_value = 19.0
    node.inputs[7].default_value = 65.0
    node.inputs[8].default_value = 15.0
    node.inputs[9].default_value = 13.717399597167969
    node.inputs[10].default_value = 27.434900283813477
    new_nodes["Group.002"] = node

    node = tree_nodes.new(type="GeometryNodeGroup")
    node.location = (1160, -140)
    node.node_tree = bpy.data.node_groups.get(MEGASPHERE_ITERATE_GEO_NG_NAME)
    node.inputs[6].default_value = 15.0
    node.inputs[7].default_value = 600.0
    node.inputs[8].default_value = 150.0
    node.inputs[9].default_value = 123.45700073242188
    node.inputs[10].default_value = 246.91400146484375
    new_nodes["Group.005"] = node

    node = tree_nodes.new(type="GeometryNodeGroup")
    node.location = (1400, -140)
    node.node_tree = bpy.data.node_groups.get(MEGASPHERE_ITERATE_GEO_NG_NAME)
    node.inputs[6].default_value = 17.0
    node.inputs[7].default_value = 200.0
    node.inputs[8].default_value = 20.0
    node.inputs[9].default_value = 41.15230178833008
    node.inputs[10].default_value = 82.30460357666016
    new_nodes["Group.003"] = node

    node = tree_nodes.new(type="GeometryNodeGroup")
    node.location = (1880, -140)
    node.node_tree = bpy.data.node_groups.get(MEGASPHERE_ITERATE_GEO_NG_NAME)
    node.inputs[6].default_value = 21.0
    node.inputs[7].default_value = 21.66670036315918
    node.inputs[8].default_value = 5.0
    node.inputs[9].default_value = 4.572470188140869
    node.inputs[10].default_value = 9.144969940185547
    new_nodes["Group.001"] = node

    node = tree_nodes.new(type="GeometryNodeSetPosition")
    node.location = (940, -380)
    new_nodes["Set Position.001"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (760, -520)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = (-1.0, -1.0, -1.0)
    new_nodes["Vector Math.006"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (760, -300)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = (1000.0, 1000.0, 1000.0)
    new_nodes["Vector Math.003"] = node

    node = tree_nodes.new(type="GeometryNodeSetPosition")
    node.location = (940, 60)
    new_nodes["Set Position.003"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (580, 120)
    new_nodes["Position.004"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (760, -80)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = (-1.0, -1.0, -1.0)
    new_nodes["Vector Math.007"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (760, 140)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = (1000.0, 1000.0, 1000.0)
    new_nodes["Vector Math.005"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (580, -320)
    new_nodes["Position.002"] = node

    node = tree_nodes.new(type="GeometryNodeGroup")
    node.location = (100, -140)
    node.node_tree = bpy.data.node_groups.get(MEGASPHERE_ITERATE_GEO_NG_NAME)
    node.inputs[6].default_value = 11.0
    node.inputs[7].default_value = 4.75
    node.inputs[8].default_value = 2.0
    node.inputs[9].default_value = 1.111109972000122
    node.inputs[10].default_value = 2.222219944000244
    new_nodes["Group.009"] = node

    node = tree_nodes.new(type="GeometryNodeGroup")
    node.location = (-140, -140)
    node.node_tree = bpy.data.node_groups.get(MEGASPHERE_ITERATE_GEO_NG_NAME)
    node.inputs[6].default_value = 9.0
    node.inputs[7].default_value = 22.0
    node.inputs[8].default_value = 5.5
    node.inputs[9].default_value = 3.333329916000366
    node.inputs[10].default_value = 6.666659832000732
    new_nodes["Group.010"] = node

    node = tree_nodes.new(type="GeometryNodeGroup")
    node.label = "Cull by distance"
    node.location = (-660, -240)
    node.node_tree = bpy.data.node_groups.get(MEGASPHERE_CULL_DIST_GEO_NG_NAME)
    node.inputs[2].default_value = 15.0
    new_nodes["Group.004"] = node

    node = tree_nodes.new(type="GeometryNodeGroup")
    node.location = (-400, -240)
    node.node_tree = bpy.data.node_groups.get(MEGASPHERE_LOD_GEO_NG_NAME)
    node.inputs[1].default_value = 30.0
    new_nodes["Group.011"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-860, -420)
    node.operation = "DIVIDE"
    node.inputs[0].default_value = 0.5
    node.inputs[1].default_value = 1000.0
    node.inputs[2].default_value = 0.5
    node.outputs[0].default_value = 0.0
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="GeometryNodeSetPosition")
    node.location = (-1060, -300)
    new_nodes["Set Position"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-1240, -540)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = (1000.0, 1000.0, 1000.0)
    new_nodes["Vector Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-1600, -540)
    node.operation = "MULTIPLY"
    new_nodes["Vector Math.002"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (-1780, -560)
    new_nodes["Position"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-1420, -600)
    node.operation = "SUBTRACT"
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.label = "Capture original loc"
    node.location = (-1280, -140)
    node.data_type = 'FLOAT_VECTOR'
    new_nodes["Capture Attribute"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (-1460, -320)
    new_nodes["Position.003"] = node

    node = tree_nodes.new(type="GeometryNodeSetPosition")
    node.location = (-1460, -80)
    new_nodes["Set Position.002"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-1660, -160)
    node.operation = "NORMALIZE"
    new_nodes["Vector Math.004"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (-1860, -200)
    new_nodes["Position.001"] = node

    node = tree_nodes.new(type="GeometryNodeGroup")
    node.label = "Cull by Angle"
    node.location = (-1740, 40)
    node.node_tree = bpy.data.node_groups.get(MEGASPHERE_CULL_ANGLE_GEO_NG_NAME)
    new_nodes["Group.008"] = node

    node = tree_nodes.new(type="GeometryNodeSubdivideMesh")
    node.label = "Subdiv0"
    node.location = (-1920, 100)
    new_nodes["Subdivide Mesh"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (-2120, 0)
    node.inputs[1].default_value = 6.0
    node.inputs[2].default_value = 9.0
    node.inputs[3].default_value = 0.0
    node.inputs[4].default_value = 3.0
    new_nodes["Map Range.001"] = node

    node = tree_nodes.new(type="GeometryNodeMeshIcoSphere")
    node.location = (-2120, 140)
    node.inputs[0].default_value = 1.0
    new_nodes["Ico Sphere"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (-2320, 140)
    node.inputs[1].default_value = 1.0
    node.inputs[2].default_value = 6.0
    node.inputs[3].default_value = 1.0
    node.inputs[4].default_value = 6.0
    new_nodes["Map Range"] = node

    node = tree_nodes.new(type="GeometryNodeGroup")
    node.label = "Scale Step for Distance"
    node.location = (-2640, -100)
    node.node_tree = bpy.data.node_groups.get(MEGASPHERE_SCALE_FOR_DIST_GEO_NG_NAME)
    new_nodes["Group.007"] = node

    node = tree_nodes.new(type="GeometryNodeGroup")
    node.label = "Cull by distance"
    node.location = (2880, -60)
    node.node_tree = bpy.data.node_groups.get(MEGASPHERE_CULL_DIST_GEO_NG_NAME)
    node.inputs[2].default_value = 0.0
    new_nodes["Group.034"] = node

    node = tree_nodes.new(type="GeometryNodeGroup")
    node.label = "Cull by distance"
    node.location = (2880, 220)
    node.node_tree = bpy.data.node_groups.get(MEGASPHERE_CULL_DIST_GEO_NG_NAME)
    node.inputs[2].default_value = 0.0
    new_nodes["Group.032"] = node

    node = tree_nodes.new(type="GeometryNodeJoinGeometry")
    node.location = (3140, 100)
    new_nodes["Join Geometry.005"] = node

    node = tree_nodes.new(type="GeometryNodeMergeByDistance")
    node.location = (3320, 220)
    node.inputs[2].default_value = 0.001
    new_nodes["Merge by Distance"] = node

    node = tree_nodes.new(type="GeometryNodeAttributeDomainSize")
    node.location = (2380, 60)
    new_nodes["Domain Size.008"] = node

    node = tree_nodes.new(type="GeometryNodeGroup")
    node.label = "Subdiv"
    node.location = (2600, 20)
    node.node_tree = bpy.data.node_groups.get(MEGASPHERE_SUBDIV_GEO_NG_NAME)
    node.inputs[4].default_value = 25.0
    node.inputs[5].default_value = 27.0
    node.inputs[6].default_value = 0.0
    node.inputs[7].default_value = 2.0
    node.inputs[8].default_value = 2.407409906387329
    node.inputs[9].default_value = 0.5555566549301147
    new_nodes["Group.033"] = node

    node = tree_nodes.new(type="GeometryNodeGroup")
    node.location = (2120, -140)
    node.node_tree = bpy.data.node_groups.get(MEGASPHERE_ITERATE_GEO_NG_NAME)
    node.inputs[6].default_value = 23.0
    node.inputs[7].default_value = 7.222233295440674
    node.inputs[8].default_value = 1.6666666269302368
    node.inputs[9].default_value = 1.5241566896438599
    node.inputs[10].default_value = 3.048326015472412
    new_nodes["Group"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-2940, -280)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (3520, 380)
    new_nodes["Group Output.001"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Vector Math.002"].outputs[0], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Vector Math"].inputs[1])
    tree_links.new(new_nodes["Vector Math"].outputs[0], new_nodes["Vector Math.001"].inputs[0])
    tree_links.new(new_nodes["Vector Math.001"].outputs[0], new_nodes["Set Position"].inputs[2])
    tree_links.new(new_nodes["Position"].outputs[0], new_nodes["Vector Math.002"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Vector Math.002"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Group.007"].inputs[1])
    tree_links.new(new_nodes["Map Range"].outputs[0], new_nodes["Ico Sphere"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Group.008"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Group.008"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Group.008"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Group.007"].inputs[0])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Group.004"].inputs[3])
    tree_links.new(new_nodes["Group.007"].outputs[0], new_nodes["Map Range"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Group.007"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Math.002"].inputs[0])
    tree_links.new(new_nodes["Vector Math.006"].outputs[0], new_nodes["Set Position.001"].inputs[3])
    tree_links.new(new_nodes["Vector Math.003"].outputs[0], new_nodes["Set Position.001"].inputs[2])
    tree_links.new(new_nodes["Position.002"].outputs[0], new_nodes["Vector Math.003"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Group.004"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Group.007"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Group.011"].inputs[2])
    tree_links.new(new_nodes["Group.004"].outputs[0], new_nodes["Group.011"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute"].outputs[1], new_nodes["Group Output.001"].inputs[1])
    tree_links.new(new_nodes["Ico Sphere"].outputs[0], new_nodes["Subdivide Mesh"].inputs[0])
    tree_links.new(new_nodes["Position.003"].outputs[0], new_nodes["Capture Attribute"].inputs[1])
    tree_links.new(new_nodes["Position.001"].outputs[0], new_nodes["Vector Math.004"].inputs[0])
    tree_links.new(new_nodes["Vector Math.004"].outputs[0], new_nodes["Set Position.002"].inputs[2])
    tree_links.new(new_nodes["Capture Attribute"].outputs[0], new_nodes["Set Position"].inputs[0])
    tree_links.new(new_nodes["Subdivide Mesh"].outputs[0], new_nodes["Group.008"].inputs[0])
    tree_links.new(new_nodes["Group.008"].outputs[0], new_nodes["Set Position.002"].inputs[0])
    tree_links.new(new_nodes["Set Position.002"].outputs[0], new_nodes["Capture Attribute"].inputs[0])
    tree_links.new(new_nodes["Group.007"].outputs[0], new_nodes["Map Range.001"].inputs[0])
    tree_links.new(new_nodes["Map Range.001"].outputs[0], new_nodes["Subdivide Mesh"].inputs[1])
    tree_links.new(new_nodes["Set Position"].outputs[0], new_nodes["Group.004"].inputs[0])
    tree_links.new(new_nodes["Position.004"].outputs[0], new_nodes["Vector Math.005"].inputs[0])
    tree_links.new(new_nodes["Vector Math.005"].outputs[0], new_nodes["Set Position.003"].inputs[2])
    tree_links.new(new_nodes["Group.033"].outputs[0], new_nodes["Group.034"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Group.033"].inputs[2])
    tree_links.new(new_nodes["Group.007"].outputs[0], new_nodes["Group.033"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Group.034"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Group.033"].inputs[10])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Group.032"].inputs[1])
    tree_links.new(new_nodes["Group.032"].outputs[0], new_nodes["Join Geometry.005"].inputs[0])
    tree_links.new(new_nodes["Group.034"].outputs[0], new_nodes["Join Geometry.005"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Group.034"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Group.032"].inputs[3])
    tree_links.new(new_nodes["Join Geometry.005"].outputs[0], new_nodes["Merge by Distance"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[7], new_nodes["Vector Math.006"].inputs[0])
    tree_links.new(new_nodes["Group.033"].outputs[1], new_nodes["Group Output.001"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[7], new_nodes["Vector Math.007"].inputs[0])
    tree_links.new(new_nodes["Vector Math.007"].outputs[0], new_nodes["Set Position.003"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Group"].inputs[2])
    tree_links.new(new_nodes["Group.007"].outputs[0], new_nodes["Group"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Group"].inputs[4])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Group"].inputs[5])
    tree_links.new(new_nodes["Group"].outputs[0], new_nodes["Domain Size.008"].inputs[0])
    tree_links.new(new_nodes["Group"].outputs[2], new_nodes["Group.033"].inputs[11])
    tree_links.new(new_nodes["Domain Size.008"].outputs[2], new_nodes["Group.033"].inputs[3])
    tree_links.new(new_nodes["Group"].outputs[0], new_nodes["Group.032"].inputs[0])
    tree_links.new(new_nodes["Group"].outputs[1], new_nodes["Group.033"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Group.001"].inputs[2])
    tree_links.new(new_nodes["Group.007"].outputs[0], new_nodes["Group.001"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Group.001"].inputs[4])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Group.001"].inputs[5])
    tree_links.new(new_nodes["Group.001"].outputs[2], new_nodes["Group"].inputs[11])
    tree_links.new(new_nodes["Group.001"].outputs[0], new_nodes["Group"].inputs[0])
    tree_links.new(new_nodes["Group.001"].outputs[1], new_nodes["Group"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Group.002"].inputs[2])
    tree_links.new(new_nodes["Group.007"].outputs[0], new_nodes["Group.002"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Group.002"].inputs[4])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Group.002"].inputs[5])
    tree_links.new(new_nodes["Group.002"].outputs[2], new_nodes["Group.001"].inputs[11])
    tree_links.new(new_nodes["Group.002"].outputs[1], new_nodes["Group.001"].inputs[1])
    tree_links.new(new_nodes["Group.002"].outputs[0], new_nodes["Group.001"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Group.003"].inputs[2])
    tree_links.new(new_nodes["Group.007"].outputs[0], new_nodes["Group.003"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Group.003"].inputs[4])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Group.003"].inputs[5])
    tree_links.new(new_nodes["Group.003"].outputs[0], new_nodes["Group.002"].inputs[0])
    tree_links.new(new_nodes["Group.003"].outputs[1], new_nodes["Group.002"].inputs[1])
    tree_links.new(new_nodes["Group.003"].outputs[2], new_nodes["Group.002"].inputs[11])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Group.005"].inputs[2])
    tree_links.new(new_nodes["Group.007"].outputs[0], new_nodes["Group.005"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Group.005"].inputs[4])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Group.005"].inputs[5])
    tree_links.new(new_nodes["Group.005"].outputs[0], new_nodes["Group.003"].inputs[0])
    tree_links.new(new_nodes["Group.005"].outputs[1], new_nodes["Group.003"].inputs[1])
    tree_links.new(new_nodes["Group.005"].outputs[2], new_nodes["Group.003"].inputs[11])
    tree_links.new(new_nodes["Set Position.003"].outputs[0], new_nodes["Group.005"].inputs[0])
    tree_links.new(new_nodes["Set Position.001"].outputs[0], new_nodes["Group.005"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Group.006"].inputs[2])
    tree_links.new(new_nodes["Group.007"].outputs[0], new_nodes["Group.006"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Group.006"].inputs[4])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Group.006"].inputs[5])
    tree_links.new(new_nodes["Group.006"].outputs[2], new_nodes["Group.005"].inputs[11])
    tree_links.new(new_nodes["Group.006"].outputs[1], new_nodes["Set Position.001"].inputs[0])
    tree_links.new(new_nodes["Group.006"].outputs[0], new_nodes["Set Position.003"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Group.009"].inputs[2])
    tree_links.new(new_nodes["Group.007"].outputs[0], new_nodes["Group.009"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Group.009"].inputs[4])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Group.009"].inputs[5])
    tree_links.new(new_nodes["Group.009"].outputs[0], new_nodes["Group.006"].inputs[0])
    tree_links.new(new_nodes["Group.009"].outputs[1], new_nodes["Group.006"].inputs[1])
    tree_links.new(new_nodes["Group.009"].outputs[2], new_nodes["Group.006"].inputs[11])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Group.010"].inputs[2])
    tree_links.new(new_nodes["Group.007"].outputs[0], new_nodes["Group.010"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Group.010"].inputs[4])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Group.010"].inputs[5])
    tree_links.new(new_nodes["Group.011"].outputs[1], new_nodes["Group.010"].inputs[1])
    tree_links.new(new_nodes["Group.011"].outputs[0], new_nodes["Group.010"].inputs[0])
    tree_links.new(new_nodes["Group.010"].outputs[2], new_nodes["Group.009"].inputs[11])
    tree_links.new(new_nodes["Group.010"].outputs[0], new_nodes["Group.009"].inputs[0])
    tree_links.new(new_nodes["Group.010"].outputs[1], new_nodes["Group.009"].inputs[1])
    tree_links.new(new_nodes["Merge by Distance"].outputs[0], new_nodes["Group Output.001"].inputs[0])

    return new_node_group

# depending on the name passed to function, create the right set of nodes in a group and pass back
def create_custom_geo_node_group(node_group_name):
    if node_group_name == MEGASPHERE_SCALE_FOR_DIST_GEO_NG_NAME:
        return create_geo_ng_scale_for_dist()
    elif node_group_name == MEGASPHERE_CULL_ANGLE_GEO_NG_NAME:
        return create_geo_ng_cull_by_angle()
    elif node_group_name == MEGASPHERE_CULL_DIST_GEO_NG_NAME:
        return create_geo_ng_cull_by_dist()
    elif node_group_name == MEGASPHERE_LOD_GEO_NG_NAME:
        return create_geo_ng_level_of_detail()
    elif node_group_name == MEGASPHERE_SUBDIV_GEO_NG_NAME:
        return create_geo_ng_subdiv()
    elif node_group_name == MEGASPHERE_ITERATE_GEO_NG_NAME:
        return create_geo_ng_iterate()
    elif node_group_name == MEGASPHERE_GEO_NG_NAME:
        return create_geo_ng_megasphere()
    # error
    print("Unknown name passed to create_custom_geo_node_group: " + str(node_group_name))
    return None

def ensure_geo_node_group(node_group_name, override_create):
    # check if custom node group already exists, and create/override if necessary
    node_group = bpy.data.node_groups.get(node_group_name)
    if node_group is None or override_create:
        # create the custom node group
        node_group = create_custom_geo_node_group(node_group_name)
        if node_group is None:
            return None
        # if override create is enabled, then ensure new group name will be "first", meaning:
        #     group name does not have suffix like '.001', '.002', etc.
        if override_create:
            node_group.name = node_group_name
    return node_group

def ensure_mega_sphere_geo_nodes(override_create):
    ensure_geo_node_group(MEGASPHERE_SCALE_FOR_DIST_GEO_NG_NAME, override_create)
    ensure_geo_node_group(MEGASPHERE_CULL_ANGLE_GEO_NG_NAME, override_create)
    ensure_geo_node_group(MEGASPHERE_CULL_DIST_GEO_NG_NAME, override_create)
    ensure_geo_node_group(MEGASPHERE_LOD_GEO_NG_NAME, override_create)
    ensure_geo_node_group(MEGASPHERE_SUBDIV_GEO_NG_NAME, override_create)
    ensure_geo_node_group(MEGASPHERE_ITERATE_GEO_NG_NAME, override_create)
    ensure_geo_node_group(MEGASPHERE_GEO_NG_NAME, override_create)

def create_individual_geo_ng(new_node_group, big_space_rig, proxy_place_bone_name_0e=None, proxy_place_bone_name_6e=None):
    # initialize variables
    new_nodes = {}
    new_node_group.inputs.new(type='NodeSocketMaterial', name="Material")
    new_node_group.outputs.new(type='NodeSocketVector', name="Original Loc")
    tree_nodes = new_node_group.nodes
    # delete old nodes before adding new nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="GeometryNodeGroup")
    node.label = "MegaSphere"
    node.location = (-40, -20)
    node.node_tree = bpy.data.node_groups.get(MEGASPHERE_GEO_NG_NAME)
    node.inputs[0].default_value = 10.0
    node.inputs[1].default_value = 1.0
    node.inputs[2].default_value = 0.0
    node.inputs[3].default_value = 0.0
    node.inputs[4].default_value = 9999.0
    node.inputs[5].default_value = 64000
    new_nodes["MegaSphere.Group"] = node

    node = tree_nodes.new(type="GeometryNodeSetMaterial")
    node.location = (220, 120)
    new_nodes["Set Material"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (400, 40)
    new_nodes["Group Output"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-220, 80)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="FunctionNodeInputVector")
    node.label = "Obs 6e"
    # location
    if proxy_place_bone_name_0e is None or proxy_place_bone_name_6e is None:
        node.location = (-220, -260)
    else:
        node.location = (-400, -260)
    # driver X
    drv_obs_6e_x = node.driver_add('vector', 0).driver
    v_obs_6e_x = drv_obs_6e_x.variables.new()
    v_obs_6e_x.type = 'TRANSFORMS'
    v_obs_6e_x.name = "var"
    v_obs_6e_x.targets[0].id = big_space_rig
    v_obs_6e_x.targets[0].bone_target = PROXY_OBSERVER_6E_BNAME
    v_obs_6e_x.targets[0].transform_type = 'LOC_X'
    v_obs_6e_x.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_obs_6e_x.targets[0].data_path = "location.x"
    drv_obs_6e_x.expression = v_obs_6e_x.name
    # driver Y
    drv_obs_6e_y = node.driver_add('vector', 1).driver
    v_obs_6e_y = drv_obs_6e_y.variables.new()
    v_obs_6e_y.type = 'TRANSFORMS'
    v_obs_6e_y.name = "var"
    v_obs_6e_y.targets[0].id = big_space_rig
    v_obs_6e_y.targets[0].bone_target = PROXY_OBSERVER_6E_BNAME
    v_obs_6e_y.targets[0].transform_type = 'LOC_Y'
    v_obs_6e_y.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_obs_6e_y.targets[0].data_path = "location.y"
    drv_obs_6e_y.expression = v_obs_6e_y.name
    # driver Z
    drv_obs_6e_z = node.driver_add('vector', 2).driver
    v_obs_6e_z = drv_obs_6e_z.variables.new()
    v_obs_6e_z.type = 'TRANSFORMS'
    v_obs_6e_z.name = "var"
    v_obs_6e_z.targets[0].id = big_space_rig
    v_obs_6e_z.targets[0].bone_target = PROXY_OBSERVER_6E_BNAME
    v_obs_6e_z.targets[0].transform_type = 'LOC_Z'
    v_obs_6e_z.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_obs_6e_z.targets[0].data_path = "location.z"
    drv_obs_6e_z.expression = v_obs_6e_z.name
    # finished adding drivers to node
    new_nodes["Vector"] = node

    node = tree_nodes.new(type="FunctionNodeInputVector")
    node.label = "Obs 0e"
    # location
    if proxy_place_bone_name_0e is None or proxy_place_bone_name_6e is None:
        node.location = (-220, -400)
    else:
        node.location = (-400, -540)
    # driver X
    drv_obs_0e_x = node.driver_add('vector', 0).driver
    v_obs_0e_x = drv_obs_0e_x.variables.new()
    v_obs_0e_x.type = 'TRANSFORMS'
    v_obs_0e_x.name = "var"
    v_obs_0e_x.targets[0].id = big_space_rig
    v_obs_0e_x.targets[0].bone_target = PROXY_OBSERVER_0E_BNAME
    v_obs_0e_x.targets[0].transform_type = 'LOC_X'
    v_obs_0e_x.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_obs_0e_x.targets[0].data_path = "location.x"
    drv_obs_0e_x.expression = v_obs_0e_x.name
    # driver Y
    drv_obs_0e_y = node.driver_add('vector', 1).driver
    v_obs_0e_y = drv_obs_0e_y.variables.new()
    v_obs_0e_y.type = 'TRANSFORMS'
    v_obs_0e_y.name = "var"
    v_obs_0e_y.targets[0].id = big_space_rig
    v_obs_0e_y.targets[0].bone_target = PROXY_OBSERVER_0E_BNAME
    v_obs_0e_y.targets[0].transform_type = 'LOC_Y'
    v_obs_0e_y.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_obs_0e_y.targets[0].data_path = "location.y"
    drv_obs_0e_y.expression = v_obs_0e_y.name
    # driver Z
    drv_obs_0e_z = node.driver_add('vector', 2).driver
    v_obs_0e_z = drv_obs_0e_z.variables.new()
    v_obs_0e_z.type = 'TRANSFORMS'
    v_obs_0e_z.name = "var"
    v_obs_0e_z.targets[0].id = big_space_rig
    v_obs_0e_z.targets[0].bone_target = PROXY_OBSERVER_0E_BNAME
    v_obs_0e_z.targets[0].transform_type = 'LOC_Z'
    v_obs_0e_z.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_obs_0e_z.targets[0].data_path = "location.z"
    drv_obs_0e_z.expression = v_obs_0e_z.name
    # finished adding drivers to node
    new_nodes["Vector.001"] = node

    if proxy_place_bone_name_0e != None and proxy_place_bone_name_6e != None:
        # place 6e location
        node = tree_nodes.new(type="FunctionNodeInputVector")
        node.label = "Place 6e"
        node.location = (-400, -400)
        # driver X
        drv_place_6e_x = node.driver_add('vector', 0).driver
        v_place_6e_x = drv_place_6e_x.variables.new()
        v_place_6e_x.type = 'TRANSFORMS'
        v_place_6e_x.name = "var"
        v_place_6e_x.targets[0].id = big_space_rig
        v_place_6e_x.targets[0].bone_target = proxy_place_bone_name_6e
        v_place_6e_x.targets[0].transform_type = 'LOC_X'
        v_place_6e_x.targets[0].transform_space = 'TRANSFORM_SPACE'
        v_place_6e_x.targets[0].data_path = "location.x"
        drv_place_6e_x.expression = v_place_6e_x.name
        # driver Y
        drv_place_6e_y = node.driver_add('vector', 1).driver
        v_place_6e_y = drv_place_6e_y.variables.new()
        v_place_6e_y.type = 'TRANSFORMS'
        v_place_6e_y.name = "var"
        v_place_6e_y.targets[0].id = big_space_rig
        v_place_6e_y.targets[0].bone_target = proxy_place_bone_name_6e
        v_place_6e_y.targets[0].transform_type = 'LOC_Y'
        v_place_6e_y.targets[0].transform_space = 'TRANSFORM_SPACE'
        v_place_6e_y.targets[0].data_path = "location.y"
        drv_place_6e_y.expression = v_place_6e_y.name
        # driver Z
        drv_place_6e_z = node.driver_add('vector', 2).driver
        v_place_6e_z = drv_place_6e_z.variables.new()
        v_place_6e_z.type = 'TRANSFORMS'
        v_place_6e_z.name = "var"
        v_place_6e_z.targets[0].id = big_space_rig
        v_place_6e_z.targets[0].bone_target = proxy_place_bone_name_6e
        v_place_6e_z.targets[0].transform_type = 'LOC_Z'
        v_place_6e_z.targets[0].transform_space = 'TRANSFORM_SPACE'
        v_place_6e_z.targets[0].data_path = "location.z"
        drv_place_6e_z.expression = v_place_6e_z.name
        # finished adding drivers to node
        new_nodes["Vector.002"] = node

        # place 0e location
        node = tree_nodes.new(type="FunctionNodeInputVector")
        node.label = "Place 0e"
        node.location = (-400, -680)
        # driver X
        drv_place_0e_x = node.driver_add('vector', 0).driver
        v_place_0e_x = drv_place_0e_x.variables.new()
        v_place_0e_x.type = 'TRANSFORMS'
        v_place_0e_x.name = "var"
        v_place_0e_x.targets[0].id = big_space_rig
        v_place_0e_x.targets[0].bone_target = proxy_place_bone_name_0e
        v_place_0e_x.targets[0].transform_type = 'LOC_X'
        v_place_0e_x.targets[0].transform_space = 'TRANSFORM_SPACE'
        v_place_0e_x.targets[0].data_path = "location.x"
        drv_place_0e_x.expression = v_place_0e_x.name
        # driver Y
        drv_place_0e_y = node.driver_add('vector', 1).driver
        v_place_0e_y = drv_place_0e_y.variables.new()
        v_place_0e_y.type = 'TRANSFORMS'
        v_place_0e_y.name = "var"
        v_place_0e_y.targets[0].id = big_space_rig
        v_place_0e_y.targets[0].bone_target = proxy_place_bone_name_0e
        v_place_0e_y.targets[0].transform_type = 'LOC_Y'
        v_place_0e_y.targets[0].transform_space = 'TRANSFORM_SPACE'
        v_place_0e_y.targets[0].data_path = "location.y"
        drv_place_0e_y.expression = v_place_0e_y.name
        # driver Z
        drv_place_0e_z = node.driver_add('vector', 2).driver
        v_place_0e_z = drv_place_0e_z.variables.new()
        v_place_0e_z.type = 'TRANSFORMS'
        v_place_0e_z.name = "var"
        v_place_0e_z.targets[0].id = big_space_rig
        v_place_0e_z.targets[0].bone_target = proxy_place_bone_name_0e
        v_place_0e_z.targets[0].transform_type = 'LOC_Z'
        v_place_0e_z.targets[0].transform_space = 'TRANSFORM_SPACE'
        v_place_0e_z.targets[0].data_path = "location.z"
        drv_place_0e_z.expression = v_place_0e_z.name
        # finished adding drivers to node
        new_nodes["Vector.003"] = node

        node = tree_nodes.new(type="ShaderNodeVectorMath")
        node.location = (-220, -420)
        node.operation = "SUBTRACT"
        new_nodes["Vector Math"] = node

        node = tree_nodes.new(type="ShaderNodeVectorMath")
        node.location = (-220, -260)
        node.operation = "SUBTRACT"
        new_nodes["Vector Math.001"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Set Material"].inputs[2])
    tree_links.new(new_nodes["MegaSphere.Group"].outputs[1], new_nodes["Group Output"].inputs[1])
    tree_links.new(new_nodes["MegaSphere.Group"].outputs[0], new_nodes["Set Material"].inputs[0])
    tree_links.new(new_nodes["Set Material"].outputs[0], new_nodes["Group Output"].inputs[0])
    if proxy_place_bone_name_0e is None or proxy_place_bone_name_6e is None:
        tree_links.new(new_nodes["Vector"].outputs[0], new_nodes["MegaSphere.Group"].inputs[6])
        tree_links.new(new_nodes["Vector.001"].outputs[0], new_nodes["MegaSphere.Group"].inputs[7])
    else:
        tree_links.new(new_nodes["Vector"].outputs[0], new_nodes["Vector Math.001"].inputs[0])
        tree_links.new(new_nodes["Vector.001"].outputs[0], new_nodes["Vector Math"].inputs[0])
        tree_links.new(new_nodes["Vector.002"].outputs[0], new_nodes["Vector Math.001"].inputs[1])
        tree_links.new(new_nodes["Vector.003"].outputs[0], new_nodes["Vector Math"].inputs[1])
        tree_links.new(new_nodes["Vector Math"].outputs[0], new_nodes["MegaSphere.Group"].inputs[7])
        tree_links.new(new_nodes["Vector Math.001"].outputs[0], new_nodes["MegaSphere.Group"].inputs[6])

    return new_node_group

def add_mega_sphere_geo_nodes_to_object(ob, big_space_rig, proxy_place_bone_name_0e, proxy_place_bone_name_6e):
    geo_nodes_mod = ob.modifiers.new(name="MegaSphere.GeometryNodes", type='NODES')
    create_individual_geo_ng(geo_nodes_mod.node_group, big_space_rig, proxy_place_bone_name_0e, proxy_place_bone_name_6e)

def create_mega_sphere(context, big_space_rig, override_create, place_bone_name):
    # ensure that node groups exist that will be used later by the Mega Sphere geometry nodes modifier
    ensure_mega_sphere_geo_nodes(override_create)
    # create mesh object, that will receive Mega Sphere geometry nodes which overwrite geometry
    bpy.ops.mesh.primitive_plane_add(size=1)
    ob = context.active_object
    ob.name = MEGASPHERE_OBJ_NAME
    ob.parent = big_space_rig
    if place_bone_name != "":
        proxy_place_bone_name_0e, proxy_place_bone_name_6e = get_0e_6e_from_place_bone_name(big_space_rig,
                                                                                            place_bone_name)
    else:
        proxy_place_bone_name_0e, proxy_place_bone_name_6e = None, None

    add_mega_sphere_geo_nodes_to_object(ob, big_space_rig, proxy_place_bone_name_0e, proxy_place_bone_name_6e)

class BSR_MegaSphereCreate(bpy.types.Operator):
    bl_description = "Create a sphere of mega-meter proportions. Active object must be Big Space Rig for this to work"
    bl_idname = "big_space_rig.create_mega_sphere"
    bl_label = "Create Mega Sphere"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scn = context.scene
        active_ob = context.active_object
        # error checks
        if not is_big_space_rig(active_ob):
            self.report({'ERROR'}, "Unable to Create Mega Sphere because Active Object is not a Big Space Rig.")
            return {'CANCELLED'}
        place_bone_name = ""
        if scn.BSR_MegaSphereUsePlace:
            place_bone_name = scn.BSR_MegaSpherePlaceBoneName
        create_mega_sphere(context, active_ob, scn.BSR_MegaSphereOverrideCreateNG, place_bone_name)
        return {'FINISHED'}
