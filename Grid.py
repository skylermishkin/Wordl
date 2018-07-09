import math


class Grid(object):
    def __init__(self, cols, rows, px_x=0, px_y=0, width=0, height=0):
        """ctor

        :param int cols:
        :param int rows:
        :param int px_x: upper left pixel x
        :param int px_y: upper left pixel y
        :param int width: pixel width
        :param int height: pixel height
        """
        self.cols = cols
        self.rows = rows
        self.px_x = px_x
        self.px_y = px_y
        self.width = width
        self.height = height

        # tile properties
        self.twidth = self.width / self.cols
        self.theight = self.height / self.rows

        self.position_pxcoords = []
        self._cache_position_pxcoords()

    def coord_from_pos(self, pos):
        """

        :param int pos:
        :return coord: (col,row)
        """
        if pos > self.rows * self.cols:
            raise RuntimeError("Position is greater than area of grid.")

        row = 0
        curr_pos = 0
        while curr_pos + self.cols < pos + 1:
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

    def position_from_path_pos(self, pos):
        coord = self.coord_from_path_pos(pos)
        return self.position_from_coord(coord)

    def pxcoord_from_path_pos(self, pos):
        coord = self.coord_from_path_pos(pos)
        return self.pxcoord_from_coord(coord)

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
        return self.px_x + ((coord[0]) * self.twidth), self.px_y + ((coord[1]) * self.theight)

    def position_snapped_to_grid(self, pxcoord):
        # TODO non-overlap option
        euclidean_distances = []
        for i in range(self.rows * self.cols):
            pos_pxcoord = self.position_pxcoords[i]
            euclidean_distances.append(math.hypot(pxcoord[0] - pos_pxcoord[0], pxcoord[1] - pos_pxcoord[1]))
        min_dist = min(euclidean_distances)
        print("Snapped to pos {}".format(euclidean_distances.index(min_dist)))
        return euclidean_distances.index(min_dist)

    def position_from_pxcoord(self, pxcoord):
        """Checks each position to see if it contains the pxcoord, and returns it. Returns None otherwise.

        :param pxcoord:
        :return:
        """
        nearest_pos = self.position_snapped_to_grid(pxcoord)
        nearest_pxcoord = self.position_pxcoords[nearest_pos]
        minx = nearest_pxcoord[0] - 0.5 * self.twidth
        maxx = nearest_pxcoord[0] + 0.5 * self.twidth
        miny = nearest_pxcoord[1] - 0.5 * self.theight
        maxy = nearest_pxcoord[1] + 0.5 * self.theight
        if minx <= pxcoord[0] <= maxx:
            if miny <= pxcoord[1] <= maxy:
                return nearest_pos
        return None

    def path_pos_from_pxcoord(self, pxcoord):
        # TODO: only works for top and left sides
        pos = self.position_from_pxcoord(pxcoord)
        if pos is not None:
            for path_pos in range(self.rows * 2 + self.cols * 2):
                print("pos {}, coord from pos {}, coord from pppos {}".format(pos,
                                                                              self.coord_from_pos(pos),
                                                                              self.coord_from_path_pos(path_pos)))
                if self.coord_from_path_pos(path_pos) == self.coord_from_pos(pos):
                    return path_pos
        return None

    def _cache_position_pxcoords(self):
        for i in range(self.rows * self.cols):
            pos_coord = self.coord_from_pos(i)
            pos_pxcoord = self.pxcoord_from_coord(pos_coord)
            self.position_pxcoords.append(pos_pxcoord)

    def bbox_coord(self, coord):
        return (coord[0] - self.twidth * 0.5,
                coord[1] - self.theight * 0.5,
                coord[0] + self.twidth * 0.5,
                coord[1] + self.theight * 0.5)
