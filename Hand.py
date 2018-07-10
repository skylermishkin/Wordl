from settings import *
from Grid import *
from Tile import *

from natsort import natsorted


class Hand(object):
    def __init__(self, canvas, grid, rows=10, cols=10, hidden=False, *args, **kwargs):
        self.canvas = canvas
        self.rows = rows
        self.cols = cols
        self._hidden = hidden

        self.changed = True  # flag for update

        self.cwidth = self.canvas.winfo_reqwidth()
        self.cheight = self.canvas.winfo_reqheight()
        self.twidth = (self.cwidth - LR_PAD * 2) / (BOARD_WIDTH + 4)
        self.theight = (self.cheight - TB_PAD * 2) / (BOARD_HEIGHT + 6)
        self.width = self.twidth * self.cols
        self.height = self.theight * self.rows

        self.grid = grid

        # canvas objects
        self.tiles = []  # [[Tile, pos], ...]
        self._outline = None
        self.outline()
        self.highlights = []

    def outline(self):
        if self._outline is not None:
            self.canvas.delete(self._outline)
        self._outline = self.canvas.create_rectangle(self.grid.px_x, self.grid.px_y,
                                                     self.grid.px_x + self.grid.width,
                                                     self.grid.px_y + self.grid.height,
                                                     fill="white", outline="black")

    def add(self, letter):
        if len(self.tiles) < self.rows * self.cols:
            used_positions = [t[1] for t in self.tiles]
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
        self.tiles.append([new_tile, i])
        self.changed = True
        print("Hand: {}".format(self.tiles))

    def update(self):
        # TODO: adding a new tile executes highlighting; movement surprisingly does not
        for t in self.tiles:
            if t[1] != t[0].grid_pos:
                t[1] = t[0].grid_pos
                self.changed = True
        if not self._hidden and self.changed:

            self._highlight_words()
            self.changed = False

    def toggle_visibility(self):
        if self._hidden:
            self.reveal()
        else:
            self.hide()

    def hide(self):
        if not self._hidden:
            self._hidden = True
            # clear existing highlights
            for h in self.highlights:
                self.canvas.delete(h)
                self.highlights.remove(h)
            for t in self.tiles:
                t[0].hide()

    def reveal(self):
        if self._hidden:
            self._hidden = False
            for t in self.tiles:
                t[0].reveal()
            self.update()

    def _positions_used(self):
        return [e[1] for e in self.tiles]

    def _highlight_words(self):
        # short-circuit if tiles are being moved
        for t in self.tiles:
            if t[0].is_moving():
                return

        words = []
        # clear existing highlights
        for h in self.highlights:
            self.canvas.delete(h)
            self.highlights.remove(h)
        # ID all words and highlight real ones
        grouped_tiles = self._group_tiles()
        for group in grouped_tiles:
            word = "".join([tile.text for tile in group])
            if word.lower() in DICTIONARY:
                words.append(word)
                self._highlight_group(group)
        print("Highlighted words in hand: {}".format(words))

    def _group_tiles(self):
        tile_groups = []
        positions_used = natsorted(self._positions_used())
        idx = 0
        while idx < len(positions_used):
            tmp_group = [self._tile_at_pos(positions_used[idx])]  # start contig at the current index
            contig_length = 1
            for i, p in enumerate(positions_used[idx+1:]):  # iterate through remaining tiles
                # TODO: check for spanning multiple rows
                if p - 1 == positions_used[idx + i]:  # ensure position is contiguous from the last
                    contig_length += 1
                    tmp_group.append(self._tile_at_pos(p))
                else:
                    break
            tile_groups.append(tmp_group)
            idx += contig_length
        return tile_groups

    def _highlight_group(self, group):
        ul_pxcoord = (group[0].pxcoord()[0] - group[0].grid.twidth * 0.5,
                      group[0].pxcoord()[1] - group[0].grid.theight * 0.5)
        br_pxcoord = (group[-1].pxcoord()[0] + group[-1].grid.twidth * 0.5,
                      group[-1].pxcoord()[1] + group[-1].grid.theight * 0.5)
        self.highlights.append(self.canvas.create_rectangle(ul_pxcoord[0], ul_pxcoord[1],
                                                            br_pxcoord[0], br_pxcoord[1],
                                                            fill="white", outline="yellow",
                                                            width=HIGHLIGHT_WIDTH))
        for t in self.tiles:
            t[0].hide()
            t[0].reveal()

    def _tile_at_pos(self, pos):
        for t in self.tiles:
            if t[1] == pos:
                return t[0]
        return None

    def regrid(self, new_grid):
        self.grid = new_grid
        for t in self.tiles:
            t[0]._pxcoord = new_grid.position_pxcoords[t[1]]
        self.update()
