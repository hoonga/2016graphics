class Ray:
    def __init__(self, o, v):
        self.o = o
        self.v = v.normalized()
