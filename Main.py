# DDA test
from PIL import Image
import math

picture_width = 512
picture_height = 512
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

    dda_impl(start, x, y, a_map, exchange_xy, flip_x, flip_y, color)


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


for i in range(1, 16):
    xe = (math.sin(i * 3.1415926 / 8) * 21 + picture_width / 2)
    ye = (math.cos(i * 3.1415926 / 8) * 21 + picture_height / 2)
    xe = int(xe)
    ye = int(ye)
    dda((picture_width / 2, picture_height / 2), (xe, ye), pixels,
        (int(128 * i / 16.0) + 128, int(128 * i / 16.0) + 128, int(128 * i / 16.0) + 128))
    if i == 1:
        break
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



print i
