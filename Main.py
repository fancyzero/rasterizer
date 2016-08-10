# DDA test
from PIL import Image
import math

img = Image.new("RGB", (32, 32))
pixels = img.load()


def dda(start, end, a_map, color):
    exchange_xy = False
    flip_x = False
    flip_y = False

    x = end[0] - start[0]
    y = end[1] - start[1]
    print x, y
    if y == 0:
        slope = 1
    else:
        slope = abs(float(x) / y)

    if slope > 1:
        exchange_xy = True
        x, y = y, x
        slope = abs(float(x) / y)

    if x < 0:
        flip_x = True
        x = -x
    if y < 0:
        flip_y = True
        y = -y

    dda_impl(start, x, y, slope, a_map, exchange_xy, flip_x, flip_y, color)


def dda_impl(start, x_diff, y_diff, slope, a_map, exchange_xy, flip_x, flip_y, color):
    print start, x_diff, y_diff, slope, exchange_xy, flip_x, flip_x
    aa = slope
    x = 0
    y = 0
    while y <= y_diff:
        xw = x
        yw = y
        if flip_x:
            xw = -xw
        if flip_y:
            yw = -yw
        if exchange_xy:
            xw, yw = yw, xw
        a_map[yw + start[1], xw + start[0]] = color
        aa += slope
        if aa > 1:
            aa -= 1
            x += 1
        y += 1


for i in range(0, 16):
    xe = math.sin(i * 3.1415926 / 8) * 10 + 16
    ye = math.cos(i * 3.1415926 / 8) * 10 + 16
    dda((16, 16), (xe, ye), pixels, (int(128 * i / 16.0), int(128 * i / 16.0), int(128 * i / 16.0)))
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
