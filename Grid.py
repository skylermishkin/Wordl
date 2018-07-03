import math


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

    def coord_from_pos(self, pos):
        """

        :param int pos:
        :return coord: (col,row)
        """
        if pos > self.rows * self.cols:
            raise RuntimeError("Position is greater than area of grid.")

        row = 0
        curr_pos = 0
        while curr_pos + self.cols <= pos:
            row += 1
            curr_pos += self.cols
        col = 0
        while curr_pos + 1 <= pos:
            col += 1
            curr_pos += 1

        return col, row

    def coord_from_path_pos(self, pos):
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

    def position_from_coord(self, coord):
        return coord[0] + coord[1] * self.cols

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

    def pxcoord_from_coord(self, coord):
        """ Given integer 2d coordinates (in coord_from_pos), return the pixel coordinates
        (for passing to canvas stuff).

        :param coord:
        :return px_x, px_y: the pixel coordinates
        """
        return self.px_x + (coord[0] * self.twidth), self.px_y + (coord[1] * self.theight)

    def pxcoord_snapped_to_grid(self, pxcoord):
        # brute force!!GRRYAYAAHH!!@#!@$!#$%!#
        position_pxcoords = []
        euclidean_distances = []
        for i in range(self.rows * self.cols):
            pos_coord = self.coord_from_pos(i)
            pos_pxcoord = self.pxcoord_from_coord(pos_coord)
            position_pxcoords.append(pos_pxcoord)
            euclidean_distances.append(math.hypot(pxcoord[0] - pos_pxcoord[0], pxcoord[1] - pos_pxcoord[1]))
        min_dist = min(euclidean_distances)
        print("Min dist {} to pos {}".format(min_dist, position_pxcoords[euclidean_distances.index(min_dist)]))
        return position_pxcoords[euclidean_distances.index(min_dist)]
