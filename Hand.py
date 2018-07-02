from settings import *
from Grid import *


class Hand(object):
    def __init__(self, canvas, width=10, height=10, hidden=False, *args, **kwargs):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.hidden = hidden

        self.grid = Grid(width, height)
        self.collection = []
        self.state = set()  # set((letter, grid_coord), ...)

    def create(self):
        # TODO: draw?
        pass

    def update(self):
        pass

    def add(self, letter):
        self.collection.append(letter)

        if len(self.state) == 0:
            next_avail_coord = (0, 0)
        else:
            used_coords = [e[1] for e in self.state]
            used_positions = [self.grid.position_from_coords(c) for c in used_coords]
            for i in range(self.height * self.width):
                if i not in used_positions:
                    next_avail_coord = self.grid.coords_from_pos(i)
                    break
            print("Hand is full.")
            return
        self.state.add((letter, next_avail_coord))

        # TODO: draw the tile

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