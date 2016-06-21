from maths import Vec3
from primitive import *
from PIL import Image
from cam import Cam
from material import *
from light import Light
from ray import Ray
import numpy as np

depth=0
samples=0

primitives = []
lights = []

ia=0

img=None

def getClose(ray):
    closest = -1
    result = None
    for p in primitives:
        hit = p.getIntersect(ray)
        if hit is not None:
            d = ray.v.dot(hit.p-ray.o)
            if d < closest or closest == -1:
                result = hit
                closest = d
    return result

def getShadow(ray):
    for p in primitives:
        if p.getHit(ray):
            return True
    return False

def getColor(ray, depth):
    result = np.array([0,0,0],float)
    if depth == 0:
        return result

    hit = getClose(ray)
    if hit is None:
        return result

    # Phong
    for l in lights:
        p = hit.p + hit.n/1000
        if getShadow(Ray(p, l.pos - p)):
            continue
        lm = (l.pos - hit.p).normalized()
        kl = lm.dot(hit.n)
        if kl > 0:
            result += kl*hit.m.d*l.m.d*hit.c
        kv = -ray.v.dot(2*kl*hit.n - lm)
        if kv > 0:
            result += (kv**hit.m.sh)*hit.m.s*l.m.s
    result += ia*hit.m.a*hit.c
    if hit.m.r > 0:
        reflect = -2*ray.v.dot(hit.n)*hit.n + ray.v
        result += hit.m.r*getColor(Ray(hit.p+hit.n/1000,reflect), depth-1)
    return result


def makeImage(cam, img, samples):
    print "making image"
    pixels = img.load()
    dz = -near*cam.Z
    for i in xrange(img.size[0]):
        dx = cam.w*(float(i)/img.size[0] - 0.5)*cam.X
        for j in xrange(img.size[1]):
            dy = cam.h*(0.5 - float(j)/img.size[1])*cam.Y
            color = np.array([0.,0.,0.])
            for k in np.linspace(-1./samples, 1./samples, num=samples):
                ddx = cam.w/img.size[0]*k*cam.X
                for l in np.linspace(-1./samples, 1./samples, num=samples):
                    ddy = cam.h/img.size[1]*l*cam.Y
                    o = dz+dx+dy+ddx+ddy
                    v = o-cam.p
                    c = getColor(Ray(o,v), depth)/samples**2
                    color += c
            pixels[i,j] = tuple(map(int,255*color))
    return img

if __name__ == '__main__':
    import sys
    near, fov = map(float, sys.argv[1:3])
    width, height, depth, samples = map(int, sys.argv[3:7])
    cam = Cam(Vec3(0,0,0),Vec3(0,0,-1),Vec3(0,1,0),near,fov,float(width)/height)
    primitives.append(Sphere(blue,Vec3(0,10,-30),Vec3(0,1,0),Vec3(0,0,1),5))
    primitives.append(Sphere(red,Vec3(0,0,-30),Vec3(0,1,0),Vec3(0,0,1),5))
    primitives.append(Sphere(green,Vec3(0,-10,-30),Vec3(0,1,0),Vec3(0,0,1),5))
    primitives.append(Sphere(world_map,Vec3(-10,-10,-30),Vec3(0,1,0),Vec3(0,0,1),5))
    primitives.append(Sphere(world_bumpy,Vec3(10,-10,-30),Vec3(0,1,0),Vec3(0,0,1),5))
    primitives.append(Triangle(cyan,[Vec3(-30,-15,0),Vec3(30,-15,0), Vec3(30,-15,-40)]))
    primitives.append(Triangle(cyan,[Vec3(30,-15,-40),Vec3(-30,-15,-40),Vec3(-30,-15,0)]))
    primitives.append(Triangle(world_bumpy,[Vec3(30,-15,-40),Vec3(30,15,-40),Vec3(-30,15,-40)],
        c=[Vec3(1,1,0),Vec3(1,0,0),Vec3(0,0,0)]))
    primitives.append(Triangle(world_bumpy,[Vec3(-30,15,-40),Vec3(-30,-15,-40),Vec3(30,-15,-40)],
        c=[Vec3(0,0,0),Vec3(0,1,0),Vec3(1,1,0)]))
    lights.append(Light(Vec3(0, 10, -20), white))
    lights.append(Light(Vec3(0, 10, -39), white))
    for l in lights:
        ia += l.m.a
    img = Image.new('RGB', (width, height), 'black')
    img = makeImage(cam, img, samples)
    img.save("result.bmp","BMP")
