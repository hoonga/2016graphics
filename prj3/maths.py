import numpy as n

class Vec3:
    def __init__(self, x, y, z, dtype=float):
        self.arr = n.array([x, y, z], dtype=dtype)

    def dot(self, other):
        return n.dot(self.arr, other.arr)

    def cross(self, other):
        return Vec3(*n.cross(self.arr, other.arr))

    def __add__(self, other):
        return Vec3(*(self.arr + other.arr))

    def __sub__(self, other):
        return Vec3(*(self.arr - other.arr))

    def __str__(self):
        return str(self.arr)

    def __iter__(self):
        return self.arr.__iter__()

    def norm(self):
        return sum(self.arr*self.arr)**0.5

    def normsqr(self):
        return sum(self.arr*self.arr)

    def normalize(self):
        self.arr /= self.norm()
        return self


class Quaternion:
    def __init__(self, w, x, y, z, dtype=float):
        self.w = dtype(w);
        self.arr = n.array([x, y, z], dtype)
        self._len = self.norm()

    def __mul__(self, other):
        w = self.w*other.w - n.dot(self.arr, other.arr)
        arr = self.w*other.arr + other.w*self.arr + n.cross(self.arr, other.arr)
        return Quaternion(w, *arr)

    def __add__(self, other):
        return Quaternion(self.w + other.w, *(self.arr + other.arr))

    def __sub__(self, other):
        return Quaternion(self.w - other.w, *(self.arr - other.arr))

    def __str__(self):
        return str(n.concatenate(([self.w], self.arr)))

    def norm(self):
        return (self.w*self.w + sum(self.arr*self.arr))**0.5

    def normalize(self):
        self.w /= self._len
        self.arr /= self._len
        self._len = self.norm()
        return self

    def inv(self):
        return Quaternion(-self.w, *(self.arr/self._len))


# test codes
if __name__ == '__main__':
    print "making 2 vectors a(1, 0, 1) b(0, 1, 0)"
    a = Vec3(1, 0, 1)
    b = Vec3(0, 1, 0)
    print "a "+str(a)
    print "b "+str(b)
    print "a.norm() = " + str(a.norm())
    print "a.normalize() = " + str(a.normalize())
    print "a.dot(b) = " + str(a.dot(b))
    print "a.cross(b) = " + str(a.cross(b))
    print "iter"
    for i in b : print i

    print "making 2 quaternions q(1,0,0,0), p(0,1,1,1)"
    q = Quaternion(1,0,0,0)
    p = Quaternion(0,1,1,1)
    print q
    print p
    print "p*q = " + str(p*q)
    print "p.norm() = " + str(p.norm())
    print "p.normalize() = " + str(p.normalize())
    print "p.inv() = " + str(p.inv())
