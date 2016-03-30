#include"shape.h"
#include<stdio.h>

#define rad(x) ((x)*M_PI/180)

Shape::Shape(GLfloat *coord, GLfloat *color)
{
    for (int i = 0; i < 3; i++) {
        this->coord[i] = coord[i];
        this->color[i] = color[i];
        rotation[i] = 0;
    }
    this->color[3] = color[3];
    rotation[3] = 0;
}

void Shape::rotate(GLfloat angle, GLfloat x, GLfloat y, GLfloat z)
{
    rotation[0] = angle;
    rotation[1] = x;
    rotation[2] = y;
    rotation[3] = z;
}

void Shape::translate(GLfloat x, GLfloat y, GLfloat z)
{
    coord[0] = x;
    coord[1] = y;
    coord[2] = z;
}

void Shape::paint(GLfloat *color)
{
    for (int i = 0; i < 4; i++)
        this->color[i] = color[i];
}

void Shape::initDraw()
{
    glColor4fv(color);
    glPushMatrix();
    glRotatef(rotation[0], rotation[1], rotation[2], rotation[3]);
    glTranslatef(coord[0], coord[1], coord[2]);
}

void Shape::endDraw()
{
    glPopMatrix();
}

Cylinder::Cylinder(GLfloat *coord, GLfloat *color, GLfloat radius, GLfloat height,
        int slices, bool lids, GLfloat range)
    : Shape(coord, color), radius(radius), slices(slices), lids(lids)
      , range(range), height(height)
{
}

void Cylinder::draw()
{
    initDraw();
    if(!radius)
        return;
    if(height)
        drawSide();
    if(lids)
        drawLid();
    endDraw();
}

void Cylinder::drawSide()
{
    GLfloat h = 0.5*height;
    GLfloat t = -0.5*range;
    GLfloat dt = range/slices;
    GLfloat r = radius;

    glBegin(GL_TRIANGLE_STRIP);
    for (; t <= 0.5*range; t += dt) {
        glVertex3f(r*sin(rad(t)), h, r*cos(rad(t)));
        glVertex3f(r*sin(rad(t)), -h, r*cos(rad(t)));
    }
    glEnd();
}

void Cylinder::drawLid()
{
    GLfloat h = 0.5*height;
    GLfloat t = -0.5*range;
    GLfloat dt = range/slices;
    GLfloat r = radius;

    // top
    glBegin(GL_TRIANGLE_FAN);
    glVertex3f(0, h, 0);
    for(; t <= 0.5*range; t += dt)
        glVertex3f(r*sin(rad(t)), h, r*cos(rad(t)));
    glEnd();

    // no height == only top
    if(!height)
        return;

    // bottom
    glBegin(GL_TRIANGLE_FAN);
    glVertex3f(0, -h, 0);
    for(t = -0.5*range; t <= range; t += dt)
        glVertex3f(r*sin(rad(t)), -h, r*cos(rad(t)));
    glEnd();
}

Torus::Torus(GLfloat *coord, GLfloat *color, GLfloat R, GLfloat r, int slices,
        int rings, GLfloat R_range, GLfloat r_range)
    : Shape(coord, color), R(R), r(r), slices(slices), rings(rings)
      , R_range(R_range), r_range(r_range)
{
}

void Torus::draw()
{
    initDraw();
    GLfloat t = -0.5*R_range;
    GLfloat dt = R_range/rings;
    GLfloat w = -0.5*r_range;
    GLfloat dw = r_range/slices;

    for(; t <= 0.5*R_range; t += dt) {
        glBegin(GL_TRIANGLE_STRIP);
        for(w = -0.5*r_range; w <= 0.5*r_range; w += dw) {
            glVertex3f(sin(rad(t))*(R + r*cos(rad(w))), r*sin(rad(w)), cos(rad(t))*(R + r*cos(rad(w))));
            glVertex3f(sin(rad(t+dt))*(R + r*cos(rad(w))), r*sin(rad(w)), cos(rad(t+dt))*(R + r*cos(rad(w))));
        }
        glEnd();
    }
    endDraw();
}

Box::Box(GLfloat *coord, GLfloat *color, GLfloat *xyz) : Shape(coord, color)
{
    for (int i = 0; i < 3; i++)
        this->xyz[i] = xyz[i];
}

void Box::draw()
{
    initDraw();
    GLfloat x = xyz[0];
    GLfloat y = xyz[1];
    GLfloat z = xyz[2];
    glBegin(GL_TRIANGLE_STRIP);

    glVertex3f(x, y, z);
    glVertex3f(x, y, -z);
    glVertex3f(-x, y, -z);
    glVertex3f(-x, y, z);
    glVertex3f(-x, -y, z);
    glVertex3f(-x, -y, -z);
    glVertex3f(x, -y, -z);
    glVertex3f(-x, y, -z);
    glVertex3f(x, y, -z);
    glVertex3f(x, -y, z);
    glVertex3f(-x, -y, z);
    glVertex3f(x, y, z);
    glVertex3f(x, -y, -z);
    glEnd();
    endDraw();
}
