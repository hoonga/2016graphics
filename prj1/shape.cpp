#include "shape.h"

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
    coord[0] += x;
    coord[1] += y;
    coord[2] += z;
}

void Shape::paint(GLfloat *color)
{
    for (int i = 0; i < 4; i++)
        this->color[i] = color[i];
}

Cylinder::Cylinder(GLfloat *coord, GLfloat *color, GLfloat radius, int slices,
                    bool lids, GLfloat range)
        : Shape(coord, color), radius(radius), slices(slices), lids(lids)
          , range(range)
{
}

void Cylinder::draw()
{
}

Torus::Torus(GLfloat *coord, GLfloat *color, GLfloat R, GLfloat r, int slices,
            GLfloat R_range, GLfloat r_range)
        : Shape(coord, color), R(R), r(r), slices(slices), R_range(R_range)
          , r_range(r_range)
{
}

void Torus::draw()
{}
