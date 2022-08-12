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
import bmesh

def get_cursor_location(context):
    # error check
    if context is None or context.scene is None or context.scene.cursor is None:
        return None
    return context.scene.cursor.location

def select_object(ob, s):
    ob.select_set(s == True)

def create_mesh_obj_from_pydata(verts=[], faces=[], edges=[], obj_name=None, mesh_name=None,
                                collection_name="Collection"):
    if obj_name is None:
        obj_name = "Object"
    if mesh_name is None:
        mesh_name = obj_name

    mesh = bpy.data.meshes.new(mesh_name)
    obj = bpy.data.objects.new(obj_name, mesh)
    col = bpy.data.collections.get(collection_name)
    col.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    mesh.from_pydata(verts, edges, faces)
    return obj
