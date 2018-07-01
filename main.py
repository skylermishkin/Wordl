try:
    import Tkinter as tk
except:
    import tkinter as tk
import time

from Game import *
from settings import *


# hack to draw circles
def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x - r, y - r, x + r, y + r, **kwargs)


tk.Canvas.create_circle = _create_circle


class WordlApp(object):
    def __init__(self):
        """ctor

        """
        self.root = tk.Tk(className="  Wordl  ")
        self._create_menus()

        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, highlightthickness=0, background="white")
        self.cwidth = self.canvas.winfo_reqwidth()
        self.cheight = self.canvas.winfo_reqheight()
        self.canvas.bind("<Configure>", self._on_resize)

        self.game = None
        self._create_new_game()
        self.canvas.pack()

        # Flags for state of the game
        self._determining_power = False
        self._setting_board = False
        self._exploring = False
        self._finalizing = False

        # app lifecycle
        self.persist = True
        while self.persist:
            self.manage()
            self.root.after(10)
            self.root.update_idletasks()
            self.root.update()
        self.root.destroy()

    def manage(self):
        if self._determining_power:
            pass
        elif self._setting_board:
            pass
        elif self._exploring:
            pass
        elif self._finalizing:
            pass
        self.game.update()

    def _create_menus(self):
        # instantiate a parent tk Menu
        menu_bar = tk.Menu(self.root)

        # File menu pulldowns
        file_menu = tk.Menu(menu_bar)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Game", command=self._create_new_game)
        file_menu.add_command(label="Open...", command=self._open_map)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._exit)

        # help menu pulldowns
        help_menu = tk.Menu(menu_bar)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About...", command=self._about_wordl)

        self.root.config(menu=menu_bar)

    def _exit(self):
        self.root.quit()
        self.persist = False

    def _create_new_game(self):
        print("Creating new game.")
        self.canvas.delete("all")
        self.game = None
        self.game = Game(self.canvas)
        self._determining_power = True

    def _about_wordl(self, *event):
        print("It's chill")

    def _open_map(self, *event):
        print("You are not ready yet")

    def _on_resize(self, event):
        wscale = float(event.width) / self.cwidth
        hscale = float(event.height) / self.cheight
        self.cwidth = event.width
        self.cheight = event.height
        # resize the canvas
        self.canvas.config(width=self.cwidth, height=self.cheight)
        # rescale all the objects tagged with the "all" tag
        # TODO: this needs to also scal text size
        self.canvas.scale("all", 0, 0, wscale, hscale)


if __name__ == "__main__":
    app = WordlApp()

