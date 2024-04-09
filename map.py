import math
from algebra import *
from brush import *


def Parallelepiped(p0, p1, c = 7):
    x0, y0, z0 = p0
    x1, y1, z1 = p1
    result = []
    dx, dy, dz = sgn(x1 - x0), sgn(y1 - y0), sgn(z1 - z0)
    result = [
        [[
            [x0, y0, z0], [x1, y0, z0], [x1, y1, z0], [x0, y1, z0]
        ], c, [0, 0, -dz]],
        [[
            [x0, y0, z1], [x1, y0, z1], [x1, y1, z1], [x0, y1, z1]
        ], c, [0, 0, dz]],
        [[
            [x0, y0, z0], [x0, y0, z1], [x0, y1, z1], [x0, y1, z0]
        ], c, [-dx, 0, 0]],
        [[
            [x1, y0, z0], [x1, y0, z1], [x1, y1, z1], [x1, y1, z0]
        ], c, [dx, 0, 0]],
        [[
            [x0, y0, z0], [x1, y0, z0], [x1, y0, z1], [x0, y0, z1]
        ], c, [0, -dy, 0]],
        [[
            [x0, y1, z0], [x1, y1, z0], [x1, y1, z1], [x0, y1, z1]
        ], c, [0, dy, 0]],
    ]
    for i in range(6):
        result[i][2] = [result[i][2], -scalar_vector_multiplying(result[i][0][0], result[i][2])]
    return result
def Triangle(p0, p1, p2, c = 7, side = 0):
    n = normal_vertex([p0, p1, p2])
    d = -scalar_vector_multiplying(n, p0)
    if side == 0:
        return [
            [
                [p0, p1, p2],
                c,
                [n, d]
            ],
            [
                [p0, p1, p2],
                c,
                [vector_multiplied_on_number(n, -1), -d]
            ],
        ]
    else:
        s = 1 if side == 1 else -1
        return [
            [
                [p0, p1, p2],
                c,
                [vector_multiplied_on_number(n, s), s * d]
            ]
        ]
def Regular_prism(center, radius, height, number, c = 7):
    x0, y0, z0 = center
    d = sgn(height)
    delta = 2 * math.pi / number
    cur_a = 0
    Base1 = []
    Base2 = []
    prism = []
    for i in range(number):
        dx1, dy1 = radius * math.cos(cur_a), radius * math.sin(cur_a)
        Base1.append([x0 + dx1, y0 + dy1, z0])
        Base2.append([x0 + dx1, y0 + dy1, z0 + height])
        cur_a += delta
    for i in range(number):
        k = (i + 1) % number
        p0 = Base1[i]
        p1 = Base1[k]
        p2 = Base2[k]
        p3 = Base2[i]
        math_plane = (p0, p1, p2, p3)
        normal_vector = vector_multiplied_on_number(normal_vertex(math_plane, True), d)
        D = -scalar_vector_multiplying(p0, normal_vector)
        prism.append((math_plane, c, [normal_vector, D]))
    prism.append([Base1, c, [vector_multiplied_on_number([0, 0, -1], d),
                             -scalar_vector_multiplying([0, 0, -1], Base1[0])]])
    prism.append([Base2, c, [vector_multiplied_on_number([0, 0, 1], d),
                             -scalar_vector_multiplying([0, 0, 1], Base2[0])]])
    return prism
def Regular_pyramid(center, radius, height, number, c = 7):
    x0, y0, z0 = center
    delta = 2 * math.pi / number
    d = 1#sgn(height)
    cur_a = 0
    Base = []
    pyramid = []
    for i in range(number):
        dx1, dy1 = radius * math.cos(cur_a), radius * math.sin(cur_a)
        Base.append([x0 + dx1, y0 + dy1, z0])
        cur_a += delta
    for i in range(number):
        p0 = Base[i]
        p1 = Base[(i + 1) % number]
        math_plane = [p0, p1, [x0, y0, z0 + height]]
        normal_vector = vector_multiplied_on_number(normal_vertex(math_plane, True), d)
        D = -scalar_vector_multiplying(p0, normal_vector)
        pyramid.append([math_plane, c, [normal_vector, D]])
        pyramid.append([[p0, p1, center], c, [vector_multiplied_on_number([0, 0, -1], d), D]])
    #pyramid.append([Base, c, vector_multiplied_on_number([0, 0, -1], d)])
    return pyramid

def Sphere(center, radius, number, c = 7):
    delta_a = 2 * math.pi / number
    delta_z = math.pi / number
    cur_z = 0
    cur_a = 0
    x0, y0, z0 = center
    result = []
    tablet = []
    for i in range(number):
        tablet.append([math.cos(cur_a), math.sin(cur_a)])
        cur_a += delta_a
    for i in range(number):
        small_radius_1, small_radius_2 = radius * math.sin(cur_z), radius * math.sin(cur_z + delta_a/2)
        dz1, dz2 = radius * math.cos(cur_z), radius * math.cos(cur_z + delta_z)
        for j in range(number):
            cos_a1, sin_a1 = tablet[j]
            cos_a2, sin_a2 = tablet[(j + 1) % number]
            p0 = [x0 + small_radius_1 * cos_a1, y0 + small_radius_1 * sin_a1, z0 + dz1]
            p1 = [x0 + small_radius_2 * cos_a1, y0 + small_radius_2 * sin_a1, z0 + dz2]
            p2 = [x0 + small_radius_2 * cos_a2, y0 + small_radius_2 * sin_a2, z0 + dz2]
            p3 = [x0 + small_radius_1 * cos_a2, y0 + small_radius_1 * sin_a2, z0 + dz1]
            if i == 0 or i == number - 1:
                if i == 0:
                    math_plane = [p0, p1, p2]
                else:
                    math_plane = [p0, p1, p3]
                normal_vector = normal_vertex(math_plane, True)

                D = -scalar_vector_multiplying(p0, normal_vector)
                if positioning((x0, y0, z0), (normal_vector, D)) is True:
                    normal_vector = vector_multiplied_on_number(normal_vector, -1)
                result.append([math_plane, c, [normal_vector, D]])
            else:
                math_plane = [p0, p1, p2, p3]
                normal_vector = normal_vertex(math_plane, True)

                D = -scalar_vector_multiplying(p0, normal_vector)
                if positioning((x0, y0, z0), (normal_vector, D)) is True:
                    normal_vector = vector_multiplied_on_number(normal_vector, -1)
                result.append([math_plane, c, [normal_vector, D]])

        cur_z += delta_z
    return result

def Regular_truncated_pyramid(center, first_radius, second_radius, height, number, c = 7):
    x0, y0, z0 = center
    delta = 2 * math.pi / number
    cur_a = 0
    Base1 = []
    Base2 = []
    regular_truncated_pyramid = []
    for i in range(number):
        dx1, dy1 = first_radius * math.cos(cur_a), first_radius * math.sin(cur_a)
        dx2, dy2 = second_radius * math.cos(cur_a), second_radius * math.sin(cur_a)
        Base1.append([x0 + dx1, y0 + dy1, z0])
        Base2.append([x0 + dx2, y0 + dy2, z0 + height])
        cur_a += delta
    for i in range(number):
        k = (i + 1) % number
        p0 = Base1[i]
        p1 = Base1[k]
        p2 = Base2[k]
        p3 = Base2[i]
        math_plane = (p0, p1, p2, p3)
        normal_vector = normal_vertex(math_plane, True)
        regular_truncated_pyramid.append([math_plane, c, normal_vector])
    regular_truncated_pyramid.append([Base1, c, [[0, 0, -1], -scalar_vector_multiplying(Base1[0], [0, 0, -1])]])
    regular_truncated_pyramid.append([Base2, c, [[0, 0, 1], -scalar_vector_multiplying(Base2[0], [0, 0, 1])]])
    return regular_truncated_pyramid

def Stul(pos, size):
    result = []
    result += Parallelepiped((-0.3*size, -0.3*size, -0.05*size), (0.3*size, 0.3*size, 0.05*size))
    result += Parallelepiped((-0.28*size, -0.28*size, -0.6*size), (-0.18*size, -0.18*size, -0.05*size), 8)
    result += Parallelepiped((0.18*size, -0.28*size, -0.6*size), (0.28*size, -0.18*size, -0.05*size), 8)
    result += Parallelepiped((0.18*size, 0.18*size, -0.6*size), (0.28*size, 0.28*size, -0.05*size), 8)
    result += Parallelepiped((-0.28*size, 0.18*size, -0.6*size), (-0.18*size, 0.28*size, -0.05*size), 8)
    result += Parallelepiped((-0.28*size, 0.18*size, 0.05*size), (0.28*size, 0.28*size, 0.75*size), 11)
    for i in range(36):
        result[i][0] = transfer(result[i][0], pos[0], pos[1], pos[2])
    return result

def generate_torus(center, section_radius, overall_radius, num_sections, num_points_per_section, c=7):
    torus = []
    delta_phi = 2 * math.pi / num_sections
    delta_alpha = 2 * math.pi / num_points_per_section
    phi = delta_phi/2
    for i in range(num_sections):
        torus_section = []
        cos_p, sin_p = math.cos(phi), math.sin(phi)
        alpha = delta_alpha/2
        for j in range(num_points_per_section):
            cos_a, sin_a = math.cos(alpha), math.sin(alpha)

            x0 = overall_radius * cos_p + center[0]
            y0 = overall_radius * sin_p + center[1]
            z0 = center[2]

            x = x0 + section_radius * cos_a * cos_p
            y = y0 + section_radius * cos_a * sin_p
            z = z0 + section_radius * sin_a

            torus_section.append([[x, y, z], [x0, y0, z0]])

            alpha += delta_alpha

        torus.append(torus_section)
        phi += delta_phi
    torus_faces = []
    for i in range(num_sections):
        section0 = torus[i]
        section1 = torus[(i + 1) % num_sections]

        for j in range(num_points_per_section):
            p0 = section0[j][0]
            p1 = section0[(j + 1) % num_points_per_section][0]
            p2 = section1[(j + 1) % num_points_per_section][0]
            p3 = section1[j][0]
            normal_vector = normal_vertex([p0, p1, p2], True)
            if positioning(section0[j][1], normal_vector, p0):
                normal_vector = vector_multiplied_on_number(normal_vector, -1)
            torus_faces.append([
                [p0, p1, p2, p3],
                c,
                [normal_vector, -scalar_vector_multiplying(vector, p0)]
            ])
    return torus_faces

def make_collision_box(brush, BBOX):
    collision_box = []
    for i in range(len(brush)):
        dist = 0
        n = brush[i][2][0]
        for j in range(8):
            dist = max(dist, scalar_vector_multiplying(BBOX[j], vector_multiplied_on_number(n, -1)))
        collision_box.append([n, brush[i][2][1] - dist])
    return collision_box


BBOX = transfer(BBOX, 0, 0, -0.75)

brushes = []
matrix = []
collision_boxes_types = []



brushes.append(Parallelepiped((-100, -100, -1), (100, 100, 0), 9))
brushes.append(Parallelepiped((-101, -100, -1), (-100, 100, 100), 9))
brushes.append(Parallelepiped((-101, 100, -1), (101, 101, 100), 9))
brushes.append(Parallelepiped((100, -100, -1), (101, 100, 100), 9))
brushes.append(Parallelepiped((-101, -101, -1), (101, -100, 100), 9))
#brushes.append(Parallelepiped((-101, -101, 100), (101, 101, 101), 9))
brushes.append(Parallelepiped((-90, 60, 0), (-79.2, 69.6, 5), 11))
brushes.append(Parallelepiped((-5, -5, 50), (5, 5, 60), 11))
brushes.append(rotation(Parallelepiped((-10, -10, 0), (10, 10, 1)), (1/4, 1/4, 0), (-10, -10, -10)))


col1 = []
col2 = []
for i in range(len(brushes)):
    matrix += brushes[i]
    col1.append(make_collision_box(brushes[i], BBOX))
    col2.append(make_collision_box(brushes[i], BBOX2))

collision_boxes_types.append(col1)
collision_boxes_types.append(col2)


def save(file_name, matrix):
    map_file = open(file_name+".txt", "w")
    for plane in matrix:
        for dot in plane[0]:
            map_file.write(" ".join(map(str, dot)) + ",")
        map_file.write("|")
        map_file.write(" ".join(map(str, plane[2][0])))
        map_file.write("|" + str(plane[1]) + "\n")
    map_file.close()
    return
def load(file_name):
    try:
        map_file = open(file_name + ".txt", "r")
        Map = map_file.read()
        map_file.close()
        planes = Map.split("\n")
    except FileNotFoundError:
        planes = ''
    M = []
    for plane in planes:
        if not(plane == '' or '#' in plane):
            s = plane.split(",|")
            s2 = s[1].split("|")
            colour = int(s2[1])
            if s2[0] == 'N':
                vector = None
            else:
                 vector = list(map(float, s2[0].split()))
            tops = s[0]
            H = []
            for top in tops.split(','):
                x, y, z = map(float, top.split())
                H.append([x, y, z])
            if vector is None:
                vector = normal_vertex(H)
            M.append([H, colour, [vector, -scalar_vector_multiplying(vector, H[0])]])
    return M


def save_bsp_tree(file_name, node, bsp_file = None):
    if bsp_file is None:
        bsp_file = open(file_name + ".bsp", "w")
    if node.root is not None:
        bsp_file.write(str(node.number) + '|')
        if node.left is None:
            bsp_file.write(str(-1))
        else:
            bsp_file.write(str(node.left.number))
        bsp_file.write(' ')
        if node.right is None:
            bsp_file.write(str(-1))
        else:
            bsp_file.write(str(node.right.number))
        bsp_file.write('|')
        if node.mid is None:
            N = 1
            bsp_file.write(str(N) + '\n')
            for dot in node.root[0]:
                bsp_file.write(" ".join(map(str, dot)) + ",")
            bsp_file.write("|")
            bsp_file.write(" ".join(map(str, node.root[2])))
            bsp_file.write("|" + str(node.root[1]) + "\n")
        else:
            N = 1 + len(node.mid)
            bsp_file.write(str(N) + '\n')
            for dot in node.root[0]:
                bsp_file.write(" ".join(map(str, dot)) + ",")
            bsp_file.write("|")
            bsp_file.write(" ".join(map(str, node.root[2])))
            bsp_file.write("|" + str(node.root[1]) + "\n")
            for i in range(0, N - 1):
                for dot in node.mid[i][0]:
                    bsp_file.write(" ".join(map(str, dot)) + ",")
                bsp_file.write("|")
                bsp_file.write(" ".join(map(str, node.mid[i][2])))
                bsp_file.write("|" + str(node.mid[i][1]) + "\n")
            save_bsp_tree(file_name, node.left, bsp_file)
            save_bsp_tree(file_name, node.right, bsp_file)
    else:
        bsp_file.write(str(node.number) + '|-1 -1|0\n')
def load_bsp_tree(file_name, node):
    try:
        file = open(file_name + ".bsp", "r")
        Bsp = file.read()
        file.close()
        Bsp = Bsp.split("\n")
    except FileNotFoundError:
        Bsp = ''
    k = 0
    result = {}
    for i in Bsp:
        pass


node = BSP()
print("Начало построения...")
node.set_bsp_tree(matrix)
print("Конец")
