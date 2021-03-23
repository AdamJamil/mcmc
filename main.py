import math
import random
import numpy
from tkinter import *
import tkinter
import time


width, height = 600, 600
x_min, y_min, x_max, y_max = -10, -10, 13, 13
m_x = width / (x_max - x_min)
m_y = height / (y_max - y_min)
b_x = -x_min * m_x
b_y = -y_min * m_y


def coord_to_px(x, y):
    return m_x * float(x) + b_x, height - (m_y * float(y) + b_y)


def f(x, y):  # function which is proportional to 2D gaussian, our target PDF to approximate
    x_0, y_0 = 1, 0
    s_x, s_y = 2, 2

    def norm(z, z_0, s_z):
        return ((z - z_0) ** 2) / (2 * (s_z ** 2))

    return math.exp(-(norm(x, x_0, s_x) + norm(y, y_0, s_y)))


def line(x1, y1, x2, y2, canvas):
    canvas.create_line(*coord_to_px(x1, y1), *coord_to_px(x2, y2))


def point(x, y, canvas):
    tl_point = [i - 1 for i in coord_to_px(x, y)]
    br_point = [i + 1 for i in coord_to_px(x, y)]
    canvas.create_oval(*tl_point, *br_point, fill="red")


if __name__ == "__main__":
    master = Tk()

    canvas = Canvas(master, width=width, height=height)
    canvas.pack()

    x, y = 0, 0
    prev_f = f(x, y)
    # points = [[x, y]]
    x_coords, y_coords = [x], [y]

    for _ in range(1000):
        dist = numpy.random.gamma(1.0, 2.0)  # distance we will jump
        theta = random.uniform(0, 2 * math.pi)  # angle we are jumping towards
        tar_x, tar_y = x + math.cos(theta) * dist, y + math.sin(theta) * dist
        next_f = f(tar_x, tar_y)
        alpha = next_f / prev_f

        if random.random() <= alpha:  # accept proposed new point
            line(x, y, tar_x, tar_y, canvas)
            # point(tar_x, tar_y, canvas)
            x, y = tar_x, tar_y
            prev_f = next_f
            time.sleep(0.01)

        x_coords.append(x)
        y_coords.append(y)

        master.update()

    from matplotlib import pyplot as PLT
    from matplotlib import cm as CM

    PLT.hexbin(x_coords, y_coords, gridsize=30, cmap=CM.jet, bins=None)
    PLT.axis([x_min, x_max, y_min, y_max])

    cb = PLT.colorbar()
    PLT.show()

    master.mainloop()
