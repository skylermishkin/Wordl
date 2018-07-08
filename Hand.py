from settings import *
from Grid import *
from Tile import *


class Hand(object):
    def __init__(self, canvas, grid, rows=10, cols=10, hidden=False, *args, **kwargs):
        self.canvas = canvas
        self.rows = rows
        self.cols = cols
        self._hidden = hidden

        self.cwidth = self.canvas.winfo_reqwidth()
        self.cheight = self.canvas.winfo_reqheight()
        self.twidth = (self.cwidth - LR_PAD * 2) / (BOARD_WIDTH + 4)
        self.theight = (self.cheight - TB_PAD * 2) / (BOARD_HEIGHT + 6)
        self.width = self.twidth * self.cols
        self.height = self.theight * self.rows

        self.grid = grid

        # canvas objects
        self.tiles = {}  # {Tile: pos, ...}
        ul_pxcoord = self.grid.pxcoord_from_coord((0, 0))
        br_pxcoord = self.grid.pxcoord_from_coord((self.cols, self.rows))
        self.outline = self.canvas.create_rectangle(ul_pxcoord[0]-0.5*self.twidth, ul_pxcoord[1]-0.5*self.theight,
                                                    br_pxcoord[0]-0.5*self.twidth, br_pxcoord[1]-0.5*self.theight,
                                                    fill="white", outline="black")

    def add(self, letter):
        if len(self.tiles) < self.rows * self.cols:
            used_positions = [self.tiles[tile] for tile in self.tiles]
            for i in range(self.rows * self.cols):
                if i not in used_positions:
                    print("Assigning {} to position {}".format(letter, i))
                    next_avail_coord = self.grid.coord_from_pos(i)
                    break
        else:
            print("Hand is full.")
            return
        color = RANK_COLOR[LETTER_RANK[letter]]
        new_tile = Tile(self.canvas,
                        self.grid.pxcoord_from_coord(next_avail_coord),
                        grid=self.grid,
                        color=color, text=letter,
                        width=self.twidth, height=self.theight, frozen=False)
        new_tile.reveal()
        self.tiles[new_tile] = i
        print("Hand: {}".format(self.tiles))

    def update(self):
        for tile in self.tiles:
            self.tiles[tile] = tile.grid_pos

    def toggle_visibility(self):
        if self._hidden:
            self.reveal()
        else:
            self.hide()

    def hide(self):
        if not self._hidden:
            self._hidden = True
            for tile in self.tiles:
                tile.hide()

    def reveal(self):
        if self._hidden:
            self._hidden = False
            for tile in self.tiles:
                tile.reveal()

    def _positions_used(self):
        return [self.grid.position_from_coord(e[1]) for e in self.tiles]

    def _highlight_words(self):
        # TODO: dictionary integration
        pass