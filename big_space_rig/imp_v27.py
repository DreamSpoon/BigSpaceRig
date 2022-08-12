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
    if context is None or context.scene is None:
        return None
    return context.scene.cursor_location

def select_object(ob, s):
    ob.select = s == True

def create_mesh_obj_from_pydata(verts=[], faces=[], edges=[], obj_name=None, mesh_name=None):
    if obj_name is None:
        obj_name = "Object"
    if mesh_name is None:
        mesh_name = obj_name

    mesh = bpy.data.meshes.new(mesh_name)
    obj = bpy.data.objects.new(obj_name, mesh)
    bpy.context.scene.objects.link(obj)
    bpy.context.scene.objects.active = obj
    obj.select = True
    mesh = bpy.context.object.data

    verts_list = []
    bm = bmesh.new()
    for v in verts:
        new_v = bm.verts.new(v)
        verts_list.append(new_v)
    for e in edges:
        edge_verts = [verts_list[v_index] for v_index in e]
        bm.edges.new(edge_verts)
    for f in faces:
        face_verts = [verts_list[v_index] for v_index in f]
        bm.faces.new(face_verts)
    bm.to_mesh(mesh)
    bm.free()

    return obj
