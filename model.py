from tkinter import *
from math import ceil, floor


class Figure:
    def __init__(self, fig_type, orientation, left, top, event_generator=None):
        self.__type = fig_type
        self.orient = orientation
        self.__left = left
        self.__top = top
        self.__points = []
        self.__generate_event = event_generator

        if self.__type == "square":
            self.__points.append((left, top))
            self.__points.append((left + 1, top))
            self.__points.append((left, top + 1))
            self.__points.append((left + 1, top + 1))

        elif self.__type == "line":
            if self.orient == "left" or self.orient == "right":
                for i in range(left, left + 4, 1):
                    self.__points.append((i, top))
            else:
                for i in range(top, top + 4, 1):
                    self.__points.append((left, i))

        elif self.__type == "pistol":
            self.__setup_pistol(left, top)

    def rotate(self, clockwise=False):
        if self.__type == "square":
            return
        x, y = self.get_center()
        for i in range(len(self.__points)):
            if clockwise:
                self.__points[i] = (y - self.__points[i][1] + x, self.__points[i][0] - x + y)
            else:
                self.__points[i] = (self.__points[i][1] - y + x, x - self.__points[i][0] + y)
        self.orient = self.__next_orient(self.orient, clockwise)

        if self.__generate_event is not None:
            self.__generate_event("<<Figure-Rotate>>", when='tail')

        print(self.orient)
        for i in self.__points:
            print(i)
        x, y = self.get_center()
        print(x, y,)

    def get_box(self):
        (left, top), (right, bottom) = self.__points[0], self.__points[0]
        for point in self.__points:
            if left > point[0]:
                left = point[0]
            if right < point[0]:
                right = point[0]
            if top > point[1]:
                top = point[1]
            if bottom < point[1]:
                bottom = point[1]
        return left, top, right, bottom

    def get_center(self):
        left, top, right, bottom = self.get_box()
        return (left + right) / 2, (top + bottom) / 2

    def __setup_pistol(self, left=None, top=None):
        if left is None or top is None:
            left, top = self.__points[0]
        self.__points = []
        if self.__type == "pistol":
            if self.orient == "left":
                for i in range(top, top + 3, 1):
                    self.__points.append((left + 1, i))
                self.__points.append((left, top + 2))
            elif self.orient == "right":
                for i in range(top, top + 3, 1):
                    self.__points.append((left, i))
                self.__points.append((left + 1, top))
            elif self.orient == "up":
                for i in range(left, left + 3, 1):
                    self.__points.append((i, top + 1))
                self.__points.append((left, top))
            elif self.orient == "down":
                for i in range(left, left + 3, 1):
                    self.__points.append((i, top))
                self.__points.append((left + 2, top + 1))

    def move_by(self, x=0, y=0):
        for i in range(len(self.__points)):
            self.__points[i] = self.__points[i][0]+x, self.__points[i][1]+y
        if self.__generate_event is not None:
            self.__generate_event("", when='tail')

    @staticmethod
    def __next_orient(orient, clockwise):
        if orient == "left":
            return "up" if clockwise else "down"

        if orient == "right":
            return "up" if not clockwise else "down"

        if orient == "up":
            return "right" if clockwise else "left"

        if orient == "down":
            return "right" if not clockwise else "left"

    def get_points(self):
        return self.__points

    def get_type(self):
        return self.__type


class Field:
    def __init__(self, lines, columns, buffer=4):
        self.__figure = None
        self.__lines = lines
        self.__columns = columns
        self.__buffer = buffer
        self.__field = [[self.__empty_clr()] * self.__columns] * (self.__lines + self.__buffer)

    @staticmethod
    def __get_color(figure):
        fig_type = figure.get_type()
        return 'red' if fig_type == 'square' else 'green' if fig_type == 'line' else 'blue'

    @staticmethod
    def __empty_clr():
        return 'white'

    def add_figure(self, figure):
        self.__figure = figure
        for point in figure.get_points():
            self.__field[floor(point[0])][floor(point[1])] = self.__get_color(figure)


def draw(fig):
    for point in fig.get_points():
        c.create_rectangle(point[0] * 16, point[1] * 16, (point[0] + 1)*16, (point[1] + 1)*16, fill='red')

def move(c, fig, x=0, y=0):
    c.delete(ALL)
    fig.move_by(x, y)
    for point in fig.get_points():
        c.create_rectangle(point[0] * 16, point[1] * 16, (point[0] + 1)*16, (point[1] + 1)*16, fill='red')


def rotate(c, fig):
    fig.rotate()
    c.delete(ALL)
    for point in fig.get_points():
        c.create_rectangle(point[0] * 16, point[1] * 16, (point[0] + 1)*16, (point[1] + 1)*16, fill='red')


r = Tk()
c = Canvas(r)
r.geometry('500x500')
c['width'] = '500'
c['height'] = '500'
c.place(x=0, y=0)

side = 20
m = Figure("square", "down", 2, 2)
rotate(c, m)
r.bind_all('<Escape>', lambda e: exit())
r.bind('<space>', lambda e, c=c, fig=m: rotate(c, fig))
r.bind('a', lambda e, c=c, fig=m: move(c, fig, x=-1))
r.bind('w', lambda e, c=c, fig=m: move(c, fig, y=-1))
r.bind('d', lambda e, c=c, fig=m: move(c, fig, x=1))
r.bind('s', lambda e, c=c, fig=m: move(c, fig, y=1))


r.mainloop()
