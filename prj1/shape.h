#include"node.h"

/*
 * virual class for drawable shapes
 *
 */

class Shape {
    public :
        // shape must be a part of a node
        Shape(Node &node);
        ~Shape();

        virtual void draw() = 0;
        Node &node;

    private:
        // index in node.shapes
        int index;
};
