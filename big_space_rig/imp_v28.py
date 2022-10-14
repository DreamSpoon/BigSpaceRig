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

def get_cursor_location(context):
    # error check
    if context is None or context.scene is None or context.scene.cursor is None:
        return None
    return context.scene.cursor.location

def select_object(ob, s):
    ob.select_set(s == True)


def get_root_collection():
    # create an array of False values, one for each collection
    has_parent = {}
    for c in bpy.data.collections:
        has_parent[c] = False
    # do parent check for each collection
    for col in bpy.data.collections:
        for sub_col in col.children:
            has_parent[sub_col] = True
    # get the one item where "has parent" is False
    for d in has_parent:
        if not has_parent[d]:
            return d

def create_mesh_obj_from_pydata(verts=[], faces=[], edges=[], obj_name=None, mesh_name=None,
                                collection_name=None):
    if obj_name is None:
        obj_name = "Object"
    if mesh_name is None:
        mesh_name = obj_name

    mesh = bpy.data.meshes.new(mesh_name)
    obj = bpy.data.objects.new(obj_name, mesh)
    # check that a collection exists for this new mesh object
    if collection_name is None:
        col = get_root_collection()
    else:
        col = bpy.data.collections.get(collection_name)
        if col is None:
            col = get_root_collection()
    if col is None:
        return None
    # link object to a collection
    col.objects.link(obj)
    # set new object as the active object
    bpy.context.view_layer.objects.active = obj
    # create object mesh from input data
    mesh.from_pydata(verts, edges, faces)
    return obj

def set_object_hide(obj, hide_val):
    obj.hide_set(hide_val)
