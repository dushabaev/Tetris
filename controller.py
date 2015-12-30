from random import randint

from view import *


def on_leave(e):
    e.widget['state'] = NORMAL


def on_enter(e):
    e.widget['state'] = ACTIVE


class Controller:
    def __init__(self, master):
        self.scores = None
        self.paused = False
        self.master = master
        self.frame = Frame(self.master)
        self.frame.pack()

        self.is_boost = False
        self.sleep = 300
        self.is_game_over = False

        self.__field = None
        self.__view = None
        self.__next_figure = None

        self.after = None
        self.score = None

        self.master.bind('<Escape>', lambda e: self.menu(True))

    def add_new_figure(self):
        from copy import deepcopy
        old = deepcopy(self.__next_figure)

        x = self.rand_col(self.__field, old)
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
        if not self.paused:
            if self.__field.can_figure_fall():
                self.__field.figure_make_fall_tick()
                self.score.set(str(int(self.score.get()) + 1))
            else:
                if self.is_boost:
                    self.disable_boost()
                if not self.is_game_over:
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
        else:
            self.add_high_score()

    def restart(self):
        self.is_game_over = False
        self.score.set('0')
        self.__field.clear()

    def on_erase_row(self):
        self.score.set(str(int(self.score.get()) + self.__field.get_columns()))

    def menu(self, paused=False):
        self.paused = paused
        cpy = None
        if paused:
            cpy = self.frame
            cpy.pack_forget()
            self.frame = Frame(self.master)
            self.frame.pack()
        else:
            self.clear()

        cfg = {
            'activeforeground': 'red',
            'activebackground': self.master['bg'],
            'font': 'videophreak 48 bold',
            'cursor': 'hand2'
        }
        items = [
            Label(self.frame, cfg, text='PLAY' if not paused else 'RESUME'),
            Label(self.frame, cfg, text='HIGH SCORES'),
            Label(self.frame, cfg, text='EXIT')
        ]

        for i in items:
            if i['text'] == 'HIGH SCORES' and paused:
                continue
            i.pack(side=TOP)
            i.bind('<Enter>', on_enter)
            i.bind('<Leave>', on_leave)

        def back(event):
            event.widget.master.destroy()
            cpy.pack()
            self.frame = cpy
            self.paused = False

        items[0].bind('<Button-1>', (lambda e: self.play()) if not paused else back)
        items[1].bind('<Button-1>', lambda e: self.show_high_scores())
        items[2].bind('<Button-1>', lambda e: exit())

    def load_high_scores(self, row=0):
        import pickle
        f = open('scores.pckl', 'rb')

        self.scores = pickle.load(f)

        font = 'videophreak 48 bold'
        for score in self.scores:
            Label(self.frame, text=score[0], font=font + ' underline').grid(sticky=W, padx=100)
            Label(self.frame, text=str(score[1]), font=font).grid(row=row, column=1, sticky=E)
            row += 1
        f.close()

    def save_high_scores(self):
        import pickle
        f = open('scores.pckl', 'wb')
        self.scores.sort(reverse=True, key=lambda record: record[1])
        self.scores = self.scores[:5]
        pickle.dump(self.scores, f)
        f.close()

    def show_high_scores(self):
        self.clear()
        self.load_high_scores()
        back = Label(self.frame, text='Back', cursor='hand2', font='videophreak 36 bold', activeforeground='red',
                     activebackground=self.master['bg'])
        clear = Label(self.frame, text='Clear', cursor='hand2', font='videophreak 36 bold', activeforeground='red',
                      activebackground=self.master['bg'])

        back.bind('<Button-1>', lambda e: self.menu())
        back.bind('<Enter>', on_enter)
        back.bind('<Leave>', on_leave)
        back.grid(column=0, sticky=W)

        clear.bind('<Button-1>', lambda e: self.clear_high_scores())
        clear.bind('<Enter>', on_enter)
        clear.bind('<Leave>', on_leave)
        clear.grid(row=back.grid_info()['row'], column=1, sticky=E)

    def clear_high_scores(self):
        import pickle
        f = open('scores.pckl', 'wb')
        self.scores = []
        for i in range(5):
            self.scores.append(('Empty', 0))
        pickle.dump(self.scores, f)
        f.close()
        self.show_high_scores()

    def add_record(self, record):
        self.scores.append(record)
        self.save_high_scores()

        self.show_high_scores()

    def add_high_score(self):
        self.clear()

        name = StringVar()
        name.set('Name')

        e = Entry(self.frame, justify='center', font='videophreak 48 bold', textvariable=name)
        e.grid(columnspan=2)

        self.load_high_scores(1)

        e.bind('<Return>', lambda e: self.add_record((name.get(), int(self.score.get()))))

        e.icursor(END)
        e.selection_range(0, END)
        e.focus()

    def play(self):
        self.clear()
        self.is_game_over = False
        self.__field = Field(8, 16)
        self.__view = View(self.frame, 129, 257, self.__field, 'white')
        self.score = self.__view.score

        self.__next_figure = self.random_figure(0, 0)
        self.__view.set_next(self.__next_figure)

        self.__field.add_figure(self.random_figure(None, 0))

        self.__field.on_data_change = self.__view.draw
        self.__field.on_game_over = self.game_over
        self.__field.on_erase_row = self.on_erase_row

        self.master.bind('<Key>', self.on_key_press)
        self.fall()

    def clear(self):
        self.frame.destroy()
        self.frame = Frame(self.master)
        self.frame.pack()

    @staticmethod
    def rand_col(field, figure):
        return randint(0, field.get_columns() - figure.get_width()-1)

    def random_figure(self, left, top):
        figures = Figure.get_figures()
        directions = ['left', 'up', 'down', 'right']

        choice = figures[randint(0, len(figures) - 1)], directions[randint(0, len(directions) - 1)]
        f = Figure(*(choice + (0, top)))
        if left is not None:
            f.move_by(left)
        else:
            f.move_by(randint(0, self.rand_col(self.__field, f)))
        return f


r = Tk()
r.geometry('+300+100')
r.title('TETRIS')

app = Controller(r)
app.menu()

r.mainloop()
