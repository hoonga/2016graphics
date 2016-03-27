#include<GL/gl.h>
#include<GL/glu.h>
#include<GL/glut.h>
#include<cmath>

/*
 * Shape
 * a drawable shape
 * has coords
 * self coords
 * shape
 */

class Shape {
    public:
        Shape(GLfloat *coord, GLfloat *color);
        virtual void draw() = 0;
        virtual void rotate(GLfloat angle, GLfloat x, GLfloat y, GLfloat z);
        virtual void translate(GLfloat x, GLfloat y, GLfloat z);
        virtual void paint(GLfloat *color);
    protected:
        GLfloat coord[3];
        GLfloat color[4];
        GLfloat rotation[4];
};

class Cylinder : public Shape {
    public:
        Cylinder(GLfloat *coord, GLfloat *color, GLfloat radius, GLfloat height,
                int slices, bool lids=true, GLfloat range=2*M_PI);
        virtual void draw();

    private:
        GLfloat radius;
        GLfloat height;
        GLfloat range;
        int slices;
        bool lids;
};

class Torus : public Shape {
    public:
        Torus(GLfloat *coord, GLfloat *color, GLfloat R, GLfloat r, int slices,
                int rings, GLfloat R_range=2*M_PI, GLfloat r_range=2*M_PI);
        virtual void draw();

    private:
        GLfloat R;
        GLfloat r;
        int slices;
        int rings;
        GLfloat R_range;
        GLfloat r_range;
};
