#include"node.h"

/*
 * virual class for drawable shapes
 *
 */

class Shape {
    public :
        // shape must be a part of a node
        Shape(Node &node);

        virtual void draw();
        Node node;
};
