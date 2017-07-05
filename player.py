__author__ = 'lhurd'


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
