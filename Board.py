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
        self.grid = Grid(self.width, self.height,
                         px_x=self.lr_pad,
                         px_y=self.theight + self.tb_pad,
                         width=self.twidth * self.width,
                         height=self.theight * self.height)

        # canvas objects
        self._pathlings = []  # list of rects used to make the board path
        self._players = {}
        # TODO update to self.players = {Player: pos}
        print(self._players)
        self.tile_map = {}  # {pos: Tile(), ...}
        self._active_hand = None

        self._add_listeners()

    def setup(self):
        # Tile stuff
        pool = self._generate_pool()
        print("Pool: ", pool)
        tile_positions = self._generate_letter_positions(pool)
        print("Tile map:", tile_positions)
        for t in tile_positions:
            pos = t[0]
            letter = t[1]
            rank = [r for r in RANK_LETTERS if letter in RANK_LETTERS[r]][0]
            self.tile_map[pos] = Tile(self.canvas,
                                    width=self.twidth,
                                    height=self.theight,
                                    coords=self.grid.pxcoords_from_coords(self.grid.coords_from_path_pos(pos)),
                                    color=RANK_COLOR[rank],
                                    text=letter,
                                    frozen=True)

        # Player stuff
        for i in range(self.num_players):
            p = Player(self.canvas,
                       coords=self.grid.pxcoords_from_coords((i, 0)),  # this will break if you have more than width players
                       diameter=self.theight*0.5)
            p.is_active = True if i is 0 else False
            self._players[p] = i

    def create(self):
        self._create_path()
        for t in self.tile_map:
            self.tile_map[t].create()
        for player in self._players:
            player.create()

    def _create_path(self):
        # delete old pathlings; not optimal, maybe not required
        for g in self._pathlings:
            self.canvas.delete(g)
        # iterate through positions on the board and print a rectangle
        for pos in range(self.width * 2 + self.height * 2):
            self._pathlings.append(self.canvas.create_rectangle(
                *bbox_coords(self.grid.pxcoords_from_coords(self.grid.coords_from_path_pos(pos)),
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
        for player in self._players:
            if player.is_active:
                print("Pos before: {}".format(self._players[player]))
                self._players[player] += 1
                self._players[player] = self.grid.sanitized_path_pos(self._players[player])
                print("Pos after: {}".format(self._players[player]))
                x, y = self.grid.pxcoords_from_coords(self.grid.coords_from_path_pos(self._players[player]))
                player.move(x - player.coords[0], y - player.coords[1])

    def _move_player_down(self, event):
        print("Moving player down")
        for player in self._players:
            if player.is_active:
                print("Pos before: {}".format(self._players[player]))
                self._players[player] -= 1
                self._players[player] = self.grid.sanitized_path_pos(self._players[player])
                print("Pos after: {}".format(self._players[player]))
                x, y = self.grid.pxcoords_from_coords(self.grid.coords_from_path_pos(self._players[player]))
                player.move(x - player.coords[0], y - player.coords[1])

    def _collect_tile(self, event):
        for player in self._players:
            if player.is_active:
                for pos in self.tile_map:
                    if pos == self._players[player]:
                        print("Collecting {} tile.".format(self.tile_map[pos].text))
                        player.add_to_hand(self.tile_map[pos].text)
                        self.tile_map[pos].reroll()

    def _generate_letter_positions(self, pool):
        letter_map = []
        ranks_to_sample = [r for r in RANK_POP for _ in range(RANK_POP[r])]
        pos = 0
        empty = False
        while pos <= self.height * 2 + self.width * 2:
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
            letter_map.append((pos, letter))
            pool.remove(letter)
            pos += random.randint(1, 6)
        return letter_map

    @staticmethod
    def _generate_pool():
        # Requires variables from settings.py to be locally available
        pool = set()
        for rank in RANK_LETTERS:
            pool.update(set(random.sample(RANK_LETTERS[rank], RANK_POP[rank])))
        return pool
