#include"node.h"
#include<stdio.h>

#define rad(x) ((x)*M_PI/180)
void reshape(int, int);
void display();
void timer(int);
void keyboard(unsigned char, int, int);
void mouse(int, int, int, int);
void motion(int, int);

unsigned int time_step = 50;

Node *root;

// predef for shapes
GLfloat WHITE[4] = {1, 1, 1, 1};
GLfloat BLACK[4] = {0.1, 0.1, 0.1, 1};
GLfloat GRAY[4] = {0.3, 0.3, 0.3, 1};
GLfloat RED[4] = {1, 0, 0, 0};
GLfloat BLUE[4] = {0, 0, 1, 1};
GLfloat GREEN[4] = {0, 1,0, 1};
GLfloat O[3] = {0, 0, 0};
int SLICES = 50;
int RINGS = 50;

// cam postions
GLfloat cam_x = 0, cam_y = -40, cam_z = 100;
GLfloat rotx = 0, roty = 0, rotz = 0;

int main(int argc, char **argv)
{
    // Init procedure
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_DOUBLE|GLUT_RGBA|GLUT_DEPTH);
    glutInitWindowSize(800, 600);
    glutInitWindowPosition(0,0);
    glutCreateWindow("GLaDOS");

    // create glados
    GLfloat t0[3] =  {0, 0, 0};
    GLfloat r0[4] = {0,};
    Branch *inital_position = new Branch(t0, r0);
    root = new Node();
    root->parent = inital_position;

    // base rings, center cylinder
    for (int i = 0; i < 4; i++) {
        for (int j = 0; j < 4; j++){
            Torus *t = new Torus(O, WHITE, 40, 4, SLICES, RINGS, 80);
            t->rotate(j*90, 0, 1, 0);
            root->shapes.push_back(t);
        }
        root->shapes.push_back(new Torus(O, BLACK, 40, 3.5, SLICES, RINGS));
        O[1] -= 10;
    }
    O[1] = -20;
    root->shapes.push_back(new Cylinder(O, BLACK, 10, 50, SLICES));
    O[1] = 0;

    // begining of body
    GLfloat t1[3] = {0, -45, 0};
    GLfloat r1[4] = {0, 0, 1, 0};
    Node *joint1 = new Node(root, t1, r1);
    r1[0] = -180;
    t1[1] = -10;
    Node *cable_node = new Node(joint1, t1, r1);
    Torus *cable = new Torus(O, GRAY, 15, 3.5, SLICES, RINGS, 100);
    cable->rotate(90, 0, 0, 1);
    cable_node->shapes.push_back(cable);

    // upper body
    Node *upper_body = new Node(cable_node, t1, r1);
    Cylinder *ubody_c = new Cylinder(O, GREEN, 10, 8, SLICES);
    ubody_c->rotate(90, 0, 0, 1);
    Torus *ubody_t = new Torus(O, GREEN, 10, 5, SLICES, RINGS);
    ubody_t->rotate(90, 0, 0, 1);
    Torus *ubody_plate = new Torus(O, GREEN, 12, 7.5, SLICES, RINGS, 120, 180);
    ubody_plate->rotate(90, 0, 0, 1);
    upper_body->shapes.push_back(ubody_plate);
    upper_body->shapes.push_back(ubody_c);
    upper_body->shapes.push_back(ubody_t);

    // lower body
    GLfloat t2[3] = {0, -5, 0};
    GLfloat r2[4] = {0, 1, 0, 0};
    Node *joint2 = new Node(upper_body, t1, r2);
    Node *lower_body = new Node(joint2, t2, r0);
    lower_body->shapes.push_back(new Cylinder(O, WHITE, 5, 10, SLICES));
    Torus *lbody_plate = new Torus(O, WHITE, 5, 5, SLICES, RINGS, 180, 180);
    lbody_plate->rotate(90, 0, 0, 1);

    // head
    GLfloat t3[3] = {0, -2.5, 0};
    Node *joint3 = new Node(lower_body, t2, r2);
    Node *neck = new Node(joint3, t3, r0);
    Node *head = new Node(neck, t3, r0);
    neck->shapes.push_back(new Cylinder(O, GRAY, 2.5, 5, SLICES));
    Cylinder *head_c = new Cylinder(O, GRAY, 5, 5, SLICES, true, 180);
    head_c->rotate(-90, 0, 0, 1);
    Torus *head_t = new Torus(O, GRAY, 5, 3, SLICES, RINGS, 180, 180);
    head_t->rotate(-90, 0, 0, 1);
    GLfloat xyz[3] = {0.5, 0.5, 1};
    O[1] = -8;
    Box *eye = new Box(O, GRAY, xyz);
    head->shapes.push_back(head_c);
    head->shapes.push_back(head_t);
    head->shapes.push_back(eye);

    // assign callbacks
    glutReshapeFunc(reshape);
    glutDisplayFunc(display);
    glutTimerFunc(time_step, timer, 0);
    glutKeyboardFunc(keyboard);
    glutMouseFunc(mouse);
    glutMotionFunc(motion);

    // start
    glutMainLoop();
}

void reshape(int w, int h)
{
    glViewport(0, 0, w, h);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluPerspective(45.0f, (GLfloat)w / (GLfloat)h, .1f, 500.0f);
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
}


void cam()
{
    glLoadIdentity();
    glRotatef(rotx, 1, 0, 0);
    glRotatef(roty, 0, 1, 0);
    glTranslatef(-cam_x, -cam_y, -cam_z);
}

void display()
{
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    cam();
    glEnable(GL_DEPTH_TEST);
    root->draw();
    glutSwapBuffers();
}

void timer(int value)
{
    glutPostRedisplay();
    glutTimerFunc(time_step, timer, 0);
}


void keyboard(unsigned char key, int x, int y)
{
    printf("x %f y %f z %f\n",cam_x, cam_y, cam_z);
    const float v = 1;
    switch(key) {
        case 'w':
            cam_x += v*sin(rad(roty));
            cam_z -= v*cos(rad(roty));
            break;
        case 's':
            cam_x -= v*sin(rad(roty));
            cam_z += v*cos(rad(roty));
            break;
        case 'a':
            cam_x -= v*cos(rad(roty));
            cam_z -= v*sin(rad(roty));
            break;
        case 'd':
            cam_x += v*cos(rad(roty));
            cam_z += v*sin(rad(roty));
            break;
        case ' ':
            cam_y += v;
            break;
        case 'f':
            cam_y -= v;
            break;
    }
}

GLfloat prevx, prevy;

void mouse(int button, int state, int x, int y)
{
    prevx = x;
    prevy = y;
}

void motion(int x, int y)
{
    printf("rotx %f roty %f\n",rotx, roty);
    roty += (x - prevx);
    rotx += (y - prevy);
    prevx = x;
    prevy = y;
}
