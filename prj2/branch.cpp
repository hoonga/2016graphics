#include"branch.h"

Branch::Branch(GLfloat *translation, GLfloat *rotation)
{
    for (int i = 0; i < 3; i++) {
        this->translation[i] = translation[i];
        this->rotation[i] = rotation[i];
    }
    this->rotation[3] = rotation[3];
}
