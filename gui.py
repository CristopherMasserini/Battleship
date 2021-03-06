import tkinter

# First is some set up and creation of functions to be used for ease
# In the building of the user interface


# Returns what state the buttons should be for relief and highlight.
# Initially, relief = raised and color = blue.
# If button is hit and a miss (state_all == miss), it will be sunken and green.
# If button is hit and a hit on a hit (state_all == hit), it will be sunken and red.
def button_state_all(state_all: str) -> tuple:
    if state_all == "initial":
        return "raised", "blue",
    elif state_all == "miss":
        return "sunken", "green"
    elif state_all == "hit":
        return "sunken", "red"


# Creates the player boards
def player_boards():
    # Creates left player board. Buttons should be clicked to "attack" enemy ships.
    # # If a button is clicked where a ship is, should turn red and the ship take damage/be destroyed
    relief, color = button_state_all("initial")
    left_frame = tkinter.Frame(mainWindow, relief="sunken")
    left_frame.grid(row=1, column=0, sticky="nsew", columnspan=10, rowspan=10)
    for x in range(0, 10):
        for y in range(1, 11):
            missile_button = tkinter.Button(mainWindow,
                                            text=f"({x},{y})", relief=relief, highlightbackground=color,
                                            state="disabled")
            missile_button.grid(row=y, column=x, sticky="nsew")

    # Creates right player board. Buttons should be clicked to "attack" enemy ships.
    # If a button is clicked where a ship is, should turn red and the ship take damage/be destroyed
    right_frame = tkinter.Frame(mainWindow, relief="sunken", borderwidth=1)
    right_frame.grid(row=1, column=11, sticky="nsew", columnspan=10, rowspan=10)
    for x in range(11, 21):
        for y in range(1, 11):
            missile_button = tkinter.Button(mainWindow,
                                            text=f"({x},{y})", relief=relief, highlightbackground=color,
                                            state="disabled")
            missile_button.grid(row=y, column=x, sticky="nsew")


# Creation of the user interface
mainWindow = tkinter.Tk()
mainWindow.title("Battleship")
mainWindow.geometry("1280x960-8-200")

# Configure the columns and the rows
for i in range(0, 22):
    mainWindow.columnconfigure(i, weight=1)
for i in range(0, 11):
    mainWindow.rowconfigure(i, weight=1)

# Adds name of the game on the top row.
label = tkinter.Label(mainWindow)
label.grid(row=0, column=10)

# Creates the separating frame between the two players boards
# This is where the interaction is located
separating_frame = tkinter.Frame(mainWindow, relief="raised", borderwidth=1, background="gray")
separating_frame.grid(row=1, column=10, sticky="nsew", columnspan=1, rowspan=10)

# Creates the entry to enter the column and row where one wants to fire
resultLabel = tkinter.Label(mainWindow, text="             Column to attack \t Row to attack", bg="gray", anchor="w")
resultLabel.grid(row=4, column=10, sticky="new")
resultFrame = tkinter.Label(mainWindow)
resultFrame.grid(row=4, column=10, sticky="sew")
resultCol = tkinter.Entry(resultFrame)
resultRow = tkinter.Entry(resultFrame)
resultCol.pack(side="left")
resultRow.pack(side="right")


# Creates the label to show the number of ships left for player one and player two
def score_box(p1_score: tuple, p2_score: tuple, p1_name: str, p2_name: str):
    p1_alive, p1_dead = p1_score
    p2_alive, p2_dead = p2_score

    p1_score_box = tkinter.Label(mainWindow, text=f"Ships for {p1_name}\nAlive:{p1_alive}    Dead:{p1_dead}")
    p1_score_box.grid(row=0, column=3, sticky="nsew", columnspan=4)

    p2_score_box = tkinter.Label(mainWindow, text=f"Ships for {p2_name}\nAlive:{p2_alive}    Dead:{p2_dead}")
    p2_score_box.grid(row=0, column=14, sticky="nsew", columnspan=4)


# Adds a quit button to quit game
def quit_game():
    quit_button = tkinter.Button(mainWindow, text="Quit", command=mainWindow.destroy)
    quit_button.grid(row=10, column=10, sticky="nsew")


# Adds a label clearly stating who won
def wins_label(p1_wins: int, p2_wins: int, p1_name: str, p2_name: str):
    wins_board = tkinter.Label(mainWindow, text=f"Games won\n\n{p1_name}: {p1_wins}\n{p2_name}: {p2_wins}",
                               relief="raised", bg="black", fg="white")
    wins_board.grid(row=1, column=10, rowspan=2, sticky="nsew")


# Adds a label clearly stating if it was a hit or miss
def shot_label(shot: str):
    if shot == 'hit':
        shot_sign = tkinter.Label(mainWindow, text=f"You hit a ship!", relief="raised", bg="red", fg="black")
        shot_sign.grid(row=7, column=10, rowspan=2, sticky="nsew")
    elif shot == 'kill':
        shot_sign = tkinter.Label(mainWindow, text=f"You destroyed a ship!", relief="raised", bg="black", fg="white")
        shot_sign.grid(row=7, column=10, rowspan=2, sticky="nsew")
    elif shot == "miss":
        shot_sign = tkinter.Label(mainWindow, text=f"You missed!", relief="raised", bg="green", fg="black")
        shot_sign.grid(row=7, column=10, rowspan=2, sticky="nsew")
    else:
        win = tkinter.Label(mainWindow, text=f"{shot} won the game!", relief="raised", bg="yellow", fg="black")
        win.grid(row=7, column=10, rowspan=2, sticky="nsew")


# Builds the screen
def set_up():
    mainWindow.mainloop()


if __name__ == "__main__":
    set_up()
