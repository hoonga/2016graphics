from numpy import array as a


class Intersect:
    def __init__(self, p, n, m, c=a([1.,1.,1.])):
        self.p = p
        self.n = n
        self.m = m
        self.c = c
