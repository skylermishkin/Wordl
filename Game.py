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

        self.canvas.focus_set()
        """
        # setup mouse handling
        self._mousex = None
        self._mousey = None
        self.canvas.bind('<Button-1>', self._on_click)
        self.canvas.bind('<ButtonRelease-1>', self._on_release)
        """

        # canvas objects
        self.board = Board(self.canvas, num_players=self.num_players)

        self.setup()
        self.create()

    def update(self):
        self.board.update()

        self.canvas.after(10)
        self.canvas.update()

    def create(self):
        self.board.create()

    def setup(self):
        self.board.setup()

    def _on_move(self, event):
        self._mousex, self._mousey = event.x, event.y

    def _on_click(self, event):
        self._mousex, self._mousey = event.x, event.y
        print("Click: {}, {}".format(self._mousex, self._mousey))

    def _on_release(self, event):
        self._mousex, self._mousey = event.x, event.y
        print("Release: {}, {}".format(self._mousex, self._mousey))
