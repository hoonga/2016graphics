import pyglet.gl as gl
import numpy as n
from maths import *


class Cam:
    gLA = gl.gluLookAt
    gP = gl.gluPerspective
    gLI = gl.glLoadIdentity
    gMM = gl.glMatrixMode
    GMV = gl.GL_MODELVIEW
    GP = gl.GL_PROJECTION
    def __init__(self, pos, look, up, fov=45, aspect=1, zn=0.1, zf=500.0):
        self.pos = pos
        self.look = look
        self.up = up
        self.setSystem()
        self.fov = fov
        self.aspect = aspect
        self.zn = zn
        self.zf = zf

    def lookAt(self):
        gMM(GMV)
        gLI()
        gLA(*n.concatenate([self.pos.arr, self.look.arr, self.look.up]))
        gMM(GP)
        gLI()
        gP(self.fov, self.aspect, self.zn, self.zf)
        gMM(GMV)


    def setSystem(self):
        self.Z = (self.pos - self.look).normalized()
        self.X = (self.up.cross(Z)).normalized()
        self.Y = (self.Z.cross(X)).normailzed()


class Trackball:
    def __init__(self, pos, cam):
        self.pos = pos
        self.rel_cam_pos = cam.pos - self.pos
        self.cam = cam

    def rotate(self, vec1, vec2):
        q = Quaternion(vec2.dot(vec1) + (vec1.normsqr()*vec2.normsqr())**0.5,
               *vec2.cross(vec1))
        p = Quaternion(0, *self.rel_cam_pos)
        u = Quaternion(0, *self.cam.up)
        p = q*p*q.inv()
        u = q*u*q.inv()
        self.rel_cam_pos = Vec3(*p.arr)
        self.cam.up = Vec3(*u.arr)
        setCam()

    def setCam(self):
        self.cam.look = self.pos
        self.cam.pos = self.pos + self.rel_cam_pos
        self.cam.setSystem()
        self.cam.lookAt()

    def translate(self, vec):
        self.pos += vec
        setCam()


class TrackballCam:
    gVP = gl.glViewport
    def __init__(self, w, h, fov):
        self.cam = Cam(Vec3(0, 0, -10), Vec3(0, 0, 0), Vec3(0, 1, 0), fov, float(w)/h)
        self.tb = Trackball(Vec3(0, 0, 0), self.cam)

    def translate(self, x0, y0, x1, y1):
        dx = x1 - x0
        dy = y1 - y0
        self.tb.translate(self.cam.X*dx + self.cam.Y*dy)

    def rotate(self, x0, y0, x1, y1):
        vec1 = self.cam.X*x0 + self.cam.Y.y0
        vec2 = self.cam.X*x1 + self.cam.Y.y1
        z1 = vec1.norm()
        z2 = vec2.norm()
        if z1 > 10:
            vec1 /= z1/10
        else:
            vec1 += self.cam.Z*(10 - z1)
        if z2 > 10:
            vec2 /= z2/10
        else:
            vec2 += self.cam.Z*(10 - z2)
        self.tb.rotate(vec1, vec2)
