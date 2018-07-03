class Grid(object):
    def __init__(self, cols, rows, px_x=0, px_y=0, width=0, height=0):
        self.cols = cols
        self.rows = rows
        self.px_x = px_x
        self.px_y = px_y
        self.width = width
        self.height = height

        self.twidth = self.width / self.cols
        self.theight = self.height / self.rows

    def coords_from_path_pos(self, pos):
        """ Converts 0-based integer position on the perimeter path to a 0-based integer 2d coordinate.
        0,0 coordinate corresponding to the upper left most position (0).
        If you provide a position outside the 0 to n range, weird things will happen.

        :param int pos: 1-based positioning
        :return x, y: x y integer coordinates on the board grid
        """
        x = 0
        y = 0
        prior_corner_pos = self.cols
        if pos <= self.cols:
            x = pos
        elif pos > prior_corner_pos:
            x = self.cols
            y = pos - prior_corner_pos
            prior_corner_pos = self.cols + self.rows
        if pos > prior_corner_pos:
            y = self.rows
            x = self.cols - (pos - prior_corner_pos)
            prior_corner_pos = self.cols * 2 + self.rows
        if pos > prior_corner_pos:
            x = 0
            y = self.rows - (pos - prior_corner_pos)
        return x, y

    def position_from_coords(self, coords):
        # TODO: fix
        return coords[0] + coords[1]

    def sanitized_path_pos(self, pos):
        """ Keeps the position within the range of positions on a perimeter path.

        :param pos:
        :return pos:
        """
        max_pos = self.cols * 2 + self.rows * 2
        if pos < 0:
            pos = max_pos + pos
        elif pos >= max_pos:
            pos = pos - max_pos
        return pos

    def pxcoords_from_coords(self, coords):
        """ Given integer 2d coordinates (in _coords_from_pos), return the pixel coordinates
        (for passing to canvas stuff).

        :param coords:
        :return px_x, px_y: the pixel coordinates
        """
        return self.px_x + (coords[0] * self.twidth), self.px_y + (coords[1] * self.theight)
