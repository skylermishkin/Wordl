from settings import *
from CanvasObject import *
from Hand import *


class Player(CanvasObject):
    def __init__(self, canvas, pxcoord=None, grid=None, grid_pos=None, diameter=100, color="yellow", name="Player{}", *args, **kwargs):
        CanvasObject.__init__(self, canvas, pxcoord, grid, grid_pos)
        self.diameter = diameter
        self.color = color
        self.name = name

        self.num_words = None  # int (2,8)
        self.word_lengths = None  # list of ints
        self.power = None  # int (1,6)

        self.is_active = False

        # canvas objects
        self._circle = None
        self._config_box = None
        self.hand_grid = Grid(HAND_WIDTH, HAND_HEIGHT,
                              px_x=2 * self.grid.twidth + LR_PAD,
                              px_y=3 * self.grid.theight + TB_PAD,
                              width=int(BOARD_WIDTH / 3) * self.grid.twidth,
                              height=int(BOARD_HEIGHT / 2) * self.grid.theight)
        self.hand = Hand(self.canvas, grid=self.hand_grid, hidden=(not self.is_active))

    def update(self):
        if not self.is_active:
            self.hand.hide()
        else:
            self.hand.reveal()
        self.hand.update()

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
        self.grid_pos = self.grid.path_pos_from_pxcoord(self._pxcoord)

    def determine_power(self):
        s = sum(self.word_lengths)
        for p in POWER_LENGTHS:
            if s in POWER_LENGTHS[p]:
                self.power = p
                return
        raise RuntimeError("Word length sum {} was outside 65".format(s))
