# coding: utf-8
import Tkinter as tk
from threading import Timer
from pirobot import MOVEMENTS, STOP
from pirobot.talks import Talks

KEY_UP = 'Up'
KEY_DOWN = 'Down'
KEY_LEFT = 'Left'
KEY_RIGHT = 'Right'

KEYS = (KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT)

KEY_MOVEMENTS = dict(zip(KEYS, MOVEMENTS))


class Application(tk.Frame):
    label_state = None
    key_state = None
    debounced = None
    debounce_time = 0.05
    movements_queue = None
    previous_state = None
    talks = None

    def __init__(self, master):
        self.debounced = dict()
        self.key_state = set()

        tk.Frame.__init__(self, master)
        master.minsize(width=640, height=480)

        master.bind("<Key>", self.key_pressed)
        master.bind("<KeyRelease>", self.key_released)

        self.pack()
        self.createWidgets()

        self.talks = Talks()
        self.talks.start()
        self.movements_queue = self.talks.queue

        self.state_updated()

    def createWidgets(self):
        self.label_state = tk.Label(self)
        self.label_state.pack({'side': 'bottom'})

    def key_pressed(self, event):
        if event.keysym in KEYS:
            timer = self.debounced.get(event.keysym)
            if timer:
                timer.cancel()
            self.key_state.add(event.keysym)
            self.state_updated()

    def key_released(self, event):
        if event.keysym in KEYS:
            timer = self.debounced.get(event.keysym)
            if timer:
                timer.cancel()
            timer = Timer(self.debounce_time, lambda: self.remove_keysym(event.keysym))
            self.debounced[event.keysym] = timer
            timer.start()

    def remove_keysym(self, keysym):
        self.key_state.discard(keysym)
        self.state_updated()

    def state_updated(self):
        state = self.state
        if state != self.previous_state:
            self.previous_state = state
            self.movements_queue.put(state)
            self.label_state.config(text=', '.join(state))

    @property
    def state(self):
        if not self.key_state:
            state = [STOP]
        else:
            state = map(lambda s: KEY_MOVEMENTS[s], self.key_state)
        return set(state)

if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()

    try:
        root.destroy()
    except tk.TclError:
        pass
