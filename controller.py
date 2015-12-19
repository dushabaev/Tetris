from random import randint

from view import *


class Controller:
    def __init__(self, field: Field, view: View):
        self.is_boost = False
        self.sleep = 300
        self.is_game_over = False
        self.__field = field
        self.__view = view

        self.__next_figure = self.random_figure(0, 0)
        self.__view.set_next(self.__next_figure)

        self.__field.add_figure(self.random_figure(self.rand_col(self.__field), 0))
        self.after = None
        self.score = self.__view.score

    def add_new_figure(self):
        from copy import deepcopy
        old = deepcopy(self.__next_figure)

        x = self.rand_col(self.__field)
        self.__next_figure.move_by(x=x, y=self.__field.get_buffer_size() - self.__next_figure.get_height() - 1)
        self.__field.add_figure(self.__next_figure)

        new = self.random_figure(0, 0)
        self.__view.set_next(new, old)
        self.__next_figure = deepcopy(new)

    def on_key_press(self, event):
        if self.is_boost:
            return
        if event.keysym == "Left" and self.__field.can_figure_move(x=-1):
            self.__field.move_figure_by(x=-1)
        elif event.keysym == "Right" and self.__field.can_figure_move(x=1):
            self.__field.move_figure_by(x=1)
        elif event.keysym == "Up":
            self.__field.figure_rotate()
        elif event.keysym == "Down":
            self.enable_boost()

    def fall(self):
        if self.is_game_over:
            return
        if self.__field.can_figure_fall():
            self.__field.figure_make_fall_tick()
            self.score.set(str(int(self.score.get())+1))
        else:
            if self.is_boost:
                self.disable_boost()
            self.add_new_figure()
        self.after = self.__view.master.after(int(self.sleep), self.fall)

    def disable_boost(self):
        self.is_boost = False
        self.sleep *= 10

    def enable_boost(self):
        self.is_boost = True
        self.sleep /= 10

    def game_over(self):
        self.is_game_over = True
        from tkinter import messagebox
        if messagebox.askyesno('GAME OVER', 'Restart ?'):
            self.restart()

    def restart(self):
        self.is_game_over = False
        self.__field.clear()

    def on_erase_row(self):
        self.score.set(str(int(self.score.get())+self.__field.get_columns()))

    @staticmethod
    def rand_col(field):
        return randint(0, field.get_columns() - 4)

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

f.on_data_change = v.draw
f.on_game_over = app.game_over
f.on_erase_row = app.on_erase_row

r.bind('<Key>', app.on_key_press)
app.fall()

r.mainloop()
