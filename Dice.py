import random


class Dice(object):
    def __init__(self, sides=6):
        self.sides = 6

    def roll(self, num_rolls=1):
        if num_rolls == 1:
            return random.randint(1, self.sides)
        else:
            return [random.randint(1, self.sides) for _ in range(num_rolls)]
