from math import tan, pi


class Cam:
    def __init__(self, p, l, u, near, fov, ratio):
        self.p = p
        self.l = l
        self.u = u
        self.near = near
        self.Z = (p-l).normalized()
        self.X = u.cross(self.Z).normalized()
        self.Y = self.Z.cross(self.X).normalized()
        self.h = tan(pi*fov/180)*near
        self.w = self.h*ratio
