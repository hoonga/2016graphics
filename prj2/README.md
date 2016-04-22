#Way to compile

This tar has a Makefile.
use 'make run' to compile and run ELF

#commands
## rotation
just left-click and drag


## translation
just right-click and drag

## zoom
press key '=' to zoom in
press key '-' to zoom out
press key ']' to zoom faster
press key '[' to zoom slower

##dolly
press key '+' or shift+'=' to dolly in
press key '_' or shift+'-' to dolly out
press key '}' or shift+']' to dolly faster
press key '{' or shift+'[' to dolly slower

##show all
press spacebar

##reset camera
press enter

##seek
not implemented

#implementation
## class Camera
has fov, position, where it looks, and an up vector

## class Trackball
has a Camera, position, position of cam relative to the center
the Camera attached always look at the center of the ball, keeps relative coordinate except for rotations and dolly-in/out
when rotation, 2 coordinates on the ball is calculated from screen coordinates.
2 coordinates can be thought as vectors, and again quaternions.
With the help of Eigen math library, we calculate rotations with quaternions.
When translation, we change the world coordinate position of the ball, which is calculated through camera's coordinate system.
Dolly-in/out was done equally.
Zooms are implemented by changing cam's fov value, which then alters the projection matrix.
Show all is implemented by positioning the trackball's world coordinate to (0,0,0), pulling the camera back regarding the fov.
