from tkinter import *

from model import *


class View:
    def __init__(self, master, width, height, field: Field, empty_clr):
        self.master = master
        self.f = field
        self.__lines, self.__columns = self.f.get_lines(), self.f.get_columns()
        self.__width, self.__height = width, height
        self.__dx, self.__dy = floor(self.__width / self.__columns), floor(self.__height / self.__lines)
        Label(self.master, text="TETRIS", font='videophreak 16 bold').grid(columnspan=2)

        Label(self.master, text="Score:", font='videophreak 16 bold').grid(column=0)
        self.score = StringVar(master)
        Label(self.master, font='videophreak 16 bold', textvariable=self.score).grid(row=1, column=1)
        self.score.set('0')

        self.field = Canvas(self.master, width=self.__width, height=self.__height)
        self.field.grid(column=0, rowspan=50)

        self.__rects = []
        self.__next_rects = []

        Label(self.master, text="Next:", font='videophreak 16 bold').grid(row=2, column=1, sticky=N)
        self.__next_figure = Canvas(self.master, width=4 * self.__dx + 1, height=4 * self.__dy + 1)
        self.__next_figure.grid(column=1, sticky=N, row=3)

        self.__empty_clr = empty_clr

        self.init_canvas()

    def init_canvas(self):
        self.__init_main_field()
        self.__init_next()

    def __init_next(self):
        for i in range(2, 4 * self.__dy, self.__dy):
            self.__next_rects.append([])
            for j in range(2, 4 * self.__dx, self.__dx):
                self.__next_rects[-1].append(
                    self.__next_figure.create_rectangle(j, i, j + self.__dx, i + self.__dy, fill=self.__empty_clr))

    def __init_main_field(self):
        for i in range(2, self.__height, self.__dy):
            self.__rects.append([])
            for j in range(2, self.__width, self.__dx):
                self.__rects[-1].append(
                    self.field.create_rectangle(j, i, j + self.__dx, i + self.__dy, fill=self.__empty_clr))

    def draw(self):
        data = self.f.get_data()
        for i in range(len(data)):
            for j in range(len(data[i])):
                self.field.itemconfig(self.__rects[i][j], fill=data[i][j])

    def draw_next(self, figure: Figure, clr):
        p = figure.get_points()
        for x, y in p:
            self.__next_figure.itemconfigure(self.__next_rects[y][x], fill=clr)

    def set_next(self, figure, old=None):
        if old is not None:
            self.draw_next(old, 'white')
        self.draw_next(figure, self.f.get_color(figure))
