#include<vector>

#include"shape.h"
#include"branch.h"

/*
 * nodes have multiple shapes plugged
 * by drawing itself, it draws every shaped plugged
 * also if it has nodes it will draw them too
 */

class Node {
    public:
        Node();
        Node(Node *parent, GLfloat *translation, GLfloat *rotation);
        void draw();
        std::vector<Shape*> shapes;
        std::vector<Node*> childs;
        Branch *parent;
    private:
        int index_at_parent;
};
