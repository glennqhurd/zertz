import board
import unittest


class BoardTest(unittest.TestCase):
    def test_delta(self):
        r = 'A1'
        x = 1
        y = 1
        self.assertEqual(board.delta(r, x, y), 'B2')
        r = 'F6'
        x = -1
        y = -1
        self.assertEqual(board.delta(r, x, y), 'E5')
        r = 'B4'
        x = -1
        y = 1
        self.assertEqual(board.delta(r, x, y), 'A5')
        r = 'A5'
        x = 2
        y = -2
        self.assertEqual(board.delta(r, x, y), 'C3')
        r = 'c3'
        x = 1
        y = -1
        self.assertEqual(board.delta(r, x, y), 'd2')

    def test_neighbors(self):
        r = 'a1'
        self.assertEqual(board.neighbors(r), ['a2', 'b2', 'b1'])
        r = 'd2'
        self.assertEqual(board.neighbors(r), ['c1', 'c2', 'd3', 'e2', 'e1', 'd1'])
        r = 'a4'
        self.assertEqual(board.neighbors(r), ['b5', 'b4', 'a3'])
        r = 'b5'
        self.assertEqual(board.neighbors(r), ['a4', 'c6', 'c5', 'b4'])
        r = 'd7'
        self.assertEqual(board.neighbors(r), ['c6', 'e6', 'd6'])
        r = 'g4'
        self.assertEqual(board.neighbors(r), ['f4', 'f5', 'g3'])
        r = 'g1'
        self.assertEqual(board.neighbors(r), ['f1', 'f2', 'g2'])

    #def test_short_board_string(self):
        #board1 = board.Board()
        #self.assertEqual(board1.short_board_string(), '10861086')


if __name__ == '__main__':
    unittest.main()