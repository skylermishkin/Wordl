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


class WordlApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        #TODO: initiate canvas,
        # fill with power determination,
        # generate pool and setup board,
        # kick off explore loop
        # kick off consolidation and end of game

        self.menu, self.file_menu, self.help_menu = self._create_menus()
        self.canvas = self.Canvas()

    def _create_menus(self):
        # instantiate a parent tk Menu
        menu = tk.Menu(self)
        self.config(menu=menu)

        # File menu inheritance
        file_menu = tk.Menu(menu)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self._start_game())
        file_menu.add_command(label="Open...", command=self.callback())
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._close())

        # help menu inheritance
        help_menu = tk.Menu(menu)
        menu.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About...", command=self.callback())

        return menu, file_menu, help_menu

    @staticmethod
    def callback():
        print "called the callback!"

    def _start_game(self):
        print "...well you would've started a game."

    def _close(self):
        print "...well you would've closed."


if __name__ == "__main__":
    app = WordlApp(className="  Wordl  ")
    while True:
        app.update_idletasks()
        app.update()
        time.sleep(0.01)
