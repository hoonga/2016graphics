#include"shape.h"
#include<cmath>

class Drawable {
    protected:
        GLfloat color[4];

    public:
        Drawable(GLfloat *color);
        virtual void draw() = 0;
};

class Cylinder : Drawable {
    public:
        Cylinder(GLfloat *color, GLfloat radius, GLfloat height, GLint slices,
                bool lids=true, GLfloat range=2*M_PI);
        virtual void draw();

    private:
        GLfloat radius;
        GLfloat height;
        GLint slices;
        GLfloat range;
        bool lids;
        void draw_side();
        void draw_lids();
};

class Torus : Drawable {
    public:
        Torus(GLfloat *color, GLfloat rev_radius, GLfloat cir_radius,
                GLint sides, GLint rings, GLfloat rev_range=2*M_PI,
                GLfloat cir_range=2*M_PI);
        virtual void draw();

    private:
        GLfloat rev_radius;
        GLfloat cir_radius;
        GLint sides;
        GLint rings;
        GLfloat rev_range;
        GLfloat cir_range;
};

class Box : Drawable{
    public:
        Box(GLfloat *color, GLfloat *xyz);
        virtual void draw();

    private:
        GLfloat xyz[3];
};
