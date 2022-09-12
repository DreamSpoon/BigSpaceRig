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

import math

import bpy
from mathutils import Vector

from .rig import (PROXY_OBSERVER_6E_BNAME, PROXY_OBSERVER_0E_BNAME, OBSERVER_FOCUS_BNAME)
from .rig import (is_big_space_rig, get_6e_0e_from_place_bone_name)

ANGLE_TYPE_DEGREES = "DEGREES"
ANGLE_TYPE_DEG_MIN_SEC_FRAC = "DEG_MIN_SEC_FRAC"
ANGLE_TYPE_RADIANS = "RADIANS"
ANGLE_TYPE_ITEMS = [
    (ANGLE_TYPE_DEGREES, "Degrees", "Angle is given in Degrees, where Degrees is a floating point number"),
    (ANGLE_TYPE_DEG_MIN_SEC_FRAC, "Deg:Min:Sec:Frac", "Angle is given in (Degrees, Minutes, Seconds, Fraction of " +
         "Second) where D, M, S are integer numbers and F is a floating point number"),
    (ANGLE_TYPE_RADIANS, "Radians", "Angle is given in Radians, where Radians is a floating point number"),
]

def go_to_sphere_coords_radians(context, big_space_rig, radius_6e, radius_0e, lat_degrees, long_degrees):
    # save view mode, then switch to pose mode so pose bone locations can be set
    old_3dview_mode = context.mode
    bpy.ops.object.mode_set(mode='POSE')

    big_surf_point = Vector((
        radius_6e * math.cos(lat_degrees) * math.cos(long_degrees),
        radius_6e * math.cos(lat_degrees) * math.sin(long_degrees),
        radius_6e * math.sin(lat_degrees),
    ))
    big_mult_3e = Vector((big_surf_point[0]*1000.0,
                      big_surf_point[1]*1000.0,
                      big_surf_point[2]*1000.0,
    ))
    big_mult_floor_3e = Vector((math.floor(big_surf_point[0]*1000.0),
                            math.floor(big_surf_point[1]*1000.0),
                            math.floor(big_surf_point[2]*1000.0),
    ))
    # init "accumulators", because adjustments are performed later
    accum_6e = big_mult_floor_3e / 1000.0
    accum_0e = (big_mult_3e - big_mult_floor_3e) * 1000.0
    # "small" radius is in meters
    small_surf_point = Vector((radius_0e*math.cos(lat_degrees)*math.cos(long_degrees),
                               radius_0e*math.cos(lat_degrees)*math.sin(long_degrees),
                               radius_0e*math.sin(lat_degrees),
    ))
    small_div_floor_3e = Vector((math.floor(small_surf_point[0] / 1000.0),
                                 math.floor(small_surf_point[1] / 1000.0),
                                 math.floor(small_surf_point[2] / 1000.0),
    ))
    small_6e = small_div_floor_3e / 1000.0
    small_0e = small_surf_point - small_div_floor_3e * 1000.0
    # add small radius adjustment to accumulator
    accum_6e = accum_6e + small_6e
    accum_0e = accum_0e + small_0e
    # implement addition carry operation from accum_0e to accum_6e
    carry_div_floor_3e = Vector((math.floor(accum_0e[0]/1000.0),
                                 math.floor(accum_0e[1]/1000.0),
                                 math.floor(accum_0e[2]/1000.0),
    ))
    accum_6e = accum_6e + carry_div_floor_3e / 1000.0
    accum_0e = accum_0e - carry_div_floor_3e * 1000.0
    # set locations of Big Space Rig bones to accumulator values
    big_space_rig.pose.bones[PROXY_OBSERVER_6E_BNAME].location = accum_6e
    big_space_rig.pose.bones[PROXY_OBSERVER_0E_BNAME].location = accum_0e
    # return to original view mode
    bpy.ops.object.mode_set(mode=old_3dview_mode)

def get_rad_from_deg_min_sec(degrees, minutes, seconds, frac_sec):
    # 648000 = 180 * 3600
    return (degrees * 3600 + minutes * 60 + seconds + frac_sec) * (math.pi / 648000.0)

def go_to_sphere_coords_dmsf(context, big_space_rig, radius_6e, radius_0e, lat_degrees, lat_minutes, lat_seconds,
                      lat_frac_sec, long_degrees, long_minutes, long_seconds, long_frac_sec):
    # get super-accurate (?) latitude/longitude from input degrees, minutes, seconds
    # Note:
    # 360 degrees in full circle, 60 minutes per degree, 60 seconds per minute, so total possible points on circle =
    #     360 * 60 * 60 = 1296000
    # 1,296,000 possible numbers
    # https://docs.python.org/3/tutorial/floatingpoint.html
    # double precision floating point has 1 part in 2 ** 53 bits usable/reliable
    # 2 ** 53 = 9007199254740992
    # 9,007,199,254,740,992 possible numbers
    # the difference in orders of magnitude indicates that degrees angle floating point error is not significant
    lat_rad = get_rad_from_deg_min_sec(lat_degrees, lat_minutes, lat_seconds, lat_frac_sec)
    long_rad = get_rad_from_deg_min_sec(long_degrees, long_minutes, long_seconds, long_frac_sec)
    go_to_sphere_coords_radians(context, big_space_rig, radius_6e, radius_0e, lat_rad, long_rad)

def go_to_sphere_coords_degrees(context, big_space_rig, radius_6e, radius_0e, lat_degrees, long_degrees):
    go_to_sphere_coords_radians(context, big_space_rig, radius_6e, radius_0e, lat_degrees*(math.pi/180.0),
                                long_degrees*(math.pi/180.0))

class BSR_ObserveMegaSphere(bpy.types.Operator):
    bl_description = "View MegaSphere (set Big Space Rig's Observer 6e and 0e location) by Radius, Longitude, " \
        "Latitude coordinates"
    bl_idname = "big_space_rig.view_mega_sphere_by_rad_lat_long"
    bl_label = "Go to Coordinates"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        big_space_rig = context.active_object
        if not is_big_space_rig(big_space_rig):
            self.report({'ERROR'}, "Unable to Go to Coordinates because active object is not a Big Space Rig")
            return {'CANCELLED'}
        scn = context.scene
        if scn.BSR_ObserveSphereAngleType == ANGLE_TYPE_DEG_MIN_SEC_FRAC:
            go_to_sphere_coords_dmsf(context, big_space_rig, scn.BSR_ObserveMegaSphereRad6e,
                scn.BSR_ObserveMegaSphereRad0e, scn.BSR_ObserveMegaSphereLatDMSF_Degrees,
                scn.BSR_ObserveMegaSphereLatDMSF_Minutes, scn.BSR_ObserveMegaSphereLatDMSF_Seconds,
                scn.BSR_ObserveMegaSphereLatDMSF_FracSec, scn.BSR_ObserveMegaSphereLongDMSF_Degrees,
                scn.BSR_ObserveMegaSphereLongDMSF_Minutes, scn.BSR_ObserveMegaSphereLongDMSF_Seconds,
                scn.BSR_ObserveMegaSphereLongDMSF_FracSec)
        elif scn.BSR_ObserveSphereAngleType == ANGLE_TYPE_DEGREES:
            go_to_sphere_coords_degrees(context, big_space_rig, scn.BSR_ObserveMegaSphereRad6e,
                scn.BSR_ObserveMegaSphereRad0e, scn.BSR_ObserveMegaSphereLatDegrees,
                scn.BSR_ObserveMegaSphereLongDegrees)
        elif scn.BSR_ObserveSphereAngleType == ANGLE_TYPE_RADIANS:
            go_to_sphere_coords_radians(context, big_space_rig, scn.BSR_ObserveMegaSphereRad6e,
                scn.BSR_ObserveMegaSphereRad0e, scn.BSR_ObserveMegaSphereLatRadians,
                scn.BSR_ObserveMegaSphereLongRadians)
        return {'FINISHED'}

def go_to_place(big_space_rig, place_bone_name):
    place_bone_name_6e, place_bone_name_0e = get_6e_0e_from_place_bone_name(big_space_rig, place_bone_name)
    big_space_rig.pose.bones[PROXY_OBSERVER_6E_BNAME].location = big_space_rig.pose.bones[place_bone_name_6e].location
    big_space_rig.pose.bones[PROXY_OBSERVER_0E_BNAME].location = big_space_rig.pose.bones[place_bone_name_0e].location

class BSR_ObservePlace(bpy.types.Operator):
    bl_description = "Set Observer to Place's coordinates (6e and 0e location)"
    bl_idname = "big_space_rig.observe_place"
    bl_label = "Observe Place"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        big_space_rig = context.active_object
        if not is_big_space_rig(big_space_rig):
            self.report({'ERROR'}, "Unable to Observe Place because active object is not a Big Space Rig")
            return {'CANCELLED'}
        scn = context.scene
        place_bone_name = scn.BSR_ObservePlaceBoneName[1:len(scn.BSR_ObservePlaceBoneName)]
        if place_bone_name == "":
            self.report({'ERROR'}, "Unable to Observe Place because Place to observe is blank")
            return {'CANCELLED'}
        go_to_place(big_space_rig, place_bone_name)
        return {'FINISHED'}

def add_obs_focus_copy_rig_location_drivers(big_space_rig):
    obs_focus_bone = big_space_rig.pose.bones.get(OBSERVER_FOCUS_BNAME)
    if obs_focus_bone is None:
        return None

    drv_loc_x = obs_focus_bone.driver_add("location", 0).driver
    v_obs_focus_x = drv_loc_x.variables.new()
    v_obs_focus_x.type = 'TRANSFORMS'
    v_obs_focus_x.name                 = "obs_focus_x"
    v_obs_focus_x.targets[0].id        = big_space_rig
    v_obs_focus_x.targets[0].transform_type = 'LOC_X'
    v_obs_focus_x.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_obs_focus_x.targets[0].data_path = "location.x"
    drv_loc_x.expression = v_obs_focus_x.name

    drv_loc_y = obs_focus_bone.driver_add("location", 1).driver
    v_obs_focus_y = drv_loc_y.variables.new()
    v_obs_focus_y.type = 'TRANSFORMS'
    v_obs_focus_y.name                 = "obs_focus_y"
    v_obs_focus_y.targets[0].id        = big_space_rig
    v_obs_focus_y.targets[0].transform_type = 'LOC_Y'
    v_obs_focus_y.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_obs_focus_y.targets[0].data_path = "location.y"
    drv_loc_y.expression = v_obs_focus_y.name

    drv_loc_z = obs_focus_bone.driver_add("location", 2).driver
    v_obs_focus_z = drv_loc_z.variables.new()
    v_obs_focus_z.type = 'TRANSFORMS'
    v_obs_focus_z.name                 = "obs_focus_z"
    v_obs_focus_z.targets[0].id        = big_space_rig
    v_obs_focus_z.targets[0].transform_type = 'LOC_Z'
    v_obs_focus_z.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_obs_focus_z.targets[0].data_path = "location.z"
    drv_loc_z.expression = v_obs_focus_z.name

    return drv_loc_x, drv_loc_y, drv_loc_z

class BSR_AddObsFocusDrivers(bpy.types.Operator):
    bl_description = "Add drivers to Observer Focus (of active Big Space Rig) to copy location of active Big Space Rig"
    bl_idname = "big_space_rig.add_obs_focus_drivers"
    bl_label = "Focus Rig Location"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        big_space_rig = context.active_object
        if not is_big_space_rig(big_space_rig):
            self.report({'ERROR'}, "Unable to Add Observer Focus Copy Rig Location Drivers because active object " +
                        "is not a Big Space Rig")
            return {'CANCELLED'}
        scn = context.scene
        add_obs_focus_copy_rig_location_drivers(big_space_rig)
        return {'FINISHED'}
