from settings import *


class Hand(object):
    def __init__(self, canvas, hidden=False, *args, **kwargs):
        self.canvas = canvas
        self.hidden = hidden

    def create(self):
        pass

    def update(self):
        pass

    def add(self, letter):
        pass

    def toggle_visibility(self):
        self.hidden = not self.hidden
        if self.hidden:
            self._hide()
        else:
            self._reveal()

    def _hide(self):
        pass

    def _reveal(self):
        pass