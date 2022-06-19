import keyboard
import numpy as np
import time
import sys

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

    def __init__(self, x=0, y=0, z=0):
        self.coord = (x, y, z)
        print(x,y,z)
        Point.points_array.append(self)

    def add_vector_to_point(self, vector):
        point_x, point_y, point_z = self.coord
        vector_x, vector_y, vector_z = vector.coord
        result_point = Point(point_x + vector_x, point_y + vector_y, point_z + vector_z)
        return result_point

    def subtract_vector_from_point(self, vector):
        point_x, point_y, point_z = self.coord
        vector_x, vector_y, vector_z = vector.coord
        result_point = Point(point_x - vector_x, point_y - vector_y, point_z - vector_z)
        return result_point

    def add_point_to_point(self, point):
        point1_x, point1_y, point1_z = point.coord
        point2_x, point2_y, point2_z = self.coord
        result_vector = Vector(point2_x - point1_x, point2_y - point1_y, point2_z - point1_z)
        return result_vector

    def draw_point(self):
        x, y, z = self.coord
        canvas.create_line(x, y, x + 1, y, fill="black")

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

    def subtract_vector_from_vector(self, vector):
        vector1_x, vector1_y, vector1_z = self.coord
        vector2_x, vector2_y, vector2_z = vector.coord
        result_vector = Vector(vector1_x - vector2_x, vector1_y - vector2_y, vector1_y - vector2_z)
        return result_vector

    def spin_xy(self, angle):
        angle = radians(angle)
        transformation_matrix = [[cos(angle), -1 * sin(angle), 0], [sin(angle), cos(angle), 0], [0, 0, 1]]
        x, y, z = list(multiply_matrices(self.coord, transformation_matrix))
        return Vector(x, y, z)

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


# Глобальные переменные конечно плохо, но это вроде делает код чище
def initialize_screen(wdh, hgh):
    global wnd
    global canvas
    wnd = Tk()
    canvas = Canvas(wnd, width=wdh, height=hgh)
    canvas.pack()
    colors = "black"


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
    #origin = Point.points_array[0]
    temp_vector = Vector()
    for i in range(len(Point.points_array)):
        temp_vector = Point.points_array[i].add_point_to_point(Point.points_array[0])
        Point.points_array[i].move(Point.points_array[0])
        Point.points_array[i].add_vector_to_point(temp_vector.do_scale(0.5, 0.5, 0.5))
    redraw_screen()


def scale_2():  # S
    #origin = Point.points_array[0]
    temp_vector = Vector()
    for i in range(len(Point.points_array)):
        temp_vector = Point.points_array[i].add_point_to_point(Point.points_array[0])
        Point.points_array[i].move(Point.points_array[0])
        Point.points_array[i].add_vector_to_point(temp_vector.do_scale(2, 2, 2))
    redraw_screen()


def roted_15_degry_xy():  # R
    #origin = Point.points_array[0]
    temp_vector = Vector()
    for i in range(len(Point.points_array)):
        temp_vector = Point.points_array[i].add_point_to_point(Point.points_array[0])
        Point.points_array[i].move(Point.points_array[0])
        Point.points_array[i].add_vector_to_point(temp_vector.spin_xy(15))
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
        redraw_screen()

    if keyboard.is_pressed('ctrl + 3'):
        roted_15_degry_xy()

    if keyboard.is_pressed('ctrl + 4'):
        scale_2()


if __name__ == '__main__':
    print(id(Point(0, 0, 0)) == id(Point(0, 0, 0)))  # == False, Badly
    initialize_screen(1000, 1000)
    point = Point(0, 0, 0)
    point.draw_point()
    points = [Point(randint(100, 200), randint(100, 200), randint(100, 200)) for i in range(10)]
    #roted_15_degry_xy() # при каждом применении колво точек в статик масиве увеличивается в два раза
    handle_clicks()
    while 1:
        clearing_screen()
        handle_clicks()
        for i in range(len(Point.points_array)):
            Point.points_array[i].bias(randint(-1, 1), randint(-1, 1), randint(-1, 1))
        redraw_screen()
        #print(len(Point.points_array))
        wnd.update()
