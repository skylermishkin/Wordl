import random

from settings import *
from CanvasObject import *


class Tile(CanvasObject):
    def __init__(self, canvas, pxcoord, width=100, height=100, color="blue", text="A", frozen=False, grid=None,
                 *args, **kwargs):
        """

        :param canvas:
        :param pxcoord:
        :param width: in pixels
        :param height: in pixels
        :param color:
        :param text:
        :param frozen:
        """
        CanvasObject.__init__(self, canvas, pxcoord, grid)
        self.width = width
        self.height = height
        self.color = color
        self.text = text

        self.fontsize = int(self.height * self.width / 60)

        # canvas objects
        self._rect = None
        self._txt = None

        self.frozen = frozen
        self._moving = False
        self.grid_pos = None if self.grid is None else self.grid.position_snapped_to_grid(self._pxcoord)

    def _create(self):
        self._hidden = False
        bbox = bbox_coord(self._pxcoord, self.width, self.height)
        self._rect = self.canvas.create_rectangle(*bbox, fill=self.color, outline="black")
        if self.text is not None:
            self._txt = self.canvas.create_text(self._pxcoord[0],
                                                self._pxcoord[1],
                                                text=self.text,
                                                font="Comic {} bold".format(self.fontsize),
                                                fill="white")
        self._start_bindings()

    def _remove(self):
        self._hidden = True
        self.canvas.delete(self._rect)
        self.canvas.delete(self._txt)

    def _start_bindings(self):
        # drag binding
        self.canvas.tag_bind(self._rect, '<Button1-Motion>', self._drag)
        self.canvas.tag_bind(self._rect, '<ButtonRelease-1>', self._release)
        self.canvas.tag_bind(self._txt, '<Button1-Motion>', self._drag)
        self.canvas.tag_bind(self._txt, '<ButtonRelease-1>', self._release)
        # re-roll binding
        if self.frozen:
            self.canvas.tag_bind(self._rect, '<Double-Button-1>', self.reroll)
            self.canvas.tag_bind(self._txt, '<Double-Button-1>', self.reroll)

    def _drag(self, event):
        if self._moving:
            self.move(event.x, event.y)
        elif not self.frozen:
            self._moving = True
            self.canvas.tag_raise(self._rect)
            self.canvas.tag_raise(self._txt)
            self._pxcoord[0] = event.x
            self._pxcoord[1] = event.y

    def _release(self, event):
        self._moving = False
        if self.grid is not None:
            self.grid_pos = self.grid.position_snapped_to_grid([event.x, event.y])
            pxcoord = self.grid.position_pxcoords[self.grid_pos]
            self.move(pxcoord[0], pxcoord[1])
            self.canvas.tag_raise(self._rect)
            self.canvas.tag_raise(self._txt)
            self._pxcoord[0] = pxcoord[0]
            self._pxcoord[1] = pxcoord[1]
    
    def move(self, new_x, new_y):
        """

        :param new_x: pixels
        :param new_y: pixels
        :return:
        """
        self.canvas.coords(self._rect, *bbox_coord((new_x, new_y), self.width, self.height))
        self.canvas.coords(self._txt, new_x, new_y)
        self.canvas.tag_raise(self._rect)
        self.canvas.tag_raise(self._txt)
        self._pxcoord[0] = new_x
        self._pxcoord[1] = new_y

    def reroll(self, *args):
        """ Replaces a tile with one that's another letter from the same rank.
        """
        print("Rolling tile")
        rank = LETTER_RANK[self.text]
        replacement_options = {repl for repl in RANK_LETTERS[rank] if repl != self.text}
        repl_letter = random.sample(replacement_options, 1)[0]
        self.text = repl_letter
        self.canvas.delete(self._txt)
        self._txt = self.canvas.create_text(self._pxcoord[0],
                                            self._pxcoord[1],
                                            text=self.text,
                                            font="Comic {} bold".format(self.fontsize),
                                            fill="white")
        self._start_bindings()


def bbox_coord(coord, width, height):
    return (coord[0] - width * 0.5,
            coord[1] - height * 0.5,
            coord[0] + width * 0.5,
            coord[1] + height * 0.5,)
