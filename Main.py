# DDA test
from PIL import Image
import math

picture_width = 64
picture_height = 64
img = Image.new("RGB", (picture_width, picture_height))
pixels = img.load()


def dda(start, end, a_map, color):
    exchange_xy = False
    flip_x = False
    flip_y = False

    x = end[0] - start[0]
    y = end[1] - start[1]

    if x == 0:
        slope = 1
    else:
        slope = abs(float(y) / x)

    if slope >= 1:
        exchange_xy = True
        x, y = y, x

    if x < 0:
        flip_x = True
        x = -x
    if y < 0:
        flip_y = True
        y = -y

    dda_impl(start, int(x), int(y), a_map, exchange_xy, flip_x, flip_y, color)


def dda_impl(start, x_diff, y_diff, a_map, exchange_xy, flip_x, flip_y, color):
    error = x_diff / 2
    x = 0
    y = 0
    while x <= x_diff:
        xw = x
        yw = y
        if flip_x:
            xw = -xw
        if flip_y:
            yw = -yw
        if exchange_xy:
            xw, yw = yw, xw
        a_map[xw + start[0], yw + start[1]] = color
        print error, x, y
        error -= y_diff
        if error < 0:
            error += x_diff
            y += 1
        x += 1


def dda_triangle(v1, v2, v3, a_map, color):
    dda(v1[0:2], v2[0:2], a_map, color)
    dda(v2[0:2], v3[0:2], a_map, color)
    dda(v3[0:2], v1[0:2], a_map, color)
    pass


def dda_triangle_impl(v1, v2, v3, color):
    pass

def test_draw_mesh():
    dda_triangle((4,4),(12,22), (51,31), pixels, (256,0,0))
    dda_triangle((12,22), (51,31),(10,41), pixels, (0,256,0))



def test_draw_star():
     for i in range(0, 16):
        xe = (math.sin(i * 3.1415926 / 8) * 21 + picture_width / 2)
        ye = (math.cos(i * 3.1415926 / 8) * 21 + picture_height / 2)
        dda((picture_width / 2, picture_height / 2), (int(xe), int(ye)), pixels,
            (int(128 * i / 16.0) + 128, int(128 * i / 16.0) + 128, int(128 * i / 16.0) + 128))

test_draw_mesh()

img.show()
#
# output = ""
# for i in amap:
#     for j in i:
#         if j == 0:
#             output += "0"
#         else:
#             output += "*"
#     output += "\n"
#
# print output

