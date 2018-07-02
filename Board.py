import random

from Grid import *
from Tile import *
from Player import *
from settings import *


class Board(object):
    def __init__(self, canvas, width=BOARD_WIDTH, height=BOARD_HEIGHT, tb_pad=TB_PAD, lr_pad=LR_PAD, num_players=1, *args, **kwargs):
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
        self.grid = Grid(self.width, self.height)

        # canvas objects
        self._pathlings = []  # list of rects used to make the board path
        self._players = [[Player(canvas,
                                 self._pxcoords_from_coords(i, 0),  # this will break if you have more than width players
                                 diameter=self.theight*0.5,),
                          i] for i in range(self.num_players)]  # [[Player(), pos], ...]
        self.tile_map = {}  # {(pos, letter): Tile(), ...}
        self._active_hand = None

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
                                    coords=self._pxcoords_from_coords(*self.grid.coords_from_pos(pos)),
                                    color=RANK_COLOR[rank],
                                    text=letter,
                                    frozen=True)
        self._players[0][0].is_active = True

    def update(self):
        for p in self._players:
            player = p[0]
            if player.is_active:
                self._active_hand = player.hand

    def create(self):
        self._create_path()
        for t in self.tile_map:
            self.tile_map[t].create()
        for p in self._players:
            player = p[0]
            player.create()

    def _create_path(self):
        # delete old pathlings; not optimal, maybe not required
        for g in self._pathlings:
            self.canvas.delete(g)
        # iterate through positions on the board and print a rectangle
        for pos in range(self.width * 2 + self.height * 2):
            self._pathlings.append(self.canvas.create_rectangle(
                *bbox_coords(self._pxcoords_from_coords(*self.grid.coords_from_pos(pos)),
                             self.twidth, self.theight),
                fill="white", outline="black"))

    def _add_listeners(self):
        # simple player movement
        self.canvas.bind("<Up>", self._move_player_up)
        self.canvas.bind("<Down>", self._move_player_down)
        # simple tile pickup
        self.canvas.bind("<space>", self._collect_tile)

    def _move_player_up(self, event):
        print("Moving player up")
        for p in self._players:
            if p[0].is_active:
                p[1] += 1
                p[1] = self._clean_position(p[1])
                coords = self.grid.coords_from_pos(p[1])
                x, y = self._pxcoords_from_coords(*coords)
                p[0].move(x - p[0].coords[0], y - p[0].coords[1])

    def _move_player_down(self, event):
        print("Moving player down")
        for p in self._players:
            if p[0].is_active:
                p[1] -= 1
                p[1] = self._clean_position(p[1])
                coords = self.grid.coords_from_pos(p[1])
                x, y = self._pxcoords_from_coords(*coords)
                p[0].move(x - p[0].coords[0], y - p[0].coords[1])

    def _collect_tile(self, event):
        for p in self._players:
            if p[0].is_active:
                for l in self.tile_map:
                    if l[0] == p[1]:
                        print("Collecting {} tile.".format(l[1]))
                        p[0].add_to_hand(l[1])

    def _pxcoords_from_coords(self, x, y):
        """ Given integer 2d coordinates (in _coords_from_pos), return the pixel coordinates
        (for passing to canvas stuff).

        :param int x:
        :param int y:
        :return px_x, px_y: the pixel coordinates
        """
        return x * self.twidth + self.lr_pad, (1 + y) * self.theight + self.tb_pad

    def _clean_position(self, pos):
        """ Keeps the position within the range of positions

        :param pos:
        :return pos:
        """
        max_pos = self.width * 2 + self.height * 2
        if pos < 0:
            pos = max_pos + pos
        elif pos > max_pos:
            pos = pos - max_pos
        return pos

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
