from Tile import *


class Board(object):
    def __init__(self, canvas, width=20, height=10, *args, **kwargs):
        self.canvas = canvas
        self.width = width
        self.height = height

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

    def _draw_grid(self, topbot_pad=20, lr_pad=20):
        # delete old gridlings; not optimal
        for g in self._gridlings:
            self.canvas.delete(g)

        tile_width = (self.canvas.winfo_width() - lr_pad * 2) / (self.width + 1)
        tile_height = (self.canvas.winfo_height() - topbot_pad * 2) / (self.height + 1)
        pos = [lr_pad, topbot_pad]

        # top and bottom
        for i in range(self.width):
            pos[0] += tile_width
            self._gridlings.append(self.canvas.create_rectangle(*bbox_coords(pos, tile_width, tile_height),
                                                                fill="white", outline="black"))
            self._gridlings.append(self.canvas.create_rectangle(*bbox_coords([pos[0], pos[1]+self.height*tile_height],
                                                                             tile_width, tile_height),
                                                                fill="white", outline="black"))
        # right and left
        for i in range(self.height - 1, 0, -1):
            pos[1] += tile_height
            self._gridlings.append(self.canvas.create_rectangle(*bbox_coords(pos, tile_width, tile_height),
                                                                fill="white", outline="black"))
            self._gridlings.append(self.canvas.create_rectangle(*bbox_coords([pos[0]-(self.width-1)*tile_width, pos[1]],
                                                                             tile_width, tile_height),
                                                                fill="white", outline="black"))
