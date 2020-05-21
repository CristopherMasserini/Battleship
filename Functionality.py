import random


class Ship(object):
    """
    Creates a class for the ships of the battleship game

    Keeps track of the name of the ship, the length of the ship, health of the ship, the x and y coordinates
    as well as the orientation

    name (str): The name of the ship
    length (int): The length of the ship. Between 2 and 5 for ease of gaming
    health (int): The health of the ship. Initially the length of the ship
    coordinates (list of tuples): coordinates the ship is located in as: [(x1, y1), (x2, y2), ...]
    """
    def __init__(self, name, length, coordinates):
        self._name = name
        self._length = length
        self._health = length
        self.coordinates = coordinates
        self._alive = True

    # Gets if the ship is alive
    def get_alive(self) -> bool:
        return self._alive

    # Gets the ships health
    def get_health(self) -> int:
        return self._health

    # A method for the ship to take damage
    # If the health drops to zero, the ship is dead
    def take_damage(self) -> bool:
        self._health -= 1
        if self._health == 0:
            self._alive = False
        return self.get_alive()


class Players(object):
    """
    Creates a class for the players of the battleship game

    Keeps track of the name of the player, as well as the number of ships that are alive and dead

    name (str): The name of the player
    """
    def __init__(self, name):
        self.name = name
        self.ships = list()  # List of ships under the control of the player
        self._alive = 0  # Number of ships that are alive
        self._dead = 0  # Number of ships that are dead
        self._wins = 0  # Number of wins a player has in one run of the program

    # Resets the variables
    def reset(self):
        self.ships = list()
        self._alive = 0
        self._dead = 0

    # A method to kill a ship from the players list of ships
    def kill_ship(self, ship: Ship):
        self.ships.remove(ship)
        self._alive -= 1
        self._dead += 1

    # A method to add a ship to the players list of ships
    def add_ship(self, ship: Ship):
        self.ships.append(ship)
        self._alive += 1

    # Returns the number of living and dead ships
    def get_score(self) -> tuple:
        return self._alive, self._dead

    # Returns the number of wins
    def get_wins(self) -> int:
        return self._wins

    # Adds one to the win
    def add_win(self):
        self._wins += 1


class AutoPlayers(Players):  # Todo finish testing and edit to fit now
    """
    Creates a class for the automated players. A subclass of Players

    name (str): The name of the player
    strategy (str): The strategy the player is following
    init_hit (tuple): The location of an initial hit on a ship
    second_hit (tuple): The location of the second hit on a ship
    direction_list (list): A list of potential next coordinates in the direction from initial hit to second hit
    anti_direction_list (list):
        A list of potential next coordinates in the opposite direction from initial hit to second hit
    """
    def __init__(self, name, strategy):
        super().__init__(name=name)
        self._strategy = strategy
        self._init_hit = tuple()
        self._second_hit = tuple()
        self._direction_list = list()
        self._anti_direction_list = list()

    # Gets the players strategy
    def get_strategy(self) -> str:
        return self._strategy

    # Resets the variables
    def reset_auto(self):
        self._init_hit = tuple()
        self._second_hit = tuple()
        self._direction_list = list()
        self._anti_direction_list = list()

    # Add an initial hit
    def an_init_hit(self, coord: tuple):
        self._init_hit = coord

    # Get the initial hit
    def get_init_hit(self) -> tuple:
        return self._init_hit

    # Add a second hit
    def a_second_hit(self, coord: tuple):
        self._second_hit = coord

    # Get the second hit
    def get_second_hit(self) -> tuple:
        return self._second_hit

    # Get the direction list
    def get_direction_list(self) -> list:
        return self._direction_list

    # set the direction list
    def set_direction_list(self, new_list: list):
        self._direction_list = new_list

    # Get the anti direction list
    def get_anti_direction_list(self) -> list:
        return self._anti_direction_list

    # Resets hits list
    def a_kill(self):
        self._init_hit = tuple()
        self._second_hit = tuple()
        self._direction_list = list()
        self._anti_direction_list = list()

    # creates a list to go around the initial hit coordinates
    def around_init_hit(self) -> list:
        x_hit, y_hit = self._init_hit

        x_left = x_hit - 1
        x_right = x_hit + 1
        y_up = y_hit - 1
        y_down = y_hit + 1

        return [(x_left, y_hit), (x_right, y_hit), (x_hit, y_up), (x_hit, y_down)]

    # Develops list of coordinates to fire upon for smart fire strategy.
    # Does not care if it is valid. That check is done in strategy
    def second_hit_direction(self) -> list:
        x_hit1, y_hit1 = self._init_hit
        x_hit2, y_hit2 = self._second_hit
        dif_x = x_hit2 - x_hit1
        dif_y = y_hit2 - y_hit1

        if dif_x != 0:
            return [(x_hit2 + dif_x, y_hit1), (x_hit2 + (2 * dif_x), y_hit1), (x_hit2 + (3 * dif_x), y_hit1)]
        elif dif_y != 0:
            return [(x_hit1, y_hit2 + dif_y), (x_hit1, y_hit2 + (2 * dif_y)), (x_hit1, y_hit2 + (3 * dif_y))]

    # Develops list of coordinates to fire upon for smart fire strategy.
    # Does not care if it is valid. That check is done in strategy
    def second_hit_anti_direction(self) -> list:
        x_hit1, y_hit1 = self._init_hit
        x_hit2, y_hit2 = self._second_hit
        dif_x = x_hit1 - x_hit2
        dif_y = y_hit1 - y_hit2

        if dif_x != 0:
            return [(x_hit1 + dif_x, y_hit1), (x_hit1 + (2 * dif_x), y_hit1), (x_hit1 + (3 * dif_x), y_hit1)]
        elif dif_y != 0:
            return [(x_hit1, y_hit1 + dif_y), (x_hit1, y_hit1 + (2 * dif_y)), (x_hit1, y_hit1 + (3 * dif_y))]


# Creates a new ship with a name and length
# Offset is used for the creation of players ship on the right hand side of the screen
# Offset should be set to zero for player on left hand side
def build_ship(name: str, length: int, offset: int) -> Ship:
    coord = list()  # Coordinates of the ship
    orient1 = random.randint(0, 1)  # 0 = horizontal or 1 = vertical
    orient2 = random.randint(0, 1)  # 0 is up/right, 1 is down/left based off of first orient
    if orient1 == 0 and orient2 == 0:  # Horizontal and right
        x = random.randint(0, 10 - length) + offset
        y = random.randint(1, 10)
        pos = (x, y)  # Position of the tip of the ship
        coord.append(pos)
        for i in range(1, length):  # Creates the coordinates for the rest of the ship based off orientation
            x += 1
            pos_next = (x, y)
            coord.append(pos_next)
    elif orient1 == 0 and orient2 == 1:  # Horizontal and left
        x = random.randint(length - 1, 9) + offset
        y = random.randint(1, 10)
        pos = (x, y)  # Position of the tip of the ship
        coord.append(pos)
        for i in range(1, length):  # Creates the coordinates for the rest of the ship based off orientation
            x -= 1
            pos_next = (x, y)
            coord.append(pos_next)
    elif orient1 == 1 and orient2 == 0:  # vertical and up. Up meaning an increase in the y, which is physically down
        x = random.randint(0, 9) + offset
        y = random.randint(1, (10 - length) + 1)
        pos = (x, y)  # Position of the tip of the ship
        coord.append(pos)
        for i in range(1, length):  # Creates the coordinates for the rest of the ship based off orientation
            y += 1
            pos_next = (x, y)
            coord.append(pos_next)
    else:  # orient1 = 1, orient2 = 1, vertical and down. Down meaning a decrease in the y, which is physically up
        x = random.randint(0, 9) + offset
        y = random.randint(length, 10)
        pos = (x, y)  # Position of the tip of the ship
        coord.append(pos)
        for i in range(1, length):  # Creates the coordinates for the rest of the ship based off orientation
            y -= 1
            pos_next = (x, y)
            coord.append(pos_next)

    return Ship(name, length, coord)


# Creates a function that will test if a ship is overlapping another for that player
# Returns true if there is an overlap, false if not
def overlap(ship_check: Ship, player: Players) -> bool:
    ship_list = player.ships
    for ship in ship_list:
        for coord in ship_check.coordinates:
            if coord in ship.coordinates:
                return True
    return False


# A function that will add a ship to a given player of given length and name.
# Offset is used for creating ships on correct side of the screen. See build_ship
def create_ship(player: Players, name: str, length_of_ship: int, offset: int):
    ship_new = build_ship(name, length_of_ship, offset)
    while True:
        if overlap(ship_new, player):
            ship_new = build_ship(name, length_of_ship, offset)
        else:
            break
    player.add_ship(ship_new)


# Checks if there is a ship at the location given by the column and row
# Returns True if hit, False if miss
def hit_check(column: int, row: int, player: Players) -> tuple:
    hit = False
    kill = False
    coord = (column, row)
    ship_list = player.ships
    for ship in ship_list:
        if coord in ship.coordinates:
            ship_alive = ship.take_damage()
            hit = True
            if not ship_alive:
                player.kill_ship(ship)
                kill = True
            return hit, kill
    return hit, kill


if __name__ == "__main__":
    pass
