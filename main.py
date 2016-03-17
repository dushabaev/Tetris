from controller import *

r = Tk()
r.geometry('+300+100')
r.title('TETRIS')

app = Controller(r)
app.menu()

r.mainloop()
