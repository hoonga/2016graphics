#include<GL/gl.h>
#include<GL/glu.h>

// cam class
// position and look_vec is used

class Camera {
    public:
        Camera();
        Camera(GLfloat pos[3]);

        GLfloat pos[3];
        GLfloat look[3] = {0, 0, 0};
        GLfloat up[3] = {0, 1, 0};
        GLfloat fov = 45;
        GLfloat aspect = 1;

        void lookAt();

    private:
};
