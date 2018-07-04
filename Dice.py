import random


class Dice(object):
    def __init__(self, sides=6, canvas=None, coord=None, grid=None):
        self._sides = 6
        self._canvas = canvas
        self._coord = coord
        self._grid = grid

        self._value = 0  # yuck
        self._hidden = False

        # canvas objects if enabled
        self._rect = None
        self._txt = None

    def roll(self, num_rolls=1):
        if num_rolls == 1:
            self._value = random.randint(1, self._sides)
            if self._canvas is not None:
                self._canvas.delete(self._txt)
                self._canvas.delete(self._rect)
                self.create()
            return self._value
        else:
            values = [random.randint(1, self._sides) for _ in range(num_rolls)]
            self._value = values[-1]  # just show the last one
            if self._canvas is not None:
                self._canvas.delete(self._txt)
                self._canvas.delete(self._rect)
                self.create()
            return values

    def create(self):
        bbox = bbox_coord(self._coord, self._grid.twidth, self._grid.theight)
        self._rect = self._canvas.create_rectangle(*bbox, fill="white", outline="black")
        self._txt = self._canvas.create_text(self._coord[0],
                                             self._coord[1],
                                             text=self._value,
                                             font="Comic {} bold".format(int(self._grid.theight / 2)),
                                             fill="black")
        self._start_bindings()

    def toggle_visibility(self):
        if self._hidden:
            self.reveal()
        else:
            self.hide()

    def hide(self):
        if not self._hidden:
            self._hidden = True
            self._canvas.delete(self._rect)
            self._canvas.delete(self._txt)

    def reveal(self):
        if not self._hidden:
            self.create()

    def _start_bindings(self):
        self._canvas.tag_bind(self._rect, '<Double-Button-1>', self.roll)
        self._canvas.tag_bind(self._txt, '<Double-Button-1>', self.roll)


def bbox_coord(coord, width, height):
    return (coord[0] - width * 0.5,
            coord[1] - height * 0.5,
            coord[0] + width * 0.5,
            coord[1] + height * 0.5,)
