#include"shape.h"

Shape::Shape(Node &node) : node(node)
{
    index = node.shapes.size();
    node.shapes.push_back(this);
}

Shape::~Shape()
{
    node.shapes.erase(node.shapes.begin() + index);
}
