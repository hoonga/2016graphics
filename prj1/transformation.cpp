#include"transformation.h"

Transformation::Transformation(Node &parent, Node &child, GLfloat* matrix)
    : parent(parent), child(child)
{
    for (int i; i < 16; i++)
        this->matrix[i] = matrix[i];
}

Transformation::~Transformation()
{
    delete &child;
}
