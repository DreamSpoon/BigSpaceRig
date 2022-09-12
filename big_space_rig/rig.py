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
import math
import mathutils
from mathutils import Vector

if bpy.app.version < (2,80,0):
    from .imp_v27 import (create_mesh_obj_from_pydata, get_cursor_location)
    from rna_prop_ui import rna_idprop_ui_prop_get
else:
    from .imp_v28 import (create_mesh_obj_from_pydata, get_cursor_location)

RIG_BASENAME = "BigSpaceRig"
PROXY_SPACE_0E_BNAME = "ProxySpace0e"
PROXY_SPACE_6E_BNAME = "ProxySpace6e"
PROXY_OBSERVER_0E_BNAME = "ProxyObserver0e"
PROXY_OBSERVER_6E_BNAME = "ProxyObserver6e"
OBSERVER_FOCUS_BNAME = "ObserverFocus"
PROXY_PLACE_0E_BNAME = "ProxyPlace0e"
PROXY_PLACE_6E_BNAME = "ProxyPlace6e"
PLACE_BNAME = "Place"

OBJ_PROP_FP_POWER = "big_space_rig_fp_power"
OBJ_PROP_FP_MIN_DIST = "big_space_rig_fp_min_dist"
OBJ_PROP_FP_MIN_SCALE = "big_space_rig_fp_min_scale"
OBJ_PROP_BONE_SCL_MULT = "big_space_rig_bone_scl_mult"
OBJ_PROP_BONE_PLACE = "place_bone"

SPACE_BONEHEAD = (0, 0, 0)
SPACE_BONETAIL = (0, 10.0, 0)
PROXY_SPACE_0E_BONEHEAD = (0, 0, 0)
PROXY_SPACE_0E_BONETAIL = (0, 10.0, 0)
PROXY_SPACE_6E_BONEHEAD = (0, 0, 0)
PROXY_SPACE_6E_BONETAIL = (0, 20.0, 0)
PROXY_OBSERVER_0E_BONEHEAD = (0, 0, 0)
PROXY_OBSERVER_0E_BONETAIL = (0, 0.5, 0)
PROXY_OBSERVER_6E_BONEHEAD = (0, 0, 0)
PROXY_OBSERVER_6E_BONETAIL = (0, 2.0, 0)
OBSERVER_FOCUS_BONEHEAD = (0, 0, 0)
OBSERVER_FOCUS_BONETAIL = (0, 1.0, 0)
PROXY_PLACE_0E_BONEHEAD = (0, 0, 0)
PROXY_PLACE_0E_BONETAIL = (0, 1.0, 0)
PROXY_PLACE_6E_BONEHEAD = (0, 0, 0)
PROXY_PLACE_6E_BONETAIL = (0, 0.1, 0)
PLACE_BONEHEAD = (0, 0, 0)
PLACE_BONETAIL = (0, 5.0, 0)

SPACE_BONELAYERS = [(x==0) for x in range(32)]
PROXY_SPACE_0E_BONELAYERS = [(x==0) for x in range(32)]
PROXY_SPACE_6E_BONELAYERS = [(x==0) for x in range(32)]
PROXY_OBSERVER_0E_BONELAYERS = [(x==1) for x in range(32)]
PROXY_OBSERVER_6E_BONELAYERS = [(x==2) for x in range(32)]
PROXY_PLACE_0E_BONELAYERS = PROXY_OBSERVER_0E_BONELAYERS
PROXY_PLACE_6E_BONELAYERS = PROXY_OBSERVER_6E_BONELAYERS
OBSERVER_FOCUS_BONELAYERS = [(x==17) for x in range(32)]
PLACE_BONELAYERS = [(x==18) for x in range(32)]

RIG_BONEVIS_LAYERS = [(x in [0, 1, 2, 17, 18]) for x in range(32)]

WIDGET_TRIANGLE_OBJNAME = "WGT_Tri"
WIDGET_PINCH_TRIANGLE_OBJNAME = "WGT_PinchTri"
WIDGET_QUAD_OBJNAME = "WGT_Quad"
WIDGET_PINCH_QUAD_OBJNAME = "WGT_PinchQuad"
WIDGET_CIRCLE_OBJNAME = "WGT_Circle"
WIDGET_ICOSPHERE7_OBJNAME = "WGT_Icosphere7"

TRI_WIDGET_NAME = "WidgetTriangle"
TRI_PINCH_WIDGET_NAME = "WidgetPinchTriangle"
QUAD_WIDGET_NAME = "WidgetQuad"
PINCH_QUAD_WIDGET_NAME = "WidgetPinchQuad"
CIRCLE_WIDGET_NAME = "WidgetCircle"
ICOSPHERE7_WIDGET_NAME = "WidgetIcosphere7"

WIDGET_CIRCLE_VERT_COUNT = 32

BSRH_COLLECTION_NAME = "BigSpaceRigHidden"

PROXY_PLACE_0E_VAR_NAME_PREPEND = "proxy_place_0e"
PROXY_PLACE_6E_VAR_NAME_PREPEND = "proxy_place_6e"

def bone_name_from_datapath(datapath_str):
    left = datapath_str.find("\"")
    right = datapath_str.rfind("\"")
    return datapath_str[left+1:right]

def get_6e_0e_from_place_bone_name(big_space_rig, place_bone_name):
    if big_space_rig.animation_data is None:
        return None, None
    proxy_place_bone_name_6e = None
    proxy_place_bone_name_0e = None
    # search all drivers of Big Space Rig object, looking for named variables with bone targets - place proxies
    for drv in big_space_rig.animation_data.drivers:
        if bone_name_from_datapath(drv.data_path) != place_bone_name:
            continue
        d = drv.driver
        for v in d.variables:
            if v.name.startswith(PROXY_PLACE_6E_VAR_NAME_PREPEND):
                proxy_place_bone_name_6e = v.targets[0].bone_target
            elif v.name.startswith(PROXY_PLACE_0E_VAR_NAME_PREPEND):
                proxy_place_bone_name_0e = v.targets[0].bone_target
    return proxy_place_bone_name_6e, proxy_place_bone_name_0e

# returns False if 'armature' is not a Big Space Rig, otherwise returns True
# TODO: enhance the check - e.g. if bones are renamed, then how to check? rig/bones w/ custom props?
def is_big_space_rig(ob):
    if ob is None or not hasattr(ob, 'type') or ob.type != 'ARMATURE' or \
            ob.data.bones.get(PROXY_SPACE_0E_BNAME) is None or ob.data.bones.get(PROXY_OBSERVER_0E_BNAME) is None or \
            ob.data.bones.get(PROXY_SPACE_6E_BNAME) is None or ob.data.bones.get(PROXY_OBSERVER_6E_BNAME) is None:
        return False
    return True

# if a Big Space Rig is found in the parent-hierarchy of ob, then return the rig and the associated 'Place' bone,
# otherwise return None
def get_parent_big_space_rig(ob):
    if ob.parent is None:
        return None, None
    if is_big_space_rig(ob.parent):
        return ob.parent, ob.parent_bone
    # recursively search parent(s) for Big Space Rig
    return get_parent_big_space_rig(ob.parent)

def get_collection_by_name(root_collection, collection_name):
    if root_collection.name == collection_name:
        return root_collection

    for c in root_collection.children:
        coll = get_collection_by_name(c, collection_name)
        if coll != None:
            return coll

def collection_hide_in_viewport(context, collection_name):
    for v_layer in context.scene.view_layers:
        coll = get_collection_by_name(v_layer.layer_collection, collection_name)
        if coll is None:
            continue
        coll.hide_viewport = True

def create_widget_triangle(collection_name=None):
    verts = [(math.sin(math.radians(deg)), math.cos(math.radians(deg)), 0) for deg in [0, 120, 240]]
    edges = [ ( x, (x+1)*(x+1!=len(verts)) ) for x in range(len(verts)) ]
    if collection_name is None:
        return create_mesh_obj_from_pydata(verts, edges=edges, obj_name=WIDGET_TRIANGLE_OBJNAME)
    else:
        return create_mesh_obj_from_pydata(verts, edges=edges, obj_name=WIDGET_TRIANGLE_OBJNAME,
                                           collection_name=collection_name)

def create_widget_pinch_triangle(collection_name=None):
    verts = [(r * math.sin(math.radians(deg)), r * math.cos(math.radians(deg)), 0) for (deg, r) in
             [(0, 1), (60, 0.35), (120, 1), (180, 0.35), (240, 1), (300, 0.35)]]
    edges = [ ( x, (x+1)*(x+1!=len(verts)) ) for x in range(len(verts)) ]
    if collection_name is None:
        return create_mesh_obj_from_pydata(verts, edges=edges, obj_name=WIDGET_PINCH_TRIANGLE_OBJNAME)
    else:
        return create_mesh_obj_from_pydata(verts, edges=edges, obj_name=WIDGET_PINCH_TRIANGLE_OBJNAME,
                                           collection_name=collection_name)

def create_widget_square(collection_name=None):
    verts = [(-0.5, -0.5, 0),
             (0.5, -0.5, 0),
             (0.5, 0.5, 0),
             (-0.5, 0.5, 0), ]
    edges = [ ( x, (x+1)*(x+1!=len(verts)) ) for x in range(len(verts)) ]
    if collection_name is None:
        return create_mesh_obj_from_pydata(verts, edges=edges, obj_name=WIDGET_QUAD_OBJNAME)
    else:
        return create_mesh_obj_from_pydata(verts, edges=edges, obj_name=WIDGET_QUAD_OBJNAME,
                                           collection_name=collection_name)

def create_widget_pinch_square(collection_name=None):
    verts = [(-0.5, -0.5, 0),
             (0.0, -0.4, 0),
             (0.5, -0.5, 0),
             (0.4, 0.0, 0),
             (0.5, 0.5, 0),
             (0.0, 0.4, 0),
             (-0.5, 0.5, 0),
             (-0.4, 0.0, 0),]
    edges = [ ( x, (x+1)*(x+1!=len(verts)) ) for x in range(len(verts)) ]
    if collection_name is None:
        return create_mesh_obj_from_pydata(verts, edges=edges, obj_name=WIDGET_PINCH_QUAD_OBJNAME)
    else:
        return create_mesh_obj_from_pydata(verts, edges=edges, obj_name=WIDGET_PINCH_QUAD_OBJNAME,
                                           collection_name=collection_name)

def create_widget_circle(collection_name=None):
    verts = [(math.sin(rads), math.cos(rads), 0) for rads in \
             [index/WIDGET_CIRCLE_VERT_COUNT*2*math.pi for index in range(WIDGET_CIRCLE_VERT_COUNT)]]
    edges = [ ( x, (x+1)*(x+1!=len(verts)) ) for x in range(len(verts)) ]
    if collection_name is None:
        return create_mesh_obj_from_pydata(verts, edges=edges, obj_name=WIDGET_CIRCLE_OBJNAME)
    else:
        return create_mesh_obj_from_pydata(verts, edges=edges, obj_name=WIDGET_CIRCLE_OBJNAME,
                                           collection_name=collection_name)

def set_widget_view_layer(wgt_obj):
    # widgets are only in final layer
    wgt_obj.layers[19] = True
    for i in range(19):
        wgt_obj.layers[i] = False

def create_bsr_widgets(context):
    # if v2.79
    if bpy.app.version < (2,80,0):
        tri_obj = create_widget_triangle()
        tri_pinch_obj = create_widget_pinch_triangle()
        quad_obj = create_widget_square()
        pinch_quad_obj = create_widget_pinch_square()
        circle_obj = create_widget_circle()

        set_widget_view_layer(tri_obj)
        set_widget_view_layer(tri_pinch_obj)
        set_widget_view_layer(quad_obj)
        set_widget_view_layer(pinch_quad_obj)
        set_widget_view_layer(circle_obj)
    # else v2.8 or later
    else:
        bsrh_collection = bpy.data.collections.get(BSRH_COLLECTION_NAME)
        if bsrh_collection is None:
            bsrh_collection = bpy.data.collections.new(BSRH_COLLECTION_NAME)
            # link new collection to currently active collection
            context.view_layer.active_layer_collection.collection.children.link(bsrh_collection)
        # ensure collection is hidden, render and viewport
        bsrh_collection.hide_render = True
        collection_hide_in_viewport(context, bsrh_collection.name)

        # widgets are in Big Space Rig Hidden collection
        tri_obj = create_widget_triangle(collection_name=bsrh_collection.name)
        tri_pinch_obj = create_widget_pinch_triangle(collection_name=bsrh_collection.name)
        quad_obj = create_widget_square(collection_name=bsrh_collection.name)
        pinch_quad_obj = create_widget_pinch_square(collection_name=bsrh_collection.name)
        circle_obj = create_widget_circle(collection_name=bsrh_collection.name)

    widget_ob_dict = { TRI_WIDGET_NAME : tri_obj,
                      TRI_PINCH_WIDGET_NAME : tri_pinch_obj,
                      QUAD_WIDGET_NAME : quad_obj,
                      PINCH_QUAD_WIDGET_NAME : pinch_quad_obj,
                      CIRCLE_WIDGET_NAME: circle_obj,
                     }
    return widget_ob_dict

def get_widget_objs_from_rig(big_space_rig):
    widget_objs = {}
    for armature in bpy.data.objects:
        if armature.parent == big_space_rig or (armature.parent != None and armature.parent.parent == big_space_rig):
            if WIDGET_TRIANGLE_OBJNAME in armature.name:
                widget_objs[TRI_WIDGET_NAME] = armature
            elif WIDGET_PINCH_TRIANGLE_OBJNAME in armature.name:
                widget_objs[TRI_PINCH_WIDGET_NAME] = armature
            elif WIDGET_QUAD_OBJNAME in armature.name:
                widget_objs[QUAD_WIDGET_NAME] = armature
            elif WIDGET_PINCH_QUAD_OBJNAME in armature.name:
                widget_objs[PINCH_QUAD_WIDGET_NAME] = armature
            elif WIDGET_CIRCLE_OBJNAME in armature.name:
                widget_objs[CIRCLE_WIDGET_NAME] = armature
            elif WIDGET_ICOSPHERE7_OBJNAME in armature.name:
                widget_objs[ICOSPHERE7_WIDGET_NAME] = armature
    return widget_objs

def add_widgets_to_big_space_rig(big_space_rig, new_wgt_list):
    old_wgt_list = get_widget_objs_from_rig(big_space_rig)
    #if any widget(s) already parented to Big Space Rig, ...
    if len(old_wgt_list) > 0:
        # then parent new widgets to the old widget that is directly pareted to Big Space Rig
        for old_wgt in old_wgt_list.values():
            if old_wgt.parent == big_space_rig:
                # parent new widgets to old widget, where old widget is parented directly to Big Space Rig
                for new_wgt in new_wgt_list:
                    new_wgt.parent = old_wgt
    # no widget(s) parented to rig, so parent first widget directly to rig, and parent remaining widgets to first
    else:
        first_wgt = None
        for new_wgt in new_wgt_list:
            if first_wgt is None:
                first_wgt = new_wgt
                first_wgt.parent = big_space_rig
            else:
                new_wgt.parent = first_wgt

    # if v2.79
    if bpy.app.version < (2,80,0):
            for new_wgt in new_wgt_list:
                set_widget_view_layer(new_wgt)
    # else v2.8 or later
    else:
        bsrh_collection = bpy.data.collections.get(BSRH_COLLECTION_NAME)
        if bsrh_collection != None:
            for new_wgt in new_wgt_list:
                # do not link object if it is already in BSR Hidden collection
                if bsrh_collection.objects.get(new_wgt.name):
                    continue
                # remove object from all collections
                for coll in bpy.data.collections:
                    if coll.objects.get(new_wgt.name) != None:
                        coll.objects.unlink(new_wgt)
                # add the BSR Hidden collection
                bsrh_collection.objects.link(new_wgt)

# TODO: delete Notes and redo
# Notes:
#     - 'Field' is the Big Space Rig itself, 'ProxySpace' is intended to be like a 'TV remote controller',
#       easy to pick up and move around in the scene, without modifying the positions of objects in the rig
#     - 'ProxySpace' is a Scaled Remote Controller for an Actual World of objects
def create_bsr_armature(context, bsr_fp_power, bsr_fp_min_dist, bsr_fp_min_scale):
    widget_objs = create_bsr_widgets(context)

    old_3dview_mode = context.mode

    # create Big Space Rig and enter EDIT mode
    bpy.ops.object.armature_add(enter_editmode=True, location=(0, 0, 0))
    new_rig = context.active_object
    # the new_rig represents the "actual space", the ProxySpace bone represents the "scaled space"
    new_rig.name = RIG_BASENAME
    new_rig[OBJ_PROP_FP_POWER] = bsr_fp_power
    new_rig[OBJ_PROP_FP_MIN_DIST] = bsr_fp_min_dist
    new_rig[OBJ_PROP_FP_MIN_SCALE] = bsr_fp_min_scale
    # set min values for the custom props
    if bpy.app.version < (2,80,0):
        ui = rna_idprop_ui_prop_get(new_rig, OBJ_PROP_FP_POWER)
        ui['description'] = "Forced Perspective Distance Power"
        ui['default'] = 0.5
        ui['min'] = ui['soft_min'] = -2e38
        ui['max'] = ui['soft_max'] = 2e38
        ui = rna_idprop_ui_prop_get(new_rig, OBJ_PROP_FP_MIN_DIST)
        ui['description'] = "Forced Perspective Minimum Distance"
        ui['default'] = 0.0
        ui['min'] = ui['soft_min'] = 0.0
        ui['max'] = ui['soft_max'] = 2e38
        ui = rna_idprop_ui_prop_get(new_rig, OBJ_PROP_FP_MIN_SCALE)
        ui['description'] = "Forced Perspective Minimum Scale"
        ui['default'] = 0.0
        ui['min'] = ui['soft_min'] = 0.0
        ui['max'] = ui['soft_max'] = 2e38
    else:
        ui_data = new_rig.id_properties_ui(OBJ_PROP_FP_POWER)
        ui_data.update(description="Forced Perspective Distance Power")
        ui_data.update(default=0.5)
        ui_data = new_rig.id_properties_ui(OBJ_PROP_FP_MIN_DIST)
        ui_data.update(description="Forced Perspective Minimum Distance")
        ui_data.update(default=0.0)
        ui_data.update(min=0.0)
        ui_data = new_rig.id_properties_ui(OBJ_PROP_FP_MIN_SCALE)
        ui_data.update(description="Forced Perspective Minimum Scale")
        ui_data.update(default=0.0)
        ui_data.update(min=0.0)

    # ensure rig will display custom bone shapes
    new_rig.data.show_bone_custom_shapes = True

    # modify default bone to make ProxySpace bone, to hold proxies for observer(s) and actual place(s)
    b_proxy_space_0e = new_rig.data.edit_bones[0]
    b_proxy_space_0e.name = PROXY_SPACE_0E_BNAME
    # save bone name for later use (in Pose bones mode, where the edit bones name may not be usable - will cause error)
    bname_proxy_space_0e = b_proxy_space_0e.name
    b_proxy_space_0e.head = Vector(PROXY_SPACE_0E_BONEHEAD)
    b_proxy_space_0e.tail = Vector(PROXY_SPACE_0E_BONETAIL)
    b_proxy_space_0e.show_wire = True
    b_proxy_space_0e.layers = PROXY_SPACE_0E_BONELAYERS

    b_proxy_space_6e = new_rig.data.edit_bones.new(name=PROXY_SPACE_6E_BNAME)
    bname_proxy_space_6e = b_proxy_space_6e.name
    b_proxy_space_6e.head = Vector(PROXY_SPACE_6E_BONEHEAD)
    b_proxy_space_6e.tail = Vector(PROXY_SPACE_6E_BONETAIL)
    b_proxy_space_6e.show_wire = True
    b_proxy_space_6e.layers = PROXY_SPACE_6E_BONELAYERS

    b_proxy_observer_0e = new_rig.data.edit_bones.new(name=PROXY_OBSERVER_0E_BNAME)
    bname_proxy_obs_0e = b_proxy_observer_0e.name
    # set bone data
    b_proxy_observer_0e.head = Vector(PROXY_OBSERVER_0E_BONEHEAD)
    b_proxy_observer_0e.tail = Vector(PROXY_OBSERVER_0E_BONETAIL)
    b_proxy_observer_0e.parent = b_proxy_space_0e
    b_proxy_observer_0e.show_wire = True
    b_proxy_observer_0e.layers = PROXY_OBSERVER_0E_BONELAYERS

    b_proxy_observer_6e = new_rig.data.edit_bones.new(name=PROXY_OBSERVER_6E_BNAME)
    bname_proxy_obs_6e = b_proxy_observer_6e.name
    # set bone data
    b_proxy_observer_6e.head = Vector(PROXY_OBSERVER_6E_BONEHEAD)
    b_proxy_observer_6e.tail = Vector(PROXY_OBSERVER_6E_BONETAIL)
    b_proxy_observer_6e.parent = b_proxy_space_6e
    b_proxy_observer_6e.show_wire = True
    b_proxy_observer_6e.layers = PROXY_OBSERVER_6E_BONELAYERS

    b_observer_focus = new_rig.data.edit_bones.new(name=OBSERVER_FOCUS_BNAME)
    bname_observer_focus = b_observer_focus.name
    b_observer_focus.head = Vector(OBSERVER_FOCUS_BONEHEAD)
    b_observer_focus.tail = Vector(OBSERVER_FOCUS_BONETAIL)
    b_observer_focus.show_wire = True
    b_observer_focus.layers = OBSERVER_FOCUS_BONELAYERS

    # enter Pose mode to allow adding custom shapes
    bpy.ops.object.mode_set(mode='POSE')
    # apply custom bone shapes
    new_rig.pose.bones[bname_proxy_obs_0e].custom_shape = bpy.data.objects[widget_objs[TRI_PINCH_WIDGET_NAME].name]
    new_rig.pose.bones[bname_proxy_obs_6e].custom_shape = bpy.data.objects[widget_objs[TRI_PINCH_WIDGET_NAME].name]
    new_rig.pose.bones[bname_observer_focus].custom_shape = bpy.data.objects[widget_objs[TRI_WIDGET_NAME].name]
    new_rig.pose.bones[bname_proxy_space_0e].custom_shape = bpy.data.objects[widget_objs[CIRCLE_WIDGET_NAME].name]
    new_rig.pose.bones[bname_proxy_space_6e].custom_shape = bpy.data.objects[widget_objs[CIRCLE_WIDGET_NAME].name]
    # return to old view mode
    bpy.ops.object.mode_set(mode=old_3dview_mode)

    add_widgets_to_big_space_rig(new_rig, widget_objs.values())

    new_rig.data.layers = RIG_BONEVIS_LAYERS

    # move rig to cursor location
    new_rig.location = get_cursor_location(context)

    return new_rig

class BSR_CreateBigSpaceRig(bpy.types.Operator):
    bl_description = "Create a Big Space Rig, for 'condensed space' - e.g. Solar system simulations, " + \
        "outer-space-to-Earth-surface zoom. Rig will be created with New Rig Properties"
    bl_idname = "big_space_rig.create_big_space_rig"
    bl_label = "Create Big Space Rig"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scn = context.scene
        create_bsr_armature(context, scn.BSR_NewObserverFP_Power, scn.BSR_NewObserverFP_MinDist,
                                  scn.BSR_NewObserverFP_MinScale)
        return {'FINISHED'}

def quick_select_armature_bone(armature, bone_name):
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.select_all(action='DESELECT')
    armature.data.bones[bone_name].select = True
    armature.data.bones.active = armature.data.bones[bone_name]

class BSR_QuickSelectObserver6e(bpy.types.Operator):
    bl_description = "Switch to Pose mode and select the Observer 6e bone for movement at mega-scale (x1,000,000)"
    bl_idname = "big_space_rig.quick_select_observer_6e"
    bl_label = "Observer 6e"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        big_space_rig = context.active_object
        if not is_big_space_rig(big_space_rig):
            self.report({'ERROR'}, "Unable to Quick Select Observer 6e because active object is not a Big Space Rig")
            return {'CANCELLED'}
        quick_select_armature_bone(big_space_rig, PROXY_OBSERVER_6E_BNAME)
        return {'FINISHED'}

class BSR_QuickSelectObserver0e(bpy.types.Operator):
    bl_description = "Switch to Pose mode and select the Observer 0e bone for movement at regular scale (x1)"
    bl_idname = "big_space_rig.quick_select_observer_0e"
    bl_label = "Observer 0e"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        big_space_rig = context.active_object
        if not is_big_space_rig(big_space_rig):
            self.report({'ERROR'}, "Unable to Quick Select Observer 0e because active object is not a Big Space Rig")
            return {'CANCELLED'}
        quick_select_armature_bone(big_space_rig, PROXY_OBSERVER_0E_BNAME)
        return {'FINISHED'}

class BSR_QuickSelectObserverFocus(bpy.types.Operator):
    bl_description = "Switch to Pose mode and select the Observer Focus bone for movement within Forced " \
        "Perspective place (e.g. parent this bone to the Scene's Camera when Forced Perspective is used)"
    bl_idname = "big_space_rig.quick_select_observer_focus"
    bl_label = "Observer Focus"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        big_space_rig = context.active_object
        if not is_big_space_rig(big_space_rig):
            self.report({'ERROR'}, "Unable to Quick Select Observer Focus because active object is not a Big Space Rig")
            return {'CANCELLED'}
        quick_select_armature_bone(big_space_rig, OBSERVER_FOCUS_BNAME)
        return {'FINISHED'}

class BSR_QuickSelectPlace6e(bpy.types.Operator):
    bl_description = "Switch to Pose mode and select the Place 6e bone for movement at mega-scale (x1,000,000)"
    bl_idname = "big_space_rig.quick_select_place_6e"
    bl_label = "Place 6e"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scn = context.scene
        big_space_rig = context.active_object
        if not is_big_space_rig(big_space_rig):
            self.report({'ERROR'}, "Unable to Quick Select Place 6e because active object is not a Big Space Rig")
            return {'CANCELLED'}
        place_bone_name = scn.BSR_QuickSelectPlaceBoneName[1:len(scn.BSR_QuickSelectPlaceBoneName)]
        if place_bone_name == "":
            self.report({'ERROR'}, "Unable to Quick Select Place 6e because Place is blank")
            return {'CANCELLED'}
        place_bone_name_6e, place_bone_name_0e = get_6e_0e_from_place_bone_name(big_space_rig, place_bone_name)
        quick_select_armature_bone(big_space_rig, place_bone_name_6e)
        return {'FINISHED'}

class BSR_QuickSelectPlace0e(bpy.types.Operator):
    bl_description = "Switch to Pose mode and select the Place 0e bone for movement at regular scale (x1)"
    bl_idname = "big_space_rig.quick_select_place_0e"
    bl_label = "Place 0e"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scn = context.scene
        big_space_rig = context.active_object
        if not is_big_space_rig(big_space_rig):
            self.report({'ERROR'}, "Unable to Quick Select Place 0e because active object is not a Big Space Rig")
            return {'CANCELLED'}
        place_bone_name = scn.BSR_QuickSelectPlaceBoneName[1:len(scn.BSR_QuickSelectPlaceBoneName)]
        if place_bone_name == "":
            self.report({'ERROR'}, "Unable to Quick Select Place 0e because Place is blank")
            return {'CANCELLED'}
        place_bone_name_6e, place_bone_name_0e = get_6e_0e_from_place_bone_name(big_space_rig, place_bone_name)
        quick_select_armature_bone(big_space_rig, place_bone_name_0e)
        return {'FINISHED'}

class BSR_QuickSelectPlaceProxy(bpy.types.Operator):
    bl_description = "Switch to Pose mode and select the Place Proxy bone"
    bl_idname = "big_space_rig.quick_select_place_proxy"
    bl_label = "Place Proxy"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scn = context.scene
        big_space_rig = context.active_object
        if not is_big_space_rig(big_space_rig):
            self.report({'ERROR'}, "Unable to Quick Select Place Proxy because active object is not a Big Space Rig")
            return {'CANCELLED'}
        place_bone_name = scn.BSR_QuickSelectPlaceBoneName[1:len(scn.BSR_QuickSelectPlaceBoneName)]
        if place_bone_name == "":
            self.report({'ERROR'}, "Unable to Quick Select Place Proxy because Place is blank")
            return {'CANCELLED'}
        quick_select_armature_bone(big_space_rig, place_bone_name)
        return {'FINISHED'}
