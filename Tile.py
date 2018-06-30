class Tile(object):
    def __init__(self, canvas, coords, color="blue", text=None, *args, **kwargs):
        """

        :param canvas:
        :param tuple coords: ((x1, y1), (x2, y2))
        :param color:
        :param text:
        :param args:
        :param kwargs:
        """
        self.canvas = canvas
        self.coords = coords
        self.color = color
        self.text = text

    def check_colision(self, coords):
        return True

    def update(self, coords=None, color=None):
        if coords is not None:
            self.coords = coords
        if color is not None:
            self.color = color

        # arbitrary mvmt
        self.coords = ((self.coords[0][0]+10, self.coords[0][1]+10,),
                       (self.coords[1][0]+10, self.coords[1][1]+10,))

        self.draw()

    def draw(self):
        self.canvas.create_rectangle(self.coords[0][0],
                                     self.coords[0][1],
                                     self.coords[1][0],
                                     self.coords[1][1],
                                     fill=self.color)
