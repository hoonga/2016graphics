#include"drawable.h"

Drawable::Drawable(GLfloat *color)
{
    for(int i = 0; i < 4; i++) {
        this->color[i] = color[i];
    }
}

Cylinder::Cylinder(GLfloat *color, GLfloat radius, GLfloat height,
        GLint slices, bool lids, GLfloat range)
    : Drawable(color), radius(radius), height(height), slices(slices)
    , lids(lids), range(range)
{
}

void Cylinder::draw()
{
    if(height)
        draw_side();
    if(lids)
        draw_lids();
}

void Cylinder::draw_side()
{
    // for a more intuitive rotation, center of the cylinder will be 0,0,0
    // so all the points should be drawn at +/-(0.5)height
    // t is short for theta, dt is short for delta theta, a slice,
    // r is a short for radius
    GLfloat h = 0.5*height;
    GLfloat t = -0.5*range;
    GLfloat dt = range/slices;
    GLfloat r = radius;

    glColor3fv(color);
    glBegin(GL_TRIANGLE_STRIP);
    for (; t <= 0.5*range; t += dt) {
        glVertex3f(r*cos(t), r*sin(t), h);
        glVertex3f(r*cos(t), r*sin(t), -h);
    }
    glEnd();
}

void Cylinder::draw_lids()
{
    // since the center is at 0,0,0 h=+-(0.5)height
    // t is theta, dt is delta theta, r is radius
    GLfloat h = 0.5*height;
    GLfloat t = -0.5*range;
    GLfloat dt = range/slices;
    GLfloat r = radius;

    glColor3fv(color);

    // top
    glBegin(GL_TRIANGLE_FAN);
    glVertex3f(0, 0, h);
    for(; t <= 0.5*range; t += dt)
        glVertex3f(r*cos(t), r*sin(t), h);
    glEnd();

    // if no height, top is all we need
    if(!height)
        return;

    // bottom
    glBegin(GL_TRIANGLE_FAN);
    glVertex3f(0, 0, -h);
    for(t = -0.5*range; t <= range; t += dt)
        glVertex3f(r*cos(t), r*sin(t), -h);
    glEnd();
}

Torus::Torus(GLfloat *color, GLfloat rev_radius, GLfloat cir_radius,
        GLint sides, GLint rings, GLfloat rev_range, GLfloat cir_range)
    : Drawable(color), rev_radius(rev_radius), cir_radius(cir_radius)
    , sides(sides), rings(rings), rev_range(rev_range), cir_range(cir_range)
{
}

void Torus::draw()
{
    GLfloat R = rev_radius;
    GLfloat r = cir_radius;
    GLfloat t = -0.5*rev_range;
    GLfloat dt = rev_range/rings;
    GLfloat w = -0.5*cir_range;
    GLfloat dw = cir_range/sides;

    glColor3fv(color);
    for(; t <= 0.5*rev_range; t += dt) {
        glBegin(GL_TRIANGLE_STRIP);
        for(w = -0.5*cir_range; w <= 0.5*cir_range; w += dw) {
            glVertex3f(R*cos(t) + r*cos(w), R*sin(t), r*sin(w));
            glVertex3f(R*cos(t) + r*cos(w), R*sin(t+dt), t*sin(w));
        }
        glEnd();
    }
}

Box::Box(GLfloat *color, GLfloat *xyz) : Drawable(color)
{
    for(int i = 0; i < 3; i++) {
        this->xyz[i] = xyz[i];
    }
}

void Box::draw()
{
    GLfloat x = xyz[0];
    GLfloat y = xyz[1];
    GLfloat z = xyz[2];
    glColor3fv(color);
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
}
