from CanvasObject import *
from settings import *

import random


class Dice(CanvasObject):
    def __init__(self,  sides=6, canvas=None, pxcoord=None, grid=None, grid_pos=None, freeze=False):
        CanvasObject.__init__(self, canvas, pxcoord, grid, grid_pos)
        self._sides = sides
        self._freeze = freeze

        self.value = "#"  # will hold dice roll
        self.frozen = False  # start un-frozen
        self.highlighted = False

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
        self.canvas.tag_bind(self._rect, '<Button-1>', self._click_roll)
        self.canvas.tag_bind(self._txt, '<Button-1>', self._click_roll)

    def roll(self, num_rolls=1):
        """

        :param num_rolls:
        :param freeze:
        :return:
        """
        if not self.frozen:
            if num_rolls == 1:
                result = random.randint(1, self._sides)
                self.value = result
                if self.canvas is not None:
                    self._remove()
                    self._create()
            else:
                result = [random.randint(1, self._sides) for _ in range(num_rolls)]
                self.value = result[-1]  # just show the last one
                if self.canvas is not None:
                    self._remove()
                    self._create()
            if self._freeze:
                self.frozen = True
            print("Rolled {}".format(result))
            return result

    def _click_roll(self, event):
        self.roll()

    def highlight(self):
        if not self.highlighted and not self._hidden:
            self.highlighted = True
            bbox = bbox_coord(self._pxcoord, self.grid.twidth, self.grid.theight)
            self.canvas.delete(self._rect)
            self._rect = self.canvas.create_rectangle(*bbox, fill="white", outline="yellow", width=HIGHLIGHT_WIDTH)
            self.canvas.tag_raise(self._rect)
            self.canvas.tag_raise(self._txt)

    def unhighlight(self):
        if self.highlighted and not self._hidden:
            self.highlighted = False
            self.hide()
            self.reveal()


def bbox_coord(coord, width, height):
    return (coord[0] - width * 0.5,
            coord[1] - height * 0.5,
            coord[0] + width * 0.5,
            coord[1] + height * 0.5)
