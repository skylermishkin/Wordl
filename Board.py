from Tile import *


class Board(object):
    def __init__(self, canvas, width=20, height=10, tb_pad=20, lr_pad=20, *args, **kwargs):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.lr_pad = lr_pad
        self.tb_pad = tb_pad

        self.twidth = (self.canvas.winfo_width() - lr_pad * 2) / (self.width + 1)
        self.theight = (self.canvas.winfo_height() - tb_pad * 2) / (self.height + 1)

        # board pieces
        self._gridlings = []

        # arbitrary
        self.tiles = [Tile(self.canvas, (100, 100)) for _ in range(1)]

        self.draw()

    def update(self):
        for tile in self.tiles:
            tile.update()

    def draw(self):
        self._draw_grid()
        for tile in self.tiles:
            tile.draw()

    def _draw_grid(self):
        # delete old gridlings; not optimal
        for g in self._gridlings:
            self.canvas.delete(g)

        pos = [self.lr_pad, self.tb_pad]

        # top and bottom
        for i in range(self.width):
            pos[0] += self.twidth
            self._gridlings.append(self.canvas.create_rectangle(*bbox_coords(pos, self.twidth, self.theight),
                                                                fill="white", outline="black"))
            self._gridlings.append(self.canvas.create_rectangle(*bbox_coords([pos[0], pos[1]+self.height*self.theight],
                                                                             self.twidth, self.theight),
                                                                fill="white", outline="black"))
        # right and left
        for i in range(self.height - 1, 0, -1):
            pos[1] += self.theight
            self._gridlings.append(self.canvas.create_rectangle(*bbox_coords(pos, self.twidth, self.theight),
                                                                fill="white", outline="black"))
            self._gridlings.append(self.canvas.create_rectangle(*bbox_coords([pos[0]-(self.width-1)*self.twidth, pos[1]],
                                                                             self.twidth, self.theight),
                                                                fill="white", outline="black"))
