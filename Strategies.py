import random

# A file that contains different strategies for the automation of the game.
# This is done so later on there can be an analysis of the different strategies.

# List of the coordinates being used to shoot  # Todo make sure this stays general for mixed strategies
coordinates_shot = list()


# Checks if the location has been fired upon
def check_shot(x: int, y: int) -> bool:
    global coordinates_shot
    return (x, y) in coordinates_shot


# If an x and y coordinate is valid (in the bounds and not shot before)
def valid_coordinate(coord: tuple, bounds: tuple) -> bool:
    x, y = coord
    x_min, x_max, y_min, y_max = bounds
    if x_min <= x <= x_max and y_min <= y <= y_max and not check_shot(x, y):
        return True
    else:
        return False


# This ensures that all the random shots are "odd" parts of the board, think a checkers board.
# If this was used by itself, all ships would be hit, because no ship is of length one, but no ship would be killed
# This is used in tandem with the smart random fire so that if there is a hit, the player will be able to kill the ship
# True if the shot should be fired
def check_odd(coord: tuple) -> bool:
    x, y = coord
    return (x + y) % 2 == 1


# This strategy is a completely random firing, checking if the position was already fired upon, chooses a new location
# Bounds are the x and y bounds of the board for the random shot
# Returns the x and y location of the shot
def random_fire(bounds: tuple) -> tuple:
    x_min, x_max, y_min, y_max = bounds

    while True:
        x = random.randint(x_min, x_max)
        y = random.randint(y_min, y_max)
        if not check_shot(x, y):
            coordinates_shot.append((x, y))
            return x, y


# This strategy is to start at the minimum x and y bounds,
# Goes across the x's, drops one y than goes back across the x's. Done until all coordinates in each row is fired upon.
# Bounds are the x and y bounds of the board for the random shot
# Note: Do not have to check for y going past its limit. By the time the very last coordinate is hit, all the ships
# have to be destroyed
# Returns the x and y location of the shot
def blanket_fire(bounds: tuple) -> tuple:
    x_min, x_max, y_min, y_max = bounds

    # Where to put the next shot
    # If first condition is true. Determines where to go based off length of the coordinates shot list.
    if len(coordinates_shot) <= 1:
        coordinates_shot.append((x_min, y_min))
        return x_min, y_min
    else:
        x_prev, y_prev = coordinates_shot[len(coordinates_shot) - 2]
        if (x_prev + 1) <= x_max:
            coordinates_shot.append(((x_prev + 1), y_prev))
            return (x_prev + 1), y_prev
        else:
            coordinates_shot.append((x_min, (y_prev + 1)))
            return x_min, y_prev + 1


# This strategy is to randomly choose a location to shoot at until there is a hit.
# Once there is a hit, to shoot once on each side of the hit until there is another hit.
# Once there is the second hit, follow that direction until a kill.
# If there is a miss before the kill, need to go back to the original hit and go in the opposite direction until kill.
# Returns the x and y location of the shot
# Todo test
def smart_random_fire(bounds: tuple, fire_list: list) -> tuple:
    if len(fire_list) == 0:
        return random_fire(bounds)
    else:
        while True:
            try:
                x, y = fire_list.pop(0)
            except IndexError:
                return random_fire(bounds)

            if valid_coordinate((x, y), bounds):
                coordinates_shot.append((x, y))
                return x, y


# This strategy is to randomly choose a location to shoot at until there is a hit, but only for "odd" coordinates.
# Once there is a hit, to shoot once on each side of the hit until there is another hit.
# Once there is the second hit, follow that direction until a kill.
# If there is a miss before the kill, need to go back to the original hit and go in the opposite direction until kill.
# Returns the x and y location of the shot
# Todo test
def smart_random_odd_fire(bounds: tuple, fire_list: list) -> tuple:
    if len(fire_list) == 0:
        coord = random_fire(bounds)
        test = check_odd(coord)
        index = 1
        while not test:
            coord = random_fire(bounds)
            test = check_odd(coord)
        coordinates_shot.append(coord)
        return coord
    else:
        while True:
            try:
                x, y = fire_list.pop(0)
                if valid_coordinate((x, y), bounds):
                    coordinates_shot.append((x, y))
                    return x, y
            except IndexError:
                while not test:
                    coord = random_fire(bounds)
                    test = check_odd(coord)
                coordinates_shot.append(coord)
                return coord


# Takes the strategy from the player and picks the right function to use for shooting
# strat is the strategy, bounds are the x and y bounds for the firing functions
# Returns the x and y location of the shot # Todo test new strategies
def strategy_choose(strat: str, bounds: tuple, fire_list: list) -> tuple:
    if strat == "Random":
        return random_fire(bounds)
    elif strat == "Blanket":
        return blanket_fire(bounds)
    elif strat == "Smart random":
        return smart_random_fire(bounds, fire_list)
    elif strat == "Smart odd":
        return smart_random_odd_fire(bounds, fire_list)


if __name__ == "__main__":
    pass
