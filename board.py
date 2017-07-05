__author__ = 'lhurd'

from tables import RINGS, MIDPOINT
from collections import deque

import logging


def neighbors(r):
    if r[0] < 'd':
        n = [delta(r, d[0], d[1]) for d in
                ((-1, -1), (-1, 0), (0, 1), (1, 1), (1, 0), (0, -1))]
    elif r[0] =='d':
        n = [delta(r, d[0], d[1]) for d in
                ((-1, -1), (-1, 0), (0, 1), (1, 0), (1, -1), (0, -1))]
    else:
        n = [delta(r, d[0], d[1]) for d in
                ((-1, 0), (-1, 1), (0, 1), (1, 0), (1, -1), (0, -1))]
    return [i for i in n if i in RINGS]


def delta(r, x, y):
    return chr(ord(r[0]) + x) + str(int(r[1]) + y)


def neighbors_cache():
    d = {}
    for r in RINGS:
        d[r] = tuple(neighbors(r))
    return d


class Board:
    NEIGHBORS = neighbors_cache()

    def __init__(self):
        self.board = {}
        for r in RINGS:
            self.board[r] = ' '
        self.marbles = {'b': 10, 'g': 8, 'w': 6}

    def short_board_string(self):
        return ''.join([self.board[r] for r in RINGS])

    # TODO(lhurd): Remove sides bounding empty hexes.
    def print_board(self):
        b = self.board
        print '   A4 B5 C6 D7 E6 F5 G4'
        print '            __'
        print '         __/%s \\__' % b['d7']
        print '      __/%s \__/%s \__' % (b['c6'], b['e6'])
        print '   __/%s \__/%s \__/%s \__' % (b['b5'], b['d6'], b['f5'])
        print '  /%s \__/%s \__/%s \__/%s \\' % (b['a4'], b['c5'], b['e5'],
                                                 b['g4'])
        print '  \__/%s \__/%s \__/%s \__/' % (b['b4'], b['d5'], b['f4'])
        print '  /%s \__/%s \__/%s \__/%s \\' % (b['a3'], b['c4'], b['e4'],
                                                 b['g3'])
        print '  \__/%s \__/%s \__/%s \__/' % (b['b3'], b['d4'], b['f3'])
        print '  /%s \__/%s \__/%s \__/%s \\' % (b['a2'], b['c3'], b['e3'],
                                                 b['g2'])
        print '  \__/%s \__/%s \__/%s \__/' % (b['b2'], b['d3'], b['f2'])
        print '  /%s \__/%s \__/%s \__/%s \\' % (b['a1'], b['c2'], b['e2'],
                                                 b['g1'])
        print '  \__/%s \__/%s \__/%s \__/' % (b['b1'], b['d2'], b['f1'])
        print '     \__/%s \__/%s \__/' % (b['c1'], b['e1'])
        print '        \__/%s \__/' % b['d1']
        print '           \__/\n'
        print '   A1 B1 C1 D1 E1 F1 G1'

    def accessible_rings(self):
        return [r for r in RINGS if self.accessible(r)]

    def empty_rings(self):
        return [r for r in RINGS if self.board[r] == ' ']

    def accessible(self, r):
        if self.board[r] == '.':  # Check ring has not already been removed.
            return False
        n = Board.NEIGHBORS[r]
        if len(n) < 6:  # True for rings on the edge of the board.
            return True
        else:  # Check for two vacant rings that are consecutive.
            vacant = [self.board[r] == '.' for r in n]
            for i in range(6):
                if vacant[i] and vacant[(i + 1) % 6]:
                    return True
        return False

    def remove_captured(self):
        visited = set()
        queue = deque()
        for r in RINGS:
            if self.board[r] == ' ':
                visited.add(r)
                queue.append(r)
        while queue:
            r = queue.popleft()
            for n in Board.NEIGHBORS[r]:
                if n not in visited and self.board[n] != '.':
                    visited.add(n)
                    queue.append(n)
        # remove and count
        count = {'b': 0, 'g': 0, 'w': 0}
        for r in RINGS:
            if self.board[r] != '.' and r not in visited:
                count[self.board[r]] += 1
                self.board[r] = '.'
        return count

    def standard_move(self, marble, placed, removed, player):
        if self.board[placed] != ' ':
            logging.debug('Ring: %s not empty or not present.',
                          placed)
            return False, None
        if self.board[removed] != ' ':
            logging.debug('Ring to be removed: %s not empty or not present.',
                          removed)
            return False, None
        if not self.accessible(removed):
            logging.debug('Ring to be removed: %s not accessible.',
                          removed)
            return False, None
        # If there are no marbles left in the supply, the player uses his own.
        marbles = self.marbles if sum(
            self.marbles.values()) else player.marbles
        if marbles[marble] == 0:
            logging.debug('No %s marbles are available.', marble)
            return False, None

        # Place marble.
        self.board[placed] = marble
        marbles[marble] -= 1

        # Remove ring.
        self.board[removed] = '.'
        return True, self.remove_captured()

    def single_capture(self, src, dest):
        mid = MIDPOINT.get(tuple(sorted((src, dest))))
        if mid is None:
            return None
        captured = self.board[mid]
        self.board[mid] = ' '
        self.board[dest] = self.board[src]
        self.board[src] = ' '
        return captured

    # TODO(lhurd): Account for multiple jumps.
    def legal_captures(self):
        captures = []
        for (a, b), c in MIDPOINT.items():
            if (self.board[a] in 'bgw' and self.board[c] in 'bgw' and
                        self.board[b] == ' '):
                captures.append('%s-%s' % (a, b))
        return captures

    def legal_standard_moves(self, player):
        moves = []
        # If there are no marbles left in the supply, the player uses his own.
        marbles = self.marbles if sum(
            self.marbles.values()) else player.marbles
        empty = self.empty_rings()
        accessible = self.accessible_rings()
        for s in empty:
            for d in accessible:
                if d == s:
                    continue
                for m in 'bgw':
                    if marbles[m] == 0:
                        continue
                    moves.append('%s%s,%s' % (m, s, d))
        return moves



