from settings import *
from CanvasObject import *
from Hand import *


class Player(CanvasObject):
    def __init__(self, canvas, pxcoord, diameter=100, color="yellow", grid=None, *args, **kwargs):
        CanvasObject.__init__(self, canvas, pxcoord, grid)
        self.diameter = diameter
        self.color = color

        self.is_active = True
        self.num_words = 0
        self.word_lengths = []

        # canvas objects
        self._circle = None
        self._config_box = None
        self.hand = Hand(self.canvas, hidden=(not self.is_active))

    def _create(self):
        # body
        self._circle = self.canvas.create_circle(self._pxcoord[0], self._pxcoord[1],
                                                 self.diameter * 0.5, fill=self.color)
        # config box
        # TODO

    def _remove(self):
        self._hidden = True
        self.canvas.delete(self._circle)
        self.canvas.delete(self._config_box)
        self._circle = None
        self._config_box = None
        self.hand.hide()

    def _start_bindings(self):
        pass

    def add_to_hand(self, letter):
        self.hand.add(letter)

    def hide(self):
        if not self._hidden:
            self._hidden = True
            self._remove()
            self.hand.hide()

    def reveal(self):
        if self._hidden:
            self._hidden = False
            self._create()
            self.hand.reveal()

    def move(self, new_x, new_y):
        """

        :param new_x: pixels
        :param new_y: pixels
        :return:
        """
        self.canvas.move(self._circle, new_x - self._pxcoord[0], new_y - self._pxcoord[1])
        self._pxcoord[0] = new_x
        self._pxcoord[1] = new_y
