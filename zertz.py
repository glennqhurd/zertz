__author__ = 'lhurd'

import logging
import random
import re

from board import Board
from player import Player
from tables import MIDPOINT

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
    return False


def prompt_for_move(board, player):
    legal = board.legal_captures()
    if len(legal) == 0:
        legal = board.legal_standard_moves(player)
    valid = False
    m = ''
    while not valid:
        m = raw_input('Move? ')
        valid = m.lower() in legal
        if not valid:
            print legal
    return m


def random_move(board, player):
    legal = board.legal_captures()
    if len(legal) == 0:
        legal = board.legal_standard_moves(player)
    return legal[random.randint(0, len(legal) - 1)]


if __name__ == '__main__':
    p1 = Player('Human Player')
    p2 = Player('Computer Player')
    b = Board()
    # for move_num, move in enumerate(SAMPLE_GAME):
    move_num = 1
    b.print_board()
    while True:
        if move_num % 2 == 1:
            cur_player = p1
            move = random_move(b, cur_player)
        else:
            cur_player = p2
            move = random_move(b, cur_player)
        print '\nMove %s Player: %s Move %s' % (
            move_num, cur_player.name, move)
        move_num += 1
        game_over = make_move(b, move, cur_player)
        print b.short_board_string(p1, p2)
        b.print_marbles(p1, p2)
        if game_over:
            print 'Game won by %s' % cur_player.name
            break
