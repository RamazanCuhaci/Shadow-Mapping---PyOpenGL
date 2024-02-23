# Shadow-Mapping---PyOpenGL
Depth map shadow, spot lights and Blinn-Phong practice

## Installing Notes: 
- On Windows install PyOpenGL and PyOpenGL-accelerate by downlading packages from: http://www.lfd.uci.edu/~gohlke/pythonlibs 
- Installing them as: pip install [package-name]. This is needed as official pip repo does not have glut in it.

## The summary for program below:
    
- One on the left side  above object looking down on objects and the other one in front of all the object in slightly higher position looking down on objects.
- The one at the front of objects move side to side paralle to x axis in a left right sinusoidal pattern.
- The other spotlight rotate around a circle always looking at the center point of the scene which is centered below the tree object.
- Calculate shadow maps for both lights.
- Shadows of both spotlights switchable by the user using "1" and "2" keys so that we can render the scene with shadow maps or not.
- Another ambient light which has a constant intensity for the whole scene.
- The animation of the spotlights should be able to be switched on or off by the user with key press "a".



https://github.com/RamazanCuhaci/Shadow-Mapping---PyOpenGL/assets/45862194/f07935d7-22b6-4c70-92b5-b17cb886c779




## Key Configuration
----------------
- Hit ESC key to quit.
- Alt + Left Mouse Button: Rotation around center of the object
- Alt + Right Mouse Button: Zoom in and out
- F key to reset view
- 1 key to on/off Spot Light 1's depth map
- 2 key to on/off Spot Light 2's depth map
- Q key to on/off Spot Light 1
- W key to on/off Spot Light 2
- A key to on/off animation of Spot Light 1
- S key to on/off animation of Spot Light 2
- B key to on/off Blinn's specular
