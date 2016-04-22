import pyglet.gl as gl
import numpy as n
from maths import *


class Cam:
    gLA = gl.glLookAt
    gLI = gl.glLoadIdentity
    gMM = gl.glMatrixMode
    GMV = gl.GL_MODEL_VIEW
    def __init__(self, pos, look, up):
        self.pos = pos
        self.look = look
        self.up = up

    def lookAt(self):
        gMM(GMV)
        GLI()
        gLA(*n.concatenate([self.pos.arr, self.look.arr, self.look.up]))


class Trackball:
    def __init__(self, pos, cam):
        self.pos = pos
        self.rel_cam_pos = cam.pos - self.pos
        self.cam = cam

    def rotate(self, vec1, vec2):
        q = Quaternion(vec1.dot(vec2) + (vec1.norsqrm()*vec2.normsqr())**0.5,
               *vec1.cross(vec2))
        p = Quaternion(0, *self.rel_cam_pos)
        u = Quaternion(0, *self.cam.up)
        p = q*p*q.inv()
        u = q*u*q.inv()
        self.rel_cam_pos = Vec3(*p.arr)
        self.cam.up = Vec3(*u.arr)
        setCam()

    def setCam(self):
        self.cam.pos = self.pos + self.rel_cam_pos
        self.cam.lookAt()

    def translate(self, vec):
        self.pos += vec
        setCam()
