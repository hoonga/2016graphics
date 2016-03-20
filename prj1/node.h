// gl
#include<GL/gl.h>
#include<GL/glu.h>
#include<GL/glut.h>

#include<cmath>
#include<vector>

#include"shape.h"

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

class Translation;

class Node {
    public:
        Translation &parent;
        std::vector<Translation*> childs;

        void rotate();
        void rotate_to_vector();
    private:
        std::vector<Shape*> shapes;
};

