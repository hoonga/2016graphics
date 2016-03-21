#include<GL/gl.h>
#include<GL/glu.h>
#include<GL/freeglut.h>
#include<cmath>
#include<algorithm>

#include"node.h"

void resize();
void display();

int main(int argc, char** argv) {
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH);
    glutInitWindowSize(800,600);
    glutInitWindowPosition(0,0);
    glutCreateWindow("GLaDOS");

    glutReshapeFunc(resize);
    glutDisplayFunc(display);
}
