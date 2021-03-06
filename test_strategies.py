import unittest
import strategies as strat


# Testing different helper functions
class TestHelpers(unittest.TestCase):
    # Testing the check shot function
    def test_coordinates_shot(self):
        strat.coordinates_shot = list()
        strat.coordinates_shot.append((1, 2))

        self.assertEqual(strat.coordinates_shot, [(1, 2)])

    # Testing the check shot function
    def test_check_shot(self):
        strat.coordinates_shot = list()
        strat.coordinates_shot.append((1, 2))

        self.assertTrue(strat.check_shot(1, 2))

    # Testing the check shot function
    def test_check_shot_2(self):
        strat.coordinates_shot = list()
        strat.coordinates_shot.append((1, 2))

        self.assertFalse(strat.check_shot(3, 4))

        # Testing the strategy choose function with random strategy
    def test_strategy_choose_random(self):
        strat.coordinates_shot = list()
        x, y = strat.strategy_choose("Random", (0, 9, 1, 10), list())

        self.assertIn(x, range(0, 10))
        self.assertIn(y, range(1, 11))

    # Testing the strategy choose function with random strategy
    def test_strategy_choose_blanket(self):
        strat.coordinates_shot = list()
        x, y = strat.strategy_choose("Blanket", (0, 9, 1, 10), list())

        self.assertIn(x, range(0, 10))
        self.assertIn(y, range(1, 11))
        self.assertEqual(strat.coordinates_shot, [(0, 1)])

    def test_strategy_choose_smart_random(self):
        strat.coordinates_shot = list()
        x, y = strat.strategy_choose("Smart random", (0, 9, 1, 10), list())

        self.assertIn(x, range(0, 10))
        self.assertIn(y, range(1, 11))

    def test_strategy_choose_smart_odd(self):
        strat.coordinates_shot = list()
        x, y = strat.strategy_choose("Smart odd", (0, 9, 1, 10), list())

        self.assertIn(x, range(0, 10))
        self.assertIn(y, range(1, 11))
        self.assertTrue(strat.check_odd((x, y)))

    # Checks the coordinates, odd should be true
    def test_check_odd_true(self):
        x = 1
        y = 2
        self.assertTrue(strat.check_odd((x, y)))

    # Checks the coordinates, odd should be false
    def test_check_odd_false(self):
        x = 5
        y = 7
        self.assertFalse(strat.check_odd((x, y)))

    # Checks the coordinates, valid should be true
    def test_valid_coordinate_true(self):
        x = 1
        y = 7
        self.assertTrue(strat.valid_coordinate((x, y), (0, 9, 1, 10)))

    # Checks the coordinates, valid should be true
    def test_valid_coordinate_true_2(self):
        x = 13
        y = 9
        self.assertTrue(strat.valid_coordinate((x, y), (11, 20, 1, 10)))

    # Checks the coordinates, valid should be false
    def test_valid_coordinate_false(self):
        x = 10
        y = 1
        self.assertFalse(strat.valid_coordinate((x, y), (0, 9, 1, 10)))

    # Checks the coordinates, valid should be false
    def test_valid_coordinate_false_2(self):
        x = 15
        y = 0
        self.assertFalse(strat.valid_coordinate((x, y), (11, 20, 1, 10)))


# Testing functions for different strategies
class TestStrategies(unittest.TestCase):

    # Testing the random fire function
    def test_random_fire(self):
        strat.coordinates_shot = list()
        x, y = strat.random_fire((0, 9, 1, 10))

        self.assertIn(x, range(0, 10))
        self.assertIn(y, range(1, 11))
        self.assertEqual(strat.coordinates_shot, [(x, y)])

    # Testing the random fire function
    def test_blanket_fire(self):
        strat.coordinates_shot = list()
        x, y = strat.blanket_fire((0, 9, 1, 10))

        self.assertIn(x, range(0, 9))
        self.assertIn(y, range(1, 10))
        self.assertEqual(strat.coordinates_shot, [(0, 1)])

    # Testing the random fire function for multiple shots
    # Interestingly enough, you have to add the second blanket fire with different bounds
    # Because the function was set up for alternating fire between two players
    def test_blanket_fire_2(self):
        strat.coordinates_shot = list()
        strat.blanket_fire((0, 9, 1, 10))
        strat.blanket_fire((11, 20, 1, 10))
        x, y = strat.blanket_fire((0, 9, 1, 10))

        self.assertIn(x, range(0, 10))
        self.assertIn(y, range(1, 11))
        self.assertIn((1, 1), strat.coordinates_shot)

    # Testing the random fire function for fire until another row
    # Interestingly enough, you have to add the second blanket fire with different bounds
    # Because the function was set up for alternating fire between two players
    def test_blanket_fire_n(self):
        strat.coordinates_shot = list()
        for i in range(0, 39):
            strat.blanket_fire((0, 9, 1, 10))
            strat.blanket_fire((11, 20, 1, 10))

        x, y = strat.blanket_fire((0, 9, 1, 10))

        self.assertIn(x, range(0, 10))
        self.assertIn(y, range(1, 11))
        self.assertIn((1, 2), strat.coordinates_shot)
        self.assertIn((12, 1), strat.coordinates_shot)

    # Testing the smart random odd fire function to make sure random shot is odd
    def test_smart_random_odd_fire(self):
        strat.coordinates_shot = list()
        x, y = strat.smart_random_odd_fire((0, 9, 1, 10), list())

        self.assertIn(x, range(0, 10))
        self.assertIn(y, range(1, 11))
        self.assertTrue(strat.check_odd((x, y)))


if __name__ == '__main__':
    unittest.main()
