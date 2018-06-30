class Tile(object):
    def __init__(self, canvas, coords, width=100, height=100, color="blue", text="A", *args, **kwargs):
        """

        :param canvas:
        :param tuple coords:
        :param width:
        :param height:
        :param color:
        :param text:
        :param args:
        :param kwargs:
        """
        self.canvas = canvas
        self.coords = list(coords)
        self.width = width
        self.height = height
        self.color = color
        self.text = text

        # hold canvas objects
        self._rect = None
        self._txt = None

        self.draw()

    def check_colision(self, coords):
        # TODO
        return True

    def update(self, coords=None, color=None):
        if coords is not None:
            self.coords = coords
        if color is not None:
            self.color = color

        # arbitrary mvmt
        self.coords[0] += 1
        self.coords[1] += 1

        self.canvas.move(self._rect, self.coords[0], self.coords[1])
        self.canvas.move(self._txt, self.coords[0], self.coords[1])

    def draw(self):
        bbox = bbox_coords(self.coords, self.width, self.height)
        self._rect = self.canvas.create_rectangle(*bbox, fill=self.color)
        if self.text is not None:
            self._txt = self.canvas.create_text(self.coords[0] + self.width * 0.5,
                                                self.coords[1] + self.height * 0.5,
                                                text=self.text,
                                                font="Comic {} bold".format(self.height / 2),
                                                fill="White")


def bbox_coords(coords, width, height):
    return (coords[0],
            coords[1],
            coords[0] + width,
            coords[1] + height,)
