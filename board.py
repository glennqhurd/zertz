__author__ = 'lhurd'

from collections import deque
import copy
import logging
import re

from tables import RINGS, MIDPOINT, INFINITY, NEGATIVE_INFINITY


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
    STD_PATTERN = '([bgw])([a-g][1-8]),([a-g][1-8])'
    CAPTURE_PATTERN = '(([a-g][1-8])-)+([a-g][1-8])'

    def __init__(self, other=None, player=None, opponent=None):
        if other:
            self.board = copy.copy(other.board)
            self.marbles = copy.copy(other.marbles)
            self.player = copy.deepcopy(other.player)
            self.opponent = copy.deepcopy(other.opponent)
        else:
            self.board = {}
            self.player = player
            self.opponent = opponent
            for r in RINGS:
                self.board[r] = ' '
                self.marbles = {'b': 10, 'g': 8, 'w': 6}

    def short_board_string(self):
        return ''.join([str(self.player.marbles['b']) +
                        str(self.player.marbles['g']) +
                        str(self.player.marbles['w']) +
                        str(self.player.opponent.marbles['b']) +
                        str(self.player.opponent.marbles['g']) +
                        str(self.player.opponent.marbles['w'])] +
                       [self.board[r] for r in RINGS])

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
        self.print_marbles()

    def accessible_rings(self):
        return [r for r in RINGS if self.accessible(r)]

    def empty_rings(self):
        return [r for r in RINGS if self.board[r] == ' ']

    def accessible(self, r):
        if self.board[r] != ' ':  # Check ring is present and empty..
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

    def standard_move_helper(self, marble, placed, removed):
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
            self.marbles.values()) else self.player.marbles
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
        if captured not in 'bgw':
            raise Exception('Illegal capture %s -> %s.' % (src, dest))
        self.board[mid] = ' '
        self.board[dest] = self.board[src]
        self.board[src] = ' '
        return captured

    def legal_captures(self):
        captures = []
        for (a, b), c in MIDPOINT.items():
            if (self.board[a] in 'bgw' and self.board[c] in 'bgw' and
                        self.board[b] == ' '):
                captures += self.extend_capture([a, c, b])
            elif (self.board[b] in 'bgw' and self.board[c] in 'bgw' and
                          self.board[a] == ' '):
                captures += self.extend_capture([b, c, a])
        return ['-'.join(c[::2]) for c in captures]

    def extend_capture(self, jump_list):
        continuations = []
        jumped = set(jump_list[1::2])  # marbles that have already been jumped
        for (a, b), c in MIDPOINT.items():
            if c not in jumped and self.board[c] in 'bgw':
                if a == jump_list[-1] and self.board[b] == ' ':
                    continuations += self.extend_capture(jump_list + [c, b])
                elif b == jump_list[-1] and self.board[a] == ' ':
                    continuations += self.extend_capture(jump_list + [c, a])
        if continuations:
            return continuations
        else:
            return [jump_list]

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

    def print_marbles(self):
        print 'Supply [Black %s Grey %s White %s]' % (self.marbles['b'],
                                                      self.marbles['g'],
                                                      self.marbles['w'])
        for p in (self.player, self.opponent):
            print 'Name: %s [Black %s Grey %s White %s]' % (p.name,
                                                            p.marbles['b'],
                                                            p.marbles['g'],
                                                            p.marbles['w'])

    def legal_moves(self):
        legal = self.legal_captures()
        if len(legal) == 0:
            legal = self.legal_standard_moves(self.player)
        return legal

    def try_move(self, move):
        new_board = Board(self)
        win = new_board.make_move(move)
        return win, new_board

    def make_move(self, move):
        status, marbles = self.capture_move(move)
        if status:
            self.player.add_marbles(marbles)
        else:
            status, marbles = self.standard_move(move)
            if status:
                self.player.add_marbles(marbles)
            else:
                raise Exception('Illegal move %s.', move)
        t = self.player
        self.player = self.opponent
        self.opponent = t
        return self.opponent.has_won()

    def standard_move(self, move):
        m = re.match(self.STD_PATTERN, move.lower())
        if not m:
            return False, None
        return self.standard_move_helper(m.group(1), m.group(2), m.group(3))

    def capture_move(self, move):
        m = re.match(self.CAPTURE_PATTERN, move.lower())
        if not m:
            # logging.debug('Badly formed move string: %s.', move)
            return False, None
        rl = move.split('-')
        count = {'b': 0, 'g': 0, 'w': 0}
        for i in range(len(rl) - 1):
            if tuple(sorted((rl[i], rl[i + 1]))) not in MIDPOINT:
                return False, None
            count[self.single_capture(rl[i], rl[i + 1])] += 1
        return True, count

    def evaluate(self):
        s1 = self.player.score()
        if s1 == INFINITY:
            return INFINITY
        s2 = self.opponent.score()
        if s2 == INFINITY:
            return NEGATIVE_INFINITY
        logging.debug('%s %d %s %d = %d', self.player.name, s1,
                      self.opponent.name, s2, s1 - s2)
        return s1 - s2


if __name__ == '__main__':
    b = Board()
    for r in RINGS:
        b.board[r] = '.'
    b.board['a1'] = 'b'
    b.board['e4'] = 'b'
    b.board['g1'] = 'b'
    b.board['d3'] = 'g'
    b.board['e5'] = 'g'
    b.board['a3'] = 'w'
    b.board['b4'] = 'w'
    b.board['e2'] = ' '
    b.board['e3'] = ' '
    b.board['f3'] = ' '
    b.board['f4'] = ' '
    b.board['g3'] = ' '
    print b.legal_captures()
