#include"node.h"

Node::Node() : parent(NULL), shapes(std::vector<Shape*>())
               , childs(std::vector<Node*>()), index_at_parent(0)
{
}

Node::Node(Node *parent, GLfloat *translation, GLfloat *rotation)
    : shapes(std::vector<Shape*>()), childs(std::vector<Node*>())
{
    index_at_parent = parent->childs.size();
    Branch *b = new Branch(, );
    this->parent = b;
    parent->childs.push_back(this);
}

void Node::draw()
{
    if(parent == NULL) {
        glLoadIdentity();
    } else {
        glRotatef(parent->rotation[0],
                parent->rotation[1],
                parent->rotation[2],
                parent->rotation[3]);
        glTranslatef(parent->translation[0],
                parent->translation[1],
                parent->translation[2]);
    }
    glPushMatrix();

    // draw shapes
    std::vector<Shape*>::iterator sit = shapes.begin();
    for (; sit != shapes.end(); sit++) {
        (*sit)->draw();
    }
    // draw childs
    std::vector<Node*>::iterator cit = childs.begin();
    for (; cit != childs.end(); cit++) {
        (*cit)->draw();
    }
    glPopMatrix();
}
