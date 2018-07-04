import random


class Dice(object):
    def __init__(self, sides=6, canvas=None, coord=None, grid=None):
        self._sides = sides
        self._canvas = canvas
        self._coord = coord  # pixels
        self._grid = grid

        self.value = "#"  # will hold dice roll
        self._hidden = False

        # canvas objects if enabled
        self._rect = None
        self._txt = None

    def roll(self, num_rolls=1):
        print("Rolling die")
        if num_rolls == 1:
            self.value = random.randint(1, self._sides)
            if self._canvas is not None:
                self.remove()
                self.create()
            return self.value
        else:
            values = [random.randint(1, self._sides) for _ in range(num_rolls)]
            self.value = values[-1]  # just show the last one
            if self._canvas is not None:
                self.remove()
                self.create()
            return values

    def create(self):
        bbox = bbox_coord(self._coord, self._grid.twidth, self._grid.theight)
        self._rect = self._canvas.create_rectangle(*bbox, fill="white", outline="black")
        self._txt = self._canvas.create_text(*self._coord,
                                             text=self.value,
                                             font="Comic {} bold".format(int(self._grid.theight / 2)),
                                             fill="black")
        self._start_bindings()

    def remove(self):
        self._canvas.delete(self._rect)
        self._canvas.delete(self._txt)
        #self._canvas.update_idletasks()

    def toggle_visibility(self):
        if self._hidden:
            self.reveal()
        else:
            self.hide()

    def hide(self):
        if not self._hidden:
            self._hidden = True
            self.remove()

    def reveal(self):
        if not self._hidden:
            self.create()

    def _start_bindings(self):
        self._canvas.tag_bind(self._rect, '<Double-Button-1>', self._click_roll)
        self._canvas.tag_bind(self._txt, '<Double-Button-1>', self._click_roll)

    def _click_roll(self, event):
        self.roll()


def bbox_coord(coord, width, height):
    return (coord[0] - width * 0.5,
            coord[1] - height * 0.5,
            coord[0] + width * 0.5,
            coord[1] + height * 0.5,)
