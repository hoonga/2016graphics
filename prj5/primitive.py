from maths import Vec3
from intersect import Intersect
from numpy import array
from math import atan2, asin, pi


class Sphere:
    def __init__(self, m, pos, up, front, r):
        self.pos = pos
        self.Y = up.normalized()
        self.Z = front.normalized()
        self.X = up.cross(front).normalized()
        self.r = r
        self.m = m

    def getIntersect(self, ray):
        l = (self.pos - ray.o).dot(ray.v)
        if l < 0:
            return None
        l *= l
        d = (self.pos - ray.o).dot(self.pos - ray.o)
        t = self.r**2 - d + l;
        if t < 0:
            return None
        s = l**0.5 - t**0.5
        p = ray.o + ray.v*s
        n = (p - self.pos).normalized()
        if self.m.tex is not None:
            x = n.dot(self.X)
            y = n.dot(self.Y)
            z = n.dot(self.Z)
            u = 0.5+atan2(z,x)/(2*pi)
            v = 0.5-asin(1 if y > 1 else -1 if y < -1 else y)/pi
            c = self.m.getColor(u,v)
        else:
            c = array([1.,1.,1.])
        if self.m.bump is not None:
            Z = n
            X = self.X
            Y = Z.cross(X)
            b = self.m.getNormal(u,v)
            n = (X*b.arr[0] + Y*b.arr[1] + Z*b.arr[2]).normalized()
        return Intersect(p, n, self.m, c)

    def getHit(self, ray):
        l = (self.pos - ray.o).dot(ray.v)
        if l < 0:
            return False
        l *= l
        d = (self.pos - ray.o).normsqr()
        t = self.r**2 - d + l;
        if t < 0:
            return False
        return True


class Triangle:
    def __init__(self, m, v, n=None, c=None):
        self.m = m
        self.v = v
        self.n = n
        self.c = c

    def getHit(self, ray):
        e1 = self.v[1] - self.v[0]
        e2 = self.v[2] - self.v[0]
        h = ray.v.cross(e2)
        a = e1.dot(h)
        if -0.00001 < a < 0.00001:
            return False
        f = 1/a
        s = ray.o - self.v[0]
        u = f*s.dot(h)
        if u < 0 or u > 1:
            return False
        q = s.cross(e1)
        v = f*q.dot(ray.v)
        if v < 0 or v+u > 1:
            return False
        t = f*e2.dot(q)
        if t > 0.00001:
            return True
        else:
            return False

    def getIntersect(self, ray):
        e1 = self.v[1] - self.v[0]
        e2 = self.v[2] - self.v[0]
        h = ray.v.cross(e2)
        a = e1.dot(h)
        if -0.00001 < a < 0.00001:
            return None
        f = 1/a
        s = ray.o - self.v[0]
        u = f*s.dot(h)
        if u < 0 or u > 1:
            return None
        q = s.cross(e1)
        v = f*q.dot(ray.v)
        if v < 0 or v+u > 1:
            return None
        t = f*e2.dot(q)
        if t > 0.00001:
            p = ray.o + t*ray.v
            if self.n is not None:
                n = (u*self.n[1]+v*self.n[2]+(1-u-v)*self.n[0]).normalized()
            else:
                n = e1.cross(e2).normalized()
            if self.m.bump is not None:
                coord = u*self.c[1]+v*self.c[2]+(1-u-v)*self.c[0]
                n = self.m.getNormal(coord.arr[0],coord.arr[1])
            if self.c is not None:
                coord = u*self.c[1]+v*self.c[2]+(1-u-v)*self.c[0]
                c = self.m.getColor(coord.arr[0], coord.arr[1])
            else:
                c = array([1.,1.,1.])
            return Intersect(p,n,self.m,c)
