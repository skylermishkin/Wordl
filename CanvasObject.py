class CanvasObject(object):
    def __init__(self, canvas, pxcoord, grid=None):
        self._pxcoord = pxcoord
        self.canvas = canvas
        self.grid = grid

        self._hidden = True  # don't draw until reveal

    def _create(self):
        self._hidden = False
        # canvas.create
        self._start_bindings()

    def _remove(self):
        self._hidden = True
        raise NotImplementedError  # canvas.delete

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
        if not self._hidden:
            self._hidden = False
            self._create()

    def _start_bindings(self):
        pass  # canvas.tag_bind

    def move(self, new_x, new_y):
        """

        :param new_x: pixels
        :param new_y: pixels
        :return:
        """
        # canvas.move
        self._pxcoord[0] = new_x
        self._pxcoord[1] = new_y
