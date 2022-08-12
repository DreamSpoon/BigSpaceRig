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

# TODO: show current rig stats, including bones by way of list box

bl_info = {
    "name": "Big Space Rig",
    "description": "Use 'forced perspective' optical illusion to 'condense space' between objects. Display " \
        "far away objects at a smaller scale and closer distance than would be realistic. Multi-scale proxy-place" \
        "model helps with placing objects extreme distances apart (e.g. 1000 km distances between objects).",
    "author": "Dave",
    "version": (0, 1, 0),
    "blender": (2, 80, 0),
    "location": "View 3D -> Tools -> BigSpaceRig",
    "category": "Other",
#    "wiki_url": "https://github.com/DreamSpoon/BigSpaceRig#readme",
}

import bpy
from bpy.props import PointerProperty

from .rig import (OBJ_PROP_FP_POWER, OBJ_PROP_FP_MIN_DIST, OBJ_PROP_FP_MIN_SCALE, OBJ_PROP_BONE_SCL_MULT, OBJ_PROP_BONE_PLACE)
from .rig import (BSR_CreateBigSpaceRig, is_big_space_rig)
from .attach import (BSR_AttachCreatePlace, BSR_AttachSinglePlace, BSR_AttachMultiPlace)
from .geo_nodes import BSR_AddGeoNodes
from .mega_sphere import BSR_MegaSphereCreate

if bpy.app.version < (2,80,0):
    Region = "TOOLS"
else:
    Region = "UI"

class BSR_PT_Rig(bpy.types.Panel):
    bl_label = "Rig"
    bl_space_type = "VIEW_3D"
    bl_region_type = Region
    bl_category = "BigSpaceRig"

    def draw(self, context):
        scn = context.scene
        layout = self.layout
        box = layout.box()
        box.label(text="Create Rig")
        box.operator("big_space_rig.create_big_space_rig")
        box.label(text="New Rig Properties:")
        box.prop(scn, "BSR_NewObserverFP_Power")
        box.prop(scn, "BSR_NewObserverFP_MinDist")
        box.prop(scn, "BSR_NewObserverFP_MinScale")

class BSR_PT_Attach(bpy.types.Panel):
    bl_label = "Attach"
    bl_space_type = "VIEW_3D"
    bl_region_type = Region
    bl_category = "BigSpaceRig"

    def draw(self, context):
        scn = context.scene
        layout = self.layout
        box = layout.box()
        box.label(text="Attach")
        box.operator("big_space_rig.create_proxy_place")
        box.operator("big_space_rig.attach_single_place")
        box.operator("big_space_rig.attach_multi_place")
        box.prop(scn, "BSR_AttachPreCreateRig")
        box.prop(scn, "BSR_AttachNoReParent")
        box.prop(scn, "BSR_UsePlaceScaleFP")

class BSR_PT_GeoNodes(bpy.types.Panel):
    bl_label = "Geometry Nodes"
    bl_space_type = "VIEW_3D"
    bl_region_type = Region
    bl_category = "BigSpaceRig"

    def draw(self, context):
        scn = context.scene
        layout = self.layout
        box = layout.box()
        box.operator("big_space_rig.add_geo_nodes")
        box.prop(scn, "BSR_GeoNodesOverrideCreate")
        box.prop(scn, "BSR_GeoNodesCreateUseAltGroup")
        col = box.column()
        col.active = scn.BSR_GeoNodesCreateUseAltGroup
        col.prop(scn, "BSR_GeoNodesCreateAltGroup")

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
        box.prop(active_ob, '["'+OBJ_PROP_FP_POWER+'"]')
        box.prop(active_ob, '["'+OBJ_PROP_FP_MIN_DIST+'"]')
        box.prop(active_ob, '["'+OBJ_PROP_FP_MIN_SCALE+'"]')

class BSR_PT_MegaSphere(bpy.types.Panel):
    bl_label = "Mega Sphere"
    bl_space_type = "VIEW_3D"
    bl_region_type = Region
    bl_category = "BigSpaceRig"

    def draw(self, context):
        active_ob = context.active_object
        scn = context.scene
        layout = self.layout
        box = layout.box()
        box.label(text="Create")
        col = box.column()
        col.active = is_big_space_rig(active_ob)
        col.operator("big_space_rig.create_mega_sphere")
        col.prop(scn, "BSR_MegaSphereRadius")
        col.prop(scn, "BSR_MegaSphereOverrideCreateNG")
        col.prop(scn, "BSR_MegaSphereUsePlace")
        if col.active:
            subcol = col.column()
            subcol.active = scn.BSR_MegaSphereUsePlace
            subcol.prop(scn, "BSR_MegaSpherePlaceBoneName")

classes = [
    BSR_PT_Rig,
    BSR_PT_Attach,
    BSR_PT_MegaSphere,
    BSR_CreateBigSpaceRig,
    BSR_AttachCreatePlace,
    BSR_AttachMultiPlace,
    BSR_AttachSinglePlace,
    BSR_MegaSphereCreate,
]
# geometry node support is only for Blender v2.9+ (or maybe v3.0+ ...)
# TODO: check what version is needed for current geometry nodes setup
if bpy.app.version >= (2,90,0):
    classes.extend([
        BSR_PT_GeoNodes,
        BSR_AddGeoNodes,
    ])
classes.extend([
    BSR_PT_ActiveRig,
])

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    register_props()

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bts.BSR_MegaSpherePlaceBoneName
    del bts.BSR_MegaSphereUsePlace
    del bts.BSR_MegaSphereOverrideCreateNG
    del bts.BSR_MegaSphereRadius
    del bts.BSR_GeoNodesCreateAltGroup
    del bts.BSR_GeoNodesCreateUseAltGroup
    del bts.BSR_GeoNodesOverrideCreate
    del bts.BSR_UsePlaceScaleFP
    del bts.BSR_AttachNoReParent
    del bts.BSR_AttachPreCreateRig
    del bts.BSR_NewObserverFP_MinScale
    del bts.BSR_NewObserverFP_MinDist
    del bts.BSR_NewObserverFP_Power

def only_geo_node_group_poll(self, object):
    return object.type == 'GEOMETRY'

def bone_items(self, context):
    ob = context.active_object
    if not is_big_space_rig(ob):
        return
    return [(bone.name, bone.name, "") for bone in ob.data.bones if bone.get(OBJ_PROP_BONE_PLACE) == True]

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
        "'forced perspective' effect begins", default=0.0)
    bts.BSR_NewObserverFP_MinScale = bp.FloatProperty(name="FP Min Scale",
        description="Forced Perspective Minimum Scale value, which is the minimum scale to apply with the " +
        "'Forced Perspective' effect", default=0.0)

    bts.BSR_AttachPreCreateRig = bp.BoolProperty(name="Create Rig if Needed", description="Create a new " +
        "Big Space Rig before attaching objects, if no Big Space Rig was active before pressing attach button",
        default=True)
    bts.BSR_AttachNoReParent = bp.BoolProperty(name="Do not Re-Parent", description="Objects that already " +
        "have a parent object will not be 're-parented' to the Big Space Rig. Only the 'root parents', and " +
        "non-parented objects will be attached to Big Space Rig", default=True)
    bts.BSR_UsePlaceScaleFP =  bp.BoolProperty(name="Use Place Scaling", description="Apply a 'forced perspective' " +\
        "scaling effect to places as they move away from the observer - farther away objects 'shrink' to maintain " +\
        "close range to observer. Some accuracy is lost due to greater floating point rounding error", default=False)

    bts.BSR_GeoNodesOverrideCreate = bp.BoolProperty(name="Override Create", description="Big Space Rig Geometry " +
        "Nodes custom node group is re-created when geometry nodes are added to object(s), and any previous custom " +
        "group with the same name is deprecated", default=False)
    bts.BSR_GeoNodesCreateUseAltGroup = bp.BoolProperty(name="Use Alt Group", description="Add Big Space Rig " +
        "Geometry Nodes group to alternate geometry node group (click to unlock)", default=False)
    bts.BSR_GeoNodesCreateAltGroup = bp.PointerProperty(name="Alt Group", description="Alternative Geometry Nodes " +
        "group to receive Big Space Rig new Geometry Nodes", type=bpy.types.NodeTree, poll=only_geo_node_group_poll)

    bts.BSR_MegaSphereRadius = bp.FloatProperty(name="Mega Sphere Radius", description="Radius of sphere, in " + \
        "mega-meters", default=1.0)
    bts.BSR_MegaSphereOverrideCreateNG = bp.BoolProperty(name="Override Create", description="Mega Sphere Geometry " +
        "Nodes custom node group is re-created when Mega Sphere is created, and any previous custom group with the " +
        "same name is deprecated", default=False)
    bts.BSR_MegaSphereUsePlace = bp.BoolProperty(name="Use Place Offset", description="Create MegaSphere centered " + \
        "at given Place in Big Space Rig", default=False)
    bts.BSR_MegaSpherePlaceBoneName = bpy.props.EnumProperty(name="Place", description="Sphere center " + \
        "place bone", items=bone_items)

if __name__ == "__main__":
    register()
