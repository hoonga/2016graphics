#include<GL/gl.h>
#include<GL/glu.h>
#include<GL/glut.h>

/*
 * first rotate
 * then translate
 */
class Branch {
    public:
        Branch(GLfloat *translation, GLfloat *rotation);
        GLfloat translation[3];
        GLfloat rotation[4];
};
