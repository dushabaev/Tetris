from view import *
from random import randint

class Controller:
    def __init__(self, field: Field, view: View):
        self.__field = field
        self.__view = view

        choice = randint(0, len(Figure.get_figures())-1)
        
