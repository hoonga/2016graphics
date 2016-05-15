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
        Cam.gMM(Cam.GP)
        Cam.gLI()
        Cam.gP(self.fov, self.aspect, self.zn, self.zf)
        Cam.gMM(Cam.GMV)
        Cam.gLI()
        Cam.gLA(*n.concatenate([self.pos.arr, self.look.arr, self.up.arr]))


    def setSystem(self):
        self.Z = (self.pos - self.look).normalized()
        self.X = (self.up.cross(self.Z)).normalized()
        self.Y = (self.Z.cross(self.X)).normalized()


class Trackball:
    def __init__(self, pos, cam):
        self.pos = pos
        self.rel_cam_pos = cam.pos - self.pos
        self.cam = cam

    def rotate(self, vec1, vec2):
        q = Quaternion(vec2.dot(vec1) + (vec1.normsqr()*vec2.normsqr())**0.5,
               *vec2.cross(vec1)).normalized()
        p = Quaternion(0, *self.rel_cam_pos)
        u = Quaternion(0, *self.cam.up)
        p = (q*p)*q.inv()
        u = (q*u)*q.inv()
        self.rel_cam_pos = Vec3(*p.arr)
        self.cam.up = Vec3(*u.arr)
        self.setCam()

    def setCam(self):
        self.cam.look = self.pos
        self.cam.pos = self.pos + self.rel_cam_pos
        self.cam.setSystem()
        self.cam.lookAt()

    def translate(self, vec):
        self.pos += vec
        self.setCam()


class TrackballCam:
    gVP = gl.glViewport
    def __init__(self, w, h, fov):
        self.cam = Cam(Vec3(0, 0, -50), Vec3(0, 0, 0), Vec3(0, 1, 0), fov, float(w)/h)
        self.tb = Trackball(Vec3(0, 0, 0), self.cam)
        self.resize(w, h)

    def translate(self, dx, dy):
        self.tb.translate(self.cam.X*dx + self.cam.Y*dy)

    def rotate(self, x0, y0, x1, y1):
        vec1 = self.cam.X*x0 + self.cam.Y*y0
        vec2 = self.cam.X*x1 + self.cam.Y*y1
        z1 = vec1.normsqr()
        z2 = vec2.normsqr()
        if z1 > 250000:
            vec1 /= n.sqrt(z1)/500
        else:
            vec1 += self.cam.Z*n.sqrt(250000 - z1)
        if z2 > 250000:
            vec2 /= n.sqrt(z2)/500
        else:
            vec2 += self.cam.Z*n.sqrt(250000 - z2)
        self.tb.rotate(vec2, vec1)

    def dolly(self, z):
        self.tb.rel_cam_pos -= self.cam.Z*z
        self.tb.setCam()

    def zoom(self, fov):
        self.cam.fov += fov if 45 > self.cam.fov + fov > 15 else 0
        self.cam.lookAt()

    def resize(self, w, h):
        TrackballCam.gVP(0, 0, w, h)
        self.cam.aspect = float(w)/h
        self.tb.setCam()
