import numpy as n
from maths import *
from pyglet.graphics import vertex_list, Batch
from pyglet.gl import *


# assuming monomial base to be [t**3, t**2, t, 1]
BezBase = n.array([[-1, 3, -3, 1],
                   [3, -6, 3, 0],
                   [-3, 3, 0, 0],
                   [1, 0, 0, 0]], dtype=GLfloat)

BBase = 1/6.0*n.array([[-1, 3, -3, 1],
                       [3, -6, 3, 0],
                       [-3, 0, 3, 0],
                       [1, 4, 1, 0]], dtype=GLfloat)

class BSpline:
    base = BBase
    def __init__(self, points, dtype, loop):
        self.pieces = []
        l = len(points)
        for i in range(l):
            self.pieces.append(n.array([points[i%l], points[(i+1)%l],
                points[(i+2)%l], points[(i+3)%l]]))

class CMSpline:
    base = BezBase
    def __init__(self, points, dtype, loop):
        self.pieces = []
        if dtype != Quaternion:
            for i in range(1, len(points) - 2):
                piece = [points[i]]
                piece.append(points[i] + 1/6.0*(points[i + 1] - points[i - 1]))
                piece.append(points[i + 1] - 1/6.0*(points[i + 2] - points[i]))
                piece.append(points[i + 1])
                self.pieces.append(n.array(piece, dtype=GLfloat))
            if loop:
                for i in (-2, -1, 0):
                    piece = [points[i]]
                    piece.append(points[i] + 1/6.0*(points[i + 1] - points[i - 1]))
                    piece.append(points[i + 1] - 1/6.0*(points[i + 2] - points[i]))
                    piece.append(points[i + 1])
                    self.pieces.append(n.array(piece, dtype=GLfloat))
        else:
            for i in range(1, len(points) - 2):
                piece = [points[i]]
                piece.append(points[i]*(1/6.0*(points[i-1].inv()*points[i+1]).log()).exp())
                piece.append(points[i+1]*(1/6.0*(points[i].inv()*points[i+2]).log()).exp().inv())
                piece.append(points[i+1])
                self.pieces.append(piece)


class Data:
    types = {"BSPLINE" : BSpline, "CATMULL_ROM" : CMSpline}
    def __init__(self, filename):
        f = open(filename)
        l = map(lambda x : x.split('#', 1)[0], f.readlines())
        f.close()
        donelines = 0
        i = 0

        # Header
        while True:
            a = l[i]
            i += 1
            if donelines == 0:
                t = a.split()[0]
                if t:
                    self.type = Data.types[t]
                    donelines += 1
            elif donelines == 1:
                s = a.split()[0]
                if s:
                    self.sections = int(s)
                    donelines += 1
            elif donelines == 2:
                p = a.split()[0]
                if p:
                    self.points = int(p)
                    break
        # Body
        donesections = 0
        self.curves = []
        self.scales = []
        self.orients = []
        self.translates = []
        while donesections < self.sections:
            donelines = 0
            while donelines < self.points + 3:
                a = l[i].split()
                i += 1
                if not a:
                    continue
                if donelines > 0:
                    if donelines < self.points:
                        self.curves[donesections].append(
                                n.array(map(float, [a[0],0,a[1]])))

                    elif donelines == self.points:
                        self.scales.insert(donesections,
                                n.array([float(a[0])]))

                    elif donelines == self.points + 1:
                        q = Quaternion.fromRotation(*map(float, a[0:4]))
                        self.orients.insert(donesections,q)

                    else:
                        self.translates.insert(donesections,
                                n.array(map(float, a[0:3])))

                elif donelines == 0:
                    self.curves.insert(donesections,
                                [n.array(map(float, [a[0], 0, a[1]]))])
                donelines += 1
            donesections += 1
        del l


class Swept:
    def __init__(self, data, slices, rings):
        self.type = data.type
        self.sections = data.sections
        self.scales = CMSpline(data.scales, None, False)
        self.translates = CMSpline(data.translates, None, False)
        self.orients = CMSpline(data.orients, Quaternion, False)
        self.curves = []
        self.slices = slices
        self.rings = rings
        self.positions = []
        # loops
        for i in range(len(self.scales.pieces)):
            self.curves.insert(i, self.type(data.curves[i],None, True))
        # positions
        print "making positions"
        for i in range(len(self.scales.pieces)):
            scale = n.dot(BezBase, self.scales.pieces[i])
            translate = n.dot(BezBase, self.translates.pieces[i])
            rotate = self.orients.pieces[i]
            for j in n.linspace(0, 1, self.rings, endpoint=False):
                mono = n.array([j**3, j**2, j, 1], dtype=GLfloat).reshape((1,4))
                scale_ = n.dot(mono, scale)
                translate_ = n.dot(mono, translate)
                s0 = Quaternion.slerp(j, rotate[0], rotate[1])
                s1 = Quaternion.slerp(j, rotate[1], rotate[2])
                s2 = Quaternion.slerp(j, rotate[2], rotate[3])
                s3 = Quaternion.slerp(j, s0, s1)
                s4 = Quaternion.slerp(j, s1, s2)
                rotate_ = Quaternion.slerp(j, s3, s4)
                poses = []
                for l in self.curves[i].pieces:
                    for k in n.linspace(0, 1, self.slices, endpoint=False):
                        mono_ = n.array([k**3, k**2, k, 1], dtype=GLfloat)
                        pos = n.dot(n.dot(mono_, self.type.base), l)
                        pos = scale_[0]*pos
                        pos = (rotate_*Quaternion(0, *pos)*rotate_.inv()).arr
                        pos = pos + translate_
                        poses.append(*pos)
                self.positions.append(poses)
        # normals
        print "making normals"
        self.normals = []
        norms = []
        l = len(self.positions[0])
        center = sum(self.positions[0])/l
        for i in range(l):
            v1 = self.positions[0][(i+1)%l] - self.positions[0][i]
            v2 = self.positions[1][i] - self.positions[0][i]
            v3 = self.positions[0][i-1] - self.positions[0][i]
            n1 = Vec3(*n.cross(v1, v2)).normalized()
            n2 = Vec3(*n.cross(v2, v3)).normalized()
            norm = (n1+n2).normalized().arr
            if n.dot(norm, self.positions[0][i]-center) < 0:
                norm = -norm
            norms.append(norm)
        self.normals.append(norms)
        for i in range(1, len(self.positions) - 1):
            norms = []
            center = sum(self.positions[i])/l
            for j in range(l):
                v1 = self.positions[i][(j+1)%l] - self.positions[i][j]
                v2 = self.positions[i+1][j] - self.positions[i][j]
                v3 = self.positions[i][j-1] - self.positions[i][j]
                v4 = self.positions[i-1][j] - self.positions[i][j]
                n1 = Vec3(*n.cross(v1, v2)).normalized()
                n2 = Vec3(*n.cross(v2, v3)).normalized()
                n3 = Vec3(*n.cross(v3, v4)).normalized()
                n4 = Vec3(*n.cross(v4, v1)).normalized()
                norm = (n1+n2+n3+n4).normalized().arr
                if n.dot(norm, self.positions[i][j] - center) < 0:
                    norm = -norm
                norms.append(norm)
            self.normals.append(norms)
        norms = []
        center = sum(self.positions[-1])/l
        for i in range(l):
            v1 = self.positions[-1][i-1] - self.positions[-1][i]
            v2 = self.positions[-2][i] - self.positions[-1][i]
            v3 = self.positions[-1][(i+1)%l] - self.positions[-1][i]
            n1 = Vec3(*n.cross(v1, v2)).normalized()
            n2 = Vec3(*n.cross(v2, v3)).normalized()
            norm = (n1+n2).normalized().arr
            if n.dot(norm, self.positions[-1][i] - center) < 0:
                norm = -norm
            norms.append(norm)
        self.normals.append(norms)

        # making vertexes gl
        print "batching"
        self.batch = Batch()
        for i in range(1, len(self.positions)):
            poses = reduce(lambda x,y:x+y, map(lambda x,y:list(x)+list(y), self.positions[i-1], self.positions[i]))
            poses += poses[0:6]
            norms = reduce(lambda x,y:x+y, map(lambda x,y:list(x)+list(y), self.normals[i-1], self.normals[i]))
            norms += norms[0:6]
            self.batch.add(len(poses)/3, GL_TRIANGLE_STRIP, None, ('v3f/static', poses),('n3f/static', norms))


    def draw(self):
        self.batch.draw()


if __name__ == '__main__':
    import sys
    a = Data(sys.argv[1])
    print "sections "+str(a.sections)
    print "points "+str(a.points)
    print "scales "+str(a.scales)
    print "orients "+str(a.orients)
    print "translates "+str(a.translates)
    print "curves "+str(a.curves)
