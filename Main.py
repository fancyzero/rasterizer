# DDA test

import math
from fbx import *
import FbxCommon
import numpy as np
from Tkinter import *
from PIL import ImageTk, Image
import time




class LineDDA:
    def __init__(self, _start, _end):
        self.start = _start
        self.end = _end
        self.exchange_xy = False
        self.flip_x = False
        self.flip_y = False
        self.delta_x = self.end[0] - self.start[0]
        self.delta_y = self.end[1] - self.start[1]
        if self.delta_x == 0:
            slope = 1
        else:
            slope = abs(float(self.delta_y) / self.delta_x)

        if slope >= 1:
            self.exchange_xy = True
            self.delta_x, self.delta_y = self.delta_y, self.delta_x

        if self.delta_x < 0:
            self.flip_x = True
            self.delta_x = -self.delta_x
        if self.delta_y < 0:
            self.flip_y = True
            self.delta_y = -self.delta_y

        self.error = self.delta_x / 2
        self.x = 0
        self.y = 0

    def walk(self):
        if self.x <= self.delta_x:
            xw = self.x
            yw = self.y
            if self.flip_x:
                xw = -xw
            if self.flip_y:
                yw = -yw
            if self.exchange_xy:
                xw, yw = yw, xw

            self.error -= self.delta_y
            if self.error < 0:
                self.error += self.delta_x
                self.y += 1
            self.x += 1
            return True, xw + self.start[0], yw + self.start[1]
        else:
            return False,0,0


def dda(start, end, a_map, color):
    dda = LineDDA(start,end)
    while True:
        go, x, y = dda.walk()
        if go:
            a_map[x,y] = color
        else:
            break


def dda_triangle(v1, v2, v3, a_map, color):
    #find master edge

    dda(v1[0:2], v2[0:2], a_map, color)
    dda(v2[0:2], v3[0:2], a_map, color)
    dda(v3[0:2], v1[0:2], a_map, color)


def dda_triangle_impl(v1, v2, v3, color):
    pass


def fbx_vector_to_vector3(fbxv):
    return (fbxv[0], fbxv[2], fbxv[1])


def matrix_transform_vector3(mat, v):
    v = np.append(v, 1)
    v = (v * mat)
    v = (np.array(v)).flatten()
    # perspective divid
    v = v[0:3] / v[3]
    # viewport transform
    v = v * (256, 256, 1)
    v = v + (256, 256, 0)
    return v


def test_draw_mesh(in_mesh, a_map, matrix):
    verts = in_mesh.GetControlPoints()
    verts = [fbx_vector_to_vector3(v) for v in verts]
    verts = [matrix_transform_vector3(matrix,v) for v in verts]


    for i in range(in_mesh.GetPolygonCount()):
        p1 = in_mesh.GetPolygonVertex(i, 0)
        p2 = in_mesh.GetPolygonVertex(i, 1)
        p3 = in_mesh.GetPolygonVertex(i, 2)
        p1 = verts[p1]
        p2 = verts[p2]
        p3 = verts[p3]

        dda_triangle(p1, p2, p3, a_map, (255, 0, 0))


def test_draw_star():
    for i in range(0, 16):
        xe = (math.sin(i * 3.1415926 / 8) * 21 + picture_width / 2)
        ye = (math.cos(i * 3.1415926 / 8) * 21 + picture_height / 2)
        dda((picture_width / 2, picture_height / 2), (int(xe), int(ye)), pixels,
            (int(128 * i / 16.0) + 128, int(128 * i / 16.0) + 128, int(128 * i / 16.0) + 128))


mgr, scene = FbxCommon.InitializeSdkObjects()
converter = FbxCommon.FbxGeometryConverter(mgr)
ret = FbxCommon.LoadScene(mgr, scene, "monkey.fbx")
converter.Triangulate(scene, False)
root = scene.GetRootNode()
mesh = root.GetChild(0)
attr_type = mesh.GetNodeAttribute().GetAttributeType()

fov = 90.0
n = near_plane = 0.1
f = far_plane = 1000

picture_width = 512
picture_height = 512
img = None
fasfda = 512

rot = 10.
def my_update(whata):
    now = time.time()*10
    theta = np.radians(now)
    c, s = np.cos(theta), np.sin(theta)
    Rz = np.matrix(((c,-s,0,0),(s,c,0,0),(0,0,1,0),(0,0,0,1)))
    Ry = np.matrix(((c,0,s,0),(0,1,0,0),(-s,0,c,0),(0,0,0,1)))

    model_matrix = np.matrix([[1, 0., 0., 0.],
                                 [0., 1., 0., 0.],
                                 [0., 0., 1., 0.],
                                 [0., 0., 3., 1]])

    proj_matrix = np.matrix([[n / 1, 0., 0., 0.],
                                [0., n / 1, 0., 0.],
                                [0., 0., -(f + n) / (f - n), -2.0 * f * n / (f - n)],
                                [0., 0., -1., 0.]])


    img = Image.new("RGB", (picture_width, picture_height))
    pixels = img.load()
    mvp =  Rz * Ry * model_matrix* proj_matrix
    test_draw_mesh(mesh.GetMesh(), pixels, mvp)
    imgtk = ImageTk.PhotoImage(img)
    panel.configure(image = imgtk)
    panel.image = imgtk


root = Tk()
imgtk = ImageTk.PhotoImage(Image.new("RGB", (picture_width, picture_height)))
panel = Label(root, image = imgtk)
panel.pack(side = "bottom", fill = "both", expand = "yes")
root.bind("<Return>", my_update)
root.mainloop()


