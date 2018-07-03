import random

from settings import *


class Tile(object):
    def __init__(self, canvas, coord, width=100, height=100, color="blue", text="A", frozen=False, snap_grid=None,
                 *args, **kwargs):
        """

        :param canvas:
        :param tuple coords:
        :param width:
        :param height:
        :param color:
        :param text:
        :param frozen:
        """
        self.canvas = canvas
        self.coord = list(coord)
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.snap_grid = snap_grid

        # canvas objects
        self._rect = None
        self._txt = None

        self._frozen = frozen
        self._moving = False
        self.grid_pos = None if self.snap_grid is None else self.snap_grid.position_snapped_to_grid(self.coord)

    def create(self):
        bbox = bbox_coord(self.coord, self.width, self.height)
        self._rect = self.canvas.create_rectangle(*bbox, fill=self.color, outline="black")
        if self.text is not None:
            self._txt = self.canvas.create_text(self.coord[0],
                                                self.coord[1],
                                                text=self.text,
                                                font="Comic {} bold".format(int(self.height / 2)),
                                                fill="white")
        self._start_bindings()

    def _start_bindings(self):
        # drag binding
        self.canvas.tag_bind(self._rect, '<Button1-Motion>', self._drag)
        self.canvas.tag_bind(self._rect, '<ButtonRelease-1>', self._release)
        self.canvas.tag_bind(self._txt, '<Button1-Motion>', self._drag)
        self.canvas.tag_bind(self._txt, '<ButtonRelease-1>', self._release)
        # re-roll binding
        if self._frozen:
            self.canvas.tag_bind(self._rect, '<Double-Button-1>', self.reroll)
            self.canvas.tag_bind(self._txt, '<Double-Button-1>', self.reroll)

    def _drag(self, event):
        if self._moving:
            self._move(event.x, event.y)
        elif not self._frozen:
            self._moving = True
            self.canvas.tag_raise(self._rect)
            self.canvas.tag_raise(self._txt)
            self.coord[0] = event.x
            self.coord[1] = event.y

    def _release(self, event):
        self._moving = False
        if self.snap_grid is not None:
            # TODO: still a bit off; I think from where on the tile you grab compared to it's center
            self._move(event.x, event.y)
            self.grid_pos = self.snap_grid.position_snapped_to_grid((event.x, event.y))
            pxcoord = self.snap_grid.position_pxcoords[self.grid_pos]
            self._move(pxcoord[0], pxcoord[1])
            self.canvas.tag_raise(self._rect)
            self.canvas.tag_raise(self._txt)
        self.canvas.after(10)
    
    def _move(self, new_x, new_y):
        """

        :param new_x: pixels
        :param new_y: pixels
        :return:
        """
        self.canvas.move(self._rect, new_x - self.coord[0], new_y - self.coord[1])
        self.canvas.move(self._txt, new_x - self.coord[0], new_y - self.coord[1])
        self.coord[0] = new_x
        self.coord[1] = new_y
        self.canvas.after(10)

    def reroll(self, *args):
        """ Replaces a tile with one that's another letter from the same rank.
        """
        print("Re-rolling")
        rank = LETTER_RANK[self.text]
        replacement_options = {repl for repl in RANK_LETTERS[rank] if repl != self.text}
        repl_letter = random.sample(replacement_options, 1)[0]
        self.text = repl_letter
        self.canvas.delete(self._txt)
        self._txt = self.canvas.create_text(self.coord[0],
                                            self.coord[1],
                                            text=self.text,
                                            font="Comic {} bold".format(int(self.height / 2)),
                                            fill="white")
        self._start_bindings()


def bbox_coord(coord, width, height):
    return (coord[0] - width * 0.5,
            coord[1] - height * 0.5,
            coord[0] + width * 0.5,
            coord[1] + height * 0.5,)
