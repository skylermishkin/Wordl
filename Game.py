from Board import *
from Player import *
from Tile import *


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

        # setup mouse handling
        self._mousex = None
        self._mousey = None
        self.canvas.bind('<Button-1>', self._on_click)
        self.canvas.bind('<ButtonRelease-1>', self._on_release)

        # canvas objects
        self.players = [Player(self.canvas) for _ in range(self.num_players)]
        self.board = Board(self.canvas)

        self.create()
        self.setup()

    def update(self):
        self.canvas.pack()

        self.board.update()
        for player in self.players:
            player.update()

        self.canvas.after(10)
        self.canvas.update()

    def create(self):
        self.board.create()
        for player in self.players:
            player.create()

    def setup(self):
        self.board.setup()
        for player in self.players:
            player.setup()

    def _on_move(self, event):
        dx = self._mousex - event.x
        dy = self._mousey - event.y
        self._mousex, self._mousey = event.x, event.y

    def _on_click(self, event):
        self._mousex, self._mousey = event.x, event.y
        print "Click: {}, {}".format(self._mousex, self._mousey)

    def _on_release(self, event):
        self._mousex, self._mousey = event.x, event.y
        print "Release: {}, {}".format(self._mousex, self._mousey)
