#include"trackball.h"

Trackball::Trackball(Camera *cam) : cam(cam)
{
}

void Trackball::setCam()
{
    for (int i = 0; i < 3; i++) {
        cam->pos[i] = pos[i] + rel_cam_pos[i];
        cam->look[i] = pos[i];
    }
    cam->lookAt();
}

void Trackball::translate(GLfloat dx, GLfloat dy, GLfloat dz)
{
    pos[0] += dx;
    pos[1] += dy;
    pos[2] += dz;
    setCam();
}

// implemented by quaternions
void Trackball::rotate(GLfloat start[3], GLfloat end[3])
{
}

void Trackball::screenMov(int x, int y, int dx, int dy)
{
}

void Trackball::screenRot(int x, int y, int dx, int dy)
{
}
