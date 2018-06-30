from Board import *
from Player import *
from Tile import *


class Game(object):
    """

    """
    def __init__(self, canvas, num_players=1, *args, **kwargs):
        """ctor

        :param canvas:
        :param num_players:
        :param args:
        :param kwargs:
        """
        self.canvas = canvas
        self.num_players = num_players

        # setup mouse
        self._mousex = None
        self._mousey = None
        self.canvas.bind('<Button-1>', self._on_click)
        self.canvas.bind('<ButtonRelease-1>', self._on_release)

        self.players = [Player(self.canvas) for _ in range(self.num_players)]
        self.board = Board(self.canvas)

        self.draw()

    def draw(self):
        self.canvas.pack()
        self._blit()

        self.board.draw()
        for player in self.players:
            player.draw()

    def _blit(self):
        self.canvas.create_rectangle(0,
                                     0,
                                     self.canvas.winfo_width(),
                                     self.canvas.winfo_height(),
                                     fill="white")

    def _on_move(self, event):
        self._mousex, self._mousey = event.x, event.y

    def _on_click(self, event):
        self._mousex, self._mousey = event.x, event.y
        print "Click: {}, {}".format(self._mousex, self._mousey)

    def _on_release(self, event):
        self._mousex, self._mousey = event.x, event.y
        print "Release: {}, {}".format(self._mousex, self._mousey)
