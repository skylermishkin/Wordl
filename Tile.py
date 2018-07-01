from settings import *

class Tile(object):
    def __init__(self, canvas, coords, width=100, height=100, color="blue", text="A", frozen=False,
                 *args, **kwargs):
        """

        :param canvas:
        :param tuple coords:
        :param width:
        :param height:
        :param color:
        :param text:
        :param frozen:
        """
        self.canvas = canvas
        self.coords = list(coords)
        self.width = width
        self.height = height
        self.color = color
        self.text = text

        # canvas objects
        self._rect = None
        self._txt = None

        self._frozen = frozen
        self._moving = False
        self.mouse_xpos = 0
        self.mouse_ypos = 0

    def update(self, coords=None, color=None, toggle_freeze=False):
        if coords is not None:
            self.coords = coords
            self._move(*self.coords)
        if color is not None:
            self.color = color
        if toggle_freeze:
            self._frozen = not self._frozen

    def create(self):
        bbox = bbox_coords(self.coords, self.width, self.height)
        self._rect = self.canvas.create_rectangle(*bbox, fill=self.color, outline="black")
        if self.text is not None:
            self._txt = self.canvas.create_text(self.coords[0] + self.width * 0.5,
                                                self.coords[1] + self.height * 0.5,
                                                text=self.text,
                                                font="Comic {} bold".format(int(self.height / 2)),
                                                fill="white")
        self._start_bindings()

    def _start_bindings(self):
        # drag binding
        self.canvas.tag_bind(self._rect, '<Button1-Motion>', self.drag)
        self.canvas.tag_bind(self._rect, '<ButtonRelease-1>', self.release)
        self.canvas.tag_bind(self._txt, '<Button1-Motion>', self.drag)
        self.canvas.tag_bind(self._txt, '<ButtonRelease-1>', self.release)

    def drag(self, event):
        if self._moving:
            new_x, new_y = event.x, event.y
            self._move(new_x, new_y)
            self.mouse_xpos = new_x
            self.mouse_ypos = new_y
        elif not self._frozen:
            self._moving = True
            self.canvas.tag_raise(self._rect)
            self.canvas.tag_raise(self._txt)
            self.mouse_xpos = event.x
            self.mouse_ypos = event.y

    def release(self, event):
        self._moving = False
        self.canvas.after(10)
    
    def _move(self, new_x, new_y):
        self.canvas.move(self._rect,
                         new_x - self.mouse_xpos, new_y - self.mouse_ypos)
        self.canvas.move(self._txt,
                         new_x - self.mouse_xpos, new_y - self.mouse_ypos)
        self.canvas.after(10)


def bbox_coords(coords, width, height):
    return (coords[0],
            coords[1],
            coords[0] + width,
            coords[1] + height,)
