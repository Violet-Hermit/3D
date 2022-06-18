from random import randint
from tkinter import *


# From Wikipedia: The Game of Life, also known simply as Life, is a cellular automaton devised by the British
# mathematician John Horton Conway in 1970. It is a zero-player game, meaning that its evolution is determined by its
# initial state, requiring no further input. One interacts with the Game of Life by creating an initial configuration
# and observing how it evolves. It is Turing complete and can simulate a universal constructor or any other Turing
# machine.
#
# The universe of the Game of Life is an infinite, two-dimensional orthogonal grid of square cells, each of which is
# in one of two possible states, live or dead (or populated and unpopulated, respectively). Every cell interacts with
# its eight neighbours, which are the cells that are horizontally, vertically, or diagonally adjacent. At each step
# in time, the following transitions occur:
#
# 1 Any live cell with fewer than two live neighbours dies, as if by underpopulation.
# 2 Any live cell with two or three live neighbours lives on to the next generation.
# 3 Any live cell with more than three live neighbours dies, as if by overpopulation.
# 4 Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
#
# These rules, which compare the behavior of the automaton to real life, can be condensed into the following:
# 1 Any live cell with two or three live neighbours survives.
# 2 Any dead cell with three live neighbours becomes a live cell.
# 3 All other live cells die in the next generation. Similarly, all other dead cells stay dead.
# The initial pattern constitutes the seed of the system. The first generation is created by applying the
# above rules simultaneously to every cell in the seed, live or dead; births and deaths occur simultaneously,
# and the discrete moment. at which this happens is sometimes called a tick. Each generation is a pure function of the
# preceding one. The rules continue to be applied repeatedly to create further generations.

class Field:

    def __init__(self, heigth: int, weigth: int, size_of_cell: int):
        self.heigth = heigth
        self.weigth = weigth
        self.size_of_cell = size_of_cell
        self.mtx = [[randint(0,1) for i in range(weigth)] for j in
                    range(heigth)]  # Creation of a matrix of cells

    def drawing_field(self):
        for i in range(len(self.mtx)):
            for j in range(len(self.mtx[i])):
                canvas.create_rectangle(i * self.size_of_cell, j * self.size_of_cell, (i + 1) * self.size_of_cell,
                                        (j + 1) * self.size_of_cell,
                                        fill="black") if 1 == self.mtx[i][j] else None

    def counting_of_neigbors(self, x, y):

        sum: int = 0
        left = x - 1 if x > 0 else x
        right = x + 2 if x < len(self.mtx[y]) - 1 else x + 1
        top = y - 1 if y > 0 else y
        bottom = y + 2 if y < len(self.mtx) - 1 else y + 1

        for i in range(left, right):
            for j in range(top, bottom):
                sum += self.mtx[i][j]
        return sum - self.mtx[x][y]

    def cell_updating(self, x, y, new_mtx):

        live = self.mtx[x][y]
        if live == 0 and self.counting_of_neigbors(x, y) == 3:
            new_mtx[x][y] = True

        if live == 1 and self.counting_of_neigbors(x, y) == 2 or self.counting_of_neigbors(x, y) == 3:
            new_mtx[x][y] = True

        if self.counting_of_neigbors(x, y) > 3 or self.counting_of_neigbors(x, y) < 2:
            new_mtx[x][y] = False

    def clearing_screen(self):
        canvas.create_rectangle(0, 0, (self.heigth + 1) * self.size_of_cell, (self.weigth + 1) * self.size_of_cell
                                , fill="white")

    def field_updating(self):
        new_mtx = self.mtx.copy()
        for i in range(len(self.mtx)):
            for j in range(len(self.mtx[i])):
                live = self.mtx[i][j]
                self.cell_updating(i, j, new_mtx)
            mtx = new_mtx



# Main cycle
if __name__ == '__main__':
    size = 1000  # size of screen
    wnd = Tk()
    canvas = Canvas(wnd, width=size, height=size)
    canvas.pack()
    colors = "black"
    field = Field(30, 30, 20)  # creating field
    field.drawing_field()
    while True:
        field.field_updating()
        field.clearing_screen()
        field.drawing_field()
        wnd.update()  # update