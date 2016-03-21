#include"node.h"

/*
 */

class Transformation {
    public:
        // Translation must have both parent and child
        Transformation(Node &parent, Node &child, GLfloat* matrix);

        GLfloat matirx[16];
        Node& parent;
        Node& child;
};
