__author__ = 'lhurd'

from board import Board
from player import Player
from tables import MIDPOINT

import logging
import re


STD_PATTERN = '([bgw])([a-g][1-8]),([a-g][1-8])'
CAPTURE_PATTERN = '(([a-g][1-8])-)+([a-g][1-8])'

SAMPLE_GAME = ['wd4,d1', 'wf2,d7', 'wb3,g4', 'wc2,f5', 'bf3,f1', 'f2-f4',
               'be5,g3', 'f4-d6', 'bc6,b1', 'c6-e5', 'bf4,a1', 'f4-d6',
               'bb4,b2', 'b3-b5', 'we6,g2', 'e6-c5', 'b5-d5-d3', 'c2-e3',
               'gd3,f3', 'e3-c2', 'gd2,f2', 'c2-e1', 'gd2,e2', 'e1-c2',
               'gd2,c1', 'c2-e1', 'wg1,d2']


def standard_move(move, board, player):
    m = re.match(STD_PATTERN, move.lower())
    if not m:
        logging.debug('Badly formed move string: %s.', move)
        return False, None
    return board.standard_move(m.group(1), m.group(2), m.group(3), player)


def capture_move(move, board):
    m = re.match(CAPTURE_PATTERN, move.lower())
    if not m:
        logging.debug('Badly formed move string: %s.', move)
        return False, None
    rl = move.split('-')
    count = {'b': 0, 'g': 0, 'w': 0}
    for i in range(len(rl) - 1):
        if tuple(sorted((rl[i], rl[i + 1]))) not in MIDPOINT:
            return False, None
        count[board.single_capture(rl[i], rl[i + 1])] += 1
    return True, count


def add_marbles(d1, d2):
    for k in d1:
        d1[k] += d2[k]


def make_move(board, move, player):
    status, marbles = capture_move(move, board)
    if status:
        add_marbles(player.marbles, marbles)
        return player.has_won()
    status, marbles = standard_move(move, board, player)
    if status:
        add_marbles(player.marbles, marbles)
        return player.has_won()
    raise Exception('Illegal move %s.' % move)
    return False



if __name__ == '__main__':
    p1 = Player('Player 1')
    p2 = Player('Player 2')
    b = Board()
    for move_num, move in enumerate(SAMPLE_GAME):
        cur_player = p1 if move_num % 2 == 0 else p2
        print '\nMove %s Player %s Move %s' % (move_num, cur_player.name, move)
        if make_move(b, move, cur_player):
            print 'Game won by %s' % cur_player.name
            b.print_board()
            print cur_player.marbles
            break
        else:
            b.print_board()
            captures = b.legal_captures()
            if captures:
                print 'Captures %s' % b.legal_captures()
            else:
                print 'Std %s' % b.legal_standard_moves(cur_player)
            print '%s: %s' % (cur_player.name, cur_player.marbles)

