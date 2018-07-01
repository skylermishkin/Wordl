import random

from Tile import *
from Player import *
from settings import *


class Board(object):
    def __init__(self, canvas, width=20, height=10, tb_pad=20, lr_pad=50, num_players=1, *args, **kwargs):
        """ctor

        :param canvas:
        :param width: num tiles wide
        :param height:  num tiles high
        :param tb_pad:
        :param lr_pad:
        :param num_players:
        """
        self.canvas = canvas
        self.width = width
        self.height = height
        self.lr_pad = lr_pad
        self.tb_pad = tb_pad
        self.num_players = num_players

        self.cwidth = self.canvas.winfo_reqwidth()
        self.cheight = self.canvas.winfo_reqheight()
        self.twidth = (self.cwidth - lr_pad * 2) / (self.width + 1)
        self.theight = (self.cheight - tb_pad * 2) / (self.height + 2)

        # canvas objects
        self._pathlings = []  # list of rects used to make the board path
        self._players = [Player(canvas,
                                self._pxcoords_from_coords(i, 0),
                                diameter=self.theight) for i in range(self.num_players)]
        self.tile_map = {}  # {(pos, letter): Tile(), ...}

        self._add_listeners()

    def setup(self):
        pool = self._generate_pool()
        print("Pool: ", pool)
        tile_positions = self._generate_tile_positions(pool)
        print("Tile map:", tile_positions)
        for t in tile_positions:
            pos = t[0]
            letter = t[1]
            rank = [r for r in RANK_LETTERS if letter in RANK_LETTERS[r]][0]
            self.tile_map[t] = Tile(self.canvas,
                                    width=self.twidth,
                                    height=self.theight,
                                    coords=self._coords_from_pos(pos),
                                    color=RANK_COLORS[rank],
                                    text=letter,
                                    frozen=True)

    def update(self):
        for t in self.tile_map:
            self.tile_map[t].update()
        for p in self._players:
            p.update()

    def create(self):
        self._create_path()
        for t in self.tile_map:
            self.tile_map[t].create()
        for p in self._players:
            p.create()

    def _create_path(self):
        # delete old pathlings; not optimal, maybe not required
        for g in self._pathlings:
            self.canvas.delete(g)
        # iterate through positions on the board and print a rectangle
        for pos in range(self.width * 2 + self.height * 2):
            self._pathlings.append(self.canvas.create_rectangle(*bbox_coords(self._coords_from_pos(pos),
                                                                             self.twidth, self.theight),
                                                                fill="white", outline="black"))

    def _add_listeners(self):
        pass

    def _coords_from_pos(self, pos):
        """ Converts 0-based integer position on the path to a 0-based integer 2d coordinate.
        0,0 coordinate corresponding to the upper left most position (0).

        :param int pos: 1-based positioning
        :return x, y: x y integer coordinates on the board grid
        """
        x = 0
        y = 0
        prior_corner_pos = self.width
        if pos <= self.width:
            x = pos
        elif pos > prior_corner_pos:
            x = self.width
            y = pos - prior_corner_pos
            prior_corner_pos = self.width + self.height
        if pos > prior_corner_pos:
            y = self.height
            x = self.width - (pos - prior_corner_pos)
            prior_corner_pos = self.width * 2 + self.height
        if pos > prior_corner_pos:
            x = 0
            y = self.height - (pos - prior_corner_pos)
        return self._pxcoords_from_coords(x, y)

    def _pxcoords_from_coords(self, x, y):
        """ Given integer 2d coordinates (from _coords_from_pos), return the pixel coordinates
        (for passing to canvas stuff).

        :param int x:
        :param int y:
        :return px_x, px_y: the pixel coordinates
        """
        return x * self.twidth + self.lr_pad, (1 + y) * self.theight + self.tb_pad

    @staticmethod
    def _generate_pool():
        # Requires variables from settings.py to be locally available
        pool = set()
        for rank in RANK_LETTERS:
            pool.update(set(random.sample(RANK_LETTERS[rank], RANK_POP[rank])))
        return pool

    @staticmethod
    def _generate_tile_positions(pool):
        tile_map = []
        ranks_to_sample = [r for r in RANK_POP for _ in range(RANK_POP[r])]
        pos = 0
        empty = False
        while pos <= 60:
            rank_picked = random.sample(ranks_to_sample, 1)[0]
            pool_options = [l for l in pool if l in RANK_LETTERS[rank_picked]]
            while len(pool_options) == 0:
                ranks_to_sample = [r for r in ranks_to_sample if r != rank_picked]
                if len(ranks_to_sample) == 0:
                    empty = True
                    break
                rank_picked = random.sample(ranks_to_sample, 1)[0]
                pool_options = [l for l in pool if l in RANK_LETTERS[rank_picked]]
            if empty:
                break
            letter = random.sample(pool_options, 1)[0]
            tile_map.append((pos, letter))
            pool.remove(letter)
            pos += random.randint(1, 6)
        return tile_map
