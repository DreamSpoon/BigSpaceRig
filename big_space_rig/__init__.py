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

bl_info = {
    "name": "Big Space Rig",
    "description": "'Solar system in a box' addon for Blender, with rig to manage very large spaces (> 10^30 m3), " \
        "and geometry nodes to create very large procedural objects. Also, a 'forced perspective' effect (optional" \
        ", per Place) to create 'condensed space' for viewing large objects that are separated by very large " \
        "distances, at correct scale (e.g. planets, moons, stars).",
    "author": "Dave",
    "version": (0, 2, 1),
    "blender": (2, 80, 0),
    "location": "View 3D -> Tools -> BigSpaceRig",
    "category": "Shader/Geometry Nodes, Other",
    "wiki_url": "https://github.com/DreamSpoon/BigSpaceRig#readme",
}

import math

import bpy
from bpy.props import PointerProperty

from .rig import (OBJ_PROP_FP_POWER, OBJ_PROP_FP_MIN_DIST, OBJ_PROP_FP_MIN_SCALE, OBJ_PROP_BONE_SCL_MULT,
    OBJ_PROP_BONE_PLACE)
from .rig import (is_big_space_rig, BSR_CreateBigSpaceRig, BSR_QuickSelectObserver6e, BSR_QuickSelectObserver0e,
    BSR_QuickSelectObserverFocus, BSR_QuickSelectPlace6e,
    BSR_QuickSelectPlace0e, BSR_QuickSelectPlaceProxy)
from .observer import (ANGLE_TYPE_ITEMS, ANGLE_TYPE_DEG_MIN_SEC_FRAC, ANGLE_TYPE_DEGREES, ANGLE_TYPE_RADIANS)
from .observer import (BSR_ObserveMegaSphere, BSR_ObservePlace)
from .place import (BSR_PlaceCreate, BSR_PlaceCreateAttachSingle, BSR_PlaceCreateAttachMulti, BSR_PlaceParentObject)
from .geo_node_place_fp import BSR_AddPlaceFP_GeoNodes
from .mega_sphere import BSR_MegaSphereCreate
from .mat_node_util import (BSR_ObserverInputCreateDuoNode, BSR_PlaceInputCreateDuoNode,
    BSR_PlaceOffsetInputCreateDuoNode, BSR_VecDiv3eMod3eCreateDuoNode, BSR_VecDiv6eCreateDuoNode,
    BSR_VecDiv5eCreateDuoNode, BSR_VecDiv4eCreateDuoNode, BSR_SnapVertexLOD_CreateGeoNode, BSR_TileXYZ3eCreateDuoNode)

if bpy.app.version < (2,80,0):
    Region = "TOOLS"
else:
    Region = "UI"

BLANK_ITEM_STR = "_"

class BSR_PT_ActiveRig(bpy.types.Panel):
    bl_label = "Active Rig"
    bl_space_type = "VIEW_3D"
    bl_region_type = Region
    bl_category = "BigSpaceRig"

    def draw(self, context):
        active_ob = context.active_object
        # display panel only if active object is a Big Space Rig
        if not is_big_space_rig(active_ob):
            return
        layout = self.layout
        box = layout.box()
        box.label(text="Active Rig: " + active_ob.name)
        box.prop(active_ob, '["'+OBJ_PROP_FP_POWER+'"]')
        box.prop(active_ob, '["'+OBJ_PROP_FP_MIN_DIST+'"]')
        box.prop(active_ob, '["'+OBJ_PROP_FP_MIN_SCALE+'"]')

class BSR_PT_CreateRig(bpy.types.Panel):
    bl_label = "Create Rig"
    bl_space_type = "VIEW_3D"
    bl_region_type = Region
    bl_category = "BigSpaceRig"

    def draw(self, context):
        scn = context.scene
        layout = self.layout
        box = layout.box()
        box.operator("big_space_rig.create_big_space_rig")
        box.label(text="New Rig Properties:")
        box.prop(scn, "BSR_NewObserverFP_Power")
        box.prop(scn, "BSR_NewObserverFP_MinDist")
        box.prop(scn, "BSR_NewObserverFP_MinScale")

class BSR_PT_Observer(bpy.types.Panel):
    bl_label = "Observer"
    bl_space_type = "VIEW_3D"
    bl_region_type = Region
    bl_category = "BigSpaceRig"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        active_ob = context.active_object
        is_bsr_active = is_big_space_rig(active_ob)
        scn = context.scene
        layout = self.layout
        box = layout.box()
        box.active = is_bsr_active
        box.label(text="Quick Select")
        box.operator("big_space_rig.quick_select_observer_6e")
        box.operator("big_space_rig.quick_select_observer_0e")
        box.operator("big_space_rig.quick_select_observer_focus")
        box = layout.box()
        box.active = is_bsr_active
        box.label(text="Observe Place")
        box.prop(scn, "BSR_ObservePlaceBoneName")
        box.operator("big_space_rig.observe_place")
        box = layout.box()
        box.active = is_bsr_active
        box.label(text="Observe MegaSphere")
        box.operator("big_space_rig.view_mega_sphere_by_rad_lat_long")
        box.label(text="Radius")
        col = box.column(align=True)
        col.prop(scn, "BSR_ObserveMegaSphereRad6e")
        col.prop(scn, "BSR_ObserveMegaSphereRad0e")
        box.label(text="Angle Type for (Lat, Long)")
        box.prop(scn, "BSR_ObserveSphereAngleType")
        if scn.BSR_ObserveSphereAngleType == ANGLE_TYPE_DEG_MIN_SEC_FRAC:
            box.label(text="Latitude")
            col = box.column(align=True)
#            col.active = is_bsr_active
            col.prop(scn, "BSR_ObserveMegaSphereLatDMSF_Degrees")
            col.prop(scn, "BSR_ObserveMegaSphereLatDMSF_Minutes")
            col.prop(scn, "BSR_ObserveMegaSphereLatDMSF_Seconds")
            col.prop(scn, "BSR_ObserveMegaSphereLatDMSF_FracSec")
            box.label(text="Longitude")
            col = box.column(align=True)
#            col.active = is_bsr_active
            col.prop(scn, "BSR_ObserveMegaSphereLongDMSF_Degrees")
            col.prop(scn, "BSR_ObserveMegaSphereLongDMSF_Minutes")
            col.prop(scn, "BSR_ObserveMegaSphereLongDMSF_Seconds")
            col.prop(scn, "BSR_ObserveMegaSphereLongDMSF_FracSec")
        elif scn.BSR_ObserveSphereAngleType == ANGLE_TYPE_DEGREES:
            box.label(text="Latitude")
            box.prop(scn, "BSR_ObserveMegaSphereLatDegrees")
            box.label(text="Longitude")
            box.prop(scn, "BSR_ObserveMegaSphereLongDegrees")
        elif scn.BSR_ObserveSphereAngleType == ANGLE_TYPE_RADIANS:
            box.label(text="Latitude")
            box.prop(scn, "BSR_ObserveMegaSphereLatRadians")
            box.label(text="Longitude")
            box.prop(scn, "BSR_ObserveMegaSphereLongRadians")

class BSR_PT_Place(bpy.types.Panel):
    bl_label = "Place"
    bl_space_type = "VIEW_3D"
    bl_region_type = Region
    bl_category = "BigSpaceRig"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        scn = context.scene
        layout = self.layout
        box = layout.box()
        box.label(text="Quick Select")
        box.prop(scn, "BSR_QuickSelectPlaceBoneName")
        box.operator("big_space_rig.quick_select_place_6e")
        box.operator("big_space_rig.quick_select_place_0e")
        box.operator("big_space_rig.quick_select_place_proxy")
        box = layout.box()
        box.label(text="Create")
        box.operator("big_space_rig.create_place")
        box.label(text="Create and Attach")
        box.operator("big_space_rig.create_attach_single_place")
        box.operator("big_space_rig.create_attach_multi_place")
        box.label(text="Create Options")
        box.prop(scn, "BSR_CreatePlaceUseObserverOffset")
        box.prop(scn, "BSR_CreatePlaceCreateRig")
        box.prop(scn, "BSR_CreatePlaceNoReParent")
        box.prop(scn, "BSR_CreatePlaceUseFP")
        box = layout.box()
        box.label(text="Parent to Place")
        box.prop(scn, "BSR_ParentPlaceBoneName")
        box.operator("big_space_rig.parent_to_place")

class BSR_PT_GeoNodes(bpy.types.Panel):
    bl_label = "FP Geometry Nodes"
    bl_space_type = "VIEW_3D"
    bl_region_type = Region
    bl_category = "BigSpaceRig"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        scn = context.scene
        layout = self.layout
        box = layout.box()
        box.label(text="Forced Perspective Geo Nodes")
        box.operator("big_space_rig.add_place_fp_geo_nodes")
        box.prop(scn, "BSR_GeoNodesOverrideCreate")
        box.prop(scn, "BSR_GeoNodesCreateUseAltGroup")
        col = box.column()
        col.active = scn.BSR_GeoNodesCreateUseAltGroup
        col.prop(scn, "BSR_GeoNodesCreateAltGroup")

class BSR_PT_MegaSphere(bpy.types.Panel):
    bl_label = "Mega Sphere"
    bl_space_type = "VIEW_3D"
    bl_region_type = Region
    bl_category = "BigSpaceRig"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        active_ob = context.active_object
        scn = context.scene
        layout = self.layout
        box = layout.box()
        box.active = is_big_space_rig(active_ob)
        box.label(text="Create")
        col = box.column()
        col.operator("big_space_rig.create_mega_sphere")
        col.prop(scn, "BSR_MegaSphereRadius")
        col.prop(scn, "BSR_MegaSphereOverrideCreateNG")
        col.prop(scn, "BSR_MegaSphereUsePlace")
        if col.active:
            subcol = col.column()
            subcol.active = scn.BSR_MegaSphereUsePlace
            subcol.prop(scn, "BSR_MegaSpherePlaceBoneName")
        box.label(text="Add Noise")
        box.prop(scn, "BSR_MegaSphereWithNoise")

class BSR_PT_CreateDuoNodes(bpy.types.Panel):
    bl_idname = "NODE_PT_BigSpaceRig"
    bl_label = "BigSpaceRig"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = Region
    bl_category = "BigSpaceRig"

    def draw(self, context):
        scn = context.scene
        layout = self.layout

        box = layout.box()
        box.label(text="Input")
        box.prop(scn, "BSR_NodeGetInputFromRig")
        col = box.column()
        col.active = (scn.BSR_NodeGetInputFromRig != BLANK_ITEM_STR)
        col.operator("big_space_rig.observer_input_create_duo_node")
        col.prop(scn, "BSR_NodeGetInputFromRigPlace")
        subcol = box.column()
        subcol.active = (scn.BSR_NodeGetInputFromRigPlace != BLANK_ITEM_STR)
        subcol.operator("big_space_rig.place_input_create_duo_node")
        subcol.operator("big_space_rig.place_offset_input_create_duo_node")
        box = layout.box()
        box.label(text="MegaSphere Util")
        box.operator("big_space_rig.snap_vertex_lod_create_geo_node")
        box = layout.box()
        box.label(text="Vector")
        box.operator("big_space_rig.tile_xyz_3e_create_duo_node")
        box.operator("big_space_rig.vec_div_3e_mod_3e_create_duo_node")
        box.operator("big_space_rig.vec_div_6e_create_duo_node")
        box.operator("big_space_rig.vec_div_5e_create_duo_node")
        box.operator("big_space_rig.vec_div_4e_create_duo_node")

classes = [
    BSR_PT_ActiveRig,
    BSR_PT_CreateRig,
    BSR_PT_Observer,
    BSR_CreateBigSpaceRig,
    BSR_QuickSelectObserver6e,
    BSR_QuickSelectObserver0e,
    BSR_QuickSelectObserverFocus,
    BSR_PT_Place,
    BSR_PlaceCreate,
    BSR_PlaceCreateAttachMulti,
    BSR_PlaceCreateAttachSingle,
    BSR_PlaceParentObject,
    BSR_QuickSelectPlace6e,
    BSR_QuickSelectPlace0e,
    BSR_QuickSelectPlaceProxy,
    BSR_PT_CreateDuoNodes,
    BSR_TileXYZ3eCreateDuoNode,
    BSR_ObserverInputCreateDuoNode,
    BSR_PlaceInputCreateDuoNode,
    BSR_PlaceOffsetInputCreateDuoNode,
    BSR_VecDiv3eMod3eCreateDuoNode,
    BSR_VecDiv6eCreateDuoNode,
    BSR_VecDiv5eCreateDuoNode,
    BSR_VecDiv4eCreateDuoNode,
    BSR_SnapVertexLOD_CreateGeoNode,
    BSR_ObservePlace,
]
# geometry node support is only for Blender v2.9+ (or maybe v3.0+ ...)
# TODO: check what version is needed for current geometry nodes setup
if bpy.app.version >= (2,90,0):
    classes.extend([
        BSR_PT_GeoNodes,
        BSR_AddPlaceFP_GeoNodes,
        BSR_PT_MegaSphere,
        BSR_MegaSphereCreate,
        BSR_ObserveMegaSphere,
    ])

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    register_props()

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    bts = bpy.types.Scene

    del bts.BSR_ParentPlaceBoneName
    del bts.BSR_QuickSelectPlaceBoneName
    del bts.BSR_ObserveMegaSphereLongFracSec
    del bts.BSR_ObserveMegaSphereLongSeconds
    del bts.BSR_ObserveMegaSphereLongMinutes
    del bts.BSR_ObserveMegaSphereLongDegrees
    del bts.BSR_ObserveMegaSphereLatFracSec
    del bts.BSR_ObserveMegaSphereLatSeconds
    del bts.BSR_ObserveMegaSphereLatMinutes
    del bts.BSR_ObserveMegaSphereLatDegrees
    del bts.BSR_ObserveMegaSphereRad0e
    del bts.BSR_ObserveMegaSphereRad6e
    del bts.BSR_ObservePlaceBoneName
    del bts.BSR_NodeGetInputFromRigPlace
    del bts.BSR_NodeGetInputFromRig
    del bts.BSR_MegaSpherePlaceBoneName
    del bts.BSR_MegaSphereUsePlace
    del bts.BSR_MegaSphereOverrideCreateNG
    del bts.BSR_MegaSphereRadius
    del bts.BSR_GeoNodesCreateAltGroup
    del bts.BSR_GeoNodesCreateUseAltGroup
    del bts.BSR_GeoNodesOverrideCreate
    del bts.BSR_CreatePlaceUseFP
    del bts.BSR_CreatePlaceNoReParent
    del bts.BSR_CreatePlaceUseObserverOffset
    del bts.BSR_CreatePlaceCreateRig
    del bts.BSR_NewObserverFP_MinScale
    del bts.BSR_NewObserverFP_MinDist
    del bts.BSR_NewObserverFP_Power

def only_geo_node_group_poll(self, object):
    return object.type == 'GEOMETRY'

def place_bone_items(self, context):
    ob = context.active_object
    if not is_big_space_rig(ob):
        return [(BLANK_ITEM_STR, "", "")]
    else:
        return [(BLANK_ITEM_STR+bone.name, bone.name, "") for bone in ob.data.bones if \
                bone.get(OBJ_PROP_BONE_PLACE) == True]

def obs_input_rig_items(self, context):
    ob = context.active_object
    rig_list = []
    for ob in bpy.data.objects:
        if is_big_space_rig(ob):
            rig_list.append(ob)
    rig_name_items = [(BLANK_ITEM_STR+rig.name, rig.name, "") for rig in rig_list]
    # if list is empty then return the "blank" list
    if len(rig_name_items) < 1:
        return [(BLANK_ITEM_STR, "", "")]
    else:
        return rig_name_items

def place_input_rig_items(self, context):
    ob = bpy.data.objects.get(context.scene.BSR_NodeGetInputFromRig)
    if not is_big_space_rig(ob):
        return [(BLANK_ITEM_STR, "", "")]
    place_item_list = [(BLANK_ITEM_STR+bone.name, bone.name, "") for bone in ob.data.bones if \
                       bone.get(OBJ_PROP_BONE_PLACE) == True]
    # if zero places found then return the "blank" list
    if len(place_item_list) < 1:
        return [(BLANK_ITEM_STR, "", "")]
    else:
        return place_item_list

def register_props():
    bts = bpy.types.Scene
    bp = bpy.props

    bts.BSR_NewObserverFP_Power = bp.FloatProperty(name="FP Power",
        description="Forced Perspective distance Power value, which is applied to the distance between Observer " +
        "and Place with math function power() for generating scales of places/objects attached to Big Space Rig. " +
        "Value is usually between zero and one. Setting this value to zero will remove the 'forced perspective' " +
        "effect", default=0.5)
    bts.BSR_NewObserverFP_MinDist = bp.FloatProperty(name="FP Min Dist",
        description="Forced Perspective Minimum Distance value, which is the minimum distance from Observer before " +
        "'forced perspective' effect begins", default=0.0, min=0.0)
    bts.BSR_NewObserverFP_MinScale = bp.FloatProperty(name="FP Min Scale",
        description="Forced Perspective Minimum Scale value, which is the minimum scale to apply with the " +
        "'Forced Perspective' effect", default=0.0, min=0.0)
    bts.BSR_CreatePlaceUseObserverOffset = bp.BoolProperty(name="Use Observer Offset", description="Offset created " +
        "Place(s) by Observer's current position", default=True)
    bts.BSR_CreatePlaceCreateRig = bp.BoolProperty(name="Create Rig if Needed", description="Create a new " +
        "Big Space Rig before creating place(s) / attaching objects, if no Big Space Rig was active", default=True)
    bts.BSR_CreatePlaceNoReParent = bp.BoolProperty(name="Do not Re-Parent", description="Objects that already " +
        "have a parent object will not be 're-parented' to the Big Space Rig. Only the 'root parents', and " +
        "non-parented objects will be attached to Big Space Rig", default=True)
    bts.BSR_CreatePlaceUseFP =  bp.BoolProperty(name="Use Place Scaling", description="Apply a 'forced perspective' " +
        "scaling effect to places as they move away from the observer - farther away objects 'shrink' to maintain " +
        "close range to observer. Some accuracy is lost due to greater floating point rounding error", default=False)
    bts.BSR_GeoNodesOverrideCreate = bp.BoolProperty(name="Override Create", description="Big Space Rig Geometry " +
        "Nodes custom node group is re-created when geometry nodes are added to object(s), and any previous custom " +
        "group with the same name is deprecated", default=False)
    bts.BSR_GeoNodesCreateUseAltGroup = bp.BoolProperty(name="Use Alt Group", description="Add Big Space Rig " +
        "Geometry Nodes group to alternate geometry node group (click to unlock)", default=False)
    bts.BSR_GeoNodesCreateAltGroup = bp.PointerProperty(name="Alt Group", description="Alternative Geometry Nodes " +
        "group to receive Big Space Rig new Geometry Nodes", type=bpy.types.NodeTree, poll=only_geo_node_group_poll)
    bts.BSR_MegaSphereRadius = bp.FloatProperty(name="Mega Sphere Radius", description="Radius of sphere, in " +
        "mega-meters", default=1.0, min=0.0)
    bts.BSR_MegaSphereOverrideCreateNG = bp.BoolProperty(name="Override Create", description="Mega Sphere Geometry " +
        "Nodes custom node group is re-created when Mega Sphere is created, and any previous custom group with the " +
        "same name is deprecated", default=False)
    bts.BSR_MegaSphereUsePlace = bp.BoolProperty(name="Use Place Offset", description="Create MegaSphere centered " +
        "at given Place in Big Space Rig", default=False)
    bts.BSR_MegaSpherePlaceBoneName = bpy.props.EnumProperty(name="Place", description="Sphere center " +
        "place bone", items=place_bone_items)
    bts.BSR_NodeGetInputFromRig = bpy.props.EnumProperty(name="Rig", description="Big Space Rig to use with " +
        "input nodes", items=obs_input_rig_items)
    bts.BSR_NodeGetInputFromRigPlace = bpy.props.EnumProperty(name="Place", description="Place to use with input " +
        "nodes", items=place_input_rig_items)
    bts.BSR_MegaSphereWithNoise = bp.BoolProperty(name="Create with noise", description="Add nodes to apply Noise3e " +
        "to MegaSphere, when MegaSphere is created", default=False)
    bts.BSR_ObservePlaceBoneName = bpy.props.EnumProperty(name="Place", description="Place to observe",
        items=place_bone_items)
    bts.BSR_ObserveMegaSphereRad6e = bp.FloatProperty(name="Radius 6e", description="Radius, in mega-meters",
        default=1.0, min=0.0)
    bts.BSR_ObserveMegaSphereRad0e = bp.FloatProperty(name="Radius 0e", description="Radius Append, in meters",
        default=0.0)
    bts.BSR_ObserveSphereAngleType = bpy.props.EnumProperty(name="Type", description="Type of angle to use in " +
        "determining (x, Y, Z) sphere location from (Latitude, Longitude) coordinates", items=ANGLE_TYPE_ITEMS)
    bts.BSR_ObserveMegaSphereLatDegrees = bp.FloatProperty(name="Degrees", description="Degrees of Latitude",
        default=0.0)
    bts.BSR_ObserveMegaSphereLatDMSF_Degrees = bp.IntProperty(name="Degrees", description="Degrees of Latitude",
        default=0, min=0, max=360)
    bts.BSR_ObserveMegaSphereLatDMSF_Minutes = bp.IntProperty(name="Minutes", description="Minutes of Latitude",
        default=0, min=0, max=60)
    bts.BSR_ObserveMegaSphereLatDMSF_Seconds = bp.IntProperty(name="Seconds", description="Seconds of Latitude",
        default=0, min=0, max=60)
    bts.BSR_ObserveMegaSphereLatDMSF_FracSec = bp.FloatProperty(name="Fraction",
        description="Fraction of second of Latitude", default=0.0, min=0.0, max=1.0)
    bts.BSR_ObserveMegaSphereLatRadians = bp.FloatProperty(name="Radians", description="Radians of Latitude",
        default=0.0)
    bts.BSR_ObserveMegaSphereLongDegrees = bp.FloatProperty(name="Degrees", description="Degrees of Longitude",
        default=0.0)
    bts.BSR_ObserveMegaSphereLongDMSF_Degrees = bp.IntProperty(name="Degrees", description="Degrees of Longitude",
        default=0, min=0, max=360)
    bts.BSR_ObserveMegaSphereLongDMSF_Minutes = bp.IntProperty(name="Minutes", description="Minutes of Longitude",
        default=0, min=0, max=60)
    bts.BSR_ObserveMegaSphereLongDMSF_Seconds = bp.IntProperty(name="Seconds", description="Seconds of Longitude",
        default=0, min=0, max=60)
    bts.BSR_ObserveMegaSphereLongDMSF_FracSec = bp.FloatProperty(name="Fraction",
        description="Fraction of second of Longitude", default=0.0, min=0.0, max=1.0)
    bts.BSR_ObserveMegaSphereLongRadians = bp.FloatProperty(name="Radians", description="Radians of Longitude",
        default=0.0)
    bts.BSR_QuickSelectPlaceBoneName = bpy.props.EnumProperty(name="Place",
        description="Place to select for quick pose", items=place_bone_items)
    bts.BSR_ParentPlaceBoneName = bpy.props.EnumProperty(name="Parent Place",
        description="Parent selected object(s) to this place", items=place_bone_items)

if __name__ == "__main__":
    register()
