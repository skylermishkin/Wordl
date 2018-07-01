import random

from Tile import *
from settings import *


class Board(object):
    def __init__(self, canvas, width=20, height=10, tb_pad=20, lr_pad=50, *args, **kwargs):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.lr_pad = lr_pad
        self.tb_pad = tb_pad

        self.cwidth = self.canvas.winfo_reqwidth()
        self.cheight = self.canvas.winfo_reqheight()
        self.twidth = (self.cwidth - lr_pad * 2) / (self.width + 1)
        self.theight = (self.cheight - tb_pad * 2) / (self.height + 2)

        # canvas objects
        self._gridlings = []
        self._bg = None
        self.tile_map = {}

    def setup(self):
        pool = self._generate_pool()
        print(pool)
        tile_positions = self._generate_tile_positions(pool)
        print(tile_positions)
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

    def create(self):
        self._create_bg()
        self._create_grid()
        for t in self.tile_map:
            self.tile_map[t].create()

    def _create_bg(self):
        # Print wordl in the background
        self._bg = self.canvas.create_text(self.cwidth * 0.5,
                                           self.cheight * 0.5,
                                           text="Wordl",
                                           font="Comic {} bold".format(int(self.cheight / 4)),
                                           fill="black")

    def _create_grid(self):
        print("creating the board grid")
        # delete old gridlings; not optimal
        for g in self._gridlings:
            self.canvas.delete(g)
        # iterate through positions on the board and print a rectangle
        for pos in range(1, self.width * 2 + self.height * 2 + 1):
            self._gridlings.append(self.canvas.create_rectangle(*bbox_coords(self._coords_from_pos(pos),
                                                                             self.twidth, self.theight),
                                                                fill="white", outline="black"))

    def _coords_from_pos(self, pos):
        """

        :param int pos: 1-based positioning
        :return x, y: x y integer coordinates
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
        return (0 + x) * self.twidth + self.lr_pad, (0 + y) * self.theight + self.tb_pad

    def _generate_pool(self):
        pool = set()
        for rank in RANK_LETTERS:
            pool.update(set(random.sample(RANK_LETTERS[rank], RANK_POP[rank])))
        return pool

    def _generate_tile_positions(self, pool):
        tile_map = []
        ranks_to_sample = [r for r in RANK_POP for _ in range(RANK_POP[r])]
        pos = 1
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
