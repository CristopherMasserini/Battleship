import functionality as fy


# Check if a player lost. If so, a new screen pops up stating that the other player won.
def check_lost(player: fy.Players):
    # The method looks for a player who lost, therefore this if statement just gives the player who won
    # is obviously the other player in the game
    if player == player1:
        play_won = player2
    else:
        play_won = player1

    # Calls the gui to create a box for the winning player
    if not player.ships:
        # Covers the shoot button until new game is given
        cover_shoot_button = gui.tkinter.Button(gui.mainWindow, relief="sunken",
                                                state="disabled", highlightbackground="gray")
        cover_shoot_button.grid(row=5, column=10, sticky="nsew")
        play_won.add_win()
        gui.wins_label(player1.get_wins(), player2.get_wins(), player1.name, player2.name)
        gui.shot_label(play_won.name)


# When the shoot button is pressed, this creates a new, deactivated, button on top of the shot
# With the correct coloring at that position
def shot(column: int, row: int):
    try:
        column_num = int(column)
        row_num = int(row)
    except ValueError:  # Catches if the value given is not a number
        return None
    # Decides which players ships to look through
    if 0 <= column_num < 10:
        player = player1
    else:
        player = player2

    # Creating the button to to show if a hit or miss
    if 0 <= column_num <= 20 and 1 <= row_num <= 10 and column_num != 10:
        hit, kill = fy.hit_check(column_num, row_num, player)
        if hit:
            relief_new, color_new = gui.button_state_all("hit")
            # Updating the score box if the shot results in a kill
            if player == player1:
                gui.score_box(player.get_score(), player2.get_score(), player1.name, player2.name)
            else:
                gui.score_box(player1.get_score(), player.get_score(), player1.name, player2.name)

            if kill:
                gui.shot_label("kill")
            else:
                gui.shot_label("hit")
        else:
            relief_new, color_new = gui.button_state_all("miss")
            gui.shot_label("miss")

        # Adding the button so that it shows if the shot hit or missed
        hit_button = gui.tkinter.Button(gui.mainWindow,
                                        text=f"({column},{row})", highlightbackground=color_new, relief=relief_new,
                                        state="disabled")
        hit_button.grid(row=row, column=column, sticky="nsew")

        # Resetting the entry widgets to be blank
        gui.resultRow.delete(0, 'end')
        gui.resultCol.delete(0, 'end')

    check_lost(player)


def new_game():
    gui.quit_game()
    gui.mainWindow.quit()
    player1.reset()
    player2.reset()
    play(player1, player2, ship_num)
    gui.set_up()


# Plays the game for the two players and set number of ships
# Player B is on the right hand side of the screen, hence the offset.
def play(player_a, player_b, ships):
    gui.player_boards()

    # Creates and puts the shoot button on the grid
    shoot_button = gui.tkinter.Button(gui.mainWindow, text=f"Shoot!", relief="raised",
                                      state="active", highlightbackground="red",
                                      command=lambda: shot(gui.resultCol.get(), gui.resultRow.get()))
    shoot_button.grid(row=5, column=10, sticky="nsew")

    # Creates a new game button
    new_game_button = gui.tkinter.Button(gui.mainWindow, text="New Game",
                                         command=new_game)
    new_game_button.grid(row=9, column=10, sticky="nsew")

    # Offset used for ship creation on correct side of the screen
    offset = 11
    for i in range(2, ships + 2):
        ship_name_a = "Ship" + str(i) + "A"
        ship_name_b = "Ship" + str(i) + "B"

        fy.create_ship(player_a, ship_name_a, i, 0)
        fy.create_ship(player_b, ship_name_b, i, offset)

    gui.score_box(player_a.get_score(), player_b.get_score(), player1.name, player2.name)
    gui.wins_label(player1.get_wins(), player2.get_wins(), player1.name, player2.name)


if __name__ == "__main__":
    ship_num = int(input("Please input number of ships: "))
    p1 = input("Please input Player 1's name: ")
    p2 = input("Please input Player 2's name: ")
    import gui
    gui.quit_game()
    player1 = fy.Players(p1)
    player2 = fy.Players(p2)
    play(player1, player2, ship_num)
    gui.set_up()
