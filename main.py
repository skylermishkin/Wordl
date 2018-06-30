import Tkinter as tk
import time

from Game import *


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Globals
WIDTH = 1000
HEIGHT = 600
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class WordlApp(object):
    def __init__(self):
        """ctor

        """
        self.root = tk.Tk(className="  Wordl  ")
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT)

        self._create_menus()

        # Flags for state of the game
        self._determining_power = False
        self._setting_board = False
        self._exploring = False
        self._finalizing = False

        self.game = self._create_new_game()

        # app lifecycle
        self.persist = True
        while self.persist:
            self.root.update_idletasks()
            self.root.update()
            self.manage()
            time.sleep(0.01)
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

        self.game.draw()

    def _create_menus(self):
        # instantiate a parent tk Menu
        menu_bar = tk.Menu(self.root)

        # File menu pulldowns
        file_menu = tk.Menu(menu_bar)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Game", command=self._create_new_game)
        file_menu.add_command(label="Open...", command=self._open_map)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._quit)

        # help menu pulldowns
        help_menu = tk.Menu(menu_bar)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About...", command=self._about_wordl)

        self.root.config(menu=menu_bar)

    def _quit(self):
        self.root.quit()
        self.persist = False

    def _create_new_game(self):
        print "Creating new game."
        self._determining_power = True
        return Game(self.canvas)

    def _about_wordl(self, event):
        print "It's chill"

    def _open_map(self, event):
        print "You are not ready yet"


if __name__ == "__main__":
    app = WordlApp()

