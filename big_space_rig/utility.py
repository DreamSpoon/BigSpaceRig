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

from math import floor

import bpy

from .rig import (is_big_space_rig, get_6e_0e_from_place_bone_name)
from .rig import (PROXY_OBSERVER_0E_BNAME, PROXY_OBSERVER_6E_BNAME)

SNAP_TYPE_6E_DOWN_0E = "6E_DOWN_0E"
SNAP_TYPE_0E_UP_6E = "0E_UP_6E"
SNAP_TYPE_BOTH = "6E_AND_0E"
# BOTH is default
SNAP_LOCATION_TYPES = [
    (SNAP_TYPE_0E_UP_6E, "0e up to 6e", "Transfer (subtract from 0e location and add to 6e location) the 0e " +
     "location digits, greater than 1000, up to the 6e location"),
    (SNAP_TYPE_6E_DOWN_0E, "6e down to 0e", "Transfer (subtract from 6e location and add to 0e location) the 6e " +
     "location digits, less than 0.001, down to the 0e location"),
    (SNAP_TYPE_BOTH, "Both", "Ensure 6e and 0e locations are aligned to their respective 'precision' boundaries. " +
     "In other words, abs(6e) is 0.001 or greater, while abs(0e) is 1000 or less"),
]

def delete_bone_keyframes(armature, bone_name):
     # try to get current action name and return if error - meaning no action(s) found
    try:
        action_name = armature.animation_data.action.name
    except:
        return
    if (action_name != None):
        a = bpy.data.actions.get(action_name)
        # loop through all location f-curves
        for curve in [c for c in a.fcurves if not c.lock and c.data_path[-len('location'):] == 'location']:
            # check for bone name in data_path
            if "[\"" + bone_name in curve.data_path:
                # delete keyframes, always the last element, so that 'remove' does not cause error
                while len(curve.keyframe_points) > 0:
                    curve.keyframe_points.remove(curve.keyframe_points[len(curve.keyframe_points)-1])

# TODO: lots of testing; does this solution work correctly? in theory and in practice?
def snap_bone_location_6e_0e(big_space_rig, bone_name_6e, bone_name_0e, snap_type, snap_delete_keyframes):
    obs_bone_6e = big_space_rig.pose.bones.get(bone_name_6e)
    obs_bone_0e = big_space_rig.pose.bones.get(bone_name_0e)
    accum_6e = obs_bone_6e.location
    accum_0e = obs_bone_0e.location

    if snap_type == SNAP_TYPE_6E_DOWN_0E:
        for i in range(0, 3):
            accum_0e[i] = ((accum_6e[i] * 1000) - floor(accum_6e[i] * 1000.0)) * 1000.0 + accum_0e[i]
            accum_6e[i] = floor(accum_6e[i] * 1000.0) / 1000.0
    elif snap_type == SNAP_TYPE_0E_UP_6E:
        for i in range(0, 3):
            accum_6e[i] = floor(accum_0e[i] / 1000.0) / 1000.0 + accum_6e[i]
            accum_0e[i] = accum_0e[i] - (floor(accum_0e[i] / 1000.0) * 1000.0)
    elif snap_type == SNAP_TYPE_BOTH:
        for i in range(0, 3):
            # first, add from 6e down to 0e, to remove any digits below the precision boundary
            accum_0e[i] = ((accum_6e[i] * 1000) - floor(accum_6e[i] * 1000.0)) * 1000.0 + accum_0e[i]
            accum_6e[i] = floor(accum_6e[i] * 1000.0) / 1000.0
            # second, transfer back to 6e from 0e any amounts needed
            accum_6e[i] = floor(accum_0e[i] / 1000.0) / 1000.0 + accum_6e[i]
            accum_0e[i] = accum_0e[i] - (floor(accum_0e[i] / 1000.0) * 1000.0)

    # set the locations
    obs_bone_6e.location = accum_6e
    obs_bone_0e.location = accum_0e

    if snap_delete_keyframes:
        # delete old keyframes on Observer 6e, 0e
        delete_bone_keyframes(big_space_rig, bone_name_6e)
        delete_bone_keyframes(big_space_rig, bone_name_0e)

    # keyframe the locations
    obs_bone_6e.keyframe_insert(data_path="location")
    obs_bone_0e.keyframe_insert(data_path="location")

class BSR_SnapLocation6e0eObserver(bpy.types.Operator):
    bl_description = "6e locations should have digits no smaller than 0.001 (1e-3), and 0e locations should have " \
        "digits no larger than 1000 (1e3). This function attempts to transfer underflows from 6e to 0e, or overflows " \
        "from 0e to 6e, or both"
    bl_idname = "big_space_rig.snap_location_6e_0e_observer"
    bl_label = "Snap Observer Location"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        big_space_rig = context.active_object
        if not is_big_space_rig(big_space_rig):
            self.report({'ERROR'}, "Unable to Snap Observer Location (6e, 0e)  because active object is not a " +
                        "Big Space Rig")
            return {'CANCELLED'}
        scn = context.scene
        snap_bone_location_6e_0e(big_space_rig, PROXY_OBSERVER_6E_BNAME, PROXY_OBSERVER_0E_BNAME,
                                     scn.BSR_SnapLocationType, scn.BSR_SnapLocationDeleteKeyframes)
        return {'FINISHED'}

class BSR_SnapLocation6e0ePlace(bpy.types.Operator):
    bl_description = "6e locations should have digits no smaller than 0.001 (1e-3), and 0e locations should have " \
        "digits no larger than 1000 (1e3). This function attempts to transfer underflows from 6e to 0e, or overflows " \
        "from 0e to 6e, or both"
    bl_idname = "big_space_rig.snap_location_6e_0e_place"
    bl_label = "Snap Place Location"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scn = context.scene
        big_space_rig = context.active_object
        if not is_big_space_rig(big_space_rig):
            self.report({'ERROR'}, "Unable to Snap Place Location (6e, 0e)  because active object is not a " +
                        "Big Space Rig")
            return {'CANCELLED'}
        bone_6e, bone_0e = get_6e_0e_from_place_bone_name(big_space_rig,
                                                          scn.BSR_SnapPlaceName[1:len(scn.BSR_SnapPlaceName)])
        snap_bone_location_6e_0e(big_space_rig, bone_6e, bone_0e, scn.BSR_SnapLocationType,
                                 scn.BSR_SnapLocationDeleteKeyframes)
        return {'FINISHED'}
