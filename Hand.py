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

        self.grid = Grid(rows, cols,
                         px_x=2 * self.twidth + LR_PAD,
                         px_y=(BOARD_HEIGHT - HAND_HEIGHT - 1) * self.theight + TB_PAD,
                         width=cols * self.twidth,
                         height=rows * self.theight)

        # canvas objects
        self.tiles = []  # [(Tile, grid_coord), ...]
        ul_pxcoord = self.grid.pxcoords_from_coords((0, 0))
        br_pxcoord = self.grid.pxcoords_from_coords((self.cols, self.rows))
        self.outline = self.canvas.create_rectangle(ul_pxcoord[0]-0.5*self.twidth, ul_pxcoord[1]-0.5*self.theight,
                                                    br_pxcoord[0]+0.5*self.twidth, br_pxcoord[1]+0.5*self.theight,
                                                    fill="white", outline="black")

    def update(self):
        for i,e in enumerate(self.tiles):
            new_coord = e[0].grid_coord
            if new_coord != e[1]:
                e[0].move()
                self.tiles[i] = [e[0], new_coord]

    def add(self, letter):
        if len(self.tiles) == 0:
            next_avail_coord = (0, 0)
        elif len(self.tiles) <= self.rows * self.cols:
            used_coords = [e[1] for e in self.tiles]
            used_positions = [self.grid.position_from_coords(c) for c in used_coords]
            for i in range(self.rows * self.cols):
                if i not in used_positions:
                    print("Assigning {} to position {}".format(letter, i))
                    next_avail_coord = self.grid.coords_from_pos(i)
                    break
        else:
            print("Hand is full.")
            return
        color = RANK_COLOR[LETTER_RANK[letter]]
        self.tiles.append([Tile(self.canvas,
                               self.grid.pxcoords_from_coords(next_avail_coord),
                               #snap_grid=self.grid,
                               color=color, text=letter, width=self.twidth, height=self.theight, frozen=False),
                          next_avail_coord])
        self.tiles[-1][0].create()
        print("Hand: {}".format(self.tiles))

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
        return [self.grid.position_from_coords(e[1]) for e in self.tiles]

    def _pxcoords_from_coords(self, x, y):
        """ Given integer 2d coordinates (in _coords_from_pos), return the pixel coordinates
        (for passing to canvas stuff).

        :param int x:
        :param int y:
        :return px_x, px_y: the pixel coordinates
        """
        return (2 + x) * self.twidth + LR_PAD, (BOARD_HEIGHT - HAND_HEIGHT -1 + y) * self.theight + TB_PAD
