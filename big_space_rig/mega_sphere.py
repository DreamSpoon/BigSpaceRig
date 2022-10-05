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

from .rig import (is_big_space_rig, get_widget_objs_from_rig, add_widgets_to_big_space_rig,
    get_6e_0e_from_place_bone_name)
from .rig import (PROXY_OBSERVER_0E_BNAME, PROXY_OBSERVER_6E_BNAME, ICOSPHERE7_WIDGET_NAME, WIDGET_ICOSPHERE7_OBJNAME)
from .node_other import (ensure_node_groups, node_group_name_for_name_and_type)
from .mat_node_util import (SNAP_VERT_LOD_GEO_NG_NAME, VEC_DIV_3E_MOD_3E_DUO_NG_NAME, TILE_XYZ_3E_DUO_NG_NAME,
    SUBDIV_SURF_WITH_INDEX_GEO_NG_NAME)
from .mat_node_util import (create_prereq_util_node_group)

if bpy.app.version < (2,80,0):
    from .imp_v27 import (create_mesh_obj_from_pydata)
else:
    from .imp_v28 import (create_mesh_obj_from_pydata)

MEGASPHERE_SUBDIV_BY_DIST_GEO_NG_NAME = "MegaSphere.NumSubdivByDist.BSR.GeoNG"
MEGASPHERE_SUBDIV_BY_PROXIMITY_GEO_NG_NAME = "MegaSphere.NumSubdivByProximity.BSR.GeoNG"
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
    new_node_group = bpy.data.node_groups.new(name=MEGASPHERE_SUBDIV_BY_DIST_GEO_NG_NAME, type='GeometryNodeTree')
    new_node_group.inputs.new(type='NodeSocketFloat', name="Subdiv Scale")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Mega Sphere Radius")
    new_node_group.inputs.new(type='NodeSocketVector', name="Observer 6e Loc")
    new_node_group.inputs.new(type='NodeSocketVector', name="Observer 0e Loc")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Max Subdiv")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Subdiv Count")
    tree_nodes = new_node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-740, -80)
    node.operation = "MULTIPLY"
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-920, -80)
    node.operation = "NORMALIZE"
    new_nodes["Vector Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-740, -340)
    node.operation = "ADD"
    new_nodes["Vector Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-920, -340)
    node.operation = "DIVIDE"
    node.inputs[1].default_value = (1e6, 1e6, 1e6)
    new_nodes["Vector Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.label = "Observer 6e less sphere surface"
    node.location = (-520, -80)
    node.operation = "SUBTRACT"
    new_nodes["Vector Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-520, -240)
    node.operation = "COMPARE"
    node.inputs[1].default_value = 0.0
    node.inputs[2].default_value = 0.0
    new_nodes["Math"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-740, -220)
    node.operation = "LENGTH"
    new_nodes["Vector Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-340, -80)
    node.operation = "LENGTH"
    new_nodes["Vector Math.006"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Observer to sphere surface dist"
    node.location = (20, -80)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = 1000.0
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (200, -80)
    node.operation = "POWER"
    node.inputs[1].default_value = 0.125
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Check zero dist"
    node.location = (380, -80)
    node.operation = "LESS_THAN"
    node.inputs[1].default_value = 1e-4
    new_nodes["Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (380, -240)
    node.operation = "DIVIDE"
    new_nodes["Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-160, -80)
    node.operation = "MULTIPLY_ADD"
    new_nodes["Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Fix zero dist"
    node.location = (560, -100)
    node.operation = "MULTIPLY_ADD"
    new_nodes["Math.006"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (740, -100)
    node.inputs[1].default_value = 0.0
    node.inputs[3].default_value = 0.0
    new_nodes["Map Range"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-1140, -200)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (920, -100)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Vector Math"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Math.004"].inputs[0])
    tree_links.new(new_nodes["Map Range"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Vector Math.001"].outputs[0], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Vector Math"].outputs[0], new_nodes["Vector Math.004"].inputs[1])
    tree_links.new(new_nodes["Vector Math.004"].outputs[0], new_nodes["Vector Math.006"].inputs[0])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Math.002"].inputs[0])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Math.004"].inputs[1])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Math.003"].inputs[0])
    tree_links.new(new_nodes["Math.004"].outputs[0], new_nodes["Math.006"].inputs[2])
    tree_links.new(new_nodes["Math.003"].outputs[0], new_nodes["Math.006"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Vector Math.001"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Math.006"].inputs[1])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Math.005"].inputs[1])
    tree_links.new(new_nodes["Vector Math.006"].outputs[1], new_nodes["Math.005"].inputs[2])
    tree_links.new(new_nodes["Math.005"].outputs[0], new_nodes["Math.001"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Math.005"].inputs[0])
    tree_links.new(new_nodes["Vector Math.001"].outputs[0], new_nodes["Vector Math.005"].inputs[0])
    tree_links.new(new_nodes["Vector Math.005"].outputs[1], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Vector Math.003"].inputs[0])
    tree_links.new(new_nodes["Vector Math.003"].outputs[0], new_nodes["Vector Math.002"].inputs[1])
    tree_links.new(new_nodes["Vector Math.002"].outputs[0], new_nodes["Vector Math.004"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Vector Math.002"].inputs[0])
    tree_links.new(new_nodes["Math.006"].outputs[0], new_nodes["Map Range"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Map Range"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Map Range"].inputs[4])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group

def create_geo_ng_scale_for_proximity():
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=MEGASPHERE_SUBDIV_BY_PROXIMITY_GEO_NG_NAME, type='GeometryNodeTree')
    new_node_group.inputs.new(type='NodeSocketGeometry', name="Geometry")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Subdiv Scale")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Max Subdiv")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Subdiv Count")
    tree_nodes = new_node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="GeometryNodeProximity")
    node.location = (-540, -180)
    node.target_element = 'POINTS'
    new_nodes["Geometry Proximity"] = node

    node = tree_nodes.new(type="GeometryNodeAttributeStatistic")
    node.location = (-360, 100)
    node.data_type = 'FLOAT'
    node.domain = 'POINT'
    new_nodes["Attribute Statistic"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-180, 100)
    node.operation = "POWER"
    node.inputs[1].default_value = 0.125
    new_nodes["Math"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Check zero dist"
    node.location = (180, 100)
    node.operation = "LESS_THAN"
    node.inputs[1].default_value = 1e-4
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (180, -60)
    node.operation = "DIVIDE"
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (0, 100)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = 0.4187
    new_nodes["Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Fix zero dist"
    node.location = (360, 80)
    node.operation = "MULTIPLY_ADD"
    new_nodes["Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (540, 80)
    node.inputs[1].default_value = 0.0
    node.inputs[3].default_value = 0.0
    new_nodes["Map Range"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-720, -80)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (720, 80)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Math.002"].inputs[0])
    tree_links.new(new_nodes["Map Range"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Math.004"].inputs[2])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Math.004"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Math.004"].inputs[1])
    tree_links.new(new_nodes["Geometry Proximity"].outputs[1], new_nodes["Attribute Statistic"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Geometry Proximity"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Attribute Statistic"].inputs[0])
    tree_links.new(new_nodes["Attribute Statistic"].outputs[3], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Math.003"].inputs[0])
    tree_links.new(new_nodes["Math.003"].outputs[0], new_nodes["Math.001"].inputs[0])
    tree_links.new(new_nodes["Math.003"].outputs[0], new_nodes["Math.002"].inputs[1])
    tree_links.new(new_nodes["Math.004"].outputs[0], new_nodes["Map Range"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Map Range"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Map Range"].inputs[4])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

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

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group

def create_geo_ng_cull_by_dist():
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=MEGASPHERE_CULL_DIST_GEO_NG_NAME, type='GeometryNodeTree')
    new_node_group.inputs.new(type='NodeSocketGeometry', name="Geometry")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Sphere Radius")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Face Size Fix")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Cull Distance")
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
    node.operation = 'NOT'
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

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (150, -770)
    node.operation = "COMPARE"
    node.inputs[1].default_value = 0.0
    node.inputs[2].default_value = 0.0
    new_nodes["Math.005"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-1150, -505)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (725, -470)
    new_nodes["Group Output"] = node

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

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group

def create_geo_ng_level_of_detail():
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=MEGASPHERE_LOD_GEO_NG_NAME, type='GeometryNodeTree')
    new_node_group.inputs.new(type='NodeSocketGeometry', name="Geometry")
    new_node_group.inputs.new(type='NodeSocketFloat', name="LOD Distance")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Sphere Radius")
    new_node_group.inputs.new(type='NodeSocketVector', name="Offset -3e")
    new_node_group.outputs.new(type='NodeSocketGeometry', name="LOD Geometry")
    new_node_group.outputs.new(type='NodeSocketGeometry', name="Geometry")
    tree_nodes = new_node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Greater than LOD dist"
    node.location = (-420, 80)
    node.operation = "GREATER_THAN"
    new_nodes["Math"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-600, 80)
    node.operation = "LENGTH"
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="GeometryNodeSeparateGeometry")
    node.location = (-240, 200)
    node.domain = "FACE"
    new_nodes["Separate Geometry"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (-960, 80)
    new_nodes["Position"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-960, 20)
    node.operation = "DIVIDE"
    node.inputs[1].default_value = (1000.0, 1000.0, 1000.0)
    new_nodes["Vector Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-780, 80)
    node.operation = "SUBTRACT"
    new_nodes["Vector Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-600, -40)
    node.operation = "MULTIPLY"
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-1180, 120)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (-60, 180)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Separate Geometry"].inputs[0])
    tree_links.new(new_nodes["Separate Geometry"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Vector Math"].outputs[1], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Separate Geometry"].outputs[1], new_nodes["Group Output"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Math.002"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Math.002"].inputs[0])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Math"].inputs[1])
    tree_links.new(new_nodes["Position"].outputs[0], new_nodes["Vector Math.001"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Vector Math.002"].inputs[0])
    tree_links.new(new_nodes["Vector Math.001"].outputs[0], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Vector Math.002"].outputs[0], new_nodes["Vector Math.001"].inputs[1])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Separate Geometry"].inputs[1])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group

def create_geo_ng_subdiv():
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=MEGASPHERE_SUBDIV_GEO_NG_NAME, type='GeometryNodeTree')
    new_node_group.inputs.new(type='NodeSocketGeometry', name="Geometry")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Subdiv")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Subdiv Index Geo")
    new_node_group.inputs.new(type='NodeSocketInt', name="Max Faces")
    new_node_group.inputs.new(type='NodeSocketInt', name="Add Faces")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Dist Subdiv Min")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Dist Subdiv Max")
    new_node_group.inputs.new(type='NodeSocketBool', name="Max FaceCount")
    new_node_group.outputs.new(type='NodeSocketGeometry', name="Geometry")
    new_node_group.outputs.new(type='NodeSocketBool', name="Max FaceCount")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Subdiv Index Geo")
    tree_nodes = new_node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="GeometryNodeGroup")
    node.location = (840, -80)
    node.node_tree = bpy.data.node_groups.get(SUBDIV_SURF_WITH_INDEX_GEO_NG_NAME)
    new_nodes["Group.001"] = node

    node = tree_nodes.new(type="GeometryNodeGroup")
    node.location = (1020, -80)
    node.node_tree = bpy.data.node_groups.get(SUBDIV_SURF_WITH_INDEX_GEO_NG_NAME)
    node.inputs[2].default_value = 0.000000
    new_nodes["Group"] = node

    node = tree_nodes.new(type="GeometryNodeInputMeshFaceNeighbors")
    node.location = (480, -200)
    new_nodes["Face Neighbors"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Face count check"
    node.location = (480, -360)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="FunctionNodeBooleanMath")
    node.location = (1020, 40)
    node.operation = "NOT"
    node.inputs[1].default_value = False
    new_nodes["Boolean Math"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (120, -200)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-60, -200)
    node.operation = "LESS_THAN"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.003"] = node

    node = tree_nodes.new(type="GeometryNodeAttributeDomainSize")
    node.location = (-600, -200)
    node.component = "MESH"
    new_nodes["Domain Size"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-240, -200)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-420, -200)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = 2.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (300, -360)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[3].default_value = 0.000000
    node.inputs[4].default_value = 2.000000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range.003"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (840, -320)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = 1.000000
    node.inputs[2].default_value = 2.000000
    node.inputs[3].default_value = 0.000000
    node.inputs[4].default_value = 1.000000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (840, -620)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[1].default_value = 1.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.007"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (660, -620)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[1].default_value = 1.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.006"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (660, -360)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 1.000000
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
    node.label = "Is one face neighbor"
    node.location = (660, -200)
    node.operation = "LESS_THAN"
    node.use_clamp = False
    node.inputs[1].default_value = 4.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-780, -200)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (1200, -80)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Map Range.003"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Domain Size"].inputs[0])
    tree_links.new(new_nodes["Math.004"].outputs[0], new_nodes["Math.003"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Map Range.003"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Map Range.003"].inputs[2])
    tree_links.new(new_nodes["Map Range.003"].outputs[0], new_nodes["Math.001"].inputs[0])
    tree_links.new(new_nodes["Domain Size"].outputs[2], new_nodes["Math.005"].inputs[0])
    tree_links.new(new_nodes["Math.005"].outputs[0], new_nodes["Math.004"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Math.004"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Math.003"].inputs[1])
    tree_links.new(new_nodes["Boolean Math"].outputs[0], new_nodes["Group Output"].inputs[1])
    tree_links.new(new_nodes["Math.003"].outputs[0], new_nodes["Math.002"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[7], new_nodes["Math.002"].inputs[1])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Boolean Math"].inputs[0])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Math.001"].inputs[1])
    tree_links.new(new_nodes["Face Neighbors"].outputs[1], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Group.001"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Group.001"].inputs[0])
    tree_links.new(new_nodes["Map Range"].outputs[0], new_nodes["Group"].inputs[1])
    tree_links.new(new_nodes["Group.001"].outputs[1], new_nodes["Group"].inputs[3])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Map Range.001"].inputs[0])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Map Range"].inputs[0])
    tree_links.new(new_nodes["Map Range.001"].outputs[0], new_nodes["Group.001"].inputs[1])
    tree_links.new(new_nodes["Group.001"].outputs[0], new_nodes["Group"].inputs[0])
    tree_links.new(new_nodes["Group"].outputs[1], new_nodes["Group Output"].inputs[2])
    tree_links.new(new_nodes["Group"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Group.001"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Math.006"].inputs[0])
    tree_links.new(new_nodes["Math.006"].outputs[0], new_nodes["Group.001"].inputs[4])
    tree_links.new(new_nodes["Math.006"].outputs[0], new_nodes["Math.007"].inputs[0])
    tree_links.new(new_nodes["Math.007"].outputs[0], new_nodes["Group"].inputs[4])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False
    return new_node_group

def create_geo_ng_iterate():
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=MEGASPHERE_ITERATE_GEO_NG_NAME, type='GeometryNodeTree')
    new_node_group.inputs.new(type='NodeSocketGeometry', name="LOD Geometry")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Subdiv Index LOD Geo")
    new_node_group.inputs.new(type='NodeSocketFloat', name="LOD Inner Verts")
    new_node_group.inputs.new(type='NodeSocketBool', name="LOD Pre-subdiv")
    new_node_group.inputs.new(type='NodeSocketInt', name="LOD Index")
    new_node_group.inputs.new(type='NodeSocketGeometry', name="Geometry")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Subdiv Index Geo")
    new_node_group.inputs.new(type='NodeSocketBool', name="Max FaceCount")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Sphere Radius")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Subdiv Count")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Subdiv Min")
    new_node_group.inputs.new(type='NodeSocketVector', name="LOD Offset")
    new_node_group.inputs.new(type='NodeSocketFloat', name="LOD Outer Distance")
    new_node_group.inputs.new(type='NodeSocketFloat', name="LOD Inner Distance")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Face Size Fix")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Cull Distance")
    new_node_group.inputs.new(type='NodeSocketInt', name="Max Faces")
    new_node_group.outputs.new(type='NodeSocketGeometry', name="LOD Geometry")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Subdiv Index LOD Geo")
    new_node_group.outputs.new(type='NodeSocketFloat', name="LOD Inner Verts")
    new_node_group.outputs.new(type='NodeSocketBool', name="LOD Pre-subdiv")
    new_node_group.outputs.new(type='NodeSocketInt', name="LOD Index")
    new_node_group.outputs.new(type='NodeSocketGeometry', name="Geometry")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Subdiv Index Geo")
    new_node_group.outputs.new(type='NodeSocketBool', name="Max Face Count")
    tree_nodes = new_node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="GeometryNodeGroup")
    node.location = (-220, -20)
    node.node_tree = bpy.data.node_groups.get(MEGASPHERE_LOD_GEO_NG_NAME)
    new_nodes["Group"] = node

    node = tree_nodes.new(type="GeometryNodeGroup")
    node.location = (-960, 80)
    node.node_tree = bpy.data.node_groups.get(MEGASPHERE_SUBDIV_GEO_NG_NAME)
    new_nodes["Group.001"] = node

    node = tree_nodes.new(type="GeometryNodeGroup")
    node.location = (-960, 280)
    node.node_tree = bpy.data.node_groups.get(MEGASPHERE_CULL_DIST_GEO_NG_NAME)
    new_nodes["Group.002"] = node

    node = tree_nodes.new(type="GeometryNodeGroup")
    node.location = (-580, 80)
    node.node_tree = bpy.data.node_groups.get(MEGASPHERE_CULL_DIST_GEO_NG_NAME)
    new_nodes["Group.003"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.label = "Capture LOD Index"
    node.location = (700, -20)
    node.data_type = "INT"
    node.domain = "FACE"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = 0.000000
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    new_nodes["Capture Attribute"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (160, -540)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-580, -120)
    node.operation = "GREATER_THAN"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Is LOD separate"
    node.location = (-400, -120)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "If subdivided"
    node.location = (340, -420)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "If pre-subdiv"
    node.location = (340, -240)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.005"] = node

    node = tree_nodes.new(type="FunctionNodeBooleanMath")
    node.location = (160, -420)
    node.operation = "NOT"
    node.inputs[1].default_value = False
    new_nodes["Boolean Math"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (520, -240)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.006"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-760, -120)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[1].default_value = 2.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.010"] = node

    node = tree_nodes.new(type="GeometryNodeJoinGeometry")
    node.location = (140, 280)
    new_nodes["Join Geometry"] = node

    node = tree_nodes.new(type="GeometryNodeAttributeDomainSize")
    node.location = (-1140, -40)
    node.component = "MESH"
    new_nodes["Domain Size"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1140, -220)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[1].default_value = 2.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.012"] = node

    node = tree_nodes.new(type="GeometryNodeInputMeshEdgeNeighbors")
    node.location = (-580, -500)
    new_nodes["Edge Neighbors"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-400, -580)
    node.operation = "LESS_THAN"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.007"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-580, -720)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.008"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-580, -600)
    node.operation = "LENGTH"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (-760, -640)
    new_nodes["Position"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Is one face neighbor"
    node.location = (-400, -400)
    node.operation = "LESS_THAN"
    node.use_clamp = False
    node.inputs[1].default_value = 2.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.009"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-220, -380)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-40, -260)
    node.operation = "ADD"
    node.use_clamp = True
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.label = "Capture LOD Inner Verts"
    node.location = (520, -20)
    node.data_type = "FLOAT"
    node.domain = "POINT"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (140, 180)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.011"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.location = (-40, 220)
    node.data_type = "FLOAT"
    node.domain = "POINT"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute.004"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.location = (-40, -40)
    node.data_type = "FLOAT"
    node.domain = "POINT"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute.005"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.label = "Reset pre-subdiv flag"
    node.location = (880, -20)
    node.data_type = "BOOLEAN"
    node.domain = "FACE"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = 0.000000
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = True
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute.001"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.label = "Capture Subdiv Index"
    node.location = (340, 20)
    node.data_type = "FLOAT"
    node.domain = "POINT"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute.003"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-1400, -100)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (1080, -60)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Domain Size"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[16], new_nodes["Group.001"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[9], new_nodes["Group.001"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[8], new_nodes["Group.003"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[15], new_nodes["Group.003"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[7], new_nodes["Group.001"].inputs[7])
    tree_links.new(new_nodes["Group.001"].outputs[1], new_nodes["Group Output"].inputs[7])
    tree_links.new(new_nodes["Group.003"].outputs[0], new_nodes["Group"].inputs[0])
    tree_links.new(new_nodes["Group.002"].outputs[0], new_nodes["Join Geometry"].inputs[0])
    tree_links.new(new_nodes["Domain Size"].outputs[2], new_nodes["Group.001"].inputs[4])
    tree_links.new(new_nodes["Group Input"].outputs[8], new_nodes["Group.002"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[8], new_nodes["Group"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[15], new_nodes["Group.002"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[10], new_nodes["Math.012"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[10], new_nodes["Group.001"].inputs[5])
    tree_links.new(new_nodes["Math.012"].outputs[0], new_nodes["Group.001"].inputs[6])
    tree_links.new(new_nodes["Group Input"].outputs[14], new_nodes["Group.003"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[14], new_nodes["Group.002"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Group.002"].inputs[0])
    tree_links.new(new_nodes["Position"].outputs[0], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Edge Neighbors"].outputs[0], new_nodes["Math.009"].inputs[0])
    tree_links.new(new_nodes["Math.007"].outputs[0], new_nodes["Math"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Math.001"].inputs[0])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Capture Attribute.002"].inputs[2])
    tree_links.new(new_nodes["Capture Attribute.002"].outputs[2], new_nodes["Group Output"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[11], new_nodes["Group"].inputs[3])
    tree_links.new(new_nodes["Math.009"].outputs[0], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Math.001"].inputs[1])
    tree_links.new(new_nodes["Vector Math"].outputs[1], new_nodes["Math.007"].inputs[0])
    tree_links.new(new_nodes["Math.008"].outputs[0], new_nodes["Math.007"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[12], new_nodes["Math.008"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[8], new_nodes["Math.008"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[9], new_nodes["Math.002"].inputs[0])
    tree_links.new(new_nodes["Math.010"].outputs[0], new_nodes["Math.002"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[13], new_nodes["Math.003"].inputs[1])
    tree_links.new(new_nodes["Math.003"].outputs[0], new_nodes["Group"].inputs[1])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Math.003"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[10], new_nodes["Math.010"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute"].outputs[5], new_nodes["Group Output"].inputs[4])
    tree_links.new(new_nodes["Capture Attribute.001"].outputs[4], new_nodes["Group Output"].inputs[3])
    tree_links.new(new_nodes["Capture Attribute.001"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.002"].outputs[0], new_nodes["Capture Attribute"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute"].outputs[0], new_nodes["Capture Attribute.001"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[9], new_nodes["Map Range"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[10], new_nodes["Map Range"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[10], new_nodes["Map Range"].inputs[3])
    tree_links.new(new_nodes["Math.012"].outputs[0], new_nodes["Map Range"].inputs[2])
    tree_links.new(new_nodes["Math.012"].outputs[0], new_nodes["Map Range"].inputs[4])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Math.005"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Math.005"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Boolean Math"].inputs[0])
    tree_links.new(new_nodes["Boolean Math"].outputs[0], new_nodes["Math.004"].inputs[0])
    tree_links.new(new_nodes["Map Range"].outputs[0], new_nodes["Math.004"].inputs[1])
    tree_links.new(new_nodes["Math.005"].outputs[0], new_nodes["Math.006"].inputs[0])
    tree_links.new(new_nodes["Math.004"].outputs[0], new_nodes["Math.006"].inputs[1])
    tree_links.new(new_nodes["Math.006"].outputs[0], new_nodes["Capture Attribute"].inputs[5])
    tree_links.new(new_nodes["Join Geometry"].outputs[0], new_nodes["Capture Attribute.003"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Math.011"].inputs[1])
    tree_links.new(new_nodes["Group"].outputs[0], new_nodes["Capture Attribute.004"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.004"].outputs[0], new_nodes["Join Geometry"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.003"].outputs[0], new_nodes["Capture Attribute.002"].inputs[0])
    tree_links.new(new_nodes["Group.001"].outputs[0], new_nodes["Group.003"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Group.001"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.005"].outputs[0], new_nodes["Group Output"].inputs[5])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Group.001"].inputs[2])
    tree_links.new(new_nodes["Group"].outputs[1], new_nodes["Capture Attribute.005"].inputs[0])
    tree_links.new(new_nodes["Group.001"].outputs[2], new_nodes["Capture Attribute.005"].inputs[2])
    tree_links.new(new_nodes["Group.001"].outputs[2], new_nodes["Capture Attribute.004"].inputs[2])
    tree_links.new(new_nodes["Math.011"].outputs[0], new_nodes["Capture Attribute.003"].inputs[2])
    tree_links.new(new_nodes["Capture Attribute.003"].outputs[2], new_nodes["Group Output"].inputs[1])
    tree_links.new(new_nodes["Capture Attribute.005"].outputs[2], new_nodes["Group Output"].inputs[6])
    tree_links.new(new_nodes["Capture Attribute.004"].outputs[2], new_nodes["Math.011"].inputs[0])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False
    return new_node_group

def create_geo_ng_megasphere():
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=MEGASPHERE_GEO_NG_NAME, type='GeometryNodeTree')
    new_node_group.inputs.new(type='NodeSocketGeometry', name="Icosphere7")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Mega Sphere Radius")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Subdivision Scale")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Max Subdiv")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Vis Angle Adjust")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Cull Distance")
    new_node_group.inputs.new(type='NodeSocketInt', name="Max Face Count")
    new_node_group.inputs.new(type='NodeSocketVector', name="Observer 6e Loc")
    new_node_group.inputs.new(type='NodeSocketVector', name="Observer 0e Loc")
    new_node_group.outputs.new(type='NodeSocketGeometry', name="Geometry")
    new_node_group.outputs.new(type='NodeSocketVector', name="MegaSphere Normal")
    new_node_group.outputs.new(type='NodeSocketFloat', name="LOD Inner Verts")
    new_node_group.outputs.new(type='NodeSocketFloat', name="LOD Outer Verts")
    new_node_group.outputs.new(type='NodeSocketInt', name="LOD Index")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Subdiv Index")
    new_node_group.outputs.new(type='NodeSocketBool', name="Max Face Count")
    tree_nodes = new_node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="GeometryNodeGroup")
    node.location = (-200, -140)
    node.node_tree = bpy.data.node_groups.get(MEGASPHERE_ITERATE_GEO_NG_NAME)
    node.inputs[7].default_value = False
    node.inputs[10].default_value = 9.000000
    node.inputs[12].default_value = 22.000000
    node.inputs[13].default_value = 6.666667
    node.inputs[14].default_value = 3.333333
    new_nodes["Group"] = node

    node = tree_nodes.new(type="GeometryNodeGroup")
    node.location = (60, -140)
    node.node_tree = bpy.data.node_groups.get(MEGASPHERE_ITERATE_GEO_NG_NAME)
    node.inputs[10].default_value = 11.000000
    node.inputs[12].default_value = 4.750000
    node.inputs[13].default_value = 2.222222
    node.inputs[14].default_value = 1.111111
    new_nodes["Group.001"] = node

    node = tree_nodes.new(type="GeometryNodeGroup")
    node.location = (1100, -140)
    node.node_tree = bpy.data.node_groups.get(MEGASPHERE_ITERATE_GEO_NG_NAME)
    node.inputs[10].default_value = 13.000000
    node.inputs[11].default_value = (0.0, 0.0, 0.0)
    node.inputs[12].default_value = 1800.000000
    node.inputs[13].default_value = 740.739990
    node.inputs[14].default_value = 370.369995
    new_nodes["Group.002"] = node

    node = tree_nodes.new(type="GeometryNodeGroup")
    node.location = (1320, -140)
    node.node_tree = bpy.data.node_groups.get(MEGASPHERE_ITERATE_GEO_NG_NAME)
    node.inputs[10].default_value = 15.000000
    node.inputs[11].default_value = (0.0, 0.0, 0.0)
    node.inputs[12].default_value = 600.000000
    node.inputs[13].default_value = 246.914001
    node.inputs[14].default_value = 123.457001
    new_nodes["Group.003"] = node

    node = tree_nodes.new(type="GeometryNodeGroup")
    node.location = (1560, -140)
    node.node_tree = bpy.data.node_groups.get(MEGASPHERE_ITERATE_GEO_NG_NAME)
    node.inputs[10].default_value = 17.000000
    node.inputs[11].default_value = (0.0, 0.0, 0.0)
    node.inputs[12].default_value = 200.000000
    node.inputs[13].default_value = 82.304604
    node.inputs[14].default_value = 41.152302
    new_nodes["Group.004"] = node

    node = tree_nodes.new(type="GeometryNodeGroup")
    node.location = (1800, -140)
    node.node_tree = bpy.data.node_groups.get(MEGASPHERE_ITERATE_GEO_NG_NAME)
    node.inputs[10].default_value = 19.000000
    node.inputs[11].default_value = (0.0, 0.0, 0.0)
    node.inputs[12].default_value = 65.000000
    node.inputs[13].default_value = 27.434900
    node.inputs[14].default_value = 13.717400
    new_nodes["Group.005"] = node

    node = tree_nodes.new(type="GeometryNodeGroup")
    node.location = (2040, -140)
    node.node_tree = bpy.data.node_groups.get(MEGASPHERE_ITERATE_GEO_NG_NAME)
    node.inputs[10].default_value = 21.000000
    node.inputs[11].default_value = (0.0, 0.0, 0.0)
    node.inputs[12].default_value = 21.666700
    node.inputs[13].default_value = 9.144970
    node.inputs[14].default_value = 4.572470
    new_nodes["Group.006"] = node

    node = tree_nodes.new(type="GeometryNodeGroup")
    node.location = (2280, -140)
    node.node_tree = bpy.data.node_groups.get(MEGASPHERE_ITERATE_GEO_NG_NAME)
    node.inputs[10].default_value = 23.000000
    node.inputs[11].default_value = (0.0, 0.0, 0.0)
    node.inputs[12].default_value = 7.222233
    node.inputs[13].default_value = 3.048326
    node.inputs[14].default_value = 1.524157
    new_nodes["Group.007"] = node

    node = tree_nodes.new(type="GeometryNodeGroup")
    node.location = (860, -540)
    node.node_tree = bpy.data.node_groups.get(MEGASPHERE_SUBDIV_BY_PROXIMITY_GEO_NG_NAME)
    new_nodes["Group.008"] = node

    node = tree_nodes.new(type="GeometryNodeGroup")
    node.location = (-4140, -340)
    node.node_tree = bpy.data.node_groups.get(MEGASPHERE_SUBDIV_BY_DIST_GEO_NG_NAME)
    new_nodes["Group.009"] = node

    node = tree_nodes.new(type="GeometryNodeGroup")
    node.location = (-2640, 100)
    node.node_tree = bpy.data.node_groups.get(MEGASPHERE_CULL_ANGLE_GEO_NG_NAME)
    new_nodes["Group.010"] = node

    node = tree_nodes.new(type="GeometryNodeGroup")
    node.location = (-1020, -240)
    node.node_tree = bpy.data.node_groups.get(MEGASPHERE_CULL_DIST_GEO_NG_NAME)
    node.inputs[2].default_value = 15.000000
    new_nodes["Group.011"] = node

    node = tree_nodes.new(type="GeometryNodeGroup")
    node.location = (-840, -240)
    node.node_tree = bpy.data.node_groups.get(MEGASPHERE_LOD_GEO_NG_NAME)
    node.inputs[1].default_value = 30.000000
    node.inputs[3].default_value = (0.0, 0.0, 0.0)
    new_nodes["Group.012"] = node

    node = tree_nodes.new(type="GeometryNodeGroup")
    node.location = (2980, 60)
    node.node_tree = bpy.data.node_groups.get(MEGASPHERE_CULL_DIST_GEO_NG_NAME)
    node.inputs[2].default_value = 0.000000
    new_nodes["Group.013"] = node

    node = tree_nodes.new(type="GeometryNodeGroup")
    node.location = (2980, 240)
    node.node_tree = bpy.data.node_groups.get(MEGASPHERE_CULL_DIST_GEO_NG_NAME)
    node.inputs[2].default_value = 0.000000
    new_nodes["Group.014"] = node

    node = tree_nodes.new(type="GeometryNodeGroup")
    node.location = (2740, 40)
    node.node_tree = bpy.data.node_groups.get(MEGASPHERE_SUBDIV_GEO_NG_NAME)
    node.inputs[5].default_value = 25.000000
    node.inputs[6].default_value = 27.000000
    new_nodes["Group.015"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (320, -360)
    new_nodes["Position"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (320, 80)
    new_nodes["Position.001"] = node

    node = tree_nodes.new(type="GeometryNodeSetPosition")
    node.location = (680, 60)
    new_nodes["Set Position"] = node

    node = tree_nodes.new(type="GeometryNodeSetPosition")
    node.location = (680, -380)
    new_nodes["Set Position.001"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (500, -80)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = (-1.0, -1.0, -1.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (500, 140)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = (1000.0, 1000.0, 1000.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (500, -520)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = (-1.0, -1.0, -1.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (500, -300)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = (1000.0, 1000.0, 1000.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.003"] = node

    node = tree_nodes.new(type="GeometryNodeAttributeDomainSize")
    node.location = (-4120, -20)
    node.component = "MESH"
    new_nodes["Domain Size"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-3940, -200)
    node.operation = "LESS_THAN"
    node.use_clamp = False
    node.inputs[1].default_value = 7.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-3940, -20)
    node.operation = "LESS_THAN"
    node.use_clamp = False
    node.inputs[1].default_value = 1.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (-3360, 20)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = 1.000000
    node.inputs[2].default_value = 7.000000
    node.inputs[3].default_value = 1.000000
    node.inputs[4].default_value = 7.000000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "If no Ico7 or Subdiv below 7"
    node.location = (-3580, -80)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="FunctionNodeBooleanMath")
    node.location = (-3760, -60)
    node.operation = "OR"
    new_nodes["Boolean Math"] = node

    node = tree_nodes.new(type="FunctionNodeBooleanMath")
    node.label = "If Ico7 and Subdiv 7 or more"
    node.location = (-3580, 120)
    node.operation = "NOT"
    node.inputs[1].default_value = False
    new_nodes["Boolean Math.001"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (-2100, -480)
    new_nodes["Position.002"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (-2280, -320)
    new_nodes["Position.003"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.label = "Capture sphere normal"
    node.location = (-2100, -140)
    node.data_type = "FLOAT_VECTOR"
    node.domain = "POINT"
    node.inputs[2].default_value = 0.000000
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (-2640, -220)
    new_nodes["Position.004"] = node

    node = tree_nodes.new(type="GeometryNodeSetPosition")
    node.location = (-2280, -80)
    node.inputs[3].default_value = (0.0, 0.0, 0.0)
    new_nodes["Set Position.002"] = node

    node = tree_nodes.new(type="GeometryNodeSubdivisionSurface")
    node.location = (-2460, 40)
    node.boundary_smooth = "ALL"
    node.uv_smooth = "PRESERVE_BOUNDARIES"
    node.inputs[2].default_value = 0.000000
    new_nodes["Subdivision Surface"] = node

    node = tree_nodes.new(type="GeometryNodeJoinGeometry")
    node.location = (-2820, 60)
    new_nodes["Join Geometry"] = node

    node = tree_nodes.new(type="GeometryNodeDeleteGeometry")
    node.location = (-3000, 180)
    node.domain = "POINT"
    node.mode = "ALL"
    new_nodes["Delete Geometry"] = node

    node = tree_nodes.new(type="GeometryNodeDeleteGeometry")
    node.location = (-3000, 0)
    node.domain = "POINT"
    node.mode = "ALL"
    new_nodes["Delete Geometry.001"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (-2820, -60)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = 7.000000
    node.inputs[2].default_value = 9.000000
    node.inputs[3].default_value = 0.000000
    node.inputs[4].default_value = 2.000000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range.001"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-2460, -160)
    node.operation = "NORMALIZE"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.004"] = node

    node = tree_nodes.new(type="GeometryNodeMeshIcoSphere")
    node.location = (-3180, 0)
    node.inputs[0].default_value = 1.000000
    new_nodes["Ico Sphere"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (-1740, -260)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = 1.000000
    node.inputs[2].default_value = 9.000000
    node.inputs[3].default_value = 0.000000
    node.inputs[4].default_value = 9.000000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range.002"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-1920, -460)
    node.operation = "MULTIPLY"
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-1740, -520)
    node.operation = "SUBTRACT"
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.006"] = node

    node = tree_nodes.new(type="GeometryNodeSetPosition")
    node.location = (-1380, -300)
    node.inputs[3].default_value = (0.0, 0.0, 0.0)
    new_nodes["Set Position.003"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.label = "Capture LOD Index"
    node.location = (-1560, -120)
    node.data_type = "INT"
    node.domain = "FACE"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = 0.000000
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    new_nodes["Capture Attribute.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1200, -420)
    node.operation = "DIVIDE"
    node.use_clamp = False
    node.inputs[1].default_value = 1000.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-1560, -460)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = (1000.0, 1000.0, 1000.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.007"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.location = (-640, -320)
    node.data_type = "FLOAT"
    node.domain = "POINT"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute.002"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (-1380, -840)
    new_nodes["Position.005"] = node

    node = tree_nodes.new(type="GeometryNodeInputMeshEdgeNeighbors")
    node.location = (-1200, -660)
    new_nodes["Edge Neighbors"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-840, -560)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1020, -780)
    node.operation = "LESS_THAN"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1200, -920)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = 60.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.006"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Is one face neighbor"
    node.location = (-1020, -600)
    node.operation = "LESS_THAN"
    node.use_clamp = False
    node.inputs[1].default_value = 2.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.007"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-1200, -800)
    node.operation = "LENGTH"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.008"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.label = "Capture pre-subdiv"
    node.location = (-1920, -100)
    node.data_type = "BOOLEAN"
    node.domain = "FACE"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = 0.000000
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = True
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute.005"] = node

    node = tree_nodes.new(type="GeometryNodeAttributeDomainSize")
    node.location = (2560, 40)
    node.component = "MESH"
    new_nodes["Domain Size.001"] = node

    node = tree_nodes.new(type="GeometryNodeJoinGeometry")
    node.location = (3160, 140)
    new_nodes["Join Geometry.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "If pre-subdiv"
    node.location = (3160, -400)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.009"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (3340, -400)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.010"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.label = "Capture LOD Index"
    node.location = (3700, 140)
    node.data_type = "INT"
    node.domain = "FACE"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = 0.000000
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    new_nodes["Capture Attribute.006"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.label = "Capture LOD Inner Verts"
    node.location = (3520, 140)
    node.data_type = "FLOAT"
    node.domain = "POINT"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute.007"] = node

    node = tree_nodes.new(type="GeometryNodeInputMeshEdgeNeighbors")
    node.location = (2980, -200)
    new_nodes["Edge Neighbors.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (3160, -200)
    node.operation = "LESS_THAN"
    node.use_clamp = False
    node.inputs[1].default_value = 2.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.011"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (3340, -200)
    node.operation = "SUBTRACT"
    node.use_clamp = True
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.012"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "If subdivided"
    node.location = (3160, -560)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.013"] = node

    node = tree_nodes.new(type="FunctionNodeBooleanMath")
    node.location = (2980, -560)
    node.operation = "NOT"
    node.inputs[1].default_value = False
    new_nodes["Boolean Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (2980, -680)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = 25.000000
    node.inputs[2].default_value = 27.000000
    node.inputs[3].default_value = 25.000000
    node.inputs[4].default_value = 27.000000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range.003"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.label = "Capture Subdiv Index"
    node.location = (3340, 140)
    node.data_type = "FLOAT"
    node.domain = "POINT"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute.008"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.location = (-460, -460)
    node.data_type = "FLOAT"
    node.domain = "POINT"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = 0.000000
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute.003"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.location = (-460, -280)
    node.data_type = "FLOAT"
    node.domain = "POINT"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = 0.000000
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute.004"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (3160, 60)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.008"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-4400, -380)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (3900, 280)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Vector Math.005"].outputs[0], new_nodes["Vector Math.006"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[7], new_nodes["Vector Math.006"].inputs[1])
    tree_links.new(new_nodes["Vector Math.006"].outputs[0], new_nodes["Vector Math.007"].inputs[0])
    tree_links.new(new_nodes["Vector Math.007"].outputs[0], new_nodes["Set Position.003"].inputs[2])
    tree_links.new(new_nodes["Position.002"].outputs[0], new_nodes["Vector Math.005"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Vector Math.005"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Group.009"].inputs[1])
    tree_links.new(new_nodes["Map Range"].outputs[0], new_nodes["Ico Sphere"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[7], new_nodes["Group.010"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Group.010"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Group.010"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Group.009"].inputs[0])
    tree_links.new(new_nodes["Math.003"].outputs[0], new_nodes["Group.011"].inputs[3])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Map Range"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[7], new_nodes["Group.009"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Math.003"].inputs[0])
    tree_links.new(new_nodes["Vector Math.002"].outputs[0], new_nodes["Set Position.001"].inputs[3])
    tree_links.new(new_nodes["Vector Math.003"].outputs[0], new_nodes["Set Position.001"].inputs[2])
    tree_links.new(new_nodes["Position"].outputs[0], new_nodes["Vector Math.003"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Group.011"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Group.009"].inputs[4])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Group.012"].inputs[2])
    tree_links.new(new_nodes["Group.011"].outputs[0], new_nodes["Group.012"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute"].outputs[1], new_nodes["Group Output"].inputs[1])
    tree_links.new(new_nodes["Position.003"].outputs[0], new_nodes["Capture Attribute"].inputs[1])
    tree_links.new(new_nodes["Position.004"].outputs[0], new_nodes["Vector Math.004"].inputs[0])
    tree_links.new(new_nodes["Vector Math.004"].outputs[0], new_nodes["Set Position.002"].inputs[2])
    tree_links.new(new_nodes["Set Position.002"].outputs[0], new_nodes["Capture Attribute"].inputs[0])
    tree_links.new(new_nodes["Group.009"].outputs[0], new_nodes["Map Range.001"].inputs[0])
    tree_links.new(new_nodes["Map Range.001"].outputs[0], new_nodes["Subdivision Surface"].inputs[1])
    tree_links.new(new_nodes["Set Position.003"].outputs[0], new_nodes["Group.011"].inputs[0])
    tree_links.new(new_nodes["Position.001"].outputs[0], new_nodes["Vector Math.001"].inputs[0])
    tree_links.new(new_nodes["Vector Math.001"].outputs[0], new_nodes["Set Position"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Group.015"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Group.013"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Group.014"].inputs[1])
    tree_links.new(new_nodes["Group.014"].outputs[0], new_nodes["Join Geometry.001"].inputs[0])
    tree_links.new(new_nodes["Group.013"].outputs[0], new_nodes["Join Geometry.001"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Group.013"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Group.014"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[8], new_nodes["Vector Math.002"].inputs[0])
    tree_links.new(new_nodes["Group.015"].outputs[1], new_nodes["Group Output"].inputs[6])
    tree_links.new(new_nodes["Group Input"].outputs[8], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Vector Math"].outputs[0], new_nodes["Set Position"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Group.007"].inputs[16])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Group.007"].inputs[8])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Group.007"].inputs[15])
    tree_links.new(new_nodes["Group.007"].outputs[0], new_nodes["Domain Size.001"].inputs[0])
    tree_links.new(new_nodes["Group.007"].outputs[7], new_nodes["Group.015"].inputs[7])
    tree_links.new(new_nodes["Domain Size.001"].outputs[2], new_nodes["Group.015"].inputs[4])
    tree_links.new(new_nodes["Group.007"].outputs[0], new_nodes["Group.014"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Group.006"].inputs[16])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Group.006"].inputs[8])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Group.006"].inputs[15])
    tree_links.new(new_nodes["Group.006"].outputs[7], new_nodes["Group.007"].inputs[7])
    tree_links.new(new_nodes["Group.006"].outputs[0], new_nodes["Group.007"].inputs[0])
    tree_links.new(new_nodes["Group.006"].outputs[5], new_nodes["Group.007"].inputs[5])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Group.005"].inputs[16])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Group.005"].inputs[8])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Group.005"].inputs[15])
    tree_links.new(new_nodes["Group.005"].outputs[7], new_nodes["Group.006"].inputs[7])
    tree_links.new(new_nodes["Group.005"].outputs[5], new_nodes["Group.006"].inputs[5])
    tree_links.new(new_nodes["Group.005"].outputs[0], new_nodes["Group.006"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Group.004"].inputs[16])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Group.004"].inputs[8])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Group.004"].inputs[15])
    tree_links.new(new_nodes["Group.004"].outputs[0], new_nodes["Group.005"].inputs[0])
    tree_links.new(new_nodes["Group.004"].outputs[5], new_nodes["Group.005"].inputs[5])
    tree_links.new(new_nodes["Group.004"].outputs[7], new_nodes["Group.005"].inputs[7])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Group.003"].inputs[16])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Group.003"].inputs[8])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Group.003"].inputs[15])
    tree_links.new(new_nodes["Group.003"].outputs[0], new_nodes["Group.004"].inputs[0])
    tree_links.new(new_nodes["Group.003"].outputs[5], new_nodes["Group.004"].inputs[5])
    tree_links.new(new_nodes["Group.003"].outputs[7], new_nodes["Group.004"].inputs[7])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Group.002"].inputs[16])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Group.002"].inputs[8])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Group.002"].inputs[15])
    tree_links.new(new_nodes["Group.002"].outputs[7], new_nodes["Group.003"].inputs[7])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Group.001"].inputs[16])
    tree_links.new(new_nodes["Group.009"].outputs[0], new_nodes["Group.001"].inputs[9])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Group.001"].inputs[8])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Group.001"].inputs[15])
    tree_links.new(new_nodes["Group.001"].outputs[7], new_nodes["Group.002"].inputs[7])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Group"].inputs[16])
    tree_links.new(new_nodes["Group.009"].outputs[0], new_nodes["Group"].inputs[9])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Group"].inputs[8])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Group"].inputs[15])
    tree_links.new(new_nodes["Group"].outputs[7], new_nodes["Group.001"].inputs[7])
    tree_links.new(new_nodes["Group"].outputs[0], new_nodes["Group.001"].inputs[0])
    tree_links.new(new_nodes["Group"].outputs[5], new_nodes["Group.001"].inputs[5])
    tree_links.new(new_nodes["Set Position.001"].outputs[0], new_nodes["Group.008"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Group.008"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Group.008"].inputs[2])
    tree_links.new(new_nodes["Group.008"].outputs[0], new_nodes["Group.003"].inputs[9])
    tree_links.new(new_nodes["Group.008"].outputs[0], new_nodes["Group.004"].inputs[9])
    tree_links.new(new_nodes["Group.008"].outputs[0], new_nodes["Group.005"].inputs[9])
    tree_links.new(new_nodes["Group.008"].outputs[0], new_nodes["Group.006"].inputs[9])
    tree_links.new(new_nodes["Group.008"].outputs[0], new_nodes["Group.007"].inputs[9])
    tree_links.new(new_nodes["Group Input"].outputs[8], new_nodes["Group.009"].inputs[3])
    tree_links.new(new_nodes["Group.008"].outputs[0], new_nodes["Group.015"].inputs[1])
    tree_links.new(new_nodes["Group"].outputs[2], new_nodes["Group.001"].inputs[2])
    tree_links.new(new_nodes["Group.001"].outputs[2], new_nodes["Group.002"].inputs[2])
    tree_links.new(new_nodes["Group.002"].outputs[2], new_nodes["Group.003"].inputs[2])
    tree_links.new(new_nodes["Group.003"].outputs[2], new_nodes["Group.004"].inputs[2])
    tree_links.new(new_nodes["Group.004"].outputs[2], new_nodes["Group.005"].inputs[2])
    tree_links.new(new_nodes["Group.005"].outputs[2], new_nodes["Group.006"].inputs[2])
    tree_links.new(new_nodes["Group.006"].outputs[2], new_nodes["Group.007"].inputs[2])
    tree_links.new(new_nodes["Group.007"].outputs[2], new_nodes["Group Output"].inputs[2])
    tree_links.new(new_nodes["Capture Attribute.008"].outputs[0], new_nodes["Capture Attribute.007"].inputs[0])
    tree_links.new(new_nodes["Group.007"].outputs[2], new_nodes["Math.012"].inputs[1])
    tree_links.new(new_nodes["Edge Neighbors.001"].outputs[0], new_nodes["Math.011"].inputs[0])
    tree_links.new(new_nodes["Math.011"].outputs[0], new_nodes["Math.012"].inputs[0])
    tree_links.new(new_nodes["Position.005"].outputs[0], new_nodes["Vector Math.008"].inputs[0])
    tree_links.new(new_nodes["Group.012"].outputs[0], new_nodes["Capture Attribute.002"].inputs[0])
    tree_links.new(new_nodes["Vector Math.008"].outputs[1], new_nodes["Math.005"].inputs[0])
    tree_links.new(new_nodes["Math.007"].outputs[0], new_nodes["Math.004"].inputs[0])
    tree_links.new(new_nodes["Math.005"].outputs[0], new_nodes["Math.004"].inputs[1])
    tree_links.new(new_nodes["Math.004"].outputs[0], new_nodes["Capture Attribute.002"].inputs[2])
    tree_links.new(new_nodes["Capture Attribute.002"].outputs[2], new_nodes["Group"].inputs[2])
    tree_links.new(new_nodes["Math.012"].outputs[0], new_nodes["Capture Attribute.007"].inputs[2])
    tree_links.new(new_nodes["Capture Attribute.007"].outputs[2], new_nodes["Group Output"].inputs[3])
    tree_links.new(new_nodes["Group.008"].outputs[0], new_nodes["Group.002"].inputs[9])
    tree_links.new(new_nodes["Group.001"].outputs[5], new_nodes["Set Position.001"].inputs[0])
    tree_links.new(new_nodes["Group.001"].outputs[0], new_nodes["Set Position"].inputs[0])
    tree_links.new(new_nodes["Set Position"].outputs[0], new_nodes["Group.002"].inputs[0])
    tree_links.new(new_nodes["Set Position.001"].outputs[0], new_nodes["Group.002"].inputs[5])
    tree_links.new(new_nodes["Group.002"].outputs[0], new_nodes["Group.003"].inputs[0])
    tree_links.new(new_nodes["Group.002"].outputs[5], new_nodes["Group.003"].inputs[5])
    tree_links.new(new_nodes["Group Input"].outputs[8], new_nodes["Group"].inputs[11])
    tree_links.new(new_nodes["Group Input"].outputs[8], new_nodes["Group.001"].inputs[11])
    tree_links.new(new_nodes["Math.006"].outputs[0], new_nodes["Math.005"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Math.006"].inputs[0])
    tree_links.new(new_nodes["Edge Neighbors"].outputs[0], new_nodes["Math.007"].inputs[0])
    tree_links.new(new_nodes["Group.010"].outputs[0], new_nodes["Subdivision Surface"].inputs[0])
    tree_links.new(new_nodes["Subdivision Surface"].outputs[0], new_nodes["Set Position.002"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Domain Size"].inputs[0])
    tree_links.new(new_nodes["Domain Size"].outputs[2], new_nodes["Math.001"].inputs[0])
    tree_links.new(new_nodes["Group.009"].outputs[0], new_nodes["Math.002"].inputs[1])
    tree_links.new(new_nodes["Group.009"].outputs[0], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Boolean Math"].inputs[0])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Boolean Math"].inputs[1])
    tree_links.new(new_nodes["Boolean Math"].outputs[0], new_nodes["Math.002"].inputs[0])
    tree_links.new(new_nodes["Boolean Math"].outputs[0], new_nodes["Boolean Math.001"].inputs[0])
    tree_links.new(new_nodes["Ico Sphere"].outputs[0], new_nodes["Delete Geometry.001"].inputs[0])
    tree_links.new(new_nodes["Boolean Math.001"].outputs[0], new_nodes["Delete Geometry.001"].inputs[1])
    tree_links.new(new_nodes["Join Geometry"].outputs[0], new_nodes["Group.010"].inputs[0])
    tree_links.new(new_nodes["Boolean Math"].outputs[0], new_nodes["Delete Geometry"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Delete Geometry"].inputs[0])
    tree_links.new(new_nodes["Delete Geometry"].outputs[0], new_nodes["Join Geometry"].inputs[0])
    tree_links.new(new_nodes["Delete Geometry.001"].outputs[0], new_nodes["Join Geometry"].inputs[0])
    tree_links.new(new_nodes["Map Range.002"].outputs[0], new_nodes["Capture Attribute.001"].inputs[5])
    tree_links.new(new_nodes["Group.009"].outputs[0], new_nodes["Map Range.002"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.005"].outputs[0], new_nodes["Capture Attribute.001"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.001"].outputs[0], new_nodes["Set Position.003"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute"].outputs[0], new_nodes["Capture Attribute.005"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.005"].outputs[4], new_nodes["Group"].inputs[3])
    tree_links.new(new_nodes["Capture Attribute.001"].outputs[5], new_nodes["Group"].inputs[4])
    tree_links.new(new_nodes["Group"].outputs[3], new_nodes["Group.001"].inputs[3])
    tree_links.new(new_nodes["Group"].outputs[4], new_nodes["Group.001"].inputs[4])
    tree_links.new(new_nodes["Group.001"].outputs[3], new_nodes["Group.002"].inputs[3])
    tree_links.new(new_nodes["Group.001"].outputs[4], new_nodes["Group.002"].inputs[4])
    tree_links.new(new_nodes["Group.002"].outputs[3], new_nodes["Group.003"].inputs[3])
    tree_links.new(new_nodes["Group.002"].outputs[4], new_nodes["Group.003"].inputs[4])
    tree_links.new(new_nodes["Group.003"].outputs[3], new_nodes["Group.004"].inputs[3])
    tree_links.new(new_nodes["Group.003"].outputs[4], new_nodes["Group.004"].inputs[4])
    tree_links.new(new_nodes["Group.004"].outputs[3], new_nodes["Group.005"].inputs[3])
    tree_links.new(new_nodes["Group.004"].outputs[4], new_nodes["Group.005"].inputs[4])
    tree_links.new(new_nodes["Group.005"].outputs[3], new_nodes["Group.006"].inputs[3])
    tree_links.new(new_nodes["Group.005"].outputs[4], new_nodes["Group.006"].inputs[4])
    tree_links.new(new_nodes["Group.006"].outputs[3], new_nodes["Group.007"].inputs[3])
    tree_links.new(new_nodes["Group.006"].outputs[4], new_nodes["Group.007"].inputs[4])
    tree_links.new(new_nodes["Boolean Math.002"].outputs[0], new_nodes["Math.013"].inputs[0])
    tree_links.new(new_nodes["Math.009"].outputs[0], new_nodes["Math.010"].inputs[0])
    tree_links.new(new_nodes["Math.013"].outputs[0], new_nodes["Math.010"].inputs[1])
    tree_links.new(new_nodes["Group.007"].outputs[3], new_nodes["Boolean Math.002"].inputs[0])
    tree_links.new(new_nodes["Group.007"].outputs[3], new_nodes["Math.009"].inputs[0])
    tree_links.new(new_nodes["Group.008"].outputs[0], new_nodes["Map Range.003"].inputs[0])
    tree_links.new(new_nodes["Map Range.003"].outputs[0], new_nodes["Math.013"].inputs[1])
    tree_links.new(new_nodes["Group.007"].outputs[4], new_nodes["Math.009"].inputs[1])
    tree_links.new(new_nodes["Math.010"].outputs[0], new_nodes["Capture Attribute.006"].inputs[5])
    tree_links.new(new_nodes["Capture Attribute.006"].outputs[5], new_nodes["Group Output"].inputs[4])
    tree_links.new(new_nodes["Capture Attribute.007"].outputs[0], new_nodes["Capture Attribute.006"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.006"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Group"].outputs[1], new_nodes["Group.001"].inputs[1])
    tree_links.new(new_nodes["Group.001"].outputs[1], new_nodes["Group.002"].inputs[1])
    tree_links.new(new_nodes["Group.002"].outputs[1], new_nodes["Group.003"].inputs[1])
    tree_links.new(new_nodes["Group.003"].outputs[1], new_nodes["Group.004"].inputs[1])
    tree_links.new(new_nodes["Group.004"].outputs[1], new_nodes["Group.005"].inputs[1])
    tree_links.new(new_nodes["Group.005"].outputs[1], new_nodes["Group.006"].inputs[1])
    tree_links.new(new_nodes["Group.006"].outputs[1], new_nodes["Group.007"].inputs[1])
    tree_links.new(new_nodes["Join Geometry.001"].outputs[0], new_nodes["Capture Attribute.008"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.002"].outputs[0], new_nodes["Capture Attribute.004"].inputs[0])
    tree_links.new(new_nodes["Group.012"].outputs[1], new_nodes["Capture Attribute.003"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.003"].outputs[0], new_nodes["Group"].inputs[5])
    tree_links.new(new_nodes["Group.007"].outputs[1], new_nodes["Math.008"].inputs[1])
    tree_links.new(new_nodes["Capture Attribute.008"].outputs[2], new_nodes["Group Output"].inputs[5])
    tree_links.new(new_nodes["Math.008"].outputs[0], new_nodes["Capture Attribute.008"].inputs[2])
    tree_links.new(new_nodes["Group.015"].outputs[2], new_nodes["Math.008"].inputs[0])
    tree_links.new(new_nodes["Group.015"].outputs[0], new_nodes["Group.013"].inputs[0])
    tree_links.new(new_nodes["Group.007"].outputs[5], new_nodes["Group.015"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.004"].outputs[0], new_nodes["Group"].inputs[0])
    tree_links.new(new_nodes["Group"].outputs[6], new_nodes["Group.001"].inputs[6])
    tree_links.new(new_nodes["Group.001"].outputs[6], new_nodes["Group.002"].inputs[6])
    tree_links.new(new_nodes["Group.002"].outputs[6], new_nodes["Group.003"].inputs[6])
    tree_links.new(new_nodes["Group.003"].outputs[6], new_nodes["Group.004"].inputs[6])
    tree_links.new(new_nodes["Group.004"].outputs[6], new_nodes["Group.005"].inputs[6])
    tree_links.new(new_nodes["Group.005"].outputs[6], new_nodes["Group.006"].inputs[6])
    tree_links.new(new_nodes["Group.006"].outputs[6], new_nodes["Group.007"].inputs[6])
    tree_links.new(new_nodes["Group.007"].outputs[6], new_nodes["Group.015"].inputs[2])
    tree_links.new(new_nodes["Capture Attribute.003"].outputs[2], new_nodes["Group"].inputs[6])
    tree_links.new(new_nodes["Capture Attribute.004"].outputs[2], new_nodes["Group"].inputs[1])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False
    return new_node_group

# depending on the name passed to function, create the right set of nodes in a group and pass back
def create_custom_geo_node_group(node_group_name):
    if node_group_name == MEGASPHERE_SUBDIV_BY_DIST_GEO_NG_NAME:
        return create_geo_ng_scale_for_dist()
    if node_group_name == MEGASPHERE_SUBDIV_BY_PROXIMITY_GEO_NG_NAME:
        return create_geo_ng_scale_for_proximity()
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
    ensure_geo_node_group(MEGASPHERE_SUBDIV_BY_DIST_GEO_NG_NAME, override_create)
    ensure_geo_node_group(MEGASPHERE_SUBDIV_BY_PROXIMITY_GEO_NG_NAME, override_create)
    ensure_geo_node_group(MEGASPHERE_CULL_ANGLE_GEO_NG_NAME, override_create)
    ensure_geo_node_group(MEGASPHERE_CULL_DIST_GEO_NG_NAME, override_create)
    ensure_geo_node_group(MEGASPHERE_LOD_GEO_NG_NAME, override_create)
    ensure_geo_node_group(MEGASPHERE_SUBDIV_GEO_NG_NAME, override_create)
    ensure_geo_node_group(MEGASPHERE_ITERATE_GEO_NG_NAME, override_create)
    ensure_geo_node_group(MEGASPHERE_GEO_NG_NAME, override_create)

def create_obs_place_input_nodes(tree_nodes, tree_links, megasphere_node, vec_d3em3e_node, big_space_rig,
                                 proxy_place_bone_name_0e, proxy_place_bone_name_6e):
    new_nodes = {}

    node = tree_nodes.new(type="FunctionNodeInputVector")
    node.label = "Obs 6e"
    # location
    if proxy_place_bone_name_0e is None or proxy_place_bone_name_6e is None:
        node.location = (-220, -300)
    else:
        node.location = (-400, -300)
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
        node.location = (-220, -440)
    else:
        node.location = (-400, -580)
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
        node.location = (-400, -440)
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
        node.location = (-400, -720)
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
        node.location = (-220, -300)
        node.operation = "SUBTRACT"
        new_nodes["Vector Math"] = node

        node = tree_nodes.new(type="ShaderNodeVectorMath")
        node.location = (-220, -460)
        node.operation = "SUBTRACT"
        new_nodes["Vector Math.001"] = node

    # if not using Place location then ...
    if proxy_place_bone_name_0e is None or proxy_place_bone_name_6e is None:
        tree_links.new(new_nodes["Vector"].outputs[0], megasphere_node.inputs[7])
        tree_links.new(new_nodes["Vector.001"].outputs[0], megasphere_node.inputs[8])
        # if using noise, then create links to next node
        if vec_d3em3e_node != None:
            tree_links.new(new_nodes["Vector"].outputs[0], vec_d3em3e_node.inputs[0])
            tree_links.new(new_nodes["Vector.001"].outputs[0], vec_d3em3e_node.inputs[1])
        return new_nodes["Vector"], new_nodes["Vector.001"]
    # else using Place location
    else:
        tree_links.new(new_nodes["Vector"].outputs[0], new_nodes["Vector Math"].inputs[0])
        tree_links.new(new_nodes["Vector.001"].outputs[0], new_nodes["Vector Math.001"].inputs[0])
        tree_links.new(new_nodes["Vector.002"].outputs[0], new_nodes["Vector Math"].inputs[1])
        tree_links.new(new_nodes["Vector.003"].outputs[0], new_nodes["Vector Math.001"].inputs[1])
        tree_links.new(new_nodes["Vector Math"].outputs[0], megasphere_node.inputs[7])
        tree_links.new(new_nodes["Vector Math.001"].outputs[0], megasphere_node.inputs[8])
        # if using noise, then create links to next node
        if vec_d3em3e_node != None:
            tree_links.new(new_nodes["Vector Math"].outputs[0], vec_d3em3e_node.inputs[0])
            tree_links.new(new_nodes["Vector Math.001"].outputs[0], vec_d3em3e_node.inputs[1])
        return new_nodes["Vector Math"], new_nodes["Vector Math.001"]

def create_apply_megasphere_nodes_regular(sphere_radius, tree_nodes, tree_links, ico7_wgt):
    new_nodes = {}

    # create nodes
    node = tree_nodes.new(type="GeometryNodeGroup")
    node.label = "MegaSphere"
    node.location = (-40, -20)
    node.node_tree = bpy.data.node_groups.get(MEGASPHERE_GEO_NG_NAME)
    node.inputs[1].default_value = sphere_radius
    node.inputs[2].default_value = 10.0
    node.inputs[3].default_value = 9999.0
    node.inputs[4].default_value = 0.0
    node.inputs[5].default_value = 0.0
    node.inputs[6].default_value = 64000
    new_nodes["MegaSphere.Group"] = node

    node = tree_nodes.new(type="GeometryNodeSetMaterial")
    node.location = (220, 120)
    new_nodes["Set Material"] = node

    node = tree_nodes.new(type="GeometryNodeObjectInfo")
    node.location = (-220, -40)
    node.transform_space = "ORIGINAL"
    node.inputs[0].default_value = ico7_wgt
    new_nodes["Object Info"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-220, 80)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (400, 40)
    new_nodes["Group Output"] = node

    # create links
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Set Material"].inputs[2])
    tree_links.new(new_nodes["MegaSphere.Group"].outputs[1], new_nodes["Group Output"].inputs[1])
    tree_links.new(new_nodes["MegaSphere.Group"].outputs[0], new_nodes["Set Material"].inputs[0])
    tree_links.new(new_nodes["Set Material"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Object Info"].outputs[3], new_nodes["MegaSphere.Group"].inputs[0])

    return new_nodes["MegaSphere.Group"]

def create_apply_megasphere_nodes_noise(sphere_radius, tree_nodes, tree_links, ico7_wgt):
    new_nodes = {}

    # create nodes
    node = tree_nodes.new(type="GeometryNodeGroup")
    node.label = "MegaSphere"
    node.location = (-40, -20)
    node.node_tree = bpy.data.node_groups.get(MEGASPHERE_GEO_NG_NAME)
    node.inputs[1].default_value = sphere_radius
    node.inputs[2].default_value = 10.0
    node.inputs[3].default_value = 9999.0
    node.inputs[4].default_value = 0.0
    node.inputs[5].default_value = 0.0
    node.inputs[6].default_value = 64000
    new_nodes["MegaSphere.Group"] = node

    node = tree_nodes.new(type="GeometryNodeGroup")
    node.location = (-40, -440)
    node.node_tree = bpy.data.node_groups.get(node_group_name_for_name_and_type(VEC_DIV_3E_MOD_3E_DUO_NG_NAME,
                                                                                'GeometryNodeTree'))
    new_nodes["Group.002"] = node

    node = tree_nodes.new(type="GeometryNodeGroup")
    node.location = (1400, -20)
    node.node_tree = bpy.data.node_groups.get(SNAP_VERT_LOD_GEO_NG_NAME)
    new_nodes["Group.001"] = node

    node = tree_nodes.new(type="GeometryNodeGroup")
    node.location = (140, -300)
    node.node_tree = bpy.data.node_groups.get(node_group_name_for_name_and_type(TILE_XYZ_3E_DUO_NG_NAME,
                                                                                'GeometryNodeTree'))
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    new_nodes["Group.003"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (-220, -620)
    new_nodes["Position"] = node

    node = tree_nodes.new(type="GeometryNodeObjectInfo")
    node.location = (-220, -100)
    node.transform_space = "ORIGINAL"
    node.inputs[0].default_value = ico7_wgt
    new_nodes["Object Info"] = node

    node = tree_nodes.new(type="GeometryNodeSetPosition")
    node.location = (1040, -200)
    new_nodes["Set Position"] = node

    node = tree_nodes.new(type="GeometryNodeGroup")
    node.location = (1220, -20)
    node.node_tree = bpy.data.node_groups.get("SubdivSurfWithIndex.BSR.GeoNG")
    node.inputs[1].default_value = 0
    new_nodes["Group.004"] = node

    node = tree_nodes.new(type="GeometryNodeMergeByDistance")
    node.location = (1580, -20)
    node.inputs[2].default_value = 0.01
    new_nodes["Merge by Distance"] = node

    node = tree_nodes.new(type="GeometryNodeSetShadeSmooth")
    node.location = (1760, -20)
    node.inputs[2].default_value = True
    new_nodes["Set Shade Smooth"] = node

    node = tree_nodes.new(type="GeometryNodeSetMaterial")
    node.location = (1940, -20)
    new_nodes["Set Material"] = node

    node = tree_nodes.new(type="ShaderNodeTexNoise")
    node.location = (320, -300)
    node.noise_dimensions = "4D"
    node.inputs[2].default_value = 5.0
    node.inputs[3].default_value = 2.0
    node.inputs[4].default_value = 0.5
    node.inputs[5].default_value = 0.0
    new_nodes["Noise Texture"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1040, -20)
    node.operation = "ADD"
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (680, -300)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = 50.0
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (500, -300)
    node.operation = "ADD"
    node.inputs[1].default_value = -0.5
    new_nodes["Math"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (860, -300)
    node.operation = "MULTIPLY"
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (1760, -180)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (2200, -40)
    new_nodes["Group Output"] = node

    # create links
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Set Material"].inputs[2])
    tree_links.new(new_nodes["MegaSphere.Group"].outputs[1], new_nodes["Group Output"].inputs[1])
    tree_links.new(new_nodes["Position"].outputs[0], new_nodes["Group.002"].inputs[2])
    tree_links.new(new_nodes["Group.002"].outputs[0], new_nodes["Group.003"].inputs[0])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Math.001"].inputs[0])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Vector Math"].inputs[1])
    tree_links.new(new_nodes["MegaSphere.Group"].outputs[1], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["MegaSphere.Group"].outputs[2], new_nodes["Math.002"].inputs[0])
    tree_links.new(new_nodes["MegaSphere.Group"].outputs[3], new_nodes["Math.002"].inputs[1])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Group.004"].inputs[2])
    tree_links.new(new_nodes["Vector Math"].outputs[0], new_nodes["Set Position"].inputs[3])
    tree_links.new(new_nodes["MegaSphere.Group"].outputs[2], new_nodes["Group.001"].inputs[1])
    tree_links.new(new_nodes["MegaSphere.Group"].outputs[3], new_nodes["Group.001"].inputs[2])
    tree_links.new(new_nodes["Group.004"].outputs[0], new_nodes["Group.001"].inputs[0])
    tree_links.new(new_nodes["Set Position"].outputs[0], new_nodes["Group.004"].inputs[0])
    tree_links.new(new_nodes["MegaSphere.Group"].outputs[0], new_nodes["Set Position"].inputs[0])
    tree_links.new(new_nodes["Merge by Distance"].outputs[0], new_nodes["Set Shade Smooth"].inputs[0])
    tree_links.new(new_nodes["Set Shade Smooth"].outputs[0], new_nodes["Set Material"].inputs[0])
    tree_links.new(new_nodes["Set Material"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Group.001"].outputs[0], new_nodes["Merge by Distance"].inputs[0])
    tree_links.new(new_nodes["Group.003"].outputs[0], new_nodes["Noise Texture"].inputs[0])
    tree_links.new(new_nodes["Group.003"].outputs[1], new_nodes["Noise Texture"].inputs[1])
    tree_links.new(new_nodes["Noise Texture"].outputs[0], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Object Info"].outputs[3], new_nodes["MegaSphere.Group"].inputs[0])
    tree_links.new(new_nodes["MegaSphere.Group"].outputs[4], new_nodes["Group Output"].inputs[2])
    tree_links.new(new_nodes["MegaSphere.Group"].outputs[5], new_nodes["Group.004"].inputs[3])
    tree_links.new(new_nodes["Group.004"].outputs[1], new_nodes["Group Output"].inputs[3])

    return new_nodes["MegaSphere.Group"], new_nodes["Group.002"]

def create_individual_geo_ng(new_node_group, ico7_wgt, override_create, use_noise, big_space_rig, sphere_radius,
                             proxy_place_bone_name_0e=None, proxy_place_bone_name_6e=None):
    # initialize variables
    node_tree_type = 'GeometryNodeTree'
    new_node_group.inputs.new(type='NodeSocketMaterial', name="Material")
    new_node_group.outputs.new(type='NodeSocketVector', name="MegaSphere Normal")
    new_node_group.outputs.new(type='NodeSocketInt', name="LOD Index")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Subdiv Index")
    tree_nodes = new_node_group.nodes
    tree_links = new_node_group.links
    # delete old nodes before adding new nodes
    tree_nodes.clear()

    # create nodes to implement MegaSphere, ensuring required node groups are created first
    if use_noise:
        ensure_node_groups(override_create,
                           [node_group_name_for_name_and_type(VEC_DIV_3E_MOD_3E_DUO_NG_NAME, node_tree_type),
                            SNAP_VERT_LOD_GEO_NG_NAME,
                            node_group_name_for_name_and_type(TILE_XYZ_3E_DUO_NG_NAME, node_tree_type)],
                           node_tree_type, create_prereq_util_node_group)
        megasphere_node, vec_d3em3e_node = create_apply_megasphere_nodes_noise(sphere_radius, tree_nodes, tree_links,
                                                                               ico7_wgt)
    else:
        megasphere_node = create_apply_megasphere_nodes_regular(sphere_radius, tree_nodes, tree_links, ico7_wgt)
        vec_d3em3e_node = None

    # create observer/place input nodes and links
    create_obs_place_input_nodes(tree_nodes, tree_links, megasphere_node, vec_d3em3e_node, big_space_rig,
                                 proxy_place_bone_name_0e, proxy_place_bone_name_6e)

    # deselect all new nodes
    for n in tree_nodes: n.select = False

    return new_node_group

def get_create_icosphere7_widget(context, big_space_rig):
    wgt_list = get_widget_objs_from_rig(big_space_rig)
    old_wgt = wgt_list.get(ICOSPHERE7_WIDGET_NAME)
    # old widget found then return it
    if old_wgt:
        return old_wgt
    # old widget not found, so create new widget and return new widget object
    else:
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=7, radius=1, align='WORLD', location=(0, 0, 0),
                                              scale=(1, 1, 1))
        ob = context.active_object
        ob.name = WIDGET_ICOSPHERE7_OBJNAME
        add_widgets_to_big_space_rig(big_space_rig, [ob])
        return ob

def add_mega_sphere_geo_nodes_to_object(ob, big_space_rig, ico7_wgt, sphere_radius, proxy_place_bone_name_0e,
                                        proxy_place_bone_name_6e, override_create, use_noise):
    geo_nodes_mod = ob.modifiers.new(name="MegaSphere.GeometryNodes", type='NODES')
    create_individual_geo_ng(geo_nodes_mod.node_group, ico7_wgt, override_create, use_noise, big_space_rig,
                             sphere_radius, proxy_place_bone_name_0e, proxy_place_bone_name_6e)

def create_megasphere_obj(collection_name=None):
    verts = []
    edges = []
    if collection_name is None:
        return create_mesh_obj_from_pydata(verts, edges=edges, obj_name=MEGASPHERE_OBJ_NAME)
    else:
        return create_mesh_obj_from_pydata(verts, edges=edges, obj_name=MEGASPHERE_OBJ_NAME,
                                           collection_name=collection_name)

def create_mega_sphere(context, big_space_rig, sphere_radius, override_create, use_noise, place_bone_name):
    # ensure that node groups exist that will be used later by the Mega Sphere geometry nodes modifier
    ensure_node_groups(override_create, [SUBDIV_SURF_WITH_INDEX_GEO_NG_NAME], 'GeometryNodeTree',
                       create_prereq_util_node_group)
    ensure_mega_sphere_geo_nodes(override_create)

    # ensure that the Icosphere7 widget mesh object is available
    ico7_wgt = get_create_icosphere7_widget(context, big_space_rig)

    # if v2.79
    if bpy.app.version < (2,80,0):
        ob = create_megasphere_obj()
        ob.layers[0] = True
        for i in range(1, 20):
            ob.layers[i] = False
    # else v2.8 or later
    else:
        # try to put MegaSphere into Big Space Rig's collection
        if len(big_space_rig.users_collection) > 0:
            ob = create_megasphere_obj(collection_name=big_space_rig.users_collection[0].name)
        else:
            ob = create_megasphere_obj(collection_name=None)

    ob.parent = big_space_rig
    if place_bone_name != "":
        proxy_place_bone_name_6e, proxy_place_bone_name_0e = get_6e_0e_from_place_bone_name(big_space_rig,
                                                                                            place_bone_name)
    else:
        proxy_place_bone_name_6e, proxy_place_bone_name_0e = None, None

    add_mega_sphere_geo_nodes_to_object(ob, big_space_rig, ico7_wgt, sphere_radius, proxy_place_bone_name_0e,
                                        proxy_place_bone_name_6e, override_create, use_noise)

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
            place_bone_name = scn.BSR_MegaSpherePlaceBoneName[1:len(scn.BSR_MegaSpherePlaceBoneName)]
        create_mega_sphere(context, active_ob, scn.BSR_MegaSphereRadius, scn.BSR_NodesOverrideCreate,
                           scn.BSR_MegaSphereWithNoise, place_bone_name)
        return {'FINISHED'}
