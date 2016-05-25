import numpy as n
from pyglet.gl import *
from pyglet.graphics import Batch, OrderedGroup
from maths import Vec3


class Surface:
    def __init__(self, poses, material=None):
        self.poses = poses
        self.N = (poses[1] - poses[0]).cross(poses[2] - poses[0]).normalize()
        self.batch = Batch()
        norms = list(self.N.arr)*len(poses)
        verts = reduce(lambda x,y:list(x)+list(y), poses)
        self.batch.add(len(poses), GL_TRIANGLE_FAN, None, ('v3f', verts),('n3f', norms))
        self.material = material

    def draw(self):
        if self.material is not None:
            self.material.set()
        self.batch.draw()

    def d(self, p):
        return self.N.dot(self.poses[0] - p)

class TransparentCube:
    def __init__(self, pos, w, l, h, material=None):
        self.pos = pos
        v1 = Vec3(w, l, h)*0.5
        v2 = Vec3(-w, l, h)*0.5
        v3 = Vec3(w, -l, h)*0.5
        v4 = Vec3(w, l, -h)*0.5
        points = []
        points.append(pos + v1)
        points.append(pos + v4)
        points.append(pos - v3)
        points.append(pos + v2)
        points.append(pos + v3)
        points.append(pos - v4)
        points.append(pos - v1)
        points.append(pos - v2)
        self.surfaces = []
        self.surfaces.append(Surface(points[0:4], material))
        self.surfaces.append(Surface(points[4:], material))
        self.surfaces.append(Surface([points[4],points[7],points[1],points[0]], material))
        self.surfaces.append(Surface([points[7],points[6],points[2],points[1]], material))
        self.surfaces.append(Surface([points[6],points[5],points[3],points[2]], material))
        self.surfaces.append(Surface([points[5],points[4],points[0],points[3]], material))

    def draw(self, vec):
        self.surfaces.sort(key=lambda x: vec.dot(x.N))
        for i in self.surfaces:
            i.draw()

class Material:
    def __init__(self, ambi, diff, spec, shin):
        self.ambi = (GLfloat*4)(*ambi)
        self.diff = (GLfloat*4)(*diff)
        self.spec = (GLfloat*4)(*spec)
        self.shin = shin

    def set(self):
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, self.ambi)
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, self.diff)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, self.spec)
        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, self.shin)

class Sphere:
    def __init__(self, pos, rad, material=None):
        self.pos = pos
        self.rad = rad
        self.q = gluNewQuadric()
        self.material = material

    def draw(self):
        glPushMatrix()
        glTranslatef(*self.pos)
        if self.material is not None:
            self.material.set()
        gluSphere(self.q, self.rad, 30, 30)
        glPopMatrix()
