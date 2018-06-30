from Tile import *


class Board(object):
    def __init__(self, canvas, num_spaces=50, *args, **kwargs):
        self.canvas = canvas
        self.num_spaces = num_spaces

        # arbitrary
        self.tiles = [Tile(self.canvas, ((100, 100), (200, 200))) for _ in range(1)]

    def draw(self):
        #TODO: draw background then foreground
        self.tiles[0].update()
