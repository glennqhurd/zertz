import player
from tables import INFINITY
import unittest


class PlayerTest(unittest.TestCase):
    def test_add_marbles(self):
        player1 = player.Player('Glenn')
        self.assertEqual(player1.marbles, {'b': 0, 'g': 0, 'w': 0})
        player1.add_marbles({'b': 2, 'g': 3, 'w': 1})
        self.assertEqual(player1.marbles, {'b': 2, 'g': 3, 'w': 1})
        player1.add_marbles({'b': 3, 'g': 0, 'w': 1})
        self.assertEqual(player1.marbles, {'b': 5, 'g': 3, 'w': 2})

    def test_has_won(self):
        player1 = player.Player('Glenn')
        self.assertEqual(player1.has_won(), False)
        player1.add_marbles({'b': 3, 'g': 3, 'w': 3})
        self.assertEqual(player1.has_won(), True)
        player2 = player.Player('Lyman')
        player2.add_marbles({'b': 6, 'g': 0, 'w': 0})
        self.assertEqual(player2.has_won(), True)
        player3 = player.Player('Becca')
        player3.add_marbles({'b': 0, 'g': 5, 'w': 0})
        self.assertEqual(player3.has_won(), True)
        player4 = player.Player('Drew')
        player4.add_marbles({'b': 0, 'g': 0, 'w': 4})
        self.assertEqual(player4.has_won(), True)

    def test_score(self):
        player1 = player.Player('Glenn')
        self.assertEqual(player1.score(), 0)
        player1.add_marbles({'b': 1, 'g': 1, 'w': 1})
        self.assertEqual(player1.score(), 137)
        player1.add_marbles({'b': 2, 'g': 2, 'w': 2})
        self.assertEqual(player1.score(), INFINITY)
        player2 = player.Player('Lyman')
        player2.add_marbles({'b': 3, 'g': 0, 'w': 0})
        self.assertEqual(player2.score(), 130)
        player2.add_marbles({'b': 3, 'g': 0, 'w': 0})
        self.assertEqual(player2.score(), INFINITY)
        player3 = player.Player('Becca')
        player3.add_marbles({'b': 0, 'g': 3, 'w': 0})
        self.assertEqual(player3.score(), 236)
        player3.add_marbles({'b': 0, 'g': 2, 'w': 0})
        self.assertEqual(player3.score(), INFINITY)
        player4 = player.Player('Drew')
        player4.add_marbles({'b': 0, 'g': 0, 'w': 2})
        self.assertEqual(player4.score(), 230)
        player4.add_marbles({'b': 0, 'g': 0, 'w': 2})
        self.assertEqual(player4.score(), INFINITY)

if __name__ == '__main__':
    unittest.main()