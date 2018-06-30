import Tkinter as tk
from Game import *


"""
Wordl design:
    menu provides interface to restart and other features
    display: graphics via Tkinter
    player:
        methods for managing collection of tiles
            orders (grid snap?)
            dictionary validation/highlighting
        methods for drawing to the canvas
            collection
            board position
    board:
        methods for managing state
            pool tiles, token tiles
        methods for drawing to the display
            board skeleton, tile positions
    Game:
        determine power methods
        generate pool methods
        set board methods
        explore loop
            turn methods
            round methods
        methods for managing state
        
"""


class WordlApp(object):
    def __init__(self):
        #TODO: power determination,
        # generate pool and setup board,
        # kick off explore loop
        # kick off consolidation and end of game

        self.root = tk.Tk(className="  Wordl  ")

        self._create_menus()

        self.canvas = tk.Canvas(self.root)

        # app lifecycle
        self.persist = True
        while self.persist:
            self.root.update_idletasks()
            self.root.update()
            time.sleep(0.01)
        self.root.destroy()

    def _create_menus(self):
        # instantiate a parent tk Menu
        menu_bar = tk.Menu(self.root)

        # File menu pulldowns
        file_menu = tk.Menu(menu_bar)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Game", command=self._start_game)
        file_menu.add_command(label="Open...", command=self.callback)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._quit)

        # help menu pulldowns
        help_menu = tk.Menu(menu_bar)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About...", command=self.callback)

        self.root.config(menu=menu_bar)

    @staticmethod
    def callback():
        print "called the callback!"

    def _quit(self):
        self.root.quit()
        self.persist = False

    def _start_game(self):
        print "...well you would've started a game."


if __name__ == "__main__":
    app = WordlApp()

