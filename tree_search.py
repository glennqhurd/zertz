"""Tree search module.

Implementation of a negamax alpha-beta pruned search.
"""

__author__ = 'lhurd'

import logging
import random

from board import Board
from player import Player
from tables import INFINITY, NEGATIVE_INFINITY

INITIAL_DEPTH = 3
MAX_CHILDREN = 4

STD_PATTERN = '([bgw])([a-g][1-8]),([a-g][1-8])'
CAPTURE_PATTERN = '(([a-g][1-8])-)+([a-g][1-8])'


def find_move(board):
    """Find the computer's move.

    Args:
      board: current board object

    Returns:
      The best move or None if the game has been lost.
    """
    best_child = None
    best_children = []
    best_value = NEGATIVE_INFINITY
    children = board.legal_moves()
    random.shuffle(children)
    for child in children[:MAX_CHILDREN]:
        new_board = Board(board)
        new_board.make_move(child)
        value = -negamax(new_board, INITIAL_DEPTH, NEGATIVE_INFINITY,
                         INFINITY)
        logging.info('Child: %s Value %d', child, value)
        if value > best_value:
            best_value = value
            best_children = []
        if value >= best_value:
            best_children.append(child)
    # If there are ties, choose randomly from among the tied choices.
    if best_children:
        best_child = best_children[random.randint(0, len(best_children) - 1)]
        # best_child = best_children[0]
    return best_child


def negamax(board, depth, alpha, beta):
    """Perform an alpha beta search of the move tree using the symmetry
    that we can flip the board to always look at things from black's point
    of view.

    Args:
      board: board
      depth: depth of search (overridden if captures are possible)
      alpha: the alpha cut-off
      beta: the beta cut-off

    Returns:
      The evaluation value (integer) of the initial move represented by
      board.
    """
    # We do not stop the search if there are pending captures.
    if depth <= 0:  # and not board.legal_captures():
        return board.evaluate()
    best_value = NEGATIVE_INFINITY
    children = board.legal_moves()
    random.shuffle(children)
    # logging.debug('len children %d', len(children))
    for child in children[:MAX_CHILDREN]:
        new_board = Board(board)
        new_board.make_move(child)
        value = negamax(new_board, depth - 1, -beta, -alpha)
        best_value = max(best_value, value)
        best_move = child
        alpha = max(alpha, value)
        if alpha >= beta:
            break
    # logging.info('%s: Depth %d best_value %d', best_move, depth, best_value)
    return best_value


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    random.seed(999)
    b = Board(player=Player('Player 1'), opponent=Player('Player 2'))
    # for move_num, move in enumerate(SAMPLE_GAME):
    move_num = 1
    b.print_board()
    while True:
        logging.info('Move %d', move_num)
        move = find_move(b)
        print '\nMove %s Player: %s Move %s' % (
            move_num, b.player.name, move)
        move_num += 1
        game_over = b.make_move(move)
        b.print_board()
        if game_over:
            print 'Game won by %s' % b.opponent.name
            break
