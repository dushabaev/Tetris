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
        else:
            self.__setup_broken_line(left, top)

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
        return right - left

    def get_height(self):
        left, top, right, bottom = self.get_box()
        return bottom - top

    def get_center(self):
        left, top, right, bottom = self.get_box()
        return (left + right) / 2, (top + bottom) / 2

    def __setup_broken_line(self, left=None, top=None):
        def line(obj, left, top, len, x=1, y=0):
            for i in range(top+y, top+y + len):
                obj.__points.append((left + x, i))

        # create points for left orientation
        if 'pistol' in self.__type or self.__type == 't':
            line(self, left, top, 3)
            types = ['pistol', 't', 'rpistol']
            top += types.index(self.__type)
            self.__points.append((left, top))
        elif 'skew' in self.__type:
            r = self.__type[0] == 'r'
            line(self, left, top, 2, int(not r))
            line(self, left, top, 2, int(r), 1)

        orients = self.get_orients()
        pos = orients.index(self.orient) - orients.index('left')
        clockwise = pos > 0
        for i in range(abs(pos)):
            self.rotate(clockwise)

        #fix negaitve points
        min_x, min_y = 0, 0
        for point in self.__points:
            min_x = min(point[0], min_x)
            min_y = min(point[1], min_y)
        min_x *= -1
        min_y *= -1
        self.__points = list(map(lambda p: (p[0] + min_x, p[1] + min_y), self.__points))

    def move_by(self, x=0, y=0):
        for i in range(len(self.__points)):
            self.__points[i] = self.__points[i][0] + x, self.__points[i][1] + y
        return self

    @staticmethod
    def get_orients():
        return ['left', 'up', 'right', 'down']

    @staticmethod
    def __next_orient(orient, clockwise):
        clockwise_orients = Figure.get_orients()
        c_clockwise_orients = list(reversed(clockwise_orients))
        orients = clockwise_orients if clockwise else c_clockwise_orients

        return orients[(orients.index(orient) + 1) % len(orients)]

    @staticmethod
    def get_figures():
        return ['square', 'line', 'pistol', 'rpistol', 't', 'skew', 'rskew']

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
            'square': '#FF4000',
            'line': '#40FF00',
            'pistol': '#00C0FF',
            'rpistol': '#C000FF',
            't': 'magenta',
            'skew': 'orange',
            'rskew': 'cyan'
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
        for i in range(self.__lines + self.__buffer):
            for j in range(self.__columns):
                self.__field[i][j] = self.__empty_cell()
        self.on_data_change()
