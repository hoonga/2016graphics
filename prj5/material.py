from PIL import Image
from numpy import array as a
from maths import Vec3


class Material:
    def __init__(self, a, d, s, sh, r=1, tex=None, bump=None):
        self.a = a
        self.d = d
        self.s = s
        self.sh = sh
        self.r = r
        self.tex = tex
        self.bump = bump

    def getColor(self, u, v):
        if self.tex is None:
            return a([1.,1.,1.])
        else:
            u, v = map(int,(u*(self.tex.size[0]-1),v*(self.tex.size[1]-1)))
            c = a(self.tex.getpixel((u,v)), float)
            return c/255

    def getNormal(self, u, v):
        if self.bump is None:
            return a([0,0,0])
        else:
            u, v = map(int,(u*(self.bump.size[0]-1),v*(self.bump.size[1]-1)))
            n = 2*a(self.bump.getpixel((u,v)), float)/255 - a([1.,1.,1])
            return Vec3(*n).normalized()

blue = Material(a([0.,0.,0.2]),a([0.,0.,1.]),a([0.3,0.3,0.3]),20)
red = Material(a([0.2,0.,0.]),a([1.,0.,0.]),a([0.3,0.3,0.3]),20)
green = Material(a([0.,0.2,0.]),a([0.,1.,0.]),a([0.3,0.3,0.3]),20)
white = Material(a([0.3,0.3,0.3]),a([0.8,0.8,0.8]),a([0.9,0.9,0.9]),0)
gray = Material(a([0.,0.,0.]),a([0.3,0.3,0.3]),a([0.3,0.3,0.3]),5)
cyan = Material(a([0.,0.,0.]),a([0.,1.,1.]),a([0.3,0.3,0.3]),5)
wm = Image.open('earth.jpg')
world_map = Material(a([0.2,0.2,0.2]),a([1.,1.,1.]),a([0.3,0.3,0.3]),80,0,wm)
wmb = Image.open('earth_bump.jpg')
world_bumpy = Material(a([0.2,0.2,0.2]),a([1.,1.,1.]),a([0.3,0.3,0.3]),80,0,wm,wmb)
bumpy = Material(a([0.2,0.2,0.2]),a([1.,1.,1.]),a([0.3,0.3,0.3]),80,0,None,wmb)
