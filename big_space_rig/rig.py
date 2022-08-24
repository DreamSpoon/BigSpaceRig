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
SPACE_BONETAIL = (0, 6.854101911, 0)
PROXY_SPACE_0E_BONEHEAD = (0, 0, 0)
PROXY_SPACE_0E_BONETAIL = (0, 6.854101911, 0)
PROXY_SPACE_6E_BONEHEAD = (0, 0, 0)
PROXY_SPACE_6E_BONETAIL = (0, 6.854101911, 0)
PROXY_OBSERVER_0E_BONEHEAD = (0, 0, 0)
PROXY_OBSERVER_0E_BONETAIL = (0, 0.034441854, 0)
PROXY_OBSERVER_6E_BONEHEAD = (0, 0, 0)
PROXY_OBSERVER_6E_BONETAIL = (0, 0.034441854, 0)
OBSERVER_FOCUS_BONEHEAD = (0, 0, 0)
OBSERVER_FOCUS_BONETAIL = (0, 0.61803399, 0)
PROXY_PLACE_0E_BONEHEAD = (0, 0, 0)
PROXY_PLACE_0E_BONETAIL = (0, 0.090169945, 0)
PROXY_PLACE_6E_BONEHEAD = (0, 0, 0)
PROXY_PLACE_6E_BONETAIL = (0, 0.090169945, 0)
PLACE_BONEHEAD = (0, 0, 0)
PLACE_BONETAIL = (0, 4, 0)

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

TRI_WIDGET_NAME = "WidgetTriangle"
TRI_PINCH_WIDGET_NAME = "WidgetPinchTriangle"
QUAD_WIDGET_NAME = "WidgetQuad"
PINCH_QUAD_WIDGET_NAME = "WidgetPinchQuad"
CIRCLE_WIDGET_NAME = "WidgetCircle"

WIDGET_CIRCLE_VERT_COUNT = 32

# returns False if 'ob' is not a Big Space Rig, otherwise returns True
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

def create_bsr_widgets(context):
    # if v2.79
    if bpy.app.version < (2,80,0):
        tri_obj = create_widget_triangle()
        tri_pinch_obj = create_widget_pinch_triangle()
        quad_obj = create_widget_square()
        pinch_quad_obj = create_widget_pinch_square()
        circle_obj = create_widget_circle()

        # widgets are only in final layer
        tri_obj.layers[19] = True
        tri_pinch_obj.layers[19] = True
        quad_obj.layers[19] = True
        pinch_quad_obj.layers[19] = True
        circle_obj.layers[19] = True
        for i in range(19):
            tri_obj.layers[i] = False
            tri_pinch_obj.layers[i] = False
            quad_obj.layers[i] = False
            pinch_quad_obj.layers[i] = False
            circle_obj.layers[i] = False
    # else v2.8 or later
    else:
        new_collection = bpy.data.collections.new("BigSpaceRigHidden")
        new_collection.hide_render = True
        # link new collection to currently active collection
        context.view_layer.active_layer_collection.collection.children.link(new_collection)
        collection_hide_in_viewport(context, new_collection.name)

        # widgets are in Big Space Rig Hidden collection
        tri_obj = create_widget_triangle(collection_name=new_collection.name)
        tri_pinch_obj = create_widget_pinch_triangle(collection_name=new_collection.name)
        quad_obj = create_widget_square(collection_name=new_collection.name)
        pinch_quad_obj = create_widget_pinch_square(collection_name=new_collection.name)
        circle_obj = create_widget_circle(collection_name=new_collection.name)

    widget_ob_dict = { TRI_WIDGET_NAME : tri_obj,
                      TRI_PINCH_WIDGET_NAME : tri_pinch_obj,
                      QUAD_WIDGET_NAME : quad_obj,
                      PINCH_QUAD_WIDGET_NAME : pinch_quad_obj,
                      CIRCLE_WIDGET_NAME: circle_obj,
                     }
    return widget_ob_dict

def get_widget_objs_from_rig(active_ob):
    widget_objs = {}
    for ob in bpy.data.objects:
        if ob.parent == active_ob or (ob.parent != None and ob.parent.parent == active_ob):
            if WIDGET_TRIANGLE_OBJNAME in ob.name:
                widget_objs[TRI_WIDGET_NAME] = ob
            elif WIDGET_PINCH_TRIANGLE_OBJNAME in ob.name:
                widget_objs[TRI_PINCH_WIDGET_NAME] = ob
            elif WIDGET_QUAD_OBJNAME in ob.name:
                widget_objs[QUAD_WIDGET_NAME] = ob
            elif WIDGET_PINCH_QUAD_OBJNAME in ob.name:
                widget_objs[PINCH_QUAD_WIDGET_NAME] = ob
            elif WIDGET_CIRCLE_OBJNAME in ob.name:
                widget_objs[CIRCLE_WIDGET_NAME] = ob
    return widget_objs

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
    b_proxy_space_0e.head = mathutils.Vector(PROXY_SPACE_0E_BONEHEAD)
    b_proxy_space_0e.tail = mathutils.Vector(PROXY_SPACE_0E_BONETAIL)
    b_proxy_space_0e.show_wire = True
    b_proxy_space_0e.layers = PROXY_SPACE_0E_BONELAYERS

    b_proxy_space_6e = new_rig.data.edit_bones.new(name=PROXY_SPACE_6E_BNAME)
    bname_proxy_space_6e = b_proxy_space_6e.name
    b_proxy_space_6e.head = mathutils.Vector(PROXY_SPACE_6E_BONEHEAD)
    b_proxy_space_6e.tail = mathutils.Vector(PROXY_SPACE_6E_BONETAIL)
    b_proxy_space_6e.show_wire = True
    b_proxy_space_6e.layers = PROXY_SPACE_6E_BONELAYERS

    b_proxy_observer_0e = new_rig.data.edit_bones.new(name=PROXY_OBSERVER_0E_BNAME)
    bname_proxy_obs_0e = b_proxy_observer_0e.name
    # set bone data
    b_proxy_observer_0e.head = mathutils.Vector(PROXY_OBSERVER_0E_BONEHEAD)
    b_proxy_observer_0e.tail = mathutils.Vector(PROXY_OBSERVER_0E_BONETAIL)
    b_proxy_observer_0e.parent = b_proxy_space_0e
    b_proxy_observer_0e.show_wire = True
    b_proxy_observer_0e.layers = PROXY_OBSERVER_0E_BONELAYERS

    b_proxy_observer_6e = new_rig.data.edit_bones.new(name=PROXY_OBSERVER_6E_BNAME)
    bname_proxy_obs_6e = b_proxy_observer_6e.name
    # set bone data
    b_proxy_observer_6e.head = mathutils.Vector(PROXY_OBSERVER_6E_BONEHEAD)
    b_proxy_observer_6e.tail = mathutils.Vector(PROXY_OBSERVER_6E_BONETAIL)
    b_proxy_observer_6e.parent = b_proxy_space_6e
    b_proxy_observer_6e.show_wire = True
    b_proxy_observer_6e.layers = PROXY_OBSERVER_6E_BONELAYERS

    b_observer_focus = new_rig.data.edit_bones.new(name=OBSERVER_FOCUS_BNAME)
    bname_observer_focus = b_observer_focus.name
    b_observer_focus.head = mathutils.Vector(OBSERVER_FOCUS_BONEHEAD)
    b_observer_focus.tail = mathutils.Vector(OBSERVER_FOCUS_BONETAIL)
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

    # parent widgets to new rig, first widget is "main parent" widget to other widgets
    if len(widget_objs) > 0:
        main_parent = None
        for w in widget_objs.values():
            if main_parent is None:
                # parent first widget to rig
                main_parent = w
                main_parent.parent = new_rig
                continue
            # parent remaining widgets to first widget
            w.parent = main_parent

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
