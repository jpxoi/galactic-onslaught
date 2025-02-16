"""
Galactic Onslaught - Menu Handler Module
Author: Jean Paul Fernandez
Date: 2023-11-24
Version: 1.0
Language: Python 3.11.2
IDE: Visual Studio Code 1.84.2
Development Platform: MacOs Sonoma 14.1

Description:
This module contains the start menu class, which represents the start menu of the game.
The start menu contains the main menu, game instructions, and game credits. The start menu
also allows the player to choose the playing keys and enter their player name. The start
menu is displayed when the game is launched.

Implementation:
The menu handler module is imported by the main game module. The start menu class is
instantiated in the main game module and is used to display the start menu. The start
menu class is also used to retrieve the chosen playing keys and player name.
"""

# Import modules
import constants
from tkinter import Canvas, PhotoImage, Entry, Button, StringVar, Radiobutton

class StartMenu:
    """
    The StartMenu class represents the start menu of the game,
    which contains the main menu, game instructions, and game credits.
    """

    def __init__(self, master, start_game_callback):
        # Store the root window as an instance variable
        self.master = master

        # Set the title and geometry of the root window
        self.master.title(constants.GAME_TITLE)
        self.master.resizable(False, False)
        self.create_window()

        self.start_game_callback = start_game_callback

        # Calculate the center of the canvas and store it as instance variables
        center_x = constants.GAME_WIDTH // 2
        center_y = constants.GAME_HEIGHT // 2

        # Default playing keys
        self.playing_keys = StringVar(value="arrows")

        # Create and pack the start menu canvas
        self.start_menu_canvas = Canvas(
            master,
            bg="#171717",
            width=constants.GAME_WIDTH,
            height=constants.GAME_HEIGHT)

        self.start_menu_canvas.pack()

        # Load and store the button images as instance variables
        self.keys_image = PhotoImage(file="")
        self.keys_sel_image = PhotoImage(file="")
        self.button_image = PhotoImage(file="")

        # Load and store the background image for the start menu
        self.background_image = PhotoImage(file="assets/img/bg/background-dark.png")
        # Background graphic made by me (Jean Paul Fernandez) using Canva's image editor [https://www.canva.com].
        # Additional graphics made by Rostik Solonenko, retrieved from Canva's free media library [https://www.canva.com/features/free-stock-photos/].
        # Editable file available as view-only at https://www.canva.com/design/DAF0EFDjc3g/cApy-RMGI9pTI6kQi9Xrmg/edit.

        # Create the background image for the start menu
        self.bg_image = self.start_menu_canvas.create_image(
            center_x,
            center_y,
            anchor="center",
            image=self.background_image)

        # Create start menu title
        self.create_text(
            center_x,
            center_y - 350,
            constants.GAME_TITLE.upper(),
            constants.GAME_LARGE_FONT_BOLD,
            constants.GAME_FONT_COLOR)

        # Create the input field for the player name
        self.create_input_field(
            center_x,
            center_y - 290,
            "Enter your player name:",
            constants.GAME_SMALL_FONT,
            constants.GAME_FONT_COLOR)

        # Create the new game and quit buttons
        self.create_button(
            center_x - 200,
            center_y - 190,
            "New Game",
            self.start_game,
            "w",
            "new-game-button")

        self.create_button(
            center_x + 200,
            center_y - 190,
            "Quit",
            self.master.destroy,
            "e",
            "quit-button")
        # Button images made by PixelChoice, retrieved from Canva's free media library [https://www.canva.com/features/free-stock-photos/].

        # Create the labels for the playing keys options selector
        self.create_text(
            center_x,
            center_y - 100,
            "Choose Space Fighter Controls:",
            constants.GAME_SMALL_FONT_BOLD,
            constants.GAME_FONT_COLOR)

        # Create the radio buttons for the playing key options (Arrow Keys and WASD Keys)
        self.create_radio_button(
            center_x - 100,
            center_y - 10,
            "Arrow Keys",
            "arrows",
            "arrow-keys")

        self.create_radio_button(
            center_x + 100,
            center_y - 10,
            "WASD Keys",
            "wasd",
            "wasd-keys")
        # Playing keys graphics made by Yuliia Duliakova, retrieved from Canva's free media library [https://www.canva.com/features/free-stock-photos/].

        # Create the game instructions title
        self.create_text(
            center_x,
            center_y + 110,
            "Game Controls:",
            constants.GAME_SMALL_FONT_BOLD,
            constants.GAME_FONT_COLOR)

        # Create the game instructions
        self.create_text(
            center_x,
            center_y + 160,
            "Press Spacebar to shoot",
            constants.GAME_SMALL_FONT,
            constants.GAME_FONT_COLOR)

        self.create_text(
            center_x,
            center_y + 200,
            "Press P to pause the game",
            constants.GAME_SMALL_FONT,
            constants.GAME_FONT_COLOR)

        self.create_text(
            center_x,
            center_y + 240,
            "Press Ctrl+Shift+B to minimize the game",
            constants.GAME_SMALL_FONT,
            constants.GAME_FONT_COLOR)

        # Create the game credits and version
        self.create_text(
            center_x,
            center_y + 325,
            "Game developed by Jean Paul Fernandez",
            constants.GAME_SMALLEST_FONT,
            constants.GAME_FONT_COLOR)

        self.create_text(
            center_x,
            center_y + 350,
            "Version 1.0",
            constants.GAME_SMALLEST_FONT,
            constants.GAME_FONT_COLOR)

        # Set focus to the canvas
        self.start_menu_canvas.focus_set()

    def create_window(self):
        """Create the window for the game."""
        # Get the screen width and height
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        # Calculate the x and y coordinates for the Tkinter window
        x = (screen_width - constants.GAME_WIDTH) // 2
        y = (screen_height - constants.GAME_HEIGHT) // 2

        # Set the window's position
        self.master.geometry(f"{constants.GAME_WIDTH}x{constants.GAME_HEIGHT}+{x}+{y}")

    def create_text(self, x, y, text, font, color):
        """Create a text on the canvas."""
        self.start_menu_canvas.create_text(
            x,
            y,
            text=text,
            font=font,
            fill=color,
            anchor="center")

    def create_button(self, x, y, text, command, anchor="center", image=""):
        """Create a button on the canvas."""
        self.button_image = PhotoImage(file=f"assets/img/btn/{image}.png")

        button = Button(
            self.start_menu_canvas,
            text=text, command=command,
            font=(constants.GAME_SMALL_FONT),
            bg="white",
            fg="black",
            activebackground="white",
            activeforeground="black",
            relief="flat",
            highlightthickness = 0,
            bd = 0,
            image=self.button_image)

        # Retain a reference to the image to prevent it from being garbage collected
        button.image = self.button_image

        self.start_menu_canvas.create_window(x, y, window=button, anchor=anchor)

    def create_radio_button(self, x, y, text, value, image):
        """Create a radio button on the canvas."""
        self.keys_image = PhotoImage(file=f"assets/img/btn/{image}.png")
        self.keys_sel_image = PhotoImage(file=f"assets/img/btn/{image}-sel.png")

        radiobutton = Radiobutton(
            self.start_menu_canvas,
            text=text,
            variable=self.playing_keys,
            value=value,
            font=(constants.GAME_SMALL_FONT),
            fg=constants.GAME_FONT_COLOR,
            indicatoron=0,
            relief="flat",
            bd=0,
            image=self.keys_image,
            selectimage=self.keys_sel_image)

        # Retain a reference to the image to prevent it from being garbage collected
        radiobutton.image = self.keys_image
        radiobutton.selectimage = self.keys_sel_image

        self.start_menu_canvas.create_window(x, y, window=radiobutton, anchor="center")

    def create_input_field(self, x, y, text, font, color):
        """Create an input field on the canvas."""
        self.start_menu_canvas.create_text(x, y, text=text, font=font, fill=color, anchor="center")

        # Create an input variable to store the input value
        self.input_var = StringVar()

        self.input_field = Entry(
            self.start_menu_canvas,
            textvariable=self.input_var,
            font=(constants.GAME_SMALL_FONT),
            bg="#171717",
            fg="#FFF",
            highlightcolor="#FFF",
            highlightthickness=1,
            bd=0)

        self.start_menu_canvas.create_window(x, y + 40, window=self.input_field, anchor="center")

    def start_game(self, load_game=False):
        """Start the game."""
        # Remove start menu elements
        self.start_menu_canvas.destroy()

        if load_game:
            # Retrieve the chosen playing keys
            chosen_keys = self.playing_keys.get()
            player_name = ""
            # Load the game
            self.start_game_callback(chosen_keys, player_name, "load")
            return

        # Retrieve the chosen playing keys
        chosen_keys = self.playing_keys.get()

        # Retrieve the player name
        player_name = self.input_var.get()

        # Validate the player name and set it to a default value if invalid
        if player_name == "":
            player_name = "Player01"

        # Remove leading, middle and trailing whitespaces
        else:
            player_name = player_name.capitalize()
            player_name = player_name.replace(" ", "")

            # Add leading zeroes if the player name is less than the minimum length
            if len(player_name) < constants.PLAYER_NAME_MIN_LENGTH:
                player_name = player_name + "0" * (
                    constants.PLAYER_NAME_MIN_LENGTH - len(player_name))

            # Truncate the player name if it exceeds the maximum length
            elif len(player_name) > constants.PLAYER_NAME_MAX_LENGTH:
                player_name = player_name[:constants.PLAYER_NAME_MAX_LENGTH]

        # Start the game
        self.start_game_callback(chosen_keys, player_name)
