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
import mathutils

from .rig import (PROXY_SPACE_0E_BNAME, PROXY_SPACE_6E_BNAME, OBSERVER_FOCUS_BNAME, PROXY_OBSERVER_0E_BNAME,
    PROXY_OBSERVER_6E_BNAME, PLACE_BNAME, PROXY_PLACE_0E_BNAME, PROXY_PLACE_6E_BNAME, PLACE_BONEHEAD, PLACE_BONETAIL,
    PROXY_PLACE_0E_BONEHEAD, PROXY_PLACE_6E_BONEHEAD, PROXY_PLACE_0E_BONETAIL, PROXY_PLACE_6E_BONETAIL,
    PLACE_BONELAYERS, PROXY_PLACE_0E_BONELAYERS, PROXY_PLACE_6E_BONELAYERS)
from .rig import (TRI_WIDGET_NAME, TRI_PINCH_WIDGET_NAME, QUAD_WIDGET_NAME, PINCH_QUAD_WIDGET_NAME, CIRCLE_WIDGET_NAME,
    WIDGET_TRIANGLE_OBJNAME, WIDGET_PINCH_TRIANGLE_OBJNAME, WIDGET_QUAD_OBJNAME,
    WIDGET_PINCH_QUAD_OBJNAME, WIDGET_CIRCLE_OBJNAME)
from .rig import (OBJ_PROP_BONE_SCL_MULT, OBJ_PROP_FP_POWER, OBJ_PROP_FP_MIN_DIST, OBJ_PROP_FP_MIN_SCALE, OBJ_PROP_BONE_PLACE)
from .rig import (create_bsr_armature, is_big_space_rig, get_widget_objs_from_rig)

if bpy.app.version < (2,80,0):
    from .imp_v27 import (select_object, get_cursor_location)
else:
    from .imp_v28 import (select_object, get_cursor_location)

PROXY_PLACE_0E_VAR_NAME_PREPEND = "proxy_place_0e"
PROXY_PLACE_6E_VAR_NAME_PREPEND = "proxy_place_6e"

# "edit bones" must be created at origin (head at origin, ...), so that pose bone locations can be used by drivers
# to perform offsets, distance calculations, etc.
def create_proxy_place(context, big_space_rig, widget_objs, use_obs_loc=False, place_loc=None, use_fp_scale=False):
    # save old view3d mode and enter Edit mode, to add bones to big_space_rig
    old_3dview_mode = context.mode

    bpy.ops.object.mode_set(mode='EDIT')

    b_place = big_space_rig.data.edit_bones.new(name=PLACE_BNAME)
    place_bname = b_place.name
    b_place.head = mathutils.Vector(PLACE_BONEHEAD)
    b_place.tail = mathutils.Vector(PLACE_BONETAIL)
    b_place.parent = big_space_rig.data.edit_bones[OBSERVER_FOCUS_BNAME]
    b_place.show_wire = True
    b_place.layers = PLACE_BONELAYERS
    # mark this bone as a Place with a custom object property
    b_place[OBJ_PROP_BONE_PLACE] = True

    b_proxy_place_0e = big_space_rig.data.edit_bones.new(name=PROXY_PLACE_0E_BNAME)
    proxy_place_0e_bname = b_proxy_place_0e.name
    b_proxy_place_0e.head = mathutils.Vector(PROXY_PLACE_0E_BONEHEAD)
    b_proxy_place_0e.tail = mathutils.Vector(PROXY_PLACE_0E_BONETAIL)
    b_proxy_place_0e.parent = big_space_rig.data.edit_bones[PROXY_SPACE_0E_BNAME]
    b_proxy_place_0e.show_wire = True
    b_proxy_place_0e.layers = PROXY_PLACE_0E_BONELAYERS

    b_proxy_place_6e = big_space_rig.data.edit_bones.new(name=PROXY_PLACE_6E_BNAME)
    proxy_place_6e_bname = b_proxy_place_6e.name
    b_proxy_place_6e.head = mathutils.Vector(PROXY_PLACE_6E_BONEHEAD)
    b_proxy_place_6e.tail = mathutils.Vector(PROXY_PLACE_6E_BONETAIL)
    b_proxy_place_6e.parent = big_space_rig.data.edit_bones[PROXY_SPACE_6E_BNAME]
    b_proxy_place_6e.show_wire = True
    b_proxy_place_6e.layers = PROXY_PLACE_6E_BONELAYERS

    # switch to Pose mode to allow adding drivers, and to set pose bone location(s)
    bpy.ops.object.mode_set(mode='POSE')

    # custom bone shape, and show as Wireframe
    big_space_rig.pose.bones[place_bname].custom_shape = bpy.data.objects[widget_objs[QUAD_WIDGET_NAME].name]
    big_space_rig.pose.bones[proxy_place_0e_bname].custom_shape = \
        bpy.data.objects[widget_objs[PINCH_QUAD_WIDGET_NAME].name]
    big_space_rig.pose.bones[proxy_place_6e_bname].custom_shape = \
        bpy.data.objects[widget_objs[PINCH_QUAD_WIDGET_NAME].name]

    # using 'forced perspective' scaling will cause far away places to "shrink" as they move away, but doing
    # this calculation increases floating point error (e.g. math operation rounding error)
    if use_fp_scale:
        # add driver to place bone to make it scale for 'forced perspective' effect - lower accuracy
        add_bone_scl_drivers(big_space_rig, OBSERVER_FOCUS_BNAME, PROXY_OBSERVER_0E_BNAME, PROXY_OBSERVER_6E_BNAME,
                             place_bname, proxy_place_0e_bname, proxy_place_6e_bname)
        add_scl_bone_loc_drivers(big_space_rig, OBSERVER_FOCUS_BNAME, PROXY_OBSERVER_0E_BNAME, PROXY_OBSERVER_6E_BNAME,
                             place_bname, proxy_place_0e_bname, proxy_place_6e_bname)
    # do not used 'forced perspective' effect, and maximize accuracy by reducing floating point error
    else:
        # no scale drivers, just location drivers - for maximum accuracy
        add_reg_bone_loc_drivers(big_space_rig, OBSERVER_FOCUS_BNAME, PROXY_OBSERVER_0E_BNAME, PROXY_OBSERVER_6E_BNAME,
                             place_bname, proxy_place_0e_bname, proxy_place_6e_bname)

    # if a place location is given then convert the location to Proxy coordinates
    if place_loc != None:
        p_loc_6e = (round(place_loc[0] / 1000000, 3),
                    round(place_loc[1] / 1000000, 3),
                    round(place_loc[2] / 1000000, 3) )
        big_space_rig.pose.bones[proxy_place_6e_bname].location = p_loc_6e
        p_loc_0e = (place_loc[0] - 1000000 * p_loc_6e[0],
                    place_loc[1] - 1000000 * p_loc_6e[1],
                    place_loc[2] - 1000000 * p_loc_6e[2] )
        big_space_rig.pose.bones[proxy_place_0e_bname].location = p_loc_0e
    # else if new proxy bone should use the proxy observer position, then do it
    elif use_obs_loc:
        big_space_rig.pose.bones[proxy_place_6e_bname].location = (
            big_space_rig.pose.bones[PROXY_OBSERVER_6E_BNAME].matrix[0][3],
            big_space_rig.pose.bones[PROXY_OBSERVER_6E_BNAME].matrix[1][3],
            big_space_rig.pose.bones[PROXY_OBSERVER_6E_BNAME].matrix[2][3])

    # insert keyframe, to prevent data loss, i.e. position erased, if user does menu Pose -> Clear Transform,
    # presses Ctrl-G to reset location, etc.
    big_space_rig.pose.bones[proxy_place_0e_bname].keyframe_insert(data_path="location")
    big_space_rig.pose.bones[proxy_place_6e_bname].keyframe_insert(data_path="location")

    big_space_rig.pose.bones[place_bname][OBJ_PROP_BONE_SCL_MULT] = 1.0

    # switch back to previous view3d mode
    bpy.ops.object.mode_set(mode=old_3dview_mode)

    return place_bname, proxy_place_6e_bname

def add_bone_scl_drivers(armature, obs_focus_bname, proxy_obs_0e_bname, proxy_obs_6e_bname, place_bname,
                         proxy_place_0e_bname, proxy_place_6e_bname):
    drv_scale_x = armature.pose.bones[place_bname].driver_add("scale", 0).driver

    v_bsr_fp_power = drv_scale_x.variables.new()
    v_bsr_fp_power.type = 'SINGLE_PROP'
    v_bsr_fp_power.name                 = "fp_pow"
    v_bsr_fp_power.targets[0].id        = armature
    v_bsr_fp_power.targets[0].data_path = "[\""+OBJ_PROP_FP_POWER+"\"]"

    v_bsr_fp_min_dist = drv_scale_x.variables.new()
    v_bsr_fp_min_dist.type = 'SINGLE_PROP'
    v_bsr_fp_min_dist.name                 = "fp_md"
    v_bsr_fp_min_dist.targets[0].id        = armature
    v_bsr_fp_min_dist.targets[0].data_path = "[\""+OBJ_PROP_FP_MIN_DIST+"\"]"

    v_bsr_fp_min_scale = drv_scale_x.variables.new()
    v_bsr_fp_min_scale.type = 'SINGLE_PROP'
    v_bsr_fp_min_scale.name                 = "fp_ms"
    v_bsr_fp_min_scale.targets[0].id        = armature
    v_bsr_fp_min_scale.targets[0].data_path = "[\""+OBJ_PROP_FP_MIN_SCALE+"\"]"

    v_extra_scale = drv_scale_x.variables.new()
    v_extra_scale.type = 'SINGLE_PROP'
    v_extra_scale.name                 = "ex_scl"
    v_extra_scale.targets[0].id        = armature
    v_extra_scale.targets[0].data_path = "pose.bones[\""+place_bname+"\"][\""+OBJ_PROP_BONE_SCL_MULT+"\"]"

    # observer focus X
    v_obs_focus_x = drv_scale_x.variables.new()
    v_obs_focus_x.type = 'TRANSFORMS'
    v_obs_focus_x.name                 = "of_x"
    v_obs_focus_x.targets[0].id        = armature
    v_obs_focus_x.targets[0].bone_target        = obs_focus_bname
    v_obs_focus_x.targets[0].transform_type = 'LOC_X'
    v_obs_focus_x.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_obs_focus_x.targets[0].data_path = "location.x"

    # observer focus Y
    v_obs_focus_y = drv_scale_x.variables.new()
    v_obs_focus_y.type = 'TRANSFORMS'
    v_obs_focus_y.name                 = "of_y"
    v_obs_focus_y.targets[0].id        = armature
    v_obs_focus_y.targets[0].bone_target        = obs_focus_bname
    v_obs_focus_y.targets[0].transform_type = 'LOC_Y'
    v_obs_focus_y.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_obs_focus_y.targets[0].data_path = "location.y"

    # observer focus Z
    v_obs_focus_z = drv_scale_x.variables.new()
    v_obs_focus_z.type = 'TRANSFORMS'
    v_obs_focus_z.name                 = "of_z"
    v_obs_focus_z.targets[0].id        = armature
    v_obs_focus_z.targets[0].bone_target        = obs_focus_bname
    v_obs_focus_z.targets[0].transform_type = 'LOC_Z'
    v_obs_focus_z.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_obs_focus_z.targets[0].data_path = "location.z"

    # proxy observer X ; scale 1
    v_proxy_obs_0e_x = drv_scale_x.variables.new()
    v_proxy_obs_0e_x.type = 'TRANSFORMS'
    v_proxy_obs_0e_x.name                 = "o_0e_x"
    v_proxy_obs_0e_x.targets[0].id        = armature
    v_proxy_obs_0e_x.targets[0].bone_target        = proxy_obs_0e_bname
    v_proxy_obs_0e_x.targets[0].transform_type = 'LOC_X'
    v_proxy_obs_0e_x.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_proxy_obs_0e_x.targets[0].data_path = "location.x"

    # proxy observer Y ; scale 1
    v_proxy_obs_0e_y = drv_scale_x.variables.new()
    v_proxy_obs_0e_y.type = 'TRANSFORMS'
    v_proxy_obs_0e_y.name                 = "o_0e_y"
    v_proxy_obs_0e_y.targets[0].id        = armature
    v_proxy_obs_0e_y.targets[0].bone_target        = proxy_obs_0e_bname
    v_proxy_obs_0e_y.targets[0].transform_type = 'LOC_Y'
    v_proxy_obs_0e_y.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_proxy_obs_0e_y.targets[0].data_path = "location.y"

    # proxy observer Z ; scale 1
    v_proxy_obs_0e_z = drv_scale_x.variables.new()
    v_proxy_obs_0e_z.type = 'TRANSFORMS'
    v_proxy_obs_0e_z.name                 = "o_0e_z"
    v_proxy_obs_0e_z.targets[0].id        = armature
    v_proxy_obs_0e_z.targets[0].bone_target        = proxy_obs_0e_bname
    v_proxy_obs_0e_z.targets[0].transform_type = 'LOC_Z'
    v_proxy_obs_0e_z.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_proxy_obs_0e_z.targets[0].data_path = "location.z"

    # proxy observer X ; scale 1000
    v_proxy_obs_6e_x = drv_scale_x.variables.new()
    v_proxy_obs_6e_x.type = 'TRANSFORMS'
    v_proxy_obs_6e_x.name                 = "o_6e_x"
    v_proxy_obs_6e_x.targets[0].id        = armature
    v_proxy_obs_6e_x.targets[0].bone_target        = proxy_obs_6e_bname
    v_proxy_obs_6e_x.targets[0].transform_type = 'LOC_X'
    v_proxy_obs_6e_x.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_proxy_obs_6e_x.targets[0].data_path = "location.x"

    # proxy observer Y ; scale 1000
    v_proxy_obs_6e_y = drv_scale_x.variables.new()
    v_proxy_obs_6e_y.type = 'TRANSFORMS'
    v_proxy_obs_6e_y.name                 = "o_6e_y"
    v_proxy_obs_6e_y.targets[0].id        = armature
    v_proxy_obs_6e_y.targets[0].bone_target        = proxy_obs_6e_bname
    v_proxy_obs_6e_y.targets[0].transform_type = 'LOC_Y'
    v_proxy_obs_6e_y.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_proxy_obs_6e_y.targets[0].data_path = "location.y"

    # proxy observer Z ; scale 1000
    v_proxy_obs_6e_z = drv_scale_x.variables.new()
    v_proxy_obs_6e_z.type = 'TRANSFORMS'
    v_proxy_obs_6e_z.name                 = "o_6e_z"
    v_proxy_obs_6e_z.targets[0].id        = armature
    v_proxy_obs_6e_z.targets[0].bone_target        = proxy_obs_6e_bname
    v_proxy_obs_6e_z.targets[0].transform_type = 'LOC_Z'
    v_proxy_obs_6e_z.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_proxy_obs_6e_z.targets[0].data_path = "location.z"

    # proxy place X ; scale 1
    v_proxy_place_0e_x = drv_scale_x.variables.new()
    v_proxy_place_0e_x.type = 'TRANSFORMS'
    v_proxy_place_0e_x.name                 = "p_0e_x"
    v_proxy_place_0e_x.targets[0].id        = armature
    v_proxy_place_0e_x.targets[0].bone_target        = proxy_place_0e_bname
    v_proxy_place_0e_x.targets[0].transform_type = 'LOC_X'
    v_proxy_place_0e_x.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_proxy_place_0e_x.targets[0].data_path = "location.x"

    # proxy place Y ; scale 1
    v_proxy_place_0e_y = drv_scale_x.variables.new()
    v_proxy_place_0e_y.type = 'TRANSFORMS'
    v_proxy_place_0e_y.name                 = "p_0e_y"
    v_proxy_place_0e_y.targets[0].id        = armature
    v_proxy_place_0e_y.targets[0].bone_target        = proxy_place_0e_bname
    v_proxy_place_0e_y.targets[0].transform_type = 'LOC_Y'
    v_proxy_place_0e_y.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_proxy_place_0e_y.targets[0].data_path = "location.y"

    # proxy place Z ; scale 1
    v_proxy_place_0e_z = drv_scale_x.variables.new()
    v_proxy_place_0e_z.type = 'TRANSFORMS'
    v_proxy_place_0e_z.name                 = "p_0e_z"
    v_proxy_place_0e_z.targets[0].id        = armature
    v_proxy_place_0e_z.targets[0].bone_target        = proxy_place_0e_bname
    v_proxy_place_0e_z.targets[0].transform_type = 'LOC_Z'
    v_proxy_place_0e_z.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_proxy_place_0e_z.targets[0].data_path = "location.z"

    # proxy place X ; scale 1000
    v_proxy_place_6e_x = drv_scale_x.variables.new()
    v_proxy_place_6e_x.type = 'TRANSFORMS'
    v_proxy_place_6e_x.name                 = "p_6e_x"
    v_proxy_place_6e_x.targets[0].id        = armature
    v_proxy_place_6e_x.targets[0].bone_target        = proxy_place_6e_bname
    v_proxy_place_6e_x.targets[0].transform_type = 'LOC_X'
    v_proxy_place_6e_x.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_proxy_place_6e_x.targets[0].data_path = "location.x"

    # proxy place Y ; scale 1000
    v_proxy_place_6e_y = drv_scale_x.variables.new()
    v_proxy_place_6e_y.type = 'TRANSFORMS'
    v_proxy_place_6e_y.name                 = "p_6e_y"
    v_proxy_place_6e_y.targets[0].id        = armature
    v_proxy_place_6e_y.targets[0].bone_target        = proxy_place_6e_bname
    v_proxy_place_6e_y.targets[0].transform_type = 'LOC_Y'
    v_proxy_place_6e_y.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_proxy_place_6e_y.targets[0].data_path = "location.y"

    # proxy place Z ; scale 1000
    v_proxy_place_6e_z = drv_scale_x.variables.new()
    v_proxy_place_6e_z.type = 'TRANSFORMS'
    v_proxy_place_6e_z.name                 = "p_6e_z"
    v_proxy_place_6e_z.targets[0].id        = armature
    v_proxy_place_6e_z.targets[0].bone_target        = proxy_place_6e_bname
    v_proxy_place_6e_z.targets[0].transform_type = 'LOC_Z'
    v_proxy_place_6e_z.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_proxy_place_6e_z.targets[0].data_path = "location.z"

    drv_scale_x.expression = "max("+v_bsr_fp_min_scale.name+","+v_extra_scale.name+"/((1+max(0,((((" + \
        v_proxy_place_0e_x.name+"-"+v_proxy_obs_0e_x.name+"-"+v_obs_focus_x.name+")+1000000*(" + \
        v_proxy_place_6e_x.name+"-"+v_proxy_obs_6e_x.name+"))**2)+((("+v_proxy_place_0e_y.name+"-" + \
        v_proxy_obs_0e_y.name+"-"+v_obs_focus_y.name+")+1000000*("+v_proxy_place_6e_y.name+"-" + \
        v_proxy_obs_6e_y.name+"))**2)+((("+v_proxy_place_0e_z.name+"-"+v_proxy_obs_0e_z.name+"-" + \
        v_obs_focus_z.name+")+1000000*("+v_proxy_place_6e_z.name+"-"+v_proxy_obs_6e_z.name+"))**2))**0.5" + \
        "-"+v_bsr_fp_min_dist.name+"))**"+v_bsr_fp_power.name+"))"

    # Y scale is copy of X scale value
    drv_scale_y = armature.pose.bones[place_bname].driver_add('scale', 1).driver
    v_scale_y = drv_scale_y.variables.new()
    v_scale_y.type = 'TRANSFORMS'
    v_scale_y.name                 = "self_scl_x"
    v_scale_y.targets[0].id        = armature
    v_scale_y.targets[0].bone_target        = place_bname
    v_scale_y.targets[0].transform_type = 'SCALE_X'
    v_scale_y.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_scale_y.targets[0].data_path = "scale.x"
    drv_scale_y.expression = v_scale_y.name
    # Z scale is copy of X scale value
    drv_scale_z = armature.pose.bones[place_bname].driver_add('scale', 2).driver
    v_scale_z = drv_scale_z.variables.new()
    v_scale_z.type = 'TRANSFORMS'
    v_scale_z.name                 = "self_scl_x"
    v_scale_z.targets[0].id        = armature
    v_scale_z.targets[0].bone_target        = place_bname
    v_scale_z.targets[0].transform_type = 'SCALE_X'
    v_scale_z.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_scale_z.targets[0].data_path = "scale.x"
    drv_scale_z.expression = v_scale_z.name

def add_scl_bone_loc_drivers(armature, observer_focus_bname, proxy_observer_0e_bname, proxy_observer_6e_bname, place_bname,
                         proxy_place_0e_bname, proxy_place_6e_bname):
    # X
    drv_loc_x = armature.pose.bones[place_bname].driver_add('location', 0).driver
    # proxy place X ; scale 1
    v_proxy_place_0e_x = drv_loc_x.variables.new()
    v_proxy_place_0e_x.type = 'TRANSFORMS'
    v_proxy_place_0e_x.name                 = PROXY_PLACE_0E_VAR_NAME_PREPEND+"_x"
    v_proxy_place_0e_x.targets[0].id        = armature
    v_proxy_place_0e_x.targets[0].bone_target        = proxy_place_0e_bname
    v_proxy_place_0e_x.targets[0].transform_type = 'LOC_X'
    v_proxy_place_0e_x.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_proxy_place_0e_x.targets[0].data_path = "location.x"
    # proxy place X ; scale 1000
    v_proxy_place_6e_x = drv_loc_x.variables.new()
    v_proxy_place_6e_x.type = 'TRANSFORMS'

    v_proxy_place_6e_x.name                 = PROXY_PLACE_6E_VAR_NAME_PREPEND+"_x"
    v_proxy_place_6e_x.targets[0].id        = armature
    v_proxy_place_6e_x.targets[0].bone_target        = proxy_place_6e_bname
    v_proxy_place_6e_x.targets[0].transform_type = 'LOC_X'
    v_proxy_place_6e_x.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_proxy_place_6e_x.targets[0].data_path = "location.x"
    # proxy observer X ; scale 1
    v_proxy_obs_0e_x = drv_loc_x.variables.new()
    v_proxy_obs_0e_x.type = 'TRANSFORMS'
    v_proxy_obs_0e_x.name                 = "proxy_obs_0e_x"
    v_proxy_obs_0e_x.targets[0].id        = armature
    v_proxy_obs_0e_x.targets[0].bone_target        = proxy_observer_0e_bname
    v_proxy_obs_0e_x.targets[0].transform_type = 'LOC_X'
    v_proxy_obs_0e_x.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_proxy_obs_0e_x.targets[0].data_path = "location.x"
    # proxy observer X ; scale 1000
    v_proxy_obs_6e_x = drv_loc_x.variables.new()
    v_proxy_obs_6e_x.type = 'TRANSFORMS'
    v_proxy_obs_6e_x.name                 = "proxy_obs_6e_x"
    v_proxy_obs_6e_x.targets[0].id        = armature
    v_proxy_obs_6e_x.targets[0].bone_target        = proxy_observer_6e_bname
    v_proxy_obs_6e_x.targets[0].transform_type = 'LOC_X'
    v_proxy_obs_6e_x.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_proxy_obs_6e_x.targets[0].data_path = "location.x"
    # observer focus X
    v_obs_focus_x = drv_loc_x.variables.new()
    v_obs_focus_x.type = 'TRANSFORMS'
    v_obs_focus_x.name                 = "obs_focus_x"
    v_obs_focus_x.targets[0].id        = armature
    v_obs_focus_x.targets[0].bone_target        = observer_focus_bname
    v_obs_focus_x.targets[0].transform_type = 'LOC_X'
    v_obs_focus_x.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_obs_focus_x.targets[0].data_path = "location.x"
    # self scale X
    v_self_scale_x = drv_loc_x.variables.new()
    v_self_scale_x.type = 'TRANSFORMS'
    v_self_scale_x.name                 = "self_scale_x"
    v_self_scale_x.targets[0].id        = armature
    v_self_scale_x.targets[0].bone_target        = place_bname
    v_self_scale_x.targets[0].transform_type = 'SCALE_X'
    v_self_scale_x.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_self_scale_x.targets[0].data_path = "scale.x"
    # driver X
    drv_loc_x.expression = "( ("+v_proxy_place_0e_x.name+" - "+v_proxy_obs_0e_x.name+" - "+v_obs_focus_x.name + \
        ") + ("+v_proxy_place_6e_x.name+" - "+v_proxy_obs_6e_x.name+") * 1000000) * "+v_self_scale_x.name

    # Y
    drv_loc_y = armature.pose.bones[place_bname].driver_add('location', 1).driver
    # proxy place Y ; scale 1
    v_proxy_place_0e_y = drv_loc_y.variables.new()
    v_proxy_place_0e_y.type = 'TRANSFORMS'
    v_proxy_place_0e_y.name                 = PROXY_PLACE_0E_VAR_NAME_PREPEND+"_y"
    v_proxy_place_0e_y.targets[0].id        = armature
    v_proxy_place_0e_y.targets[0].bone_target        = proxy_place_0e_bname
    v_proxy_place_0e_y.targets[0].transform_type = 'LOC_Y'
    v_proxy_place_0e_y.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_proxy_place_0e_y.targets[0].data_path = "location.y"
    # proxy place Y ; scale 1000
    v_proxy_place_6e_y = drv_loc_y.variables.new()
    v_proxy_place_6e_y.type = 'TRANSFORMS'
    v_proxy_place_6e_y.name                 = PROXY_PLACE_6E_VAR_NAME_PREPEND+"_y"
    v_proxy_place_6e_y.targets[0].id        = armature
    v_proxy_place_6e_y.targets[0].bone_target        = proxy_place_6e_bname
    v_proxy_place_6e_y.targets[0].transform_type = 'LOC_Y'
    v_proxy_place_6e_y.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_proxy_place_6e_y.targets[0].data_path = "location.y"
    # proxy observer Y ; scale 1
    v_proxy_obs_0e_y = drv_loc_y.variables.new()
    v_proxy_obs_0e_y.type = 'TRANSFORMS'
    v_proxy_obs_0e_y.name                 = "proxy_obs_0e_y"
    v_proxy_obs_0e_y.targets[0].id        = armature
    v_proxy_obs_0e_y.targets[0].bone_target        = proxy_observer_0e_bname
    v_proxy_obs_0e_y.targets[0].transform_type = 'LOC_Y'
    v_proxy_obs_0e_y.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_proxy_obs_0e_y.targets[0].data_path = "location.y"
    # proxy observer Y ; scale 1000
    v_proxy_obs_6e_y = drv_loc_y.variables.new()
    v_proxy_obs_6e_y.type = 'TRANSFORMS'
    v_proxy_obs_6e_y.name                 = "proxy_obs_6e_y"
    v_proxy_obs_6e_y.targets[0].id        = armature
    v_proxy_obs_6e_y.targets[0].bone_target        = proxy_observer_6e_bname
    v_proxy_obs_6e_y.targets[0].transform_type = 'LOC_Y'
    v_proxy_obs_6e_y.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_proxy_obs_6e_y.targets[0].data_path = "location.y"
    # observer Y
    v_obs_focus_y = drv_loc_y.variables.new()
    v_obs_focus_y.type = 'TRANSFORMS'
    v_obs_focus_y.name                 = "obs_focus_y"
    v_obs_focus_y.targets[0].id        = armature
    v_obs_focus_y.targets[0].bone_target        = observer_focus_bname
    v_obs_focus_y.targets[0].transform_type = 'LOC_Y'
    v_obs_focus_y.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_obs_focus_y.targets[0].data_path = "location.y"
    # self scale Y
    v_self_scale_y = drv_loc_y.variables.new()
    v_self_scale_y.type = 'TRANSFORMS'
    v_self_scale_y.name                 = "self_scale_y"
    v_self_scale_y.targets[0].id        = armature
    v_self_scale_y.targets[0].bone_target        = place_bname
    v_self_scale_y.targets[0].transform_type = 'SCALE_Y'
    v_self_scale_y.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_self_scale_y.targets[0].data_path = "scale.y"
    # driver Y
    drv_loc_y.expression = "( ("+v_proxy_place_0e_y.name+" - "+v_proxy_obs_0e_y.name+" - "+v_obs_focus_y.name + \
        ") + ("+v_proxy_place_6e_y.name+" - "+v_proxy_obs_6e_y.name+") * 1000000) * "+v_self_scale_y.name

    # Z
    drv_loc_z = armature.pose.bones[place_bname].driver_add('location', 2).driver
    # proxy place Z ; scale 1
    v_proxy_place_0e_z = drv_loc_z.variables.new()
    v_proxy_place_0e_z.type = 'TRANSFORMS'
    v_proxy_place_0e_z.name                 = PROXY_PLACE_0E_VAR_NAME_PREPEND+"_z"
    v_proxy_place_0e_z.targets[0].id        = armature
    v_proxy_place_0e_z.targets[0].bone_target        = proxy_place_0e_bname
    v_proxy_place_0e_z.targets[0].transform_type = 'LOC_Z'
    v_proxy_place_0e_z.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_proxy_place_0e_z.targets[0].data_path = "location.z"
    # proxy place Z ; scale 1000
    v_proxy_place_6e_z = drv_loc_z.variables.new()
    v_proxy_place_6e_z.type = 'TRANSFORMS'
    v_proxy_place_6e_z.name                 = PROXY_PLACE_6E_VAR_NAME_PREPEND+"_z"
    v_proxy_place_6e_z.targets[0].id        = armature
    v_proxy_place_6e_z.targets[0].bone_target        = proxy_place_6e_bname
    v_proxy_place_6e_z.targets[0].transform_type = 'LOC_Z'
    v_proxy_place_6e_z.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_proxy_place_6e_z.targets[0].data_path = "location.z"
    # proxy observer Z ; scale 1
    v_proxy_obs_0e_z = drv_loc_z.variables.new()
    v_proxy_obs_0e_z.type = 'TRANSFORMS'
    v_proxy_obs_0e_z.name                 = "proxy_obs_0e_z"
    v_proxy_obs_0e_z.targets[0].id        = armature
    v_proxy_obs_0e_z.targets[0].bone_target        = proxy_observer_0e_bname
    v_proxy_obs_0e_z.targets[0].transform_type = 'LOC_Z'
    v_proxy_obs_0e_z.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_proxy_obs_0e_z.targets[0].data_path = "location.z"
    # proxy observer Z ; scale 1000
    v_proxy_obs_6e_z = drv_loc_z.variables.new()
    v_proxy_obs_6e_z.type = 'TRANSFORMS'
    v_proxy_obs_6e_z.name                 = "proxy_obs_6e_z"
    v_proxy_obs_6e_z.targets[0].id        = armature
    v_proxy_obs_6e_z.targets[0].bone_target        = proxy_observer_6e_bname
    v_proxy_obs_6e_z.targets[0].transform_type = 'LOC_Z'
    v_proxy_obs_6e_z.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_proxy_obs_6e_z.targets[0].data_path = "location.z"
    # observer Z
    v_obs_focus_z = drv_loc_z.variables.new()
    v_obs_focus_z.type = 'TRANSFORMS'
    v_obs_focus_z.name                 = "obs_focus_z"
    v_obs_focus_z.targets[0].id        = armature
    v_obs_focus_z.targets[0].bone_target        = observer_focus_bname
    v_obs_focus_z.targets[0].transform_type = 'LOC_Z'
    v_obs_focus_z.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_obs_focus_z.targets[0].data_path = "location.z"
    # self scale Z
    v_self_scale_z = drv_loc_z.variables.new()
    v_self_scale_z.type = 'TRANSFORMS'
    v_self_scale_z.name                 = "self_scale_z"
    v_self_scale_z.targets[0].id        = armature
    v_self_scale_z.targets[0].bone_target        = place_bname
    v_self_scale_z.targets[0].transform_type = 'SCALE_Z'
    v_self_scale_z.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_self_scale_z.targets[0].data_path = "scale.z"
    # driver Z
    drv_loc_z.expression = "( ("+v_proxy_place_0e_z.name+" - "+v_proxy_obs_0e_z.name+" - "+v_obs_focus_z.name + \
        ") + ("+v_proxy_place_6e_z.name+" - "+v_proxy_obs_6e_z.name+") * 1000000) * "+v_self_scale_z.name

def add_reg_bone_loc_drivers(armature, observer_focus_bname, proxy_observer_0e_bname, proxy_observer_6e_bname, place_bname,
                         proxy_place_0e_bname, proxy_place_6e_bname):
    # X
    drv_loc_x = armature.pose.bones[place_bname].driver_add('location', 0).driver
    # proxy place X ; scale 1
    v_proxy_place_0e_x = drv_loc_x.variables.new()
    v_proxy_place_0e_x.type = 'TRANSFORMS'
    v_proxy_place_0e_x.name                 = PROXY_PLACE_0E_VAR_NAME_PREPEND+"_x"
    v_proxy_place_0e_x.targets[0].id        = armature
    v_proxy_place_0e_x.targets[0].bone_target        = proxy_place_0e_bname
    v_proxy_place_0e_x.targets[0].transform_type = 'LOC_X'
    v_proxy_place_0e_x.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_proxy_place_0e_x.targets[0].data_path = "location.x"
    # proxy place X ; scale 1000
    v_proxy_place_6e_x = drv_loc_x.variables.new()
    v_proxy_place_6e_x.type = 'TRANSFORMS'
    v_proxy_place_6e_x.name                 = PROXY_PLACE_6E_VAR_NAME_PREPEND+"_x"
    v_proxy_place_6e_x.targets[0].id        = armature
    v_proxy_place_6e_x.targets[0].bone_target        = proxy_place_6e_bname
    v_proxy_place_6e_x.targets[0].transform_type = 'LOC_X'
    v_proxy_place_6e_x.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_proxy_place_6e_x.targets[0].data_path = "location.x"
    # proxy observer X ; scale 1
    v_proxy_obs_0e_x = drv_loc_x.variables.new()
    v_proxy_obs_0e_x.type = 'TRANSFORMS'
    v_proxy_obs_0e_x.name                 = "proxy_obs_0e_x"
    v_proxy_obs_0e_x.targets[0].id        = armature
    v_proxy_obs_0e_x.targets[0].bone_target        = proxy_observer_0e_bname
    v_proxy_obs_0e_x.targets[0].transform_type = 'LOC_X'
    v_proxy_obs_0e_x.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_proxy_obs_0e_x.targets[0].data_path = "location.x"
    # proxy observer X ; scale 1000
    v_proxy_obs_6e_x = drv_loc_x.variables.new()
    v_proxy_obs_6e_x.type = 'TRANSFORMS'
    v_proxy_obs_6e_x.name                 = "proxy_obs_6e_x"
    v_proxy_obs_6e_x.targets[0].id        = armature
    v_proxy_obs_6e_x.targets[0].bone_target        = proxy_observer_6e_bname
    v_proxy_obs_6e_x.targets[0].transform_type = 'LOC_X'
    v_proxy_obs_6e_x.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_proxy_obs_6e_x.targets[0].data_path = "location.x"
    # observer focus X
    v_obs_focus_x = drv_loc_x.variables.new()
    v_obs_focus_x.type = 'TRANSFORMS'
    v_obs_focus_x.name                 = "obs_focus_x"
    v_obs_focus_x.targets[0].id        = armature
    v_obs_focus_x.targets[0].bone_target        = observer_focus_bname
    v_obs_focus_x.targets[0].transform_type = 'LOC_X'
    v_obs_focus_x.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_obs_focus_x.targets[0].data_path = "location.x"
    # driver X
    drv_loc_x.expression = "("+v_proxy_place_0e_x.name+" - "+v_proxy_obs_0e_x.name+" - "+v_obs_focus_x.name + \
        ") + ("+v_proxy_place_6e_x.name+" - "+v_proxy_obs_6e_x.name+") * 1000000"

    # Y
    drv_loc_y = armature.pose.bones[place_bname].driver_add('location', 1).driver
    # proxy place Y ; scale 1
    v_proxy_place_0e_y = drv_loc_y.variables.new()
    v_proxy_place_0e_y.type = 'TRANSFORMS'
    v_proxy_place_0e_y.name                 = PROXY_PLACE_0E_VAR_NAME_PREPEND+"_y"
    v_proxy_place_0e_y.targets[0].id        = armature
    v_proxy_place_0e_y.targets[0].bone_target        = proxy_place_0e_bname
    v_proxy_place_0e_y.targets[0].transform_type = 'LOC_Y'
    v_proxy_place_0e_y.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_proxy_place_0e_y.targets[0].data_path = "location.y"
    # proxy place Y ; scale 1000
    v_proxy_place_6e_y = drv_loc_y.variables.new()
    v_proxy_place_6e_y.type = 'TRANSFORMS'
    v_proxy_place_6e_y.name                 = PROXY_PLACE_6E_VAR_NAME_PREPEND+"y"
    v_proxy_place_6e_y.targets[0].id        = armature
    v_proxy_place_6e_y.targets[0].bone_target        = proxy_place_6e_bname
    v_proxy_place_6e_y.targets[0].transform_type = 'LOC_Y'
    v_proxy_place_6e_y.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_proxy_place_6e_y.targets[0].data_path = "location.y"
    # proxy observer Y ; scale 1
    v_proxy_obs_0e_y = drv_loc_y.variables.new()
    v_proxy_obs_0e_y.type = 'TRANSFORMS'
    v_proxy_obs_0e_y.name                 = "proxy_obs_0e_y"
    v_proxy_obs_0e_y.targets[0].id        = armature
    v_proxy_obs_0e_y.targets[0].bone_target        = proxy_observer_0e_bname
    v_proxy_obs_0e_y.targets[0].transform_type = 'LOC_Y'
    v_proxy_obs_0e_y.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_proxy_obs_0e_y.targets[0].data_path = "location.y"
    # proxy observer Y ; scale 1000
    v_proxy_obs_6e_y = drv_loc_y.variables.new()
    v_proxy_obs_6e_y.type = 'TRANSFORMS'
    v_proxy_obs_6e_y.name                 = "proxy_obs_6e_y"
    v_proxy_obs_6e_y.targets[0].id        = armature
    v_proxy_obs_6e_y.targets[0].bone_target        = proxy_observer_6e_bname
    v_proxy_obs_6e_y.targets[0].transform_type = 'LOC_Y'
    v_proxy_obs_6e_y.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_proxy_obs_6e_y.targets[0].data_path = "location.y"
    # observer Y
    v_obs_focus_y = drv_loc_y.variables.new()
    v_obs_focus_y.type = 'TRANSFORMS'
    v_obs_focus_y.name                 = "obs_focus_y"
    v_obs_focus_y.targets[0].id        = armature
    v_obs_focus_y.targets[0].bone_target        = observer_focus_bname
    v_obs_focus_y.targets[0].transform_type = 'LOC_Y'
    v_obs_focus_y.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_obs_focus_y.targets[0].data_path = "location.y"
    # driver Y
    drv_loc_y.expression = "("+v_proxy_place_0e_y.name+" - "+v_proxy_obs_0e_y.name+" - "+v_obs_focus_y.name + \
        ") + ("+v_proxy_place_6e_y.name+" - "+v_proxy_obs_6e_y.name+") * 1000000"

    # Z
    drv_loc_z = armature.pose.bones[place_bname].driver_add('location', 2).driver
    # proxy place Z ; scale 1
    v_proxy_place_0e_z = drv_loc_z.variables.new()
    v_proxy_place_0e_z.type = 'TRANSFORMS'
    v_proxy_place_0e_z.name                 = PROXY_PLACE_0E_VAR_NAME_PREPEND+"_z"
    v_proxy_place_0e_z.targets[0].id        = armature
    v_proxy_place_0e_z.targets[0].bone_target        = proxy_place_0e_bname
    v_proxy_place_0e_z.targets[0].transform_type = 'LOC_Z'
    v_proxy_place_0e_z.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_proxy_place_0e_z.targets[0].data_path = "location.z"
    # proxy place Z ; scale 1000
    v_proxy_place_6e_z = drv_loc_z.variables.new()
    v_proxy_place_6e_z.type = 'TRANSFORMS'
    v_proxy_place_6e_z.name                 = PROXY_PLACE_6E_VAR_NAME_PREPEND+"_z"
    v_proxy_place_6e_z.targets[0].id        = armature
    v_proxy_place_6e_z.targets[0].bone_target        = proxy_place_6e_bname
    v_proxy_place_6e_z.targets[0].transform_type = 'LOC_Z'
    v_proxy_place_6e_z.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_proxy_place_6e_z.targets[0].data_path = "location.z"
    # proxy observer Z ; scale 1
    v_proxy_obs_0e_z = drv_loc_z.variables.new()
    v_proxy_obs_0e_z.type = 'TRANSFORMS'
    v_proxy_obs_0e_z.name                 = "proxy_obs_0e_z"
    v_proxy_obs_0e_z.targets[0].id        = armature
    v_proxy_obs_0e_z.targets[0].bone_target        = proxy_observer_0e_bname
    v_proxy_obs_0e_z.targets[0].transform_type = 'LOC_Z'
    v_proxy_obs_0e_z.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_proxy_obs_0e_z.targets[0].data_path = "location.z"
    # proxy observer Z ; scale 1000
    v_proxy_obs_6e_z = drv_loc_z.variables.new()
    v_proxy_obs_6e_z.type = 'TRANSFORMS'
    v_proxy_obs_6e_z.name                 = "proxy_obs_6e_z"
    v_proxy_obs_6e_z.targets[0].id        = armature
    v_proxy_obs_6e_z.targets[0].bone_target        = proxy_observer_6e_bname
    v_proxy_obs_6e_z.targets[0].transform_type = 'LOC_Z'
    v_proxy_obs_6e_z.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_proxy_obs_6e_z.targets[0].data_path = "location.z"
    # observer Z
    v_obs_focus_z = drv_loc_z.variables.new()
    v_obs_focus_z.type = 'TRANSFORMS'
    v_obs_focus_z.name                 = "obs_focus_z"
    v_obs_focus_z.targets[0].id        = armature
    v_obs_focus_z.targets[0].bone_target        = observer_focus_bname
    v_obs_focus_z.targets[0].transform_type = 'LOC_Z'
    v_obs_focus_z.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_obs_focus_z.targets[0].data_path = "location.z"
    # driver Z
    drv_loc_z.expression = "("+v_proxy_place_0e_z.name+" - "+v_proxy_obs_0e_z.name+" - "+v_obs_focus_z.name + \
        ") + ("+v_proxy_place_6e_z.name+" - "+v_proxy_obs_6e_z.name+") * 1000000"

class BSR_AttachCreatePlace(bpy.types.Operator):
    bl_description = "Based on current position of Big Space Rig's ProxyObserver, create Place-ProxyPlace " + \
        "pair. Objects parented to Place will be scaled and moved as ProxyObserver moves. Note: Observer " + \
        "location must be (0, 0, 0) for this to work correctly"
    bl_idname = "big_space_rig.create_proxy_place"
    bl_label = "Create Place"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scn = context.scene
        active_ob = context.active_object
        # error checks
        if not is_big_space_rig(active_ob):
            # create a rig if needed
            if context.scene.BSR_AttachPreCreateRig:
                create_bsr_armature(context, scn.BSR_NewObserverFP_Power, scn.BSR_NewObserverFP_MinDist,
                                    scn.BSR_NewObserverFP_MinScale)
                # new active object
                active_ob = context.active_object
            else:
                self.report({'ERROR'}, "Unable to Create Place because Active Object is not a Big Space Rig.")
                return {'CANCELLED'}
        # get widgets and create
        widget_objs = get_widget_objs_from_rig(active_ob)
        create_proxy_place(context, active_ob, widget_objs, use_obs_loc=True, use_fp_scale=scn.BSR_UsePlaceScaleFP)
        return {'FINISHED'}

class BSR_AttachSinglePlace(bpy.types.Operator):
    bl_description = "Attach all selected object(s) to Big Space Rig. Rig must be selected last, and all other\n" + \
        "objects will be parented to rig. Note: this uses current position of rig's ProxyObserver"
    bl_idname = "big_space_rig.attach_single_place"
    bl_label = "Single Place"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scn = context.scene
        active_ob = context.active_object
        # get list of objects, a separate copy of context's list - because context's list may change
        selected_obs = [ob for ob in context.selected_objects]
        # error checks
        if not is_big_space_rig(active_ob):
            # create a rig if needed
            if context.scene.BSR_AttachPreCreateRig:
                create_bsr_armature(context, scn.BSR_NewObserverFP_Power, scn.BSR_NewObserverFP_MinDist,
                                    scn.BSR_NewObserverFP_MinScale)
                # new active object
                active_ob = context.active_object
            else:
                self.report({'ERROR'}, "Unable to attach object(s) because Active Object is not a Big Space Rig.")
                return {'CANCELLED'}
        if len(context.selected_objects) < 1:
            self.report({'ERROR'}, "Unable to attach object(s) to Big Space Rig because no object(s) selected")
            return {'CANCELLED'}
        widget_objs = get_widget_objs_from_rig(active_ob)
        # expand the rig by creating new bones in the rig
        place_bname, proxy_place_6e_bname = create_proxy_place(context, active_ob, widget_objs, use_obs_loc=True,
                                                               use_fp_scale=scn.BSR_UsePlaceScaleFP)

        # debug: change current frame of animation, to force Blender to update the armature, drivers, etc. in the
        # dependency graph - which Blender isn't automatically doing, for some reason...
        # all of this is done avoid errors with locations of objects/bones when parenting objects to bones
        bpy.context.scene.frame_set(bpy.context.scene.frame_current)
        bpy.context.scene.frame_set(bpy.context.scene.frame_current)

        # select only the objects that were selected before the function was called, and the
        # Big Space Rig (which may have been 'pre-created')
        bpy.ops.object.select_all(action='DESELECT')
        select_object(active_ob, True)
        for ob in selected_obs:
            # do not select objects that have a parent, if 'no re-parent' option is enabled
            if ob.parent != None and context.scene.BSR_AttachNoReParent:
                continue
            select_object(ob, True)

        # make the new Place bone the active bone, to be used for parenting objects
        active_ob.data.bones.active = active_ob.data.bones[place_bname]
        # parent all the selected object(s) to the new Place bone
        bpy.ops.object.parent_set(type='BONE')

        return {'FINISHED'}

class BSR_AttachMultiPlace(bpy.types.Operator):
    bl_description = "Attach selected objects to active Big Space Rig, creating a separate Place for each attached "+\
        "object. Select Rig last. This uses current position of objects relative to rig, and zeroes those objects' "+\
        "locations (may not work with location-keyframed objects)"
    bl_idname = "big_space_rig.attach_multi_place"
    bl_label = "Multi Place"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scn = context.scene
        active_ob = context.active_object
        # get list of objects, a separate copy of context's list - because context's list may change
        selected_obs = [ob for ob in context.selected_objects]
        # error checks
        if not is_big_space_rig(active_ob):
            # create a rig if needed
            if context.scene.BSR_AttachPreCreateRig:
                create_bsr_armature(context, scn.BSR_NewObserverFP_Power, scn.BSR_NewObserverFP_MinDist,
                                    scn.BSR_NewObserverFP_MinScale)
                # new active object
                active_ob = context.active_object
            else:
                self.report({'ERROR'}, "Unable to attach object(s) because Active Object is not a Big Space Rig.")
                return {'CANCELLED'}
        if len(context.selected_objects) < 1:
            self.report({'ERROR'}, "Unable to attach object(s) to Big Space Rig because no object(s) selected")
            return {'CANCELLED'}
        widget_objs = get_widget_objs_from_rig(active_ob)

        # select only the objects that were selected before the function was called, and the
        # Big Space Rig (which may have been 'pre-created')
        bpy.ops.object.select_all(action='DESELECT')
        select_object(active_ob, True)
        for ob in selected_obs:
            # skip the Big Space Rig for this part (it's already been selected)
            if ob == active_ob:
                continue
            # do not select objects that have a parent, if 'no re-parent' option is enabled
            if ob.parent != None and context.scene.BSR_AttachNoReParent:
                continue
            select_object(ob, True)

            place_loc = ob.matrix_world.translation - get_cursor_location(context)
            # expand the rig by creating new bones in the rig
            place_bname,proxy_place_6e_bname = create_proxy_place(context, active_ob, widget_objs, place_loc=place_loc,
                                                                  use_fp_scale=scn.BSR_UsePlaceScaleFP)

            # object's location was converted to Proxy coordinates, so zero object's location values
            ob.location.zero()
            # parent the object to the new Place,
            ob.parent = active_ob
            ob.parent_type = 'BONE'
            ob.parent_bone = place_bname
            ob.matrix_parent_inverse.identity()
            # undo translation due to bone length
            ob.matrix_parent_inverse[1][3] = -PLACE_BONETAIL[1]

        # debug: change current frame of animation, to force Blender to update the armature, drivers, etc. in the
        # dependency graph - which Blender isn't automatically updating, for some reason...
        # all of this is done to avoid errors with locations of objects/bones when parenting objects to bones
        bpy.context.scene.frame_set(bpy.context.scene.frame_current)
        bpy.context.scene.frame_set(bpy.context.scene.frame_current)
        return {'FINISHED'}
