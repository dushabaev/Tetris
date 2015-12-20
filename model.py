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

        elif "pistol" in self.__type:
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

    def get_width(self):
        left, top, right, bottom = self.get_box()
        return right-left

    def get_height(self):
        left, top, right, bottom = self.get_box()
        return bottom-top

    def get_center(self):
        left, top, right, bottom = self.get_box()
        return (left + right) / 2, (top + bottom) / 2

    def __setup_pistol(self, left=None, top=None):
        if left is None or top is None:
            left, top = self.__points[0]
        self.__points = []

        if self.orient == "left":
            for i in range(top, top + 3, 1):
                self.__points.append((left + 1, i))
            point = (left, top + 2)
            if self.__type == 'rpistol':
                point = (left, top)
            self.__points.append(point)

        elif self.orient == "right":
            for i in range(top, top + 3, 1):
                self.__points.append((left, i))
            point = (left + 1, top)
            if self.__type == 'rpistol':
                point = (left + 1, top + 2)
            self.__points.append(point)

        elif self.orient == "up":
            for i in range(left, left + 3, 1):
                self.__points.append((i, top + 1))
            point = (left, top)
            if self.__type == 'rpistol':
                point = (left + 2, top)
            self.__points.append(point)

        elif self.orient == "down":
            for i in range(left, left + 3, 1):
                self.__points.append((i, top))
            point = (left + 2, top + 1)
            if self.__type == 'rpistol':
                point = (left, top + 1)
            self.__points.append(point)

    def move_by(self, x=0, y=0):
        for i in range(len(self.__points)):
            self.__points[i] = self.__points[i][0] + x, self.__points[i][1] + y
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
        return ['square', 'line', 'pistol', 'rpistol']

    def get_points(self):
        return list(map(lambda p: (floor(p[0]), floor(p[1])), self.__points))

    def get_type(self):
        return self.__type


class Field:
    def __init__(self, columns, lines, buffer=4):
        self.on_erase_row = lambda: None
        self.__figure = None
        self.__lines = lines
        self.__columns = columns
        self.__buffer = buffer
        self.__field = []
        self.on_data_change = lambda: None
        self.on_game_over = lambda: None
        for i in range(lines + buffer):
            self.__field.append([])
            for j in range(columns):
                self.__field[-1].append(self.__empty_cell())

    @staticmethod
    def get_color(figure):
        fig_type = figure.get_type()
        clrs = {
            'square':'#FF4000',
            'line': '#40FF00',
            'pistol': '#00C0FF',
            'rpistol': '#C000FF'
        }
        return clrs[fig_type]

    @staticmethod
    def __empty_cell():
        return 'white'

    def get_buffer_size(self):
        return self.__buffer

    def figure_rotate(self):
        points = self.__figure.get_points()
        self.__set_data(points, self.__empty_cell())
        self.__figure.rotate()
        points = self.__figure.get_points()

        for point in points:
            if self.__point_is_outbound(point) or self.__get_data(point) != self.__empty_cell():
                self.__figure.rotate(True)
                break
        self.__set_data(self.__figure.get_points(), self.get_color(self.__figure))
        return self

    def can_figure_move(self, x=0, y=0):
        points = self.__figure.get_points()
        for p in points:
            tp = p[0] + x, p[1] + y
            if tp not in points and (self.__point_is_outbound(tp) or self.__get_data(tp) != self.__empty_cell()):
                return False
        return True

    def can_figure_fall(self):
        result = self.can_figure_move(y=1)
        if result:
            return result

        points = self.__figure.get_points()
        erase = set()
        for _, row in points:
            if self.is_filled(row):
                erase.add(row)

        erase = list(erase)
        erase.sort()

        for i in erase:
            self.erase_row(i)

        if len(erase) == 0:
            for _, row in points:
                if row == self.__buffer:
                    self.on_game_over()
                    return result
        return result

    def __get_data(self, point):
        return self.__field[point[1]][point[0]]

    def get_data(self):
        return self.__field[self.__buffer:]

    def __set_data(self, points, data):
        for p in points:
            self.__field[p[1]][p[0]] = data
        self.on_data_change()

    def __point_is_outbound(self, p):
        return p[0] < 0 or p[0] >= self.__columns or p[1] < 0 or p[1] >= self.__lines + self.__buffer

    def add_figure(self, figure):
        self.__figure = figure
        points = self.__figure.get_points()
        clr = self.get_color(figure)

        self.__set_data(points, clr)
        return self

    def move_figure_by(self, x=0, y=0):
        self.__set_data(self.__figure.get_points(), self.__empty_cell())
        self.__set_data(self.__figure.move_by(x, y).get_points(), self.get_color(self.__figure))
        return self

    def figure_make_fall_tick(self):
        return self.move_figure_by(y=1)

    def erase_row(self, row):
        n_row = [self.__empty_cell() for column in range(self.__columns)]
        self.__field = [n_row] + self.__field[:row] + self.__field[row + 1:]
        self.on_data_change()
        self.on_erase_row()
        return self

    def get_lines(self):
        return self.__lines

    def get_columns(self):
        return self.__columns

    def is_filled(self, row):
        for column in range(len(self.__field[row])):
            if self.__field[row][column] == self.__empty_cell():
                return False
        return True

    def clear(self):
        for i in range(self.__lines+self.__buffer):
            for j in range(self.__columns):
                self.__field[i][j] = self.__empty_cell()
        self.on_data_change()
