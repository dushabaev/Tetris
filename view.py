from tkinter import *
from model import *


class View:
    def __init__(self, master, width, height, field: Field, empty_clr):
        self.master = master
        self.f = field
        self.__lines, self.__columns = self.f.get_lines(), self.f.get_columns()
        self.__width, self.__height = width, height
        self.__dx, self.__dy = floor(self.__width/self.__columns), floor(self.__height/self.__lines)
        Label(master, text="TETRIS", font='ComicSans 16 bold').pack(side=TOP, anchor=N)

        self.field = Canvas(self.master, width=self.__width, height=self.__height)
        self.field.pack(side=LEFT)

        self.__rects = []
        Label(master, text="Next:", font='ComicSans 16 bold').pack(side=TOP)
        self.__next_figure = Canvas(self.master, width=6*self.__dx, height=6*self.__dy, bg='red')
        self.__next_figure.pack(side=TOP)

        self.__empty_clr = empty_clr

        self.init_canvas()

    def init_canvas(self):
        self.__init_main_field()
        # self.field.bind('<Key>', self.handle)
        self.__init_next()

    def __init_next(self):
        for i in range(2, 6 * self.__dy, self.__dy):
            for j in range(2, 6 * self.__dx, self.__dx):
                self.__next_figure.create_rectangle(j, i, j + self.__dx, i + self.__dy, fill=self.__empty_clr)

    def __init_main_field(self):
        for i in range(2, self.__height, self.__dy):
            self.__rects.append([])
            for j in range(2, self.__width, self.__dx):
                self.__rects[-1].append(self.field.create_rectangle(j, i, j + self.__dx, i + self.__dy, fill=self.__empty_clr))

    def draw(self):
        data = self.f.get_data()
        for i in range(len(data)):
            for j in range(len(data[i])):
                self.field.itemconfig(self.__rects[i][j], fill=data[i][j])

    def handle(self, event):
        if event.keysym == "Left":
            self.f.move_figure_by(x=-1)
        elif event.keysym == "Right":
            self.f.move_figure_by(x=1)

    def draw_next(self, figure):
        pass

    def set_next(self, type, orientation):
        figure = Figure(type, orientation, 1, 1)
        # self.__next_figure

p = Figure("pistol", "down", 5, 0)
l = Figure("line", "down", 5, 0)
s = Figure("square", "down", 2, 5)


def fall(view):
    if view.f.can_figure_fall():
        view.f.move_figure_by(y=1)
        view.draw()
        view.field.after(250, fall, view)


r = Tk()
r.geometry('+800+100')
r.title('TETRIS')
f = Field(8, 16)
f.add_figure(s)

v = View(r, 129, 257, f, 'white')
r.bind('<Key>', v.handle)
# r.bind('a', lambda e:  v.f.move_figure_by(x=-1))
# r.bind('d', lambda e: v.f.move_figure_by(x=1))


fall(v)
r.mainloop()
