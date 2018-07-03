from settings import *
from Hand import *


class Player(object):
    def __init__(self, canvas, coords, diameter=100, color="yellow", *args, **kwargs):
        self.canvas = canvas
        self.coords = coords
        self.diameter = diameter
        self.color = color

        self.is_active = True
        self.is_hidden = False

        # canvas objects
        self.circle = None
        self.hand = Hand(self.canvas, hidden=(not self.is_active))

    def add_to_hand(self, letter):
        self.hand.add(letter)

    def create(self):
        self.circle = self.canvas.create_circle(self.coords[0], self.coords[1], self.diameter * 0.5, fill=self.color)

    def move(self, dx, dy):
        """ Moves player the given pixel additions.

        :param dx: pixel change in x
        :param dy: pixel change in y
        """
        self.coords = (self.coords[0] + dx, self.coords[1] + dy)
        self.canvas.move(self.circle, dx, dy)
        self.canvas.after(10)
