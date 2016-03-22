#include"shape.h"
#include<cmath>

class Cylinder : Shape {
    public:
        Cylinder(Node &node, GLfloat *color, GLfloat radius, GLfloat height,
                GLint slices, bool lids=true, GLfloat range=2*M_PI);
        virtual void draw();

    private:
        GLfloat color[3];
        GLfloat radius;
        GLfloat height;
        GLint slices;
        GLfloat range;
        bool lids;
        void draw_side();
        void draw_lids();
};

class Torus : Shape {
    public:
        Torus(Node &node, GLfloat *color, GLfloat rev_radius,
                GLfloat cir_radius, GLint sides, GLint rings,
                GLfloat rev_range=2*M_PI, GLfloat cir_range=2*M_PI);
        virtual void draw();

    private:
        GLfloat color[3];
        GLfloat rev_radius;
        GLfloat cir_radius;
        GLint sides;
        GLint rings;
        GLfloat rev_range;
        GLfloat cir_range;
};

class Box : Shape {
    public:
        Box(Node &node, GLfloat *color, GLfloat *xyz);
        virtual void draw();

    private:
        GLfloat color[3];
        GLfloat xyz[3];
};
