from tkinter import *
from math import sqrt
from time import sleep
from threading import Thread


def circle(xc, x, r, width):
    return sqrt(r-(x - xc)**2*r/width/width)


def uncircle(xc, y, r, width):
    return sqrt(-(y**2 - r) * width**2 / r)


class Line:
    xs: int
    ys: int
    x: int
    y: int

    def get_coords(self):
        return self.x, self.y

    def get_st_coords(self):
        return self.xs, self.ys

    def __init__(self, canvas, xs1, ys1, foo, points, i, k=1):
        self.canvas = canvas
        self.xs, self.ys, self.x = xs1, ys1, points[i % (le + 1)][0]
        self.y = foo(self.x) + yr
        self.foo = foo
        self.points = points
        self.i = i % (le + 1)
        self.k = k
        self.object = None

    def move(self, vis=True, skelet=False):
        # l = len(self.points) - 1
        if self.i == 0:
            self.k = 1
        elif self.i // le > 0:
            self.k = -1
        newx = self.points[self.i][0]
        newy = self.points[self.i][1] * self.k + yr
        if skelet:
            if self.object:
                self.canvas.delete(self.object)
            if vis:
                self.object = self.canvas.create_line(self.xs, self.ys, newx, newy)
            else:
                self.object = False
        self.x, self.y = newx, newy
        self.canvas.update()
        self.i += 1 * self.k


class Moover(Thread):
    objs: tuple

    def __init__(self, time=0.5, skelet=False, *args):
        super().__init__()
        self.objs = args
        self.time = time
        self.skelet = skelet

    def run(self):
        pol = []
        while True:
            for pols in pol:
                self.objs[0].canvas.delete(pols)
            v = self.getvis()
            for i in range(len(self.objs)):
                self.objs[i].move(v[i], self.skelet)
                if not self.skelet:
                    if v[i] and v[i-1] and (self.objs[i].k != self.objs[i - 1].k or self.objs[i - 1].k == self.objs[i].k and self.objs[i].k == 1):
                        pol.append(self.objs[i].canvas.create_polygon(self.objs[i].get_st_coords(),
                                                                      self.objs[i].get_coords(),
                                                                      self.objs[i-1].get_coords(),
                                                                      fill=to_rgb((255 * self.objs[i].i // le, 255 * self.objs[i].i // le, 0)),
                                                                      width=2,
                                                                      outline='black'))
            sleep(self.time)

    def getvis(self):
        v = []
        ko = 30
        mi, ma = min(self.objs, key=lambda x: x.x).x, max(self.objs, key=lambda x: x.x).x
        for i in self.objs:
            if mi + ko < i.x < ma - ko and i.k == -1 and i.x != mi and i.x != ma:
                v.append(False)
            else:
                v.append(True)
        return v


def get_points(foo, unfoo, yp=5, speed=1):
    ac = []
    for x in range(-1000, 1000):
        try:
            ac.append((x, foo(x)))
        except:
            pass
    for y in range(-10000, 10000):
        try:
            ac.append((unfoo(y / yp) + xs, foo(unfoo(y / yp) + xs)))
            ac.append((-unfoo(y / yp) + xs, foo(-(unfoo(y / yp)) + xs)))
        except:
            pass
    return list(sorted(ac, key=lambda x: x[0]))[::speed]


def to_rgb(x):
    return '#%02x%02x%02x' % x


root = Tk()
canvas = Canvas(root, height=700, width=1000, bg='lightblue')
canvas.pack()
xs, ys = 500, 100
yr = 650
r = 1000
width = 500
# a = canvas.create_oval(150, 250, 300, 270, fill='green')
canvas.create_oval(xs - width, yr - sqrt(r), xs + width, yr + sqrt(r))
point = get_points(lambda x: circle(xs, x, r, width), lambda y: uncircle(xs, y, r, width), yp=10, speed=5)
le = len(point) - 1
print(le)
params = (canvas, xs, ys, lambda x: circle(xs, x, r, width), point)
# 4 angle
l4 = Line(*params, le // 4, -1)
l = Line(*params, le * 3 // 4, -1)
l1 = Line(*params, le // 4)
l2 = Line(*params, le * 3 // 4)
m = Moover(1e-10, False, l4, l1, l2, l).start()
root.mainloop()
