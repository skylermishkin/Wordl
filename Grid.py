class Grid(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def coords_from_pos(self, pos):
        """ Converts 0-based integer position on the path to a 0-based integer 2d coordinate.
        0,0 coordinate corresponding to the upper left most position (0).
        If you provide a position outside the 0 to n range, weird things will happen.

        :param int pos: 1-based positioning
        :return x, y: x y integer coordinates on the board grid
        """
        x = 0
        y = 0
        prior_corner_pos = self.width
        if pos <= self.width:
            x = pos
        elif pos > prior_corner_pos:
            x = self.width
            y = pos - prior_corner_pos
            prior_corner_pos = self.width + self.height
        if pos > prior_corner_pos:
            y = self.height
            x = self.width - (pos - prior_corner_pos)
            prior_corner_pos = self.width * 2 + self.height
        if pos > prior_corner_pos:
            x = 0
            y = self.height - (pos - prior_corner_pos)
        return x, y

    @staticmethod
    def position_from_coords(coords):
        return coords[0] + coords[1]

    def _clean_position(self, pos):
        """ Keeps the position within the range of positions

        :param pos:
        :return pos:
        """
        max_pos = self.width * 2 + self.height * 2
        if pos < 0:
            pos = max_pos + pos
        elif pos > max_pos:
            pos = pos - max_pos
        return pos