import unittest
import functionality as fy


class TestShip(unittest.TestCase):

    # Tests the creation of a ship
    def test_ship_creation(self):
        ship = fy.Ship("Ship1", 3, [])

        self.assertIsInstance(ship, fy.Ship)

    # Tests the coordinates of a ship
    def test_coordinates(self):
        ship = fy.Ship("Ship", 2, [(1, 2), (2, 2)])
        self.assertListEqual(ship.coordinates, [(1, 2), (2, 2)])

    # Tests the get_alive method of a ship
    def test_get_alive1(self):
        ship = fy.Ship("Ship2", 1, [])

        self.assertTrue(ship.get_alive())

    # Tests the get_health method of a ship
    def test_get_health(self):
        ship = fy.Ship("Ship3", 2, [])

        self.assertEqual(ship.get_health(), 2)

    # Tests the take_damage method of a ship
    # Takes damage once
    def test_take_damage1(self):
        ship = fy.Ship("Ship3", 2, [])

        ship.take_damage()

        self.assertEqual(ship.get_health(), 1)

    # Tests the take_damage method of a ship
    # Takes damage twice
    def test_take_damage2(self):
        ship = fy.Ship("Ship3", 2, [])

        ship.take_damage()
        ship.take_damage()

        self.assertEqual(ship.get_health(), 0)

    # Tests the get_alive method of a ship
    # Takes damage twice, should not be alive
    def test_get_alive2(self):
        ship = fy.Ship("Ship3", 2, [])

        ship.take_damage()
        ship.take_damage()

        self.assertFalse(ship.get_alive())


class TestPlayers(unittest.TestCase):

    # Tests player creation
    def test_player_creation(self):
        player = fy.Players("Player")

        self.assertIsInstance(player, fy.Players)

    # Tests number of wins
    def test_get_win(self):
        player = fy.Players("Player")

        self.assertEqual(player.get_wins(), 0)

    # Tests adding a win
    def test_add_win(self):
        player = fy.Players("Player")

        player.add_win()

        self.assertEqual(player.get_wins(), 1)

    # Tests the get_score method
    def test_get_score(self):
        player = fy.Players("Player")

        self.assertEqual(player.get_score(), (0, 0))

    # Tests add_ship method
    def test_add_ship(self):
        player = fy.Players("Player")
        ship = fy.Ship("Ship", 1, [])

        player.add_ship(ship)

        self.assertListEqual(player.ships, [ship])

    # Tests killing a ship
    def test_kill_ship1(self):
        player = fy.Players("Player")
        ship = fy.Ship("Ship", 1, [])

        player.add_ship(ship)

        player.kill_ship(ship)

        self.assertListEqual(player.ships, [])

    # Tests killing one ship in many
    def test_kill_ship2(self):
        player = fy.Players("Player")
        ship = fy.Ship("Ship", 1, [])
        ship2 = fy.Ship("Ship2", 1, [])
        ship3 = fy.Ship("Ship3", 1, [])

        player.add_ship(ship)
        player.add_ship(ship2)
        player.add_ship(ship3)

        player.kill_ship(ship2)

        self.assertListEqual(player.ships, [ship, ship3])

    # Tests killing a ship and getting the score
    def test_kill_ship_get_score(self):
        player = fy.Players("Player")
        ship = fy.Ship("Ship", 1, [])
        ship2 = fy.Ship("Ship2", 1, [])
        ship3 = fy.Ship("Ship3", 1, [])

        player.add_ship(ship)
        player.add_ship(ship2)
        player.add_ship(ship3)

        player.kill_ship(ship2)

        self.assertEqual(player.get_score(), (2, 1))

    # Tests the reset method for score
    def test_reset1(self):
        player = fy.Players("Player")
        ship = fy.Ship("Ship", 1, [])
        ship2 = fy.Ship("Ship2", 1, [])
        ship3 = fy.Ship("Ship3", 1, [])

        player.add_ship(ship)
        player.add_ship(ship2)
        player.add_ship(ship3)

        player.kill_ship(ship2)

        player.reset()
        self.assertEqual(player.get_score(), (0, 0))

    # Tests the reset method for ships
    def test_reset2(self):
        player = fy.Players("Player")
        ship = fy.Ship("Ship", 1, [])
        ship2 = fy.Ship("Ship2", 1, [])
        ship3 = fy.Ship("Ship3", 1, [])

        player.add_ship(ship)
        player.add_ship(ship2)
        player.add_ship(ship3)

        player.kill_ship(ship2)

        player.reset()
        self.assertEqual(player.ships, [])

    # Tests the reset method for wins
    def test_reset3(self):
        player = fy.Players("Player")
        ship = fy.Ship("Ship", 1, [])
        ship2 = fy.Ship("Ship2", 1, [])
        ship3 = fy.Ship("Ship3", 1, [])

        player.add_ship(ship)
        player.add_ship(ship2)
        player.add_ship(ship3)

        player.kill_ship(ship2)

        player.add_win()

        player.reset()
        self.assertEqual(player.get_wins(), 1)


class MiscFunctionality(unittest.TestCase):
    # Tests the hit_check method with a missed shot
    def test_hit_check_miss(self):
        player = fy.Players("Player")
        ship = fy.Ship("Ship", 1, [(1, 2)])

        player.add_ship(ship)
        hit, kill = fy.hit_check(1, 1, player)
        self.assertFalse(hit)
        self.assertFalse(kill)

    # Tests the hit_check method with a shot that hits and kills
    def test_hit_check_hit_kill(self):
        player = fy.Players("Player")
        ship = fy.Ship("Ship", 1, [(1, 2)])

        player.add_ship(ship)
        hit, kill = fy.hit_check(1, 2, player)
        self.assertTrue(hit)
        self.assertTrue(kill)

    # Tests the hit_check method with a shot that hits but does not kill
    def test_hit_check_hit_no_kill(self):
        player = fy.Players("Player")
        ship = fy.Ship("Ship", 2, [(1, 2), (2, 2)])

        player.add_ship(ship)
        hit, kill = fy.hit_check(1, 2, player)
        self.assertTrue(hit)
        self.assertFalse(kill)

    # Tests the overlap method with two ships that do not overlap
    def test_overlap_pass(self):
        player = fy.Players("Player")
        ship = fy.Ship("Ship", 2, [(1, 2), (2, 2)])
        ship2 = fy.Ship("Ship2", 3, [(5, 2), (6, 2), (7, 2)])

        player.add_ship(ship)
        self.assertFalse(fy.overlap(ship2, player))

    # Tests the overlap method with two ships overlap in first position
    def test_overlap_fail1(self):
        player = fy.Players("Player")
        ship = fy.Ship("Ship", 2, [(1, 2), (2, 2)])
        ship2 = fy.Ship("Ship2", 3, [(1, 2), (2, 1), (3, 1)])

        player.add_ship(ship)
        self.assertTrue(fy.overlap(ship2, player))

    # Tests the overlap method with two ships overlap in second position
    def test_overlap_fail2(self):
        player = fy.Players("Player")
        ship = fy.Ship("Ship", 2, [(1, 2), (2, 2)])
        ship2 = fy.Ship("Ship2", 3, [(2, 1), (2, 2), (2, 3)])

        player.add_ship(ship)
        self.assertTrue(fy.overlap(ship2, player))

    # Tests the overlap method with two ships overlap in different positions
    def test_overlap_fail3(self):
        player = fy.Players("Player")
        ship = fy.Ship("Ship", 2, [(1, 2), (2, 2)])
        ship2 = fy.Ship("Ship2", 3, [(4, 2), (3, 2), (2, 2)])

        player.add_ship(ship)
        self.assertTrue(fy.overlap(ship2, player))

    # Tests building a ship with no offset. First to see if it exists
    def test_build_ship1(self):
        ship = fy.build_ship("Ship", 1, 0)

        self.assertIsInstance(ship, fy.Ship)

    # Tests building a ship with no offset. Now some features of the ship
    def test_build_ship2(self):
        ship = fy.build_ship("Ship", 3, 0)

        self.assertEqual(ship.get_health(), 3)
        self.assertEqual(len(ship.coordinates), 3)

    # Tests building a ship with offset. First to see if it exists
    def test_build_ship3(self):
        ship = fy.build_ship("Ship", 1, 11)

        self.assertIsInstance(ship, fy.Ship)

    # Tests building a ship with offset. Now some features of the ship
    def test_build_ship4(self):
        ship = fy.build_ship("Ship", 3, 11)

        self.assertEqual(ship.get_health(), 3)
        self.assertEqual(len(ship.coordinates), 3)

    # Tests building a ship with offset.
    # Make sure the x coordinates are between 0 and 9
    # Make sure the y coordinates are between 1 and 10
    def test_build_ship_coord(self):
        ship = fy.build_ship("Ship", 1, 0)

        x, y = ship.coordinates[0]

        self.assertTrue(0 <= x <= 9)
        self.assertTrue(1 <= y <= 10)

    # Tests building a ship with offset. Make sure the x coordinates are between 11 and 20
    def test_build_ship_coord_offset(self):
        ship = fy.build_ship("Ship", 1, 11)

        x, y = ship.coordinates[0]

        self.assertTrue(11 <= x <= 20)
        self.assertTrue(1 <= y <= 10)

    # Tests create_ship method
    def test_create_ship(self):
        player = fy.Players("Player")

        self.assertIsNotNone(player.ships)


class TestAutoPlayers(unittest.TestCase):

    # Tests auto player creation
    def test_auto_player_creation(self):
        player = fy.AutoPlayers("Player", "Random")

        self.assertIsInstance(player, fy.AutoPlayers)

    # Tests auto player strategy
    def test_auto_player_strat(self):
        player = fy.AutoPlayers("Player", "Random")

        self.assertEqual(player.get_strategy(), "Random")

    # Tests auto player name
    def test_auto_player_name(self):
        player = fy.AutoPlayers("Player", "Random")

        self.assertEqual(player.name, "Player")


if __name__ == '__main__':
    unittest.main()
