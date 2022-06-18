from functools import lru_cache

#import graphics as gr
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
    def __init__(self, x=0, y=0, z=0):
        self.coord = (x, y, z)

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

    def move(self, x_bias, y_bias, z_bias):
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
        return multiply_matrices(self.coord, transformation_matrix)

    def spin_yz(self, angle):
        transformation_matrix = [[1, 0, 0], [0, cos(angle), -1 * sin(angle)], [0, sin(angle), cos(angle)]]
        return multiply_matrices(self.coord, transformation_matrix)

    def spin_xz(self, angle):
        transformation_matrix = [[cos(angle), 0, sin(angle)], [0, 1, 0], [-1 * sin(angle), 0, cos(angle)]]
        return multiply_matrices(self.coord, transformation_matrix)

    def do_scale(self, s0, s1, s2):
        transformation_matrix = [[s0, 0, 0], [0, s1, 0], [0, 0, s2]]
        return multiply_matrices(self.coord, transformation_matrix)

    def move(self, x_bias, y_bias, z_bias):
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
    canvas.create_rectangle(0, 0, 1000, 1000, fill="white")


# Просто умножение матриц средствами NumPy,
# тоже сделать прегрузку чтобы в случае подачи на вход масивов NumPy все продолжало работать

def multiply_matrices(mtx1, mtx2):
    matrix1 = np.array(mtx1)
    matrix2 = np.array(mtx2)
    result = matrix1.dot(matrix2).tolist()
    return result

# Утечка памяти происходит из-за модуля canvas, при каждой новой отрисовке жрётся память
# Старые эллементы не удаляются поэтому память утекает тоже самое касается и остальных проектов кроме серпинского

if __name__ == '__main__':
    initialize_screen(1000, 1000)
    point = Point(5, 5, 1)
    point.draw_point()
    points = [Point(randint(300, 700), randint(300, 700), randint(300, 700) ) for i in range(1000)]
    for i in points:
        i.draw_point()
    #wnd.update()
    while 1:
    #clearing_screen()
        for i in range(len(points)):
            points[i].move(randint(-1, 1), randint(-1, 1), randint(-1, 1))
            points[i].draw_point()
            wnd.mainloop()