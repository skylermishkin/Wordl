from abc import ABCMeta, abstractmethod


class CanvasObject:
    __metaclass__ = ABCMeta

    def __init__(self, canvas=None, pxcoord=None, grid=None, grid_pos=None):
        """ctor

        :param canvas:
        :param pxcoord: [x, y] integer pixels
        :param grid: Grid() object
        """
        self.canvas = canvas
        self.grid = grid
        self.grid_pos = grid_pos
        self._pxcoord = None if not pxcoord else list(pxcoord)
        if self._pxcoord is None and self.grid_pos is not None:
            self._pxcoord = list(self.grid.position_pxcoords[self.grid_pos])
        if self.grid_pos is None and self.grid is not None:
            self.grid_pos = self.grid.position_from_pxcoord(self._pxcoord)

        self._hidden = True  # don't draw until reveal

    @abstractmethod
    def _create(self):
        self._hidden = False
        print("nothing created")  # canvas.create
        self._start_bindings()

    @abstractmethod
    def _remove(self):
        self._hidden = True
        print("nothing deleted")  # canvas.delete

    def toggle_visibility(self):
        if self._hidden:
            self.reveal()
        else:
            self.hide()

    def hide(self):
        if not self._hidden:
            self._hidden = True
            self._remove()

    def reveal(self):
        if self._hidden:
            self._hidden = False
            self._create()

    @abstractmethod
    def _start_bindings(self):
        pass  # canvas.tag_bind

    def move(self, new_x, new_y):
        """

        :param new_x: pixels
        :param new_y: pixels
        :return:
        """
        print("movement not drawn")  # canvas.move or canvas.coords
        self._pxcoord[0] = new_x
        self._pxcoord[1] = new_y

    def is_hidden(self):
        return self._hidden

    def pxcoord(self):
        return self._pxcoord
