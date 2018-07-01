import random

from Tile import *
from util import *


class Board(object):
    def __init__(self, canvas, width=20, height=10, tb_pad=20, lr_pad=20, *args, **kwargs):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.lr_pad = lr_pad
        self.tb_pad = tb_pad

        self.cwidth = self.canvas.winfo_reqwidth()
        self.cheight = self.canvas.winfo_reqheight()
        self.twidth = (self.cwidth - lr_pad * 2) / (self.width + 1)
        self.theight = (self.cheight - tb_pad * 2) / (self.height + 1)

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
        #self.tiles = [Tile(self.canvas, (100, 100), self.twidth, self.theight) for _ in range(1)]
        for t in self.tile_map:
            self.tile_map[t].create()
            print(self.tile_map[t].coords)

    def _create_bg(self):
        self._bg = self.canvas.create_text(self.cwidth * 0.5,
                                           self.cheight * 0.5,
                                           text="Wordl",
                                           font="Comic {} bold".format(int(self.cheight / 4)),
                                           fill="black")

    def _create_grid(self):
        # delete old gridlings; not optimal
        for g in self._gridlings:
            self.canvas.delete(g)

        pos = [self.lr_pad, self.tb_pad]

        # top and bottom
        for i in range(self.width):
            pos[0] += self.twidth
            self._gridlings.append(self.canvas.create_rectangle(*bbox_coords(pos, self.twidth, self.theight),
                                                                fill="white", outline="black"))
            self._gridlings.append(self.canvas.create_rectangle(*bbox_coords([pos[0], pos[1]+self.height*self.theight],
                                                                             self.twidth, self.theight),
                                                                fill="white", outline="black"))
        # right and left
        for i in range(self.height - 1, 0, -1):
            pos[1] += self.theight
            self._gridlings.append(self.canvas.create_rectangle(*bbox_coords(pos, self.twidth, self.theight),
                                                                fill="white", outline="black"))
            self._gridlings.append(self.canvas.create_rectangle(*bbox_coords([pos[0]-(self.width-1)*self.twidth, pos[1]],
                                                                             self.twidth, self.theight),
                                                                fill="white", outline="black"))

    def _coords_from_pos(self, pos):
        x = 0
        y = 0
        # width is actually 19... check dat out yo
        if pos <= self.width:
            x = pos
        elif pos > self.width:
            x = self.width
            y = pos - x
        elif pos > self.width + self.height - 1:
            y = self.height
            x = self.width - (self.width - (pos - (self.width + self.height - 1)))
        elif pos > self.width * 2 + self.height - 2:
            x = 0
            y = self.height - (self.height - (pos - (self.width * 2 + self.height - 2)))
        print(pos, x, y)
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
