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
        virtual void scale(GLfloat x, GLfloat y, GLfloat z);
        virtual void lighting(GLint light);

    protected:
        void initDraw();
        void endDraw();

        GLfloat coord[3];
        GLfloat color[4];
        GLfloat rotation[4];
        GLfloat scales[3] = {1, 1, 1};
        GLint light = GL_LIGHT0;
};

class Cylinder : public Shape {
    public:
        Cylinder(GLfloat *coord, GLfloat *color, GLfloat radius, GLfloat height,
                int slices, bool lids=true, GLfloat range=360);
        virtual void draw();

    private:
        void drawLid();
        void drawSide();

        GLfloat radius;
        GLfloat height;
        GLfloat range;
        int slices;
        bool lids;
};

class Torus : public Shape {
    public:
        Torus(GLfloat *coord, GLfloat *color, GLfloat R, GLfloat r, int slices,
                int rings, GLfloat R_range=360, GLfloat r_range=360);
        virtual void draw();

    private:
        GLfloat R;
        GLfloat r;
        int slices;
        int rings;
        GLfloat R_range;
        GLfloat r_range;
};

class Box : public Shape {
    public:
        Box(GLfloat *coord, GLfloat *color, GLfloat *xyz);
        virtual void draw();
};
