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

from .rig import (is_big_space_rig, create_bsr_armature)
from .mega_sphere import create_mega_sphere
from .observer import go_to_sphere_coords_degrees

class BSR_EasyCreateLandscapeNoise(bpy.types.Operator):
    bl_description = "Create a Landscape with Noise with Big Space Rig and MegaSphere with Noise"
    bl_idname = "big_space_rig.easy_create_landscape_noise"
    bl_label = "Landscape Noise"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scn = context.scene
        active_ob = context.active_object
        # create a Big Space Rig if needed
        if not is_big_space_rig(active_ob):
            create_bsr_armature(context, scn.BSR_NewObserverFP_Power, scn.BSR_NewObserverFP_MinDist,
                                scn.BSR_NewObserverFP_MinScale)
            # new active object
            active_ob = context.active_object
        # get ready to view pole of sphere
        go_to_sphere_coords_degrees(context, active_ob, 1.0, 0.0, 90.0, 0.0)
        # create sphere
        create_mega_sphere(context, active_ob, 1.0, scn.BSR_NodesOverrideCreate, True, "")
        return {'FINISHED'}
