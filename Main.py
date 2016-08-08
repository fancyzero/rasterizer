# DDA test

amap = [[0 for i in range(0, 20)] for j in range(0, 20)]


def dda(start, end, amap):
    exchange_xy = False
    flip_x = False
    flip_y = False

    x = end[0] - start[0]
    y = end[1] - start[1]

    if y == 0:
        slope = 1
    else:
        slope = abs(float(x) / y)

    if slope > 1:
        flip_xy = True
        x, y = y, x

    if x < 0:
        flip_x = True
        x=-x
    if y < 0:
        flip_y = True
        y=-y

    dda_impl(start, x, y, slope, amap, exchange_xy, flip_x, flip_y)


def dda_impl(start, x_diff, y_diff, slope, amap, exchange_xy, flip_x, flip_y):
    print start, x_diff,y_diff,slope, exchange_xy,flip_x,flip_x
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
            xw = y
            yw = x

        amap[yw + start[1]][xw + start[0]] = 1
        aa += slope
        if aa > 1:
            aa -= 1
            x += 1
        y += 1


dda((10, 0), (5, 5), amap)

output = ""
for i in amap:
    for j in i:
        if j == 0:
            output += "0"
        else:
            output += "*"
    output += "\n"

print output
