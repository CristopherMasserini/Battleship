import strategies as strat
import functionality as fy
import pandas as pd


# Builds the ships for the players
def build_player_ships(player_a: fy.AutoPlayers, player_b: fy.AutoPlayers, ships: int):
    offset = 11
    for j in range(2, ships + 2):
        ship_name_a = "Ship" + str(i) + "A"
        ship_name_b = "Ship" + str(i) + "B"

        fy.create_ship(player_a, ship_name_a, j, 0)
        fy.create_ship(player_b, ship_name_b, j, offset)


# Checks if someone lost the game
def lost(player: fy.AutoPlayers) -> bool:
    alive, dead = player.get_score()
    return alive == 0


# Adds some of the stats used in the analysis
# player is the winning player
def add_stats(player: fy.AutoPlayers, ships: int):
    turns_list.append(turns_a)
    _, dead = player.get_score()
    ratio_list.append(dead/ships)
    win_strat_list.append(player.get_strategy())


# Plays the automated game until someone wins
def play(player_a: fy.AutoPlayers, player_b: fy.AutoPlayers, ships: int):
    global turns_a
    global turns_b
    global turns_list

    build_player_ships(player_a, player_b, ships)
    player_turn = "a"

    # Bounds for the player to shoot
    player_a_bounds = (11, 20, 1, 10)
    player_b_bounds = (0, 9, 1, 10)

    player_a_prev = "Miss"
    player_b_prev = "Miss"

    player_a_list_to_use = list()
    player_b_list_to_use = list()

    # Shoots a shot, based off strategy. Checks if the shot is a hit, then checks if the other player lost.
    # If the other player lost, winning players turns get added to turns list
    # The ratio of ships alive to total ships of the winning player gets added to ratio list
    while True:
        if player_turn == "a":
            first = player_a.get_init_hit()
            second = player_a.get_second_hit()

            if first:

                if not second:
                    player_a_list_to_use = player_a.around_init_hit()
                elif second and player_a_prev == 'Hit':
                    player_a_list_to_use = player_a.second_hit_direction()
                elif second and player_a_prev == 'Miss':
                    player_a_list_to_use = player_a.second_hit_anti_direction()
                    player_a.set_direction_list(player_a_list_to_use)

            x, y = strat.strategy_choose(player_a.get_strategy(), player_a_bounds, player_a_list_to_use)

            h, k = fy.hit_check(x, y, player_b)

            if h and not k:
                player_a_prev = "Hit"
                if not first:
                    player_a.an_init_hit((x, y))
                if first and not second:
                    player_a.a_second_hit((x, y))
            elif k:
                player_a_prev = "Miss"
                player_a.reset_auto()
                player_a_list_to_use = list()
            else:
                player_a_prev = "Miss"

            if lost(player_b):
                add_stats(player_a, ships)
                break

            player_turn = "b"

        else:
            first = player_b.get_init_hit()
            second = player_b.get_second_hit()

            if first:

                if not second:
                    player_b_list_to_use = player_b.around_init_hit()
                elif second and player_b_prev == 'Hit':
                    player_b_list_to_use = player_b.second_hit_direction()
                elif second and player_b_prev == 'Miss':
                    player_b_list_to_use = player_b.second_hit_anti_direction()

            x, y = strat.strategy_choose(player_b.get_strategy(), player_b_bounds, player_b_list_to_use)

            h, k = fy.hit_check(x, y, player_a)

            if h and not k:
                player_b_prev = "Hit"
                if not first:
                    player_b.an_init_hit((x, y))
                if first and not second:
                    player_b.a_second_hit((x, y))
            elif h and k:
                player_b_prev = "Miss"
                player_b.reset_auto()
                player_b_list_to_use = list()
            else:
                player_b_prev = "Miss"

            if lost(player_a):
                add_stats(player_b, ships)
                break

            player_turn = "a"

    # Resets these values so for bookkeeping
    turns_a = 0
    turns_b = 0
    strat.coordinates_shot = list()


if __name__ == "__main__":
    # turns is used to get the number of turns it took for the winning player to win.
    # turns_list records the turns for all the games
    # Note: the losing player would either be 0 or 1 turn off the winner
    turns_a = 0
    turns_b = 0
    turns_list = list()
    ratio_list = list()
    win_strat_list = list()

    # ship_num = int(input("Please input number of ships: "))
    # p1_name = input("Please input Player 1's name: ")
    # p1_strat = input("Please input Player 1's strategy \n (Random, Blanket, Smart random, Smart odd): ")
    # p2_name = input("Please input Player 2's name: ")
    # p2_strat = input("Please input Player 2's strategy \n (Random, Blanket, Smart random, Smart odd): ")
    # iterations = int(input("Please input number of iterations: "))

    # Todo delete this part, uncomment above after everything works
    # Standard for analysis is 5 ships, 250 iterations
    ship_num = 5
    p1_name = "A"
    p1_strat = "Smart random"
    p2_name = "B"
    p2_strat = "Smart random"
    iterations = 1

    player1 = fy.AutoPlayers(p1_name, p1_strat)
    player2 = fy.AutoPlayers(p2_name, p2_strat)

    data = dict()

    # Calls play for a certain number of times, used to get statistics
    for s in range(1, ship_num + 1):
        for i in range(0, iterations):
            play(player1, player2, s)
            player1.reset()
            player2.reset()

        data[f"{s}_ship(s)_turns"] = turns_list
        data[f"{s}_ship(s)_loser_ratio"] = ratio_list
        data[f"{s}_ship(s)_win_strategy"] = win_strat_list
        turns_list = list()
        ratio_list = list()
        win_strat_list = list()

    df = pd.DataFrame(data)
    print(df)
    # df.to_csv(rf'{p1_strat}_vs_{p2_strat}.csv', index=False)
