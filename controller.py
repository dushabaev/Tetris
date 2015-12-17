from random import randint

from view import *


class Controller:
    def __init__(self, field: Field, view: View):
        self.__field = field
        self.__view = view

        self.__next_figure = self.random_figure(0, 0)
        self.__view.set_next(self.__next_figure)
        # self.__view.draw_next(self.__next_figure, 'blue')

        self.__field.add_figure(self.random_figure(self.rand_col(self.__field), 0))
        self.__view.draw()

    def add_new_figure(self):
        self.__next_figure = self.random_figure(0, 0)
        self.__view.set_next(self.__next_figure)
        # self.__view.draw_next(self.__next_figure, 'blue')
        self.__next_figure.move_by(x=randint(0, self.__field.get_columns()-4))
        self.__field.add_figure(self.__next_figure)
        self.__view.draw()

    def on_key_press(self, event):
        if event.keysym == "Left":
            self.__field.move_figure_by(x=-1)
        elif event.keysym == "Right":
            self.__field.move_figure_by(x=1)
        self.__view.draw()

    def fall(self):
        if self.__field.can_figure_fall():
            self.__field.figure_make_fall_tick()
        else:
            self.add_new_figure()
        self.__view.draw()
        self.__view.master.after(350, self.fall)

    @staticmethod
    def rand_col(field):
        return randint(0, field.get_columns())

    @staticmethod
    def random_figure(left, top):
        figures = Figure.get_figures()
        directions = ['left', 'up', 'down', 'right']

        choice = figures[randint(0, len(figures) - 1)], directions[randint(0, len(directions) - 1)]
        return Figure(*(choice + (left, top)))


r = Tk()
r.geometry('+800+100')
r.title('TETRIS')
f = Field(8, 16)
v = View(r, 129, 257, f, 'white')

app = Controller(f, v)
r.bind('<Key>', app.on_key_press)
app.fall()

r.mainloop()
