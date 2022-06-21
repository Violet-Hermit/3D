import time

import keyboard
import numpy as np
from math import *
from random import randint
from tkinter import *


# Определяет поведение точкек и векторов, операции с ними
# для класов Point и Vector есть следующие аксиомы:
# Аксиома 1: разность между двумя точками — это вектор
# Аксиома 2: сумма точки и вектора — это точка
# Нужно переделывать все при помощи NumPy, но для этого нужно реализовать перегрузку конструктора,
# чтобы все операции могли проводится как с кортежами так и с масивами NumPy


class Point:
    points_array = []

    def __init__(self, x=0, y=0, z=0, set_to_static=True):
        self.coord = (x, y, z)
        Point.points_array.append(self)

    def __repr__(self):
        return str(self.coord)

    def add_vector_to_point(self, vector):
        point_x, point_y, point_z = self.coord
        vector_x, vector_y, vector_z = vector.coord
        result_point = Point(point_x + vector_x, point_y + vector_y, point_z + vector_z)
        return result_point
        # return tuple(point_x + vector_x, point_y + vector_y, point_z + vector_z)

    def subtract_vector_from_point(self, vector):
        point_x, point_y, point_z = self.coord
        vector_x, vector_y, vector_z = vector.coord
        result_point = Point(point_x - vector_x, point_y - vector_y, point_z - vector_z)
        return result_point
        # return tuple(point_x - vector_x, point_y - vector_y, point_z - vector_z)

    def add_point_to_point(self, point):
        point1_x, point1_y, point1_z = point.coord
        point2_x, point2_y, point2_z = self.coord
        result_vector = Vector(point2_x - point1_x, point2_y - point1_y, point2_z - point1_z)
        return result_vector
        # return tuple(point2_x - point1_x, point2_y - point1_y, point2_z - point1_z)

    def draw_point(self):
        x, y, z = self.coord
        canvas.create_line(x, y, x+1, y, fill="black")

    def move(self, point):
        x_bias, y_bias, z_bias = point.coord
        self.coord = (x_bias, y_bias, z_bias)

    def bias(self, x_bias, y_bias, z_bias):
        x, y, z = self.coord
        self.coord = (x + x_bias, y + y_bias, z + z_bias)


class Vector:
    def __init__(self, x=0, y=0, z=0):
        self.coord = (x, y, z)

    def add_vector_to_vector(self, vector):
        vector1_x, vector1_y, vector1_z = self.coord
        vector2_x, vector2_y, vector2_z = vector.coord
        result_vector = Vector(vector1_x + vector2_x, vector1_y + vector2_y, vector1_y + vector2_z)
        return result_vector
        # return tuple(vector1_x + vector2_x, vector1_y + vector2_y, vector1_y + vector2_z)

    def subtract_vector_from_vector(self, vector):
        vector1_x, vector1_y, vector1_z = self.coord
        vector2_x, vector2_y, vector2_z = vector.coord
        result_vector = Vector(vector1_x - vector2_x, vector1_y - vector2_y, vector1_y - vector2_z)
        return result_vector
        # return tuple((vector1_x - vector2_x, vector1_y - vector2_y, vector1_y - vector2_z))

    def spin_xy(self, angle):
        angle = radians(angle)
        transformation_matrix = [[cos(angle), -1 * sin(angle), 0], [sin(angle), cos(angle), 0], [0, 0, 1]]
        x, y, z = list(multiply_matrices(self.coord, transformation_matrix))
        return Vector(x, y, z)
        # return tuple(multiply_matrices(self.coord, transformation_matrix))

    def spin_yz(self, angle):
        transformation_matrix = [[1, 0, 0], [0, cos(angle), -1 * sin(angle)], [0, sin(angle), cos(angle)]]
        return multiply_matrices(self.coord, transformation_matrix)

    def spin_xz(self, angle):
        transformation_matrix = [[cos(angle), 0, sin(angle)], [0, 1, 0], [-1 * sin(angle), 0, cos(angle)]]
        return multiply_matrices(self.coord, transformation_matrix)

    def do_scale(self, s0, s1, s2):
        x, y, z = self.coord
        self.coord = (x * s0, y * s1, z * s2)
        return self

    def move(self, point):
        x_bias, y_bias, z_bias = point.coord
        self.x += x_bias
        self.y += y_bias
        self.z += z_bias


class Camera:
    def __init__(self, max_x, min_x, max_y, min_y, max_z, min_z):
        self.max_x = max_x
        self.min_x = min_x
        self.max_y = max_y
        self.min_y = min_y
        self.max_z = max_z
        self.min_z = min_z

    def draw_scene(self):
        pass


# Глобальные переменные конечно плохо, но это вроде делает код чище
def initialize_screen(wdh, hgh):
    global wnd
    global canvas
    wnd = Tk()
    canvas = Canvas(wnd, width=wdh, height=hgh)
    canvas.pack()


def clearing_screen():
    canvas.delete("all")


# Просто умножение матриц средствами NumPy,
# тоже сделать прегрузку чтобы в случае подачи на вход масивов NumPy все продолжало работать

def multiply_matrices(mtx1, mtx2):
    matrix1 = np.array(mtx1)
    matrix2 = np.array(mtx2)
    result = matrix1.dot(matrix2).tolist()
    return result


def scale_05():  # A
    origin = Point.points_array[0]
    temp_vector = Vector()
    for i in range(len(Point.points_array)):
        temp_vector = Vector(*Point.points_array[i].coord)
        Point.points_array[i].coord = temp_vector.do_scale(0.5, 0.5, 0.5).coord
    redraw_screen()


def scale_2():  # S
    origin = Point.points_array[0]
    temp_vector = Vector()
    for i in range(len(Point.points_array)):
        temp_vector = Vector(*Point.points_array[i].coord)
        Point.points_array[i].coord = temp_vector.do_scale(2, 2, 2).coord
    redraw_screen()


# код переделан, вместо описаных операторов пришлось использовать костыль что плохо, но это ускоряет програму и убирает
# геометрическое увеличение кол-ва точек
def roted_1_degree_xy():  # R
    origin = Point.points_array[0]
    temp_vector = Vector()
    for i in range(1, len(Point.points_array)):
        temp_vector = Vector(*Point.points_array[i].coord)
        Point.points_array[i].coord = temp_vector.spin_xy(1).coord
    redraw_screen()


def redraw_screen():  # D
    clearing_screen()
    for i in Point.points_array:
        i.draw_point()


# Утечка памяти происходит из-за модуля canvas, при каждой новой отрисовке жрётся память
# Старые эллементы не удаляются поэтому память утекает тоже самое касается и остальных проектов кроме серпинского
def handle_clicks():
    if keyboard.is_pressed('ctrl + 1'):
        scale_2()

    if keyboard.is_pressed('ctrl + 2'):
        scale_05()

    if keyboard.is_pressed('ctrl + 3'):
        roted_1_degree_xy()

    if keyboard.is_pressed('ctrl + 4'):
        redraw_screen()


if __name__ == '__main__':
    initialize_screen(1000, 1000)
    point = Point(0, 0, 0)
    print(*Point.points_array)
    points = [Point(randint(130, 150), randint(130, 150), 0) for i in range(50)]
    # roted_15_degree_xy()
    # roted_15_degree_xy()  # при каждом применении кол-во точек в статик масиве увеличивается в два раза
    # то происходит потому что в каждой операции участвует оператор из класса Point который возвращает новый экземпляр
    # класса который добавляется в статик масив или хз как он тут называется, идея создать нейтральную точку которая
    # используется только в операциях, но результатом будет ссылка которая перестанет хранить нужные данные уже после
    # вызова следующего метода
    handle_clicks()
    time2 = 0
    time1 = 0
    while 1:
        flag = True if time2 - time1 <= 0.05 else False


        time.sleep(0.05 - (time2 - time1) * flag)
        time1 = time.time()
        handle_clicks()
        redraw_screen()
        # print(len(Point.points_array))
        wnd.update()
        time2 = time.time()
