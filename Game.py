from Board import *
from Player import *
from Tile import *
from settings import *


class Game(object):
    def __init__(self, canvas, num_players=1, *args, **kwargs):
        """ctor

        :param canvas:
        :param num_players:
        :param args:
        :param kwargs:
        """
        self.canvas = canvas
        self.num_players = num_players

        self._determining_power = True
        self._setting_board = False
        self._exploring = False
        self._finalizing = False

        self.canvas.focus_set()
        # canvas objects
        self.board = Board(self.canvas, num_players=self.num_players)

        self.board.setup()
        self.board.create()

    def update(self):
        self.canvas.after(10)
        self.canvas.update()

    def _on_move(self, event):
        self._mousex, self._mousey = event.x, event.y

    def _on_click(self, event):
        self._mousex, self._mousey = event.x, event.y
        print("Click: {}, {}".format(self._mousex, self._mousey))

    def _on_release(self, event):
        self._mousex, self._mousey = event.x, event.y
        print("Release: {}, {}".format(self._mousex, self._mousey))
