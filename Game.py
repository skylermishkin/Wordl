from Board import *
from Player import *
from Hand import *
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

        self._mousex = None
        self._mousey = None
        #self.canvas.bind('<Motion>', self._on_move)
        self.canvas.bind('<Button-1>', self._on_click)

        self.players = [Player(self.canvas) for _ in range(self.num_players)]
        self.board = Board(self.canvas)

        self._draw_board()

    def draw(self):
        self.canvas.pack()
        self._draw_board()

    def _draw_board(self):
        self.canvas.create_rectangle(50, 25, 150, 75, fill="blue")

    def _on_move(self, event):
        self._mousex, self._mousey = event.x, event.y

    def _on_click(self, event):
        self._mousex, self._mousey = event.x, event.y
        print "Click: {}, {}".format(self._mousex, self._mousey)
