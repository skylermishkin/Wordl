from settings import *
from Hand import *


class Player(object):
    def __init__(self, canvas, coords, diameter=100, color="yellow", *args, **kwargs):
        self.canvas = canvas
        self.coords = coords
        self.diameter = diameter
        self.color = color

        # canvas objects
        self.circle = None

        self.hand = Hand(self.canvas)

        self.is_active = True

        self.hand = []

    def update(self, coords=None, color=None, toggle_activation=False):
        if toggle_activation:
            self.is_active = not self.is_active
        if coords is not None:
            self.coords = coords
        if color is not None:
            self.color = color

    def create(self):
        self.circle = self.canvas.create_circle(*self.coords, self.diameter * 0.5, fill=self.color)

    def setup(self):
        pass

    def move(self, coords):
        """ Moves player to the given position.

        :param coords: (x, y) pixel coordinates
        """
        self.coords = coords
