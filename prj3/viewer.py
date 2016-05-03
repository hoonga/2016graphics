import pyglet
from pyglet.gl import *
from cam import TrackballCam
from spline import *


SIZE = 400
swept = None

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
        glClearColor(0, 0, 0, 0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_POINT_SMOOTH)
        glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)
        glEnable(GL_LINE_SMOOTH)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

    def on_draw(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glColor3f(0.5, 0.5, 0.7)
        swept.draw()

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

if __name__ == "__main__":
    import sys
    main(sys.argv)
