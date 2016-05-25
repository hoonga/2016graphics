import pyglet
from pyglet.gl import *
from cam import TrackballCam
from spline import *
from transparent import TransparentCube, Material, Sphere
import ctypes


SIZE = 400
swept = None
copper = Material((0.33, 0.22, 0.22, 1),(0.77, 0.55, 0.11, 1),(0.99, 0.94, 0.80, 1),14)
plastic = Material((0, 0.05, 0.05, 1.0),(0.4, 0.5, 0.5, 1.0),(0.04, 0.7, 0.7, 1.0), 10)
gold = Material((0.12,0.12,0.06,1.0),(0.36,0.24,0.04,1.0),(0.80, 0.72, 0.20,1.0),93)
silver = Material((0.3,0.3,0.3,1.0),(0.42,0.42,0.42,1.0),(0.98,0.98,0.98,1.0),100)
rubber = Material((0,0,0,1),(0.01,0.01,0.01,1),(0.50,0.50,0.50,1.0),32.0)
chalk = Material((0.28,0.28,0.28,1),(0.2,0.2,0.2,1),(0.2,0.2,0.2,1),4)
transparent = Material((0.1, 0.1, 0.1, 0.3),(0.8, 0.8, 0.8, 0.3),(0.0, 0.0, 0.0, 0), 40)
cubes = [TransparentCube(Vec3(0,0,0),10,10,10, transparent), TransparentCube(Vec3(-10,-5,-5),5,5,5, transparent)]
spheres = [Sphere([10.0,0.0,0.0],3,copper),Sphere((-10,-10,0),4,gold), Sphere((10,0,10),6,silver),Sphere((-10,0,-10),5,rubber),Sphere((-10,0,10),7,chalk)]


def main(argv):
    global swept
    caption = "Splines"
    width = height = SIZE
    resizable = True
    swept = Swept(Data(argv[1]), 5, 5)
    try:
        config = Config(sample_buffers=1, samples=4, depth_size=16,
                double_buffer=True)
        window = Window(width, height, caption=caption, config=config,
                resizable=resizable)
    except pyglet.window.NoSuchConfigException:
        window = Window(width, height, caption=caption,
                resizable=resizable)
    pyglet.app.run()


class Window(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.set_minimum_size(200, 200)
        self.TBC = TrackballCam(args[0], args[1], 45)
        self._initialize_gl()

    def _initialize_gl(self):
        glClearColor(0, 0, 0, 1)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glDisable(GL_COLOR_MATERIAL)
        glEnable(GL_LIGHTING)

    def on_draw(self):
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_LIGHT0) # white light
        glLightfv(GL_LIGHT0, GL_AMBIENT, (GLfloat*4)(0.5, 0.5, 0.5, 0.3))
        glLightfv(GL_LIGHT0, GL_SPECULAR, (GLfloat*4)(0.2, 0.2, 0.2, .02))
        glLightfv(GL_LIGHT0, GL_POSITION, (GLfloat*4)(0.8, 30.0, 0.8, 0.0))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (GLfloat*4)(0.2, 0.2, 0.2, 1.0))
        glEnable(GL_LIGHT1) # yellow
        glLightfv(GL_LIGHT1, GL_POSITION, (GLfloat*4)(-30.0, 0.0, 0.0, 0.0))
        glLightfv(GL_LIGHT1, GL_SPECULAR, (GLfloat*4)(0.5, 0.5, 0.0, 1))
        glLightfv(GL_LIGHT1, GL_AMBIENT, (GLfloat*4)(0.1, 0.1, 0.0, 1.0))
        glLightfv(GL_LIGHT1, GL_DIFFUSE, (GLfloat*4)(0.2, 0.2, 0.0, 1.0))
        glEnable(GL_LIGHT2) # cyan
        glLightfv(GL_LIGHT2, GL_AMBIENT, (GLfloat*4)(0.0, 0.8, 0.8, 0.3))
        glLightfv(GL_LIGHT2, GL_SPECULAR, (GLfloat*4)(0.0, 0.3, 0.3, .02))
        glLightfv(GL_LIGHT2, GL_POSITION, (GLfloat*4)(0.0, 0.0, 30.0, 0.0))
        glLightfv(GL_LIGHT2, GL_DIFFUSE, (GLfloat*4)(0.0, 0.2, 0.2, 1.0))
        glEnable(GL_LIGHT3) # red like
        glLightfv(GL_LIGHT3, GL_AMBIENT, (GLfloat*4)(0.8, 0.3, 0.3, 0.3))
        glLightfv(GL_LIGHT3, GL_POSITION, (GLfloat*4)(30.0, -30.0, 30.0, 0.0))
        glLightfv(GL_LIGHT3, GL_DIFFUSE, (GLfloat*4)(0.8, 0.1, 0.1, 1.0))
        glLightfv(GL_LIGHT3, GL_SPECULAR, (GLfloat*4)(0.2, 0., 0., 1))
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        plastic.set()
        swept.draw()
        for sphere in spheres:
            sphere.draw()
        cubes.sort(key=lambda x:x.pos.dot(self.TBC.cam.pos))
        for c in cubes:
            c.draw(self.TBC.tb.rel_cam_pos)

    def on_resize(self, width, height):
        width = width if width else 1
        height = height if height else 1
        self.TBC.resize(width, height)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons & pyglet.window.mouse.LEFT:
            x -= self.width/2
            y -= self.height/2
            self.TBC.rotate(x, y, x - dx, y - dy)
        elif buttons & pyglet.window.mouse.RIGHT:
            self.TBC.translate(-dx, -dy)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self.TBC.dolly(scroll_y)

    def on_text_motion(self, motion):
        if motion == pyglet.window.key.UP:
            self.TBC.zoom(-1)
        elif motion == pyglet.window.key.DOWN:
            self.TBC.zoom(1)
        elif motion == pyglet.window.key.MOTION_BEGINNING_OF_LINE:
            self.TBC = TrackballCam(self.width, self.height, 45)

if __name__ == "__main__":
    import sys
    main(sys.argv)
