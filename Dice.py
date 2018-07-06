import random

from CanvasObject import *


class Dice(CanvasObject):
    def __init__(self,  sides=6, canvas=None, pxcoord=None, grid=None):
        CanvasObject.__init__(self, canvas, pxcoord, grid)
        self._sides = sides

        self.value = "#"  # will hold dice roll

        # canvas objects
        self._rect = None
        self._txt = None

    def _create(self):
        self._hidden = False
        bbox = bbox_coord(self._pxcoord, self.grid.twidth, self.grid.theight)
        self._rect = self.canvas.create_rectangle(*bbox, fill="white", outline="black")
        self._txt = self.canvas.create_text(*self._pxcoord,
                                             text=self.value,
                                             font="Comic {} bold".format(int(self.grid.theight / 2)),
                                             fill="black")
        self._start_bindings()

    def _remove(self):
        self.canvas.delete(self._rect)
        self.canvas.delete(self._txt)

    def _start_bindings(self):
        self.canvas.tag_bind(self._rect, '<Double-Button-1>', self._click_roll)
        self.canvas.tag_bind(self._txt, '<Double-Button-1>', self._click_roll)

    def roll(self, num_rolls=1):
        print("Rolling die")
        if num_rolls == 1:
            self.value = random.randint(1, self._sides)
            if self.canvas is not None:
                self._remove()
                self._create()
            return self.value
        else:
            values = [random.randint(1, self._sides) for _ in range(num_rolls)]
            self.value = values[-1]  # just show the last one
            if self.canvas is not None:
                self._remove()
                self._create()
            return values

    def _click_roll(self, event):
        self.roll()


def bbox_coord(coord, width, height):
    return (coord[0] - width * 0.5,
            coord[1] - height * 0.5,
            coord[0] + width * 0.5,
            coord[1] + height * 0.5,)
