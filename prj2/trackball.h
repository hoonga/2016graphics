#include"cam.h"

class Trackball {
    public:
        Trackball(Camera *cam);

        GLfloat pos[3] = {0, 0, 0};
        GLfloat ori[4] = {1, 0, 0, 0};
        GLfloat radius = 10;

        void screenRot(int x, int y, int dx, int dy);
        void screenMov(int x, int y, int dx, int dy);
        void attachCam(Camera *cam);

    private:
        Camera *cam;
        GLfloat rel_cam_pos[3] = {0, 0, -10};

        void setCam();
        // dx, dy, dz need to be derived
        void translate(GLfloat dx, GLfloat dy, GLfloat dz);
        // start, end coords need to be derived
        void rotate(GLfloat start[3], GLfloat end[3]);
};
