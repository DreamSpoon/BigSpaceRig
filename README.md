# Big Space Rig addon for Blender 3.1+
"Solar system in a box" addon for Blender, with functions to create/manage procedural planets.
- rig to manage very large spaces (> 10^30 m3)
  - manages "floating point error" for the user
  - small and large geometry can be precisely positioned within volumes large enough to hold "planet" sized geometry
    - e.g. 1000 km radius sphere
- geometry nodes to create very large procedural objects, e.g.
  - MegaSphere - a 1000 km radius (or larger) procedural icosphere, with subdivisions for use at sub-meter scale
- 'forced perspective' effect (optional, per Place)
  - create 'condensed space' for viewing large objects that are separated by very large distances, at correct scale (e.g. planets, moons, stars)
  - "Forced perspective is a technique which employs optical illusion to make an object appear farther away, closer, larger or smaller than it actually is. It manipulates human visual perception through the use of scaled objects and the correlation between them and the vantage point of the spectator or camera."
    - https://en.wikipedia.org/wiki/Forced_perspective

### Video Tutorial
Make a Desert Planet in 20 Minutes with Big Space Rig addon for Blender 3.1+
https://youtu.be/aXeRPgVCTGg/

## Install Addon in Blender
1) Start Blender
2) Go to User Preferences -> Addons -> Install addon from file
3) Choose BigSpaceRig.zip file you downloaded (available for download from 'Releases' section of this website)

Done! The addon is now installed, but **you need to enable it by clicking the checkbox beside it's name**, in the addons window.

## Overview
The addon uses a "proxy-actual" system. This allows the user to place objects at very large distances apart, using proxies to relate a small "proxy" place to a large "actual" place.
E.g. a 1 : 1,000,000 scale proxy, where a movement of 1 meter in any direction equals an "actual" movement of 1,000,000 meters (thousand kilometers).

Example, with Forced Perspective effect used:
  - a "place" is created at the center, objects are added to the place (in Blender speak, the objects are "parented" to the place)
  - the "observer" is moved 10,000 units away and a new "place" is created
  - when the observer is moved, the original "place" is moved away, and the place is scaled using "forced perspective" effect
  - the new "place" has objects added (i.e. parented to the "place")
  - the "observer" can now be moved between "places", and the objects will always look like they are the right size - even though they are actually much closer together
  - the distance between "places" is compressed, and the "observer" is used to determine the scale of each "place"
  - when the "observer" is positioned exactly at the same location as the "place", then the place be full scale (i.e. one-to-one scale)

The main method of moving around within the rig is to move the ProxyObserver0e and ProxyObserver6e bones.
Moving the ProxyObserver0e bone results in the rig's Places moving to offset the observer's movements.
E.g. if the ProxyObserver0e moves +1 along the Y axis, then all the rig's Places move -1 along the Y axis.
Name notes:
  - "6e" means one million, because base 10 to the power of 6 (to the exponent 6)
    - equals 1,000,000
  - "0e" means one, because base 10 to the power of 0 (to the exponent 0)
    - equals 1

## General Rig Notes
- *do NOT rename the following rig bones, or some rig functionality may be broken:*
  - ProxyObserver0e
  - ProxyObserver6e
  - ObserverFocus
- the following rig bones can be renamed, to organize the rig as needed (only the "Place" bones)
  - ProxyPlace0e
  - ProxyPlace6e
  - Place

## Mega Sphere Notes
With a Big Space Rig created and selected first, a mega-meter size sphere (MegaSphere) can be added to the scene. The sphere object is procedural geometry, and it can be edited in the Geometry Node Editor.

MegaSphere Geometry Nodes node group has the following inputs:
  - Icosphere7
    - Icosphere mesh object with subivision level 7
	- optional, to reduce geometry generation time
	- used as a base to create sphere surface
  - Mega Sphere Radius
    - sphere radius, in mega-meters (1 = 1000000 meters)
  - Subdivision Scale
    - increasing this value will increase the number of subdivisions, up to the current max of 27
	  - some special cases apply, like when the observer is "under" the surface of the sphere
	  - increasing to 15 (or higher) is a current workaround to fix a bug where the landscape does not generate subdivisions properly
  - Max Subdivisions
    - maximum number of subdivisions to apply to icosphere, up to the internal maximum of 27
	- anything over 27 produces the same result as a value of 27
  - Vis Angle Adjust
    - modifies how much sphere geometry is backface-culled
      - enter positive values to reduce the amount of geometry,
	  - enter negative values to increase the amount of geometry
	- start testing with small values, like -0.001, because this is a cosine value (between -1 and +1)
	  - small values can result in large changes
  - Cull Distance
    - maximum distance, from Observer, of geometry faces that result from sphere generation
	- e.g. set to a value of 100 to keep only faces within 100 meters of the Observer (armature center (0, 0, 0) of Big Space Rig)
  - Max Faces
    - maximum number of faces allowed to be generated by the node group
	- originally intended as a way to avoid crashing Blender with incredibly high face counts from too many subidivions
	- increase this value if the "Max Subdivisions" value seems to be having a problem (e.g. not enough subdivisions, even with high "Subdivision Scale" values
      - frequently needs increasing to values of 128000 or higher
	- this is not a *hard* maximum, the actual number of faces might be a bit higher
	  - tests have shown face counts 2 times as high as this value
  - Observer 6e Loc
    - Vector
    - the mega-meter scale Observer location
  - Observer 0e Loc
    - Vector
    - the meter scale Observer location

MegaSphere Geometry Nodes node group has the following outputs:
  - Geometry
    - the portion of sphere surface geometry generated, after subdivisions and backface/distance culling
  - MegaSphere Normal
    - Vector attribute
    - the "up" direction at each point on the sphere's surface
    - interpolated across faces, so this value is extremely smooth across all of sphere's surface, even if not 100% accurate (due to floating-point error)
  - LOD Inner Verts
    - Value attribute, between 0 and 1
	- "inside" of each LOD ring is marked with a 1 in this attribute
	- all other vertices have a value of 0 in this attribute
	- used by Snap Vertex LOD to "stitch together" different LOD rings
  - LOD Outer Verts
    - Value attribute, between 0 and 1
	- "outside" of each LOD ring is marked with a 1 in this attribute
	- all other vertices have a value of 0 in this attribute
	- used by Snap Vertex LOD to "stitch together" different LOD rings
  - LOD Index
    - subdivision value index of each LOD ring
	- testing with this value shows that it varies by 0.5
	  - any checks against this value
	    - e.g. if > 11
      - should be modified by 0.5
	    - e.g. if > 11.5
	  - test it, don't assume!
  - Max Face Count
    - Boolean
	- True only if attempt was made to subdivide mesh and attempt failed because maximum number of faces was reached
	- result of node group's operations, not an attribute of Geometry

Note: LOD means Level Of Detail

## Forced Perspective Notes
The scale of each "place" can be individually adjusted, with the distance automatically adjusting to account for the scale difference.
i.e. "place" have it's scale set manually and the Big Space Rig will automatically vary the distance to account for the scale of that "place".
  - to do the manual adjustment, go to the custom property of the "Place" bone, i.e.
    - enter Pose mode
	- select the "Place" bone
	- look in "Bone" settings panel
	    - Custom Properties sub-panel
		  - big_space_rig_bone_scl_mult
    - increase the "big_space_rig_bone_scl_mult" value to make the "place" larger
	  - "place" will move farther away from observer, to compensate for larger scale
	- decrease the "big_space_rig_bone_scl_mult" value to make the "place" smaller
	  - "place" will move closer away from observer, to compensate for smaller scale

The "forced perspective" effect for all objects in an armature can be easily disabled by setting the Big Space Rig object's custom property "big_space_rig_fp_power" to the value 0 (zero).
The default setting of "big_space_rig_fp_power" is 0.5 (square root), which results in objects shrinking very fast as they move away from the observer.
  - good for very large spaces
    - e.g. Solar System

Setting "big_space_rig_fp_power" to 0.25, or less, results in objects shrinking as they move very far away from the observer - but the "forced perspective" effect comes on in a less dramatic fashion - i.e. less "warping" of space.
  - better suited to "earth satellite scale"
    - e.g. giant space ships parked in Earth's orbit

### Geometry Nodes Notes
Forced Perspective Geometry Nodes:
- objects must be attached to a Big Space Rig before Geometry Nodes can be added to them

### Light and Shadow Notes
When Forced Perspective scaling is used, shadows between objects may be "wrong".
Possible solutions include, but are not limited to:
  - use of the "Sun" type of light can help overcome the problem
    - good where objects have common light source, but don't need to shadow each other
	- e.g. moon and planets, without eclipse
	  - an eclipse might be "baked" onto an object, see next
  - baked (pre-rendered) "shadow maps"
    - too complicated a subject to list all the details here, so here is just one link:
      - [Baking Textures, Light, and Shadows | Blender 2.82 Quarantine Series 1-12](https://www.youtube.com/watch?v=Eio01Yl3G1E)
      - and baked shadow maps can be used in Cycles:
        - modify original Material Shader of object (make a backup copy first):
          - use Texture Image node with original texture (e.g. 8k map of Moon),
          - attach original Texture Image node (Color socket) to Emission shader node (Color socket),
          - use Texture Image node with baked shadow map texture,
		  - attach baked shadow map Texture Image (Color socket) to Emission shader node (Strength socket),
          - attach Emission Shader output to Material Output
  - multiple render passes (compositor work required)
    - may require multiple scenes, composited together
