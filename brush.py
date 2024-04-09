from algebra import *

"""class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    def __init__(self, point):
        self.x = point.x
        self.y = point.y
        self.z = point.z
    @property
    def get(self):
        return x, y, z"""

class Plane:
    def __init__(self, math_plane = [], inverse = False):
        self.math_plane = math_plane
        self.normal_vector = normal_vertex(math_plane, inverse)
        self.dist0 = -scalar_vector_multiplying(self.normal_vector, self.math_plane[0])

class Brush:
    def __init__(self, planes):
        self.planes = planes
        self.collision_planes = list(planes)
        self.N = len(planes)
        for i in range(N):
            dist = 0
            for j in range(8):
                dist = max(dist, (BBOX[i], vector_multiplied_on_number(planes[i].normal_vector, -1)))
            self.collision_planes[i].dist0 -= dist

class Matrix:
    def __init__(self, brushes):
        brush_count = len(brushes)
        self.planes = []
        self.collision_boxes = []
        for i in range(brush_count):
            for j in range(brushes[i].N):
                self.planes.append(brushes[i].planes[j])
            self.collision_boxes.append(brushes[i].collision_planes)


