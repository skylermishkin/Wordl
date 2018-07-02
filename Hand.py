from settings import *
from Grid import *
from Tile import *


class Hand(object):
    def __init__(self, canvas, rows=10, cols=10, hidden=False, *args, **kwargs):
        self.canvas = canvas
        self.rows = rows
        self.cols = cols
        self.hidden = hidden

        self.cwidth = self.canvas.winfo_reqwidth()
        self.cheight = self.canvas.winfo_reqheight()
        self.twidth = (self.cwidth - LR_PAD * 2) / (BOARD_WIDTH + 1)
        self.theight = (self.cheight - TB_PAD * 2) / (BOARD_HEIGHT + 2)
        self.width = self.twidth * self.cols
        self.height = self.theight * self.rows

        self.grid = Grid(rows, cols)
        self.collection = []
        self.state = set()  # set((letter, grid_coord), ...)

        # canvas objects
        self.tiles = []

    def add(self, letter):
        self.collection.append(letter)
        if len(self.state) == 0:
            next_avail_coord = (0, 0)
        elif len(self.state) <= self.rows * self.cols:
            used_coords = [e[1] for e in self.state]
            used_positions = [self.grid.position_from_coords(c) for c in used_coords]
            for i in range(self.rows * self.cols):
                if i not in used_positions:
                    print("Assigning {} to position {}".format(letter, i))
                    next_avail_coord = self.grid.coords_from_pos(i)
                    break
        else:
            print("Hand is full.")
            return
        self.state.add((letter, next_avail_coord))

        self._create_tile(next_avail_coord, letter, width=self.twidth, height=self.theight)
        print("Hand: {}".format(self.state))

    def _create_tile(self, coords, letter, width, height, frozen=False):
        color = RANK_COLOR[LETTER_RANK[letter]]
        self.tiles.append(Tile(self.canvas,
                               self._pxcoords_from_coords(*coords), color=color,
                               text=letter, width=width, height=height, frozen=frozen))
        self.tiles[-1].create()

    def toggle_visibility(self):
        self.hidden = not self.hidden
        if self.hidden:
            self._hide()
        else:
            self._reveal()

    def _hide(self):
        # TODO
        pass

    def _reveal(self):
        # TODO
        pass

    def _positions_used(self):
        return [self.grid.position_from_coords(e[1]) for e in self.state]

    def _pxcoords_from_coords(self, x, y):
        """ Given integer 2d coordinates (in _coords_from_pos), return the pixel coordinates
        (for passing to canvas stuff).

        :param int x:
        :param int y:
        :return px_x, px_y: the pixel coordinates
        """
        return (2 + x) * self.twidth + LR_PAD, (3 + y) * self.theight + TB_PAD
