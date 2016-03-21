#include<GL/gl.h>
#include<GL/glu.h>
#include<GL/glut.h>

#include<cmath>
#include<vector>

/*
 * a class representing an object in space.
 * it has following attributes
 *     postion : postion regarding the global coordinate system
 *     parent : translation to parent node
 *     childs : translation to child nodes
 *     shape : information in how it will look
 *
 * has following methods
 *     rotate : rotates regard to parent
 *              ultimately changes the rotation to parent
 */

class Transformation;
class Shape;

class Node {
    public:
        Node();
        Transformation &parent;
        std::vector<Transformation*> childs;
        std::vector<Shape*> shapes;

        void rotate();
        void rotate_to_vector();
};

