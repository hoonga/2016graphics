#include"cam.h"
#include<Eigen/Geometry>
#include<Eigen/Core>
#include<cmath>

class Trackball {
    public:
        Trackball(Camera *cam);

        GLfloat pos[3] = {0, 0, 0};
        GLfloat R = 10;

        void test();
        void screenRot(int x, int y, int dx, int dy);
        void screenMov(int x, int y, int dx, int dy);
        void dolly(float depth);
        void zoom(float rate);
        void seek(int x, int y);
        void showAll();
        void attachCam(Camera *cam);

    private:
        Camera *cam;
        // it's a quaternion
        GLfloat rel_cam_pos[3] = {0, 0, -10};

        void setCam();
        // dx, dy, dz need to be derived
        void translate(GLfloat dx, GLfloat dy, GLfloat dz);
        // start, end coords need to be derived
        void rotate(GLfloat start[3], GLfloat end[3]);
};
