#include"cam.h"

Camera::Camera()
{
    pos[0] = 0;
    pos[1] = 0;
    pos[2] = -100;
}

Camera::Camera(GLfloat pos[3])
{
    for (int i = 0; i < 3; i++)
        this->pos[i] = pos[i];
}

void Camera::lookAt()
{
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    gluLookAt(pos[0], pos[1], pos[2],
            look[0], look[1], look[2],
            up[0], up[1], up[2]);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluPerspective(fov, aspect, .1, 1000);
    glMatrixMode(GL_MODELVIEW);
}

