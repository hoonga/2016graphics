#include"cam.h"

Camera::Camera()
{
    pos[0] = 0;
    pos[1] = 0;
    pos[2] = -10;
}

Camera::Camera(GLfloat pos[3])
{
    for (int i = 0; i < 3; i++)
        this->pos[i] = pos[i];
}

void Camera::look()
{
    gluLookAt(pos[0], pos[1], pos[2],
            lookAt[0], lookAt[1], lookAt[2],
            up[0], up[1], up[2]);
}

