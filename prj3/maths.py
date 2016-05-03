import numpy as n

class Vec3:
    def __init__(self, x, y, z, dtype=float):
        self.arr = n.array([x, y, z], dtype=dtype)
        self._len = self.norm()

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

    def __mul__(self, other):
        return Vec3(*self.arr*other)

    def __div__(self, other):
        return Vec3(*self.arr/other)

    def norm(self):
        return self.normsqr()**0.5

    def normsqr(self):
        return sum(self.arr*self.arr)

    def normalize(self):
        self.arr /= self._len
        self._len = self.norm()
        return self

    def normalized(self):
        return Vec3(*(self.arr/self._len))


class Quaternion:
    def __init__(self, w, x, y, z, dtype=float):
        self.w = dtype(w);
        self.arr = n.array([x, y, z], dtype)
        self._len = self.norm()
        l = sum(self.arr*self.arr)**0.5
        self._angle = n.arcsin(l if -1< l <1 else l/abs(l))
        if l:
            self._axis = self.arr/l
        else:
            self._axis = n.array([0,0,0],dtype=dtype)

    def __mul__(self, other):
        if type(other) == float or type(other) == int:
            return Quaternion(self.w*other, *(other*self.arr))
        else:
            w = self.w*other.w - n.dot(self.arr, other.arr)
            arr = self.w*other.arr + other.w*self.arr + n.cross(self.arr, other.arr)
            return Quaternion(w, *arr)

    def __rmul__(self, other):
        if type(other) == float or type(other) == int:
            return Quaternion(self.w*other, *(other*self.arr))
        else:
            w = other.w*self.w - n.dot(other.arr, self.arr)
            arr = other.w*self.w + self.w*other.arr + n.cross(other.arr, self.arr)
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

    def normalized(self):
        return Quaternion(self.w/self.norm(), *(self.arr/self.norm()))

    def inv(self):
        return Quaternion(self.w/self._len, *(self.arr/-self._len))

    def log(self):
        return Quaternion(0, *(self._angle*self._axis))

    def exp(self):
        return Quaternion(n.cos(self._angle), *(n.sin(self._angle)*self._axis))

    @staticmethod
    def slerp(t, q1, q2):
        return q1*(t*(q1.inv()*q2).log()).exp()

    @staticmethod
    def fromRotation(angle, *axis):
        return Quaternion(n.cos(angle/2), *(n.sin(angle/2)*n.array(axis)))


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
    print "3*p = " + str(3*p)
    print "p*3.0 = " + str(p*3.0)
    print "p*q = " + str(p*q)
    print "p*p = " + str(p*p)
    print "p.norm() = " + str(p.norm())
    print "p.normalize() = " + str(p.normalize())
    print "p.inv() = " + str(p.inv())
    print "p*p.inv() = " + str(p*p.inv())
