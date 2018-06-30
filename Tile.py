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

        self._moving = False
        self.mouse_xpos = 0
        self.mouse_ypos = 0

    def check_colision(self, coords):
        # TODO
        return True

    def update(self, coords=None, color=None):
        if coords is not None:
            self.coords = coords
        if color is not None:
            self.color = color

        # arbitrary mvmt
        self.canvas.move(self._rect, 0, 0)
        self.canvas.move(self._txt, 0, 0)

    def create(self):
        bbox = bbox_coords(self.coords, self.width, self.height)
        self._rect = self.canvas.create_rectangle(*bbox, fill=self.color)
        if self.text is not None:
            self._txt = self.canvas.create_text(self.coords[0] + self.width * 0.5,
                                                self.coords[1] + self.height * 0.5,
                                                text=self.text,
                                                font="Comic {} bold".format(self.height / 2),
                                                fill="black")
        # drag binding
        self.canvas.tag_bind(self._rect, '<Button1-Motion>', self._drag)
        self.canvas.tag_bind(self._rect, '<ButtonRelease-1>', self._release)

    def _drag(self, event):
        if self._moving:
            new_x, new_y = event.x, event.y
            self._move(new_x, new_y)
            self.mouse_xpos = new_x
            self.mouse_ypos = new_y
        else:
            self._moving = True
            self.canvas.tag_raise(self._rect)
            self.mouse_xpos = event.x
            self.mouse_ypos = event.y

    def _release(self, event):
        self._moving = False
    
    def _move(self, new_x, new_y):
        self.canvas.move(self._rect,
                         new_x - self.mouse_xpos, new_y - self.mouse_ypos)
        self.canvas.move(self._txt,
                         new_x - self.mouse_xpos, new_y - self.mouse_ypos)


def bbox_coords(coords, width, height):
    return (coords[0],
            coords[1],
            coords[0] + width,
            coords[1] + height,)
