from random import randint

from view import *


class Controller:
    def __init__(self, field: Field, view: View):
        self.__field = field
        self.__view = view
        self.__next_figure = self.random_figure(0, 0)

        rand_col = lambda: randint(0, field.get_columns())

        self.__field.add_figure(self.random_figure(rand_col(), 0))

    @staticmethod
    def random_figure(left, top):
        figures = Figure.get_figures()
        directions = ['left', 'up', 'down', 'right']

        choice = figures[randint(0, len(figures) - 1)], directions[randint(0, len(directions) - 1)]
        return Figure(*(choice+(left, top)))
