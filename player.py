__author__ = 'lhurd'

from tables import INFINITY


class Player:
    def __init__(self, name):
        self.name = name
        self.marbles = {'b': 0, 'g': 0, 'w': 0}

    def has_won(self):
        if (self.marbles['b'] >= 6 or self.marbles['g'] >= 5 or
                    self.marbles['w'] >= 4):
            return True
        if (self.marbles['b'] >= 3 and self.marbles['g'] >= 3 and
                    self.marbles['w'] >= 3):
            return True
        return False

    def score(self):
        b = self.marbles['b']
        g = self.marbles['g']
        w = self.marbles['w']
        # Note 0 <= delta <= 4 (you start the game four white marbles away from
        # a win).
        delta = min(max(0, 6 - b),
                    max(0, 5 - g),
                    max(0, 4 - w),
                    max(0, 3 - b) + max(0, 3 - g) + max(0, 3 - w))
        # If delta == 0 we have achieved a win.
        if delta == 0:
            return INFINITY
        else:
            return 10 * b + 12 * g + 15 * w + 100 * (4 - delta)

    def add_marbles(self, d):
        for k in self.marbles:
            self.marbles[k] += d.get(k, 0)
