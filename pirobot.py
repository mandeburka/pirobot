# coding: utf-8
import Tkinter as tk
from threading import Timer

MOVE_FORWARD = 'FORWARD'
MOVE_BACKWARD = 'BACKWARD'
MOVE_RIGHT = 'RIGHT'
MOVE_LEFT = 'LEFT'
STOP = 'STOP'

MOVEMENTS = (MOVE_FORWARD, MOVE_BACKWARD, MOVE_RIGHT, MOVE_LEFT)

KEY_UP = 'Up'
KEY_DOWN = 'Down'
KEY_LEFT = 'Left'
KEY_RIGHT = 'Right'

KEYS = (KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT)

KEY_MOVEMENTS = {
    KEY_UP: MOVE_FORWARD,
    KEY_DOWN: MOVE_BACKWARD,
    KEY_LEFT: MOVE_LEFT,
    KEY_RIGHT: MOVE_RIGHT,
}


def debounce(wait):
    """ Decorator that will postpone a functions
        execution until after wait seconds
        have elapsed since the last time it was invoked. """
    def decorator(fn):
        def debounced(*args, **kwargs):
            def call_it():
                fn(*args, **kwargs)
            try:
                debounced.t.cancel()
            except(AttributeError):
                pass
            debounced.t = Timer(wait, call_it)
            debounced.t.start()
        return debounced
    return decorator


class Application(tk.Frame):
    data = None
    key_state = None

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        master.bind("<Key>", self.key_pressed)
        master.bind("<KeyRelease>", self.key_released)
        master.minsize(width=640, height=480)
        self.pack()
        self.createWidgets()
        self.key_state = set()

    def createWidgets(self):
        self.data = tk.Label(self, text='Press any key')
        self.data.pack({'side': 'bottom'})

    def key_pressed(self, event):
        if event.keysym in KEYS:
            self.key_state.add(event.keysym)
            self.data.config(text=str(self.key_state))

    def key_released(self, event):
        self.key_state.discard(event.keysym)
        self.data.config(text=str(self.key_state))



root = tk.Tk()
app = Application(master=root)
app.mainloop()

try:
    root.destroy()
except tk.TclError:
    pass
