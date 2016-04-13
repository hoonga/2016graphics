#include<stdio.h>
#include<iostream>
#include"trackball.h"

#define deg(x) ((x)*180/M_PI)
#define rad(x) ((x)*M_PI/180)

Trackball::Trackball(Camera *cam) : cam(cam)
{
    for (int i = 0; i < 3; i++){
        rel_cam_pos[i] = cam->pos[i] - pos[i];
    }
    R = Eigen::Vector3f(rel_cam_pos).norm()*tan(rad(cam->fov)/2);
    orient = Eigen::Quaternionf();
    orient.setIdentity();
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

// implemented by quaternions and matrixes
void Trackball::rotate(GLfloat start[3], GLfloat end[3])
{
    Eigen::Vector3f v = Eigen::Vector3f(start);
    Eigen::Vector3f u = Eigen::Vector3f(end);
    Eigen::Quaternionf cur_rot = Eigen::Quaternionf();
    cur_rot.setFromTwoVectors(u,v);
    Eigen::Matrix3f cur_rotm = cur_rot.toRotationMatrix();
    Eigen::Vector3f rel_pos = Eigen::Vector3f(rel_cam_pos);
    Eigen::Vector3f ori_pos = Eigen::Vector3f(0, 0, -rel_pos.norm());
    orient = orient*cur_rot;
    Eigen::Vector3f new_pos = orient*ori_pos;
    Eigen::Vector3f up = orient*Eigen::Vector3f(0,1,0);
    for (int i = 0; i < 3; i++)
    {
        rel_cam_pos[i] = new_pos[i];
        cam->up[i] = up[i];
    }
    setCam();
}

void Trackball::screenMov(int x, int y, int x2, int y2)
{
    Eigen::Vector3f O = Eigen::Vector3f(cam->pos);
    Eigen::Vector3f P = Eigen::Vector3f(cam->look);
    Eigen::Vector3f Z = (P - O).normalized();
    Eigen::Vector3f Y = Eigen::Vector3f(cam->up);
    Eigen::Vector3f X = Y.cross(Z).normalized();
    Eigen::Vector3f D = Eigen::Vector3f(X*(x-x2) + Y*(y-y2));
    translate(D[0], D[1], D[2]);
}

void Trackball::screenRot(int x, int y, int x2, int y2)
{
    GLfloat start[3], end[3];
    GLfloat Z = 100*R*R - x*x - y*y;
    GLfloat Z2 = 100*R*R - x2*x2 - y2*y2;
    if (Z < 0) {
        // outside of trackball
        GLfloat normalizer = 10*R/sqrt(100*R*R - Z);
        start[0] = x*normalizer;
        start[1] = y*normalizer;
        start[2] = 0;
    } else {
        // on track ball
        start[0] = x;
        start[1] = y;
        start[2] = -sqrt(Z);
    }
    if (Z2 < 0) {
        GLfloat normalizer = 10*R/sqrt(100*R*R - Z2);
        end[0] = x2*normalizer;
        end[1] = y2*normalizer;
        end[2] = 0;
    } else {
        end[0] = x2;
        end[1] = y2;
        end[2] = -sqrt(Z2);
    }
    rotate(start, end);
}

void Trackball::dolly(float depth)
{
    Eigen::Vector3f O = Eigen::Vector3f(cam->pos);
    Eigen::Vector3f P = Eigen::Vector3f(cam->look);
    Eigen::Vector3f Z = (P - O).normalized();
    O += Z*depth;
    R = (P - O).norm()*tan(rad(cam->fov)/2);
    Z = (O - P);
    for (int i = 0; i < 3; i++) {
        cam->pos[i] = O[i];
        rel_cam_pos[i] = Z[i];
    }
    cam->lookAt();
}

void Trackball::zoom(float degree)
{
    Eigen::Vector3f P = Eigen::Vector3f(rel_cam_pos);
    GLfloat fov = cam->fov + degree;
    cam->fov = fov > 12 ? (fov < 90 ? fov : 89) : 12;
    R = P.norm()*tan(rad(cam->fov)/2);
    cam->lookAt();
}

void Trackball::showAll()
{
    for(int i = 0; i < 3; i++) {
        pos[i] = 0;
    }
    Eigen::Vector3f P = Eigen::Vector3f(rel_cam_pos);
    P.normalize();
    P *= 100/tan(rad(cam->fov/2));
    R = P.norm()*tan(rad(cam->fov)/2);
    for (int i = 0; i < 3; i++)
        rel_cam_pos[i] = P[i];
    setCam();
}
