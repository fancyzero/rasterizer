fov = 90.0
near_plane = 1.0
far_plane = 1000.0
picture_width = 512
picture_height = 512
import numpy



mat = numpy.matrix([[1, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]])

v=numpy.array((1,2,3,4))

v = (v * mat)
r = (numpy.array(v)).flatten()
r = r[0:3]
t = r[-1]
print r / float(t)
print r,t


