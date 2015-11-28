from math import floor


class Figure:
    def __init__(self, fig_type, orientation, left, top):
        self.__type = fig_type
        self.orient = orientation
        self.__left = left
        self.__top = top
        self.__points = []

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

        print(self.orient)
        for i in self.__points:
            print(i)
        x, y = self.get_center()
        print(x, y,)
        return self

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
        return self

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

    @staticmethod
    def get_figures():
        return ['square', 'line', 'pistol']

    def get_points(self):
        return list(map(lambda p: (floor(p[0]), floor(p[1])), self.__points))

    def get_type(self):
        return self.__type


class Field:
    def __init__(self, columns, lines, buffer=4):
        self.__figure = None
        self.__lines = lines
        self.__columns = columns
        self.__buffer = buffer
        self.__field = []
        for i in range(lines+buffer):
            self.__field.append([])
            for j in range(columns):
                self.__field[-1].append(self.__empty_cell())

    @staticmethod
    def __get_color(figure):
        fig_type = figure.get_type()
        return '#FF4000' if fig_type == 'square' else '#40FF00' if fig_type == 'line' else '#00C0FF'

    @staticmethod
    def __empty_cell():
        return 'white'

    def can_figure_move(self, x=0, y=0):
        points = self.__figure.get_points()
        for p in points:
            tp = p[0]+x, p[1]+y
            if tp not in points and (self.__point_is_outbound(tp) or self.__get_data(tp) != self.__empty_cell()):
                return False
        return True

    def can_figure_fall(self):
        return self.can_figure_move(y=1)

    def __get_data(self, point):
        return self.__field[point[1]][point[0]]

    def get_data(self):
        return self.__field[self.__buffer:]

    def __set_data(self, points, data):
        for p in points:
            self.__field[p[1]][p[0]] = data

    def __point_is_outbound(self, p):
        return p[0] < 0 or p[0] >= self.__columns or p[1] < 0 or p[1] >= self.__lines+self.__buffer

    def add_figure(self, figure):
        self.__figure = figure
        points = self.__figure.get_points()
        clr = self.__get_color(figure)

        for point in points:
            self.__field[point[1]][point[0]] = clr

        return self

    def move_figure_by(self, x=0, y=0):
        self.__set_data(self.__figure.get_points(), self.__empty_cell())
        self.__set_data(self.__figure.move_by(x, y).get_points(), self.__get_color(self.__figure))
        return self

    def get_lines(self):
        return self.__lines

    def get_columns(self):
        return self.__columns