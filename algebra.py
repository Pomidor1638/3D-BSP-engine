
from settings import *
def null(x, accuracy):
    return (abs(x) < accuracy)
def sgn(x):
    if x == 0:
        return 0
    elif x > 0:
        return 1
    else:
        return -1
def matrix_multiplying(first_matrix, second_matrix):
    n = len(first_matrix)
    l = len(second_matrix)
    m = len(second_matrix[0])
    result_matrix = [[0 for i in range(m)] for j in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(l):
                result_matrix[i][j] += first_matrix[i][k]*second_matrix[k][j]
    return result_matrix
def matrix_multiplying_by_Vinograd(matrix1, matrix2):
    rows1, cols1 = len(matrix1), len(matrix1[0])
    rows2, cols2 = len(matrix2), len(matrix2[0])
    if cols1 != rows2:
        raise ValueError("Invalid dimensions for matrix multiplication")
    row_factor = [0] * rows1
    col_factor = [0] * cols2
    for i in range(rows1):
        for j in range(cols1 // 2):
            row_factor[i] += matrix1[i][2 * j] * matrix1[i][2 * j + 1]
    for i in range(cols2):
        for j in range(rows2 // 2):
            col_factor[i] += matrix2[2 * j][i] * matrix2[2 * j + 1][i]
    result = [[0] * cols2 for _ in range(rows1)]
    for i in range(rows1):
        for j in range(cols2):
            result[i][j] = -row_factor[i] - col_factor[j]
            for k in range(cols1 // 2):
                result[i][j] += (matrix1[i][2 * k] + matrix2[2 * k + 1][j]) * (matrix1[i][2 * k + 1] + matrix2[2 * k][j])
    if cols1 % 2 != 0:
        for i in range(rows1):
            for j in range(cols2):
                result[i][j] += matrix1[i][cols1 - 1] * matrix2[cols1 - 1][j]

    return result
def scalar_vector_multiplying(vector1, vector2):
    N = len(vector1)
    summ = 0
    for i in range(N):
        summ += vector1[i] * vector2[i]
    return summ
def vector_multiplied_on_number(vector, number):
    N = len(vector)
    result = []
    for i in range(N):
        result.append(vector[i]*number)
    return result
def sum_of_vectors(vector1, vector2, sum = True):
    N = len(vector1)
    result = []
    d = 1 if sum else -1
    for i in range(N):
        result.append(vector1[i] + d*vector2[i])
    return result
def normalize(vector):
    length = 0
    for i in range(len(vector)):
        length += vector[i]*vector[i]
    length = math.sqrt(length)
    return vector_multiplied_on_number(vector, 1/length)
def module(vector):
    length = 0
    for i in range(len(vector)):
        length += vector[i] * vector[i]
    return math.sqrt(length)
def transfer(plane, dx, dy, dz):
    result = []
    for point in plane:
        result.append((point[0] + dx, point[1] + dy, point[2] + dz))
    return result
def rotation_matrix_x(angle):
    sin_a, cos_a = math.sin(angle), math.cos(angle)
    return (
        (1,      0,     0),
        (0,  cos_a, sin_a),
        (0, -sin_a, cos_a)
    )
def rotation_matrix_y(angle):
    sin_a, cos_a = math.sin(angle), math.cos(angle)
    return (
        ( cos_a,  0,  sin_a),
        (     0,  1,      0),
        (-sin_a,  0,  cos_a)
    )
def rotation_matrix_z(angle):
    sin_a, cos_a = math.sin(angle), math.cos(angle) #!!!ЭТА МАТРИЦА ПОВОРОТА ПРАВИЛЬНАЯ Т.К. УГОЛ ОТСЧИТАВАЕТСЯ ОТ ОСЕЙ Y Д0 X!!!!
    return (
        (cos_a, -sin_a, 0),
        (sin_a,  cos_a, 0),
        (    0,      0, 1)
    )
def rotation_of_plane(matrix, rotation, rot_point):
    x_rot, y_rot, z_rot = rotation
    matrix = transfer(matrix, -rot_point[0], -rot_point[1], -rot_point[2])
    return transfer(matrix_multiplying(matrix_multiplying(matrix_multiplying(matrix,
           rotation_matrix_z(z_rot)),
           rotation_matrix_x(x_rot)),
           rotation_matrix_y(y_rot)),
           rot_point[0], rot_point[1], rot_point[2])
def rotation_of_plane2(matrix, rotation):
    x_rot, y_rot, z_rot = rotation
    return matrix_multiplying(matrix_multiplying(matrix_multiplying(matrix,
           rotation_matrix_z(z_rot)),
           rotation_matrix_x(x_rot)),
           rotation_matrix_y(y_rot))
def rotation(matrix, rotation, rot_point):
    result = []
    L = len(matrix)
    for i in range(L):
        result.append([rotation_of_plane(matrix[i][0], rotation, rot_point), matrix[i][1], rotation_of_plane2([matrix[i][2][0]], rotation)[0]])
        result[i][2] = [result[i][2], -scalar_vector_multiplying(result[i][2], result[i][0][0])]
    return result
def rotation_around_a_line(matrix, lead_vector, phi):
    m = math.sqrt(scalar_vector_multiplying(lead_vector, lead_vector))
    if m != null(1, accuracy):
        lead_vector = vector_multiplied_on_number(lead_vector, 1 / m)
    x, y, z = lead_vector
    cos_phi = math.cos(phi)
    sin_phi = math.sin(phi)
    k = 1 - cos_phi
    rotation_matrix = (
        (  cos_phi + k*x*x, k*y*x + z*sin_phi, k*x*z - y*sin_phi),
        (k*x*y - z*sin_phi,   cos_phi + k*y*y, k*z*y + x*sin_phi),
        (k*x*z + y*sin_phi, k*z*y - x*sin_phi,   cos_phi + k*z*z)
    )
    result = []
    for i in range(len(matrix)):
        result.append([
            matrix_multiplying(matrix[i][0], rotation_matrix),
            matrix[i][1],
            matrix_multiplying([matrix[i][2]], rotation_matrix)[0]
        ])
    return result
def linear_perspective(plane, xs = 0, ys = 0):
    perspective = []
    for point in plane:
        x, y, z = point
        perspective.append((round(HALF_WIDTH + HALF_WIDTH*x*DIST/y/screen_koef + xs), round(HALF_HEIGHT - HALF_HEIGHT*z*DIST/y + ys)))
    return tuple(perspective)
def determinant(matrix):
    N = len(matrix)
    if N == 3:
        p0, p1, p2 = matrix
        x0, y0, z0 = p0
        x1, y1, z1 = p1
        x2, y2, z2 = p2
        dx1, dx2 = x1 - x0, x2 - x0
        dy1, dy2 = y1 - y0, y2 - y0
        dz1, dz2 = z1 - z0, z2 - z0
        A = dy1 * dz2 - dy2 * dz1
        B = dz1 * dx2 - dx1 * dz2
        C = dx1 * dy2 - dy1 * dx2

        return A * x0 + B * y0 + C * z0
    else:
        if N == 2:
            return matrix[0][0]*matrix[1][1]-matrix[0][1]*matrix[1][0]
        det = 0
        q = 1
        for m in range(N):
            M = []
            for i in range(1, N):
                L = []
                for j in range(N):
                    if (j != m):
                        L.append(matrix[i][j])
                M.append(L)
            if matrix[0][m] != 0:
                det += q*determinant(M)*matrix[0][m]
                #print(det)
            q *= -1
        return det
def normal_vertex(plane, version = True):
    p0, p1, p2 = plane[:3]
    x0, y0, z0 = p0
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    dx1, dx2 = x1 - x0, x2 - x0
    dy1, dy2 = y1 - y0, y2 - y0
    dz1, dz2 = z1 - z0, z2 - z0
    A = dy1 * dz2 - dy2 * dz1
    B = dz1 * dx2 - dx1 * dz2
    C = dx1 * dy2 - dy1 * dx2
    if not version:
        return A, B, C
    module = math.sqrt(A*A + B*B + C*C)
    return A/module, B/module, C/module
def parametr(p0, vector, plane):
    normal_vector = plane[0]
    D = plane[1]
    vector_mult = scalar_vector_multiplying(vector, normal_vector)
    if vector_mult == 0:
        return None
    return - (scalar_vector_multiplying(normal_vector, p0) + D) / vector_mult

def intersection_of_a_line_and_a_plane(p0, p1, cut_plane):
    normal_vector = cut_plane[0]
    D = cut_plane[1]
    a = sum_of_vectors(p1, p0, False)
    vector_mult = scalar_vector_multiplying(a, normal_vector)
    if vector_mult == 0:
        return None
    else:
        t = - (scalar_vector_multiplying(normal_vector, p0) + D) / vector_mult
        if (t <= 0) or (t >= 1):
            return None
        return sum_of_vectors(p0, vector_multiplied_on_number(a, t))
def distance_to_plane(point, plane):
    x, y, z = point
    A, B, C = plane[0]
    D = plane[1]
    position = A * x + B * y + C * z + D
    return position
def positioning(point, plane):
    position = distance_to_plane(point, plane)
    if null(position, accuracy):
        return None
    else:
        return position > 0
def Support_position(pos1, pos2):
    if pos1 is None:
        pos1 = 0
    else:
        pos1 = 1 if pos1 else -1
    if pos2 is None:
        pos2 = 0
    else:
        pos2 = 1 if pos1 else -1
    return (pos1 + pos2 != 0)
def Sutherland_Hodgman_algorithm(plane, cut_plane):
    L = len(plane)
    Left = []
    Right = []
    points = []
    for i in range(L):
        points.append(positioning(plane[i], cut_plane))
    if not((points.count(False) > 0) and (points.count(True) > 0)):
        if (False in points):
            return -1
        elif (True in points):
            return 1
        else:
            return 0
    #Положительная часть
    for i in range(L):
        m0 = (points[i] is True) or (points[i] is None)
        m1 = (points[(i + 1) % L] is True) or (points[(i + 1) % L] is None)
        p0 = plane[i]
        p1 = plane[(i + 1) % L]
        if (m0 and m1):
            Right.append(p0)
        elif ((m0 and (not m1))):
            p = intersection_of_a_line_and_a_plane(p0, p1, cut_plane)
            Right.append(p0)
            if p is not None:
                Right.append(p)

        elif ((m1 and (not m0))):
            p = intersection_of_a_line_and_a_plane(p0, p1, cut_plane)
            if p is not None:
                Right.append(p)


    #Отрицательная часть
        m0 = not points[i]
        m1 = not points[(i + 1) % L]
        p0 = plane[i]
        p1 = plane[(i + 1) % L]
        if (m0 and m1):
            Left.append(p0)
        elif ((m0 and (not m1))):
            p = intersection_of_a_line_and_a_plane(p0, p1, cut_plane)
            Left.append(p0)
            if p is not None:
                Left.append(p)

        elif ((m1 and (not m0))):
            p = intersection_of_a_line_and_a_plane(p0, p1, cut_plane)
            if p is not None:
                Left.append(p)
    if (len(Left) < 3) or (len(Right) < 3):
        return 1/0
    return Left, Right
def optimal_plane(matrix):
    score = None
    for test_plane in matrix:
        right = 0
        left = 0
        for plane in matrix:
            if plane == test_plane:
                continue
            for point in plane[0]:
                position = positioning(point, test_plane[2])
                if position is not None:
                    if position:
                        right += 1
                    else:
                        left += 1
        if score is None:
            score = abs(right - left)
            opt_plane = test_plane
        else:
            delta = abs(right - left)
            if (score > delta):
                score = delta
                opt_plane = test_plane
    return opt_plane
def point_on_face(point, plane):
    if positioning(point, plane[2]) is None:
        math_plane = plane[0]
        N = len(math_plane)
        k = None
        for i in range(N):
            p0 = math_plane[i]
            p1 = math_plane[(i + 1) % N]
            p2 = sum_of_vectors(p1, plane[2][0])
            n = normal_vertex([p0, p1, p2])
            p = distance_to_plane(point, (n, -scalar_vector_multiplying(n, p0)))
            if p == 0:
                return True
            if k is None:
                k = (p > 0)
            else:
                if k != (p > 0):
                    return False
        return True
    else:
        return False


def cross(v1, v2):
    ax, ay, az = v1
    bx, by, bz = v2
    A = ay*bz - az*by
    B = az*bx - ax*bz
    C = ax*by - ay*bx
    return A, B, C

k = 0
class BSP():
    def __init__(self):
        self.number = None
        self.root = None
        self.mid = None
        self.right = None
        self.left = None

    def set_bsp_tree(self, matrix):
        global k
        self.number = k
        k += 1
        if len(matrix) <= 1:
            if len(matrix) == 1:
                self.root = matrix[0]
        else:
            self.root = optimal_plane(matrix)
            root_plane = self.root[2]
            self.right = BSP()
            self.left = BSP()
            self.mid = []
            Right = []
            Left = []
            for plane in matrix:
                if (self.root != plane):
                    partition = Sutherland_Hodgman_algorithm(plane[0], root_plane)
                    if partition == 0:
                        self.mid.append(plane)
                    else:
                        if partition == 1:
                            Right.append(plane)
                        elif partition == -1:
                            Left.append(plane)
                        else:
                            Right.append((partition[1], plane[1], plane[2]))
                            Left.append((partition[0], plane[1], plane[2]))
            self.right.set_bsp_tree(Right)
            self.left.set_bsp_tree(Left)
