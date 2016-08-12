# DDA test
from PIL import Image
import math
from fbx import *
import FbxCommon
import numpy

picture_width = 512
picture_height = 512
img = Image.new("RGB", (picture_width, picture_height))
pixels = img.load()


def walk_through(node, intent="  "):
    """
    walk through all child nodes and print information
    :param node: root node
    :param intent:
    """
    assert isinstance(node, FbxNode)
    print intent + node.GetName() + "'" + node.GetTypeName() + "'"
    cnt = node.GetChildCount()

    intent += "  "
    for i in range(0, cnt):
        walk_through(node.GetChild(i), intent)


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
        try:
            a_map[xw + start[0], yw + start[1]] = color
        except IndexError:
            pass

        error -= y_diff
        if error < 0:
            error += x_diff
            y += 1
        x += 1


def dda_triangle(v1, v2, v3, a_map, color):
    dda(v1[0:2], v2[0:2], a_map, color)
    dda(v2[0:2], v3[0:2], a_map, color)
    dda(v3[0:2], v1[0:2], a_map, color)


def dda_triangle_impl(v1, v2, v3, color):
    pass


def fbx_vector_to_vector3(fbxv):
    return (fbxv[0], fbxv[2], fbxv[1])


def matrix_transform_vector3(mat, v):
    oldv = v
    v = numpy.append(v, 1)
    v = (v * mat)
    v = (numpy.array(v)).flatten()
    # perspective divid
    v = v[0:3] / v[3]
    # viewport transform
    v = v * (256, 256, 1)
    v = v + (256, 256, 0)
    return v


def test_draw_mesh(in_mesh, a_map, matrix):
    verts = in_mesh.GetControlPoints()

    for i in range(in_mesh.GetPolygonCount()):
        p1 = in_mesh.GetPolygonVertex(i, 0)
        p2 = in_mesh.GetPolygonVertex(i, 1)
        p3 = in_mesh.GetPolygonVertex(i, 2)
        p1 = fbx_vector_to_vector3(verts[p1])
        p2 = fbx_vector_to_vector3(verts[p2])
        p3 = fbx_vector_to_vector3(verts[p3])
        p1 = matrix_transform_vector3(matrix, p1)
        p2 = matrix_transform_vector3(matrix, p2)
        p3 = matrix_transform_vector3(matrix, p3)
        dda_triangle(p1, p2, p3, a_map, (255, 0, 0))


def test_draw_star():
    for i in range(0, 16):
        xe = (math.sin(i * 3.1415926 / 8) * 21 + picture_width / 2)
        ye = (math.cos(i * 3.1415926 / 8) * 21 + picture_height / 2)
        dda((picture_width / 2, picture_height / 2), (int(xe), int(ye)), pixels,
            (int(128 * i / 16.0) + 128, int(128 * i / 16.0) + 128, int(128 * i / 16.0) + 128))


mgr, scene = FbxCommon.InitializeSdkObjects()
converter = FbxCommon.FbxGeometryConverter(mgr)
ret = FbxCommon.LoadScene(mgr, scene, "d:\\monkey.fbx")
converter.Triangulate(scene, False)
root = scene.GetRootNode()
walk_through(root)
mesh = root.GetChild(0)
attr_type = mesh.GetNodeAttribute().GetAttributeType()

fov = 90.0
n = near_plane = 0.1
f = far_plane = 1000

model_matrix = numpy.matrix([[1., 0., 0., 0.],
                             [0., 1., 0., 0.],
                             [0., 0., 1., 0.],
                             [0., 0., 2., 1]])

proj_matrix = numpy.matrix([[n / 1, 0., 0., 0.],
                            [0., n / 1, 0., 0.],
                            [0., 0., -(f + n) / (f - n), -2.0 * f * n / (f - n)],
                            [0., 0., -1., 0.]])

mvp = model_matrix * proj_matrix

print "=====matrix======"
print proj_matrix
print "=====matrix======\n\n\n"

if attr_type == FbxCommon.FbxNodeAttribute.eMesh:
    test_draw_mesh(mesh.GetMesh(), pixels, mvp)

img.show()
