from tkinter import *
from model import *


class View:
    def __init__(self, master, width, height, columns, lines, empty_clr):
        self.master = master

        self.__lines, self.__columns = lines, columns
        self.__width, self.__height= width, height
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
        for i in range(2, self.__height, self.__dy):
            self.__rects.append([])
            for j in range(2, self.__width, self.__dx):
                self.__rects[-1].append(self.field.create_rectangle(j, i, j + self.__dx, i + self.__dy, fill=self.__empty_clr))
        for i in range(2, 6*self.__dy, self.__dy):
            for j in range(2, 6*self.__dx, self.__dx):
                self.__next_figure.create_rectangle(j, i, j+self.__dx, i+self.__dy, fill=self.__empty_clr)



    def draw(self, field):
        data = field.get_data()
        for i in range(len(data)):
            for j in range(len(data[i])):
                self.field.itemconfig(self.__rects[i][j], fill=data[i][j])




def draw(fig):
    points = fig.get_points()
    for point in points:
        c.create_rectangle(point[0] * 16, point[1] * 16, (point[0] + 1)*16, (point[1] + 1)*16, fill='red')


def move(c, fig, x=0, y=0):
    c.delete(ALL)
    fig.move_by(x, y)
    draw(fig)


def rotate(c, fig):
    fig.rotate()
    c.delete(ALL)
    draw(fig)


# r = Tk()
# c = Canvas(r)
# r.geometry('500x500')
# c['width'] = '500'
# c['height'] = '500'
# c.place(x=0, y=0)
#
# side = 20
p = Figure("pistol", "down", 5, 5)
l = Figure("line", "down", 5, 7)
s = Figure("square", "down", 0, 0)
# rotate(c, m)
# r.bind_all('<Escape>', lambda e: exit())
# r.bind('<space>', lambda e, c=c, fig=m: rotate(c, fig))
# r.bind('a', lambda e, c=c, fig=m: move(c, fig, x=-1))
# r.bind('w', lambda e, c=c, fig=m: move(c, fig, y=-1))
# r.bind('d', lambda e, c=c, fig=m: move(c, fig, x=1))
# r.bind('s', lambda e, c=c, fig=m: move(c, fig, y=1))


def fall(field, view):
    if field.can_figure_fall():
        field.move_figure_by(y=1)
        view.draw(field)
        print('fall')
    view.field.after(250, fall, field, view)

r = Tk()
r.geometry('+800+100')
r.title('TETRIS')
v = View(r, 257, 257, 16, 16, 'white')
f = Field(16, 16)
f.add_figure(s)

fall(f, v)

r.mainloop()
