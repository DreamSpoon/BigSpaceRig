# Big Space Rig addon for Blender
"Solar system in a box" addon for Blender, with rig to manage very large spaces (> 10^30 m3), and geometry nodes to create very large procedural objects. Also, a 'forced perspective' effect (optional, per Place) to create 'condensed space' for viewing large objects that are separated by very large distances, at correct scale (e.g. planets, moons, stars).

"Forced perspective is a technique which employs optical illusion to make an object appear farther away, closer, larger or smaller than it actually is. It manipulates human visual perception through the use of scaled objects and the correlation between them and the vantage point of the spectator or camera."
- https://en.wikipedia.org/wiki/Forced_perspective

TODO: Use images in the explanation. YouTube video also coming soon, this is hard to explain with words...

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

## Light and Shadow Notes
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

## General Rig Notes
- *do NOT rename the following rig bones, or some rig functionality may be broken:*
  - ProxyObserver0e
  - ProxyObserver6e
  - ObserverFocus
- the following rig bones can be renamed, to organize the rig as needed
  - ProxyPlace0e
  - ProxyPlace6e

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

# Geometry Nodes Notes
Forced Perspective Geometry Nodes:
- objects must be attached to a Big Space Rig before Geometry Nodes can be added to them
