"""
Galactic Onslaught is a 2D space shooter game inspired by the classic arcade game Space Invaders.
The player controls a space fighter and must destroy waves of alien ships.
The player wins the game by destroying all the alien ships.
The player loses the game if the player runs out of lives.

Author: Jean Paul Fernandez
Date: 2023-11-24

This game contains the following classes:
    - StartMenu: The StartMenu class represents the start menu of the game.
    - Game: The Game class represents the game window and its contents.
    - SpaceFighter: The SpaceFighter class represents the space fighter in the game.
    - AlienShip: The AlienShip class represents the alien ship in the game.
    - Laser: The Laser class represents the laser beams in the game.
"""

from tkinter import Tk, Canvas, PhotoImage, Entry, Button, StringVar, Radiobutton
import random
import math
import time
import constants
from leaderboard import LeaderboardManager

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
        self.master.geometry(f"{constants.GAME_WIDTH}x{constants.GAME_HEIGHT}+0+0")
        self.start_game_callback = start_game_callback

        # Calculate the center of the canvas and store it as instance variables
        center_x = constants.GAME_WIDTH // 2
        center_y = constants.GAME_HEIGHT // 2

        # Default playing keys
        self.playing_keys = StringVar(value="arrows")

        # Create and pack the start menu canvas
        self.start_menu_canvas = Canvas(
            master,
            bg="black",
            width=constants.GAME_WIDTH,
            height=constants.GAME_HEIGHT)

        self.start_menu_canvas.pack()

        # Load and store the button images as instance variables
        self.keys_image = PhotoImage(file="")
        self.keys_sel_image = PhotoImage(file="")
        self.button_image = PhotoImage(file="")

        # Load and store the background image for the start menu
        self.background_image = PhotoImage(file="assets/img/background.png")
        # Background graphic made by me (Jean Paul Fernandez) using Canva's image editor [https://www.canva.com].
        # Additional graphics made by Rostik Solonenko, retrieved from Canva's free media library [https://www.canva.com/features/free-stock-photos/].
        # Editable file available as view-only at https://www.canva.com/design/DAF0EFDjc3g/cApy-RMGI9pTI6kQi9Xrmg/edit.

        # Create the background image for the start menu
        self.bg_image = self.start_menu_canvas.create_image(
            center_x,
            center_y,
            anchor="center",
            image=self.background_image)

        # Create start menu elements
        self.create_text(
            center_x,
            center_y - 350,
            constants.GAME_TITLE,
            constants.GAME_LARGE_FONT_BOLD,
            constants.GAME_FONT_COLOR)

        self.create_input_field(
            center_x,
            center_y - 280,
            "Enter your player name:",
            constants.GAME_SMALL_FONT,
            constants.GAME_FONT_COLOR)

        # Create the main buttons
        self.create_button(
            center_x - 300,
            center_y - 175,
            "Resume Game",
            self.start_game,
            "w",
            "resume-button")

        self.create_button(
            center_x + 30,
            center_y - 175,
            "New Game",
            self.start_game,
            "center",
            "new-game-button")

        self.create_button(
            center_x + 300,
            center_y - 175,
            "Quit",
            self.master.destroy,
            "e",
            "quit-button")
        # Button images made by PixelChoice, retrieved from Canva's free media library [https://www.canva.com/features/free-stock-photos/].

        # Create the radio buttons for choosing the playing keys
        self.create_text(
            center_x,
            center_y - 75,
            "Choose Space Fighter Controls:",
            constants.GAME_SMALL_FONT_BOLD,
            constants.GAME_FONT_COLOR)

        self.create_radio_button(
            center_x - 100,
            center_y + 25,
            "Arrow Keys",
            "arrows",
            "arrow-keys")

        self.create_radio_button(
            center_x + 100,
            center_y + 25,
            "WASD Keys",
            "wasd",
            "wasd-keys")
        # Playing keys graphics made by Yuliia Duliakova, retrieved from Canva's free media library [https://www.canva.com/features/free-stock-photos/].

        # Create the game instructions
        self.create_text(
            center_x,
            center_y + 150,
            "Game Controls:",
            constants.GAME_MEDIUM_FONT_BOLD,
            constants.GAME_FONT_COLOR)

        self.create_text(
            center_x,
            center_y + 200,
            "Press Spacebar to shoot",
            constants.GAME_SMALL_FONT,
            constants.GAME_FONT_COLOR)

        self.create_text(
            center_x,
            center_y + 250,
            "Press B to minimize the game",
            constants.GAME_SMALL_FONT,
            constants.GAME_FONT_COLOR)

        # Create the game credits
        self.create_text(
            center_x,
            center_y + 350,
            "Game developed by Jean Paul Fernandez",
            constants.GAME_SMALLEST_FONT,
            constants.GAME_FONT_COLOR)


        # Set focus to the canvas
        self.start_menu_canvas.focus_set()

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
        self.button_image = PhotoImage(file=f"assets/img/{image}.png")

        button = Button(
            self.start_menu_canvas,
            text=text, command=command,
            font=(constants.GAME_SMALL_FONT),
            bg="white", fg="black",
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
        self.keys_image = PhotoImage(file=f"assets/img/{image}.png")
        self.keys_sel_image = PhotoImage(file=f"assets/img/{image}-sel.png")

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

    def start_game(self):
        """Start the game."""
        # Remove start menu elements
        self.start_menu_canvas.destroy()

        # Retrieve the chosen playing keys
        chosen_keys = self.playing_keys.get()

        # Retrieve the player name and remove spaces
        player_name = self.input_var.get()

        if player_name == "":
            player_name = "Player01"
        else:
            player_name = player_name.replace(" ", "")

        # Start the game
        self.start_game_callback(chosen_keys, player_name)

class Game:
    """
    The Game class represents the game window and its contents.
    It manages the game loop and the game elements.
    The game loop updates the game every frame.
    """
    def __init__(self, master, playing_keys, player_name):
        # Store the root window as an instance variable
        self.master = master

        # Set the title and geometry of the root window
        self.master.title(constants.GAME_TITLE)
        self.master.geometry(f"{constants.GAME_WIDTH}x{constants.GAME_HEIGHT}+0+0")

        # Create and pack the canvas widget and pack it to the root window
        self.canvas = Canvas(
            master,
            bg="black",
            width=constants.GAME_WIDTH,
            height=constants.GAME_HEIGHT)

        self.canvas.pack()

        # Define game variables
        self.player_name = player_name
        self.score = 0
        self.lives = 3
        self.paused = False
        self.level = 0
        self.game_over_status = False

        # Load and store the background image as an instance variable
        self.background_image = PhotoImage(file="assets/img/background.png")
        # Background graphic made by me (Jean Paul Fernandez) using Canva's image editor [https://www.canva.com].
        # Additional graphics made by Rostik Solonenko, retrieved from Canva's free media library [https://www.canva.com/features/free-stock-photos/].
        # Editable file available as view-only at https://www.canva.com/design/DAF0EFDjc3g/cApy-RMGI9pTI6kQi9Xrmg/edit.

        # Create two background images for seamless scrolling
        self.bg_image_1 = self.canvas.create_image(
            0,
            0,
            anchor="nw",
            image=self.background_image)

        self.bg_image_2 = self.canvas.create_image(
            0,
            -constants.GAME_HEIGHT,
            anchor="nw",
            image=self.background_image)

        # Store the alien ships in an array
        self.alien_ships = []
        self.wave_length = 0
        self.alien_ship_speed = 0

        # Create the alien ship
        for self.alien_ship in self.alien_ships:
            self.alien_ship = AlienShip(self.canvas, self.alien_ship_speed)

        # Create the space fighter
        self.space_fighter = SpaceFighter(self.canvas, playing_keys)

        # Create the score label on the canvas
        self.score_label = self.canvas.create_text(
            constants.GAME_WIDTH - 20, 30,
            text=f"Score: {self.score}",
            fill=constants.GAME_FONT_COLOR,
            font=(constants.GAME_SMALL_FONT),
            anchor="e",
            tag="score")

        # Create the lives label on the canvas
        self.lives_label = self.canvas.create_text(
            constants.GAME_WIDTH - 20, 70,
            text=f"Lives: {self.lives}",
            fill=constants.GAME_FONT_COLOR,
            font=(constants.GAME_SMALL_FONT),
            anchor="e",
            tag="lives")

        # Create a leaderboard manager
        self.leaderboard_manager = LeaderboardManager("leaderboard.txt")

        # Bind the key events to the corresponding methods
        self.canvas.bind("<B>", self.boss_key)
        self.canvas.bind("<b>", self.boss_key)

        # Set focus to the canvas
        self.canvas.focus_set()

        # Start the clock
        self.clock()

    def boss_key(self, event):
        """The boss_key method minimizes the game window."""
        self.master.iconify() # Minimize the game window

    def clock(self):
        """The clock method updates the game every frame."""
        # Check if the game is not yet over or paused
        if not self.game_over_status or not self.paused:
            # Update the screen
            self.update_screen()

            # Check if the player has destroyed an alien ship
            if len(self.alien_ships) == 0:
                self.level_up()

            self.check_collisions()

        self.master.after(1000 // constants.GAME_SPEED, self.clock)

    def check_collisions(self):
        """The check_collisions method checks for collisions between game elements."""
        # Check if the player has been hit by an alien laser
        for alien_ship in self.alien_ships:
            for alien_laser in alien_ship.alien_lasers:
                if self.pixel_collision(
                    self.space_fighter.x,
                    self.space_fighter.y,
                    self.space_fighter.space_fighter_sprites[self.space_fighter.current_sprite],
                    alien_laser.x,
                    alien_laser.y,
                    alien_laser.laser_sprites[alien_laser.current_sprite]):

                    if self.space_fighter.current_sprite == "main":
                        self.lives -= 1 # Decrement the lives by 1
                        self.update_lives() # Update the lives label on the canvas

                    alien_ship.alien_lasers.remove(alien_laser) # Remove the alien laser

        # Check if the player has been hit by an alien ship
        for alien_ship in self.alien_ships:
            if self.pixel_collision(
                self.space_fighter.x,
                self.space_fighter.y,
                self.space_fighter.space_fighter_sprites[self.space_fighter.current_sprite],
                alien_ship.x,
                alien_ship.y,
                alien_ship.alien_ship_sprites[alien_ship.current_sprite]):

                if self.space_fighter.current_sprite == "main":
                    self.lives -= 1 # Decrement the lives by 1
                    self.update_lives()

                if self.space_fighter.current_sprite == "super":
                    self.update_score()

                alien_ship.destroyed_animation() # Play the destroyed animation

                # Remove the alien ship from the alien_ships array
                if alien_ship in self.alien_ships:
                    self.alien_ships.remove(alien_ship)

        # Check if the alien ship has been hit by a laser
        for alien_ship in self.alien_ships:
            for laser in self.space_fighter.lasers:
                if self.pixel_collision(
                    alien_ship.x,
                    alien_ship.y,
                    alien_ship.alien_ship_sprites[alien_ship.current_sprite],
                    laser.x,
                    laser.y,
                    laser.laser_sprites[laser.current_sprite]):
                    self.update_score() # Update the score label on the canvas

                    alien_ship.destroyed_animation() # Play the destroyed animation

                    # Remove the alien ship from the alien_ships array
                    if alien_ship in self.alien_ships:
                        self.alien_ships.remove(alien_ship)

                    # Remove the laser from the lasers array
                    if laser in self.space_fighter.lasers:
                        self.space_fighter.lasers.remove(laser)

    def update_screen(self):
        """The update_screen method updates the game every clock tick."""
        self.scroll_background(self.alien_ship_speed // 2)

        # Move the lasers
        self.space_fighter.move_lasers()

        # Move the alien ship and handle shooting
        for alien_ship in self.alien_ships:
            alien_ship.move()
            alien_ship.move_lasers()

    def update_score(self):
        """The update_score method updates the score of the player."""
        self.score += 1 # Increment the score by 1

        # Update the score label on the canvas
        self.canvas.itemconfig(self.score_label, text=f"Score: {self.score}")

    def update_lives(self):
        """The update_lives method updates the lives of the player."""
        # Update the lives label on the canvas
        self.canvas.itemconfig(self.lives_label, text=f"Lives: {self.lives}")

        # Check if the player has no more lives
        if self.lives <= 0:
            self.game_over() # End the game

    def level_up(self):
        """The level_up method levels up the game and spawns more alien ships."""
        self.level += 1 # Increment the level by 1
        self.wave_length = int(self.level**0.7) + 2 # Calculate the wave length
        self.alien_ship_speed = int(self.level**0.6) + 1 # Calculate the alien ship speed
        self.space_fighter.speed = int(self.level**0.6)+14 # Calculate the space fighter speed

        if self.lives < 3:
            self.lives += 1 # Increment the lives by 1

        # Print the level up message on the canvas
        self.canvas.create_text(
            constants.GAME_WIDTH // 2,
            constants.GAME_HEIGHT // 2,
            text=f"LEVEL {self.level}",
            fill=constants.GAME_FONT_COLOR,
            font=(constants.GAME_LARGE_FONT_BOLD),
            anchor="center",
            tag="level_up")

        # Spawn the alien ships for the next wave
        for _ in range(self.wave_length):
            enemy = AlienShip(self.canvas, self.alien_ship_speed)
            self.alien_ships.append(enemy)

        self.canvas.after(3000, self.remove_level_up_message)

    def remove_level_up_message(self):
        """The remove_level_up method removes the level up message from the canvas."""
        self.canvas.delete("level_up")

    def game_over(self):
        """The game_over method stops the game and prints the game over screen."""
        self.game_over_status = True

        # Create the game over label on the canvas
        self.canvas.create_text(
            constants.GAME_WIDTH // 2,
            constants.GAME_HEIGHT // 2,
            text="GAME OVER",
            fill=constants.GAME_FONT_COLOR,
            font=(constants.GAME_LARGE_FONT_BOLD),
            anchor="center",
            tag="game_over")

        # Stop the game
        self.stop_game()

        # Update the leaderboard
        self.update_leaderboard()

    def stop_game(self):
        """The stop_game method stops the game."""
        # Set the paused status to True
        self.paused = True

        # Stop and remove the space fighter
        self.space_fighter.speed = 0
        self.space_fighter.remove_space_fighter()

        # Stop and remove the alien ships
        for alien_ship in self.alien_ships:
            alien_ship.speed = 0
            alien_ship.remove_alien_ship()

            # Stop and remove the alien lasers
            for alien_laser in alien_ship.alien_lasers:
                alien_laser.speed = 0
                if alien_laser in alien_ship.alien_lasers:
                    alien_ship.alien_lasers.remove(alien_laser)

    def update_leaderboard(self):
        """The update_leaderboard method updates the leaderboard."""

        # Read the leaderboard
        leaderboard = self.leaderboard_manager.read_leaderboard()
        player_exists = False

        for entry in leaderboard:
            # Check if the player exists in the leaderboard
            if entry["playerName"] == self.player_name:
                player_exists = True
                if self.score > entry["score"]:
                    self.leaderboard_manager.update_leaderboard(
                        {"playerName": self.player_name,
                        "score": self.score})
                    break
                break

        # If the player does not exist in the leaderboard, append the player to the leaderboard
        if not player_exists:
            new_leaderboard_entry = {"playerName": self.player_name, "score": self.score}
            self.leaderboard_manager.append_leaderboard(new_leaderboard_entry)

        # After updating the leaderboard, wait 3 seconds before printing it
        self.canvas.after(3000, self.print_leaderboard)

    def print_leaderboard(self):
        """The print_leaderboard method prints the leaderboard."""

        # Clear the canvas, except for the background images
        self.canvas.delete("score")
        self.canvas.delete("lives")
        self.canvas.delete("game_over")
        self.space_fighter.remove_space_fighter()

        # Read and sort the leaderboard
        leaderboard = self.leaderboard_manager.read_leaderboard()
        sorted_leaderboard = self.leaderboard_manager.sort_leaderboard(leaderboard)

        # Print Leaderboard on a table
        self.canvas.create_rectangle(
            constants.GAME_WIDTH // 2 - 200,
            constants.GAME_HEIGHT // 2 - 300,
            constants.GAME_WIDTH // 2 + 200,
            constants.GAME_HEIGHT // 2 + 300,
            outline=constants.GAME_FONT_COLOR,
            width=3,
            tag="leaderboard-table",
            dash=(5, 9)
        )

        # Create the leaderboard title on the canvas
        self.canvas.create_text(
            constants.GAME_WIDTH // 2,
            constants.GAME_HEIGHT // 2 - 350,
            text="LEADERBOARD",
            fill=constants.GAME_FONT_COLOR,
            font=(constants.GAME_LARGE_FONT_BOLD),
            anchor="center",
            tag="leaderboard-title")

        # Create the leaderboard table headers on the canvas
        self.canvas.create_text(
            constants.GAME_WIDTH // 2 - 125,
            constants.GAME_HEIGHT // 2 - 250,
            text="Rank",
            fill=constants.GAME_FONT_COLOR,
            font=(constants.GAME_SMALL_FONT_BOLD),
            anchor="center",
            tag="leaderboard-rank")

        self.canvas.create_text(
            constants.GAME_WIDTH // 2 - 50,
            constants.GAME_HEIGHT // 2 - 250,
            text="Name",
            fill=constants.GAME_FONT_COLOR,
            font=(constants.GAME_SMALL_FONT_BOLD),
            anchor="w",
            tag="leaderboard-name")

        self.canvas.create_text(
            constants.GAME_WIDTH // 2 + 125,
            constants.GAME_HEIGHT // 2 - 250,
            text="Score",
            fill=constants.GAME_FONT_COLOR,
            font=(constants.GAME_SMALL_FONT_BOLD),
            anchor="center",
            tag="leaderboard-score")

        # Create the leaderboard entries on the canvas
        for i, entry in enumerate(sorted_leaderboard):
            if entry["playerName"] == self.player_name:
                font_size = constants.GAME_SMALL_FONT_BOLD
                font_color = constants.GAME_FONT_COLOR_SUCCESS
            else:
                font_size = constants.GAME_SMALL_FONT
                font_color = constants.GAME_FONT_COLOR

            self.canvas.create_text(
                constants.GAME_WIDTH // 2 - 125,
                constants.GAME_HEIGHT // 2 - 200 + (i * 50),
                text=f"{i + 1}",
                fill=font_color,
                font=(font_size),
                anchor="center",
                tag="leaderboard-entry-rank")

            self.canvas.create_text(
                constants.GAME_WIDTH // 2 - 50,
                constants.GAME_HEIGHT // 2 - 200 + (i * 50),
                text=f"{entry['playerName']}",
                fill=font_color,
                font=(font_size),
                anchor="w",
                tag="leaderboard-entry-name")

            self.canvas.create_text(
                constants.GAME_WIDTH // 2 + 125,
                constants.GAME_HEIGHT // 2 - 200 + (i * 50),
                text=f"{entry['score']}",
                fill=font_color,
                font=(font_size),
                anchor="center",
                tag="leaderboard-entry-score")

        # Create the return to Menu label on the canvas
        self.canvas.create_text(
            constants.GAME_WIDTH // 2,
            constants.GAME_HEIGHT - 100,
            text="Press R to return to Menu",
            fill=constants.GAME_FONT_COLOR,
            font=(constants.GAME_SMALL_FONT),
            anchor="center",
            tag="return_to_menu")

        # Bind the key events to the corresponding methods
        self.canvas.bind("<R>", self.return_to_menu)
        self.canvas.bind("<r>", self.return_to_menu)

    def return_to_menu(self):
        """The return_to_menu method returns to the start menu."""
        # Destroy the canvas
        self.canvas.destroy()

    def scroll_background(self, speed):
        """The scroll_background method scrolls the background images vertically."""
        self.canvas.move(self.bg_image_1, 0, speed)
        self.canvas.move(self.bg_image_2, 0, speed)

        # The bbox method returns a tuple containing the coordinates of the specified item.
        # We just need the y coordinates of the background images.
        _, y1, _, _ = self.canvas.bbox(self.bg_image_1)
        _, y2, _, _ = self.canvas.bbox(self.bg_image_2)

        # Check if the first background image is out of the canvas
        if y1 >= constants.GAME_HEIGHT:
            # Reset its position above the second background image
            self.canvas.move(self.bg_image_1, 0, -2 * constants.GAME_HEIGHT)

        # Check if the second background image is out of the canvas
        if y2 >= constants.GAME_HEIGHT:
            # Reset its position above the first background image
            self.canvas.move(self.bg_image_2, 0, -2 * constants.GAME_HEIGHT)

    def pixel_collision(self, x1, y1, image1, x2, y2, image2):
        """The pixel_collision method checks if two images collide comparing its RGB values."""
        # Get the overlapping rectangle coordinates
        x_overlap = max(int(x1), int(x2))
        y_overlap = max(int(y1), int(y2))
        x_end = min(int(x1) + image1.width(), int(x2) + image2.width())
        y_end = min(int(y1) + image1.height(), int(y2) + image2.height())

        # Check for overlap within the rectangle
        for x in range(int(x_overlap), int(x_end)):
            for y in range(int(y_overlap), int(y_end)):
                # Get pixel values (RGBA) - handle the case where images are PhotoImage objects
                pixel1 = image1.get(x - int(x1), y - int(y1))
                pixel2 = image2.get(x - int(x2), y - int(y2))

                print(f"pixel1: {pixel1}, pixel2: {pixel2}")

                # Check if both pixels are
                if pixel1 != (0, 0, 0) and pixel2 != (0, 0, 0):
                    print("Collision detected")
                    return True  # Collision detected

        return False  # No collision

class SpaceFighter:
    """
    The SpaceFighter class represents the space fighter in the game.
    It manages the movement and shooting of the space fighter.
    """
    # Define the constructor method of the SpaceFighter class
    def __init__(self, canvas, playing_keys):
        self.canvas = canvas

        # Set the initial position of the space fighter
        self.x = constants.GAME_WIDTH // 2
        self.y = constants.GAME_HEIGHT - 90

        # Load and store the space fighter sprites as a dictionary
        self.space_fighter_sprites = {
            "main": PhotoImage(file="assets/img/space-fighter-main.png"),
            "super": PhotoImage(file="assets/img/space-fighter-super.png")
            # Sprites generated using Canva's AI image generator Magic Media [https://www.canva.com/ai-image-generator/]
            # Input prompt "3D 4K Animated and Futuristic Space Fighter. 2D view from the top of it. Place it on a black background."
            # Background removed using Canva's Magic Studio [https://www.canva.com/magic/].
            # Further modifications made using Canva's image editor [https://canva.com].
            # Editable file available as view-only at https://www.canva.com/design/DAF0D65NA5U/6-y7e9e_xXZK_j7Iaaq5TQ/edit.
        }

        # Properties of the space fighter
        self.current_sprite = "main"
        self.speed = 0
        self.width = 150
        self.height = 150

        # Create the space fighter
        self.create_space_fighter()

        # Create a list to store the lasers
        self.lasers = []

        # Bind the key events to the corresponding methods
        if playing_keys == "arrows":
            self.canvas.bind("<Left>", self.move_left)
            self.canvas.bind("<Right>", self.move_right)
            self.canvas.bind("<Up>", self.move_up)
            self.canvas.bind("<Down>", self.move_down)

        elif playing_keys == "wasd":
            # Uppercase
            self.canvas.bind("<A>", self.move_left)
            self.canvas.bind("<D>", self.move_right)
            self.canvas.bind("<W>", self.move_up)
            self.canvas.bind("<S>", self.move_down)

            # Lowercase
            self.canvas.bind("<a>", self.move_left)
            self.canvas.bind("<d>", self.move_right)
            self.canvas.bind("<w>", self.move_up)
            self.canvas.bind("<s>", self.move_down)

        self.canvas.bind("<F>", self.update_sprite)
        self.canvas.bind("<space>", self.shoot)

    def create_space_fighter(self):
        """The create_space_fighter method creates the space fighter on the canvas."""
        self.space_fighter_image = self.canvas.create_image(
            self.x,
            self.y,
            anchor="center",
            image=self.space_fighter_sprites[self.current_sprite])

    def update_sprite(self, event):
        """The update_sprite method updates the sprite of the space fighter."""

        # Check if the space fighter is in its main sprite
        if self.current_sprite == "main":
            # Change the sprite of the space fighter to super
            self.current_sprite = "super"

            self.canvas.itemconfig(
                self.space_fighter_image,
                image=self.space_fighter_sprites[self.current_sprite])

        # Check if the space fighter is in its super sprite
        elif self.current_sprite == "super":
            # Change the sprite of the space fighter to main
            self.current_sprite = "main"

            self.canvas.itemconfig(
                self.space_fighter_image,
                image=self.space_fighter_sprites[self.current_sprite])

        self.canvas.focus_set()

    def move_left(self, event):
        """The move_left method moves the space fighter to the left."""

        # Check if the space fighter is not yet at the leftmost part of the canvas
        if self.x > self.width / 2 + 15:
            self.x -= self.speed
            self.update_position(event)

    def move_right(self, event):
        """The move_right method moves the space fighter to the right."""

        # Check if the space fighter is not yet at the rightmost part of the canvas
        if self.x < constants.GAME_WIDTH - (self.width / 2 + 15):
            self.x += self.speed
            self.update_position(event)

    def move_up(self, event):
        """The move_up method moves the space fighter upwards."""

        # Check if the space fighter is not yet at the top limit of the game
        if self.y > self.height / 2 + 400:
            self.y -= self.speed
            self.update_position(event)

    def move_down(self, event):
        """The move_down method moves the space fighter downwards."""

        # Check if the space fighter is not yet at the bottommost part of the canvas
        if self.y < constants.GAME_HEIGHT - (self.height / 2 + 15):
            self.y += self.speed
            self.update_position(event)

    def update_position(self, event):
        """The update_position method updates the position of the space fighter on the canvas."""
        self.canvas.coords(self.space_fighter_image, self.x, self.y)

    def shoot(self, event):
        """The shoot method shoots a laser from the space fighter."""

        # Create a laser at the current position of the space fighter
        laser = Laser(self.canvas, self.x, self.y - 40, self.speed - 5, "up", "main")

        # Add the laser to the list of lasers
        self.lasers.append(laser)

    def move_lasers(self):
        """The move_lasers method moves the lasers in the list of lasers."""

        for laser in self.lasers:
            laser.move()

            # Remove the laser if it goes beyond the top of the canvas
            if laser.off_screen(0):
                self.lasers.remove(laser)

    def remove_space_fighter(self):
        """The remove_space_fighter method removes the space fighter from the canvas."""
        self.canvas.delete(self.space_fighter_image)

class AlienShip:
    """
    The AlienShip class represents the alien ship in the game.
    It manages the movement and shooting of the alien ship.
    A new wave of alien ships is created every time the player
    destroys an alien ship wave.
    """
    def __init__(self, canvas, speed):
        self.canvas = canvas

        # Set the initial position of the alien ship
        self.x = 0
        self.y = 0

        self.alien_ship_sprites = {
            "main": PhotoImage(file="assets/img/alien-ship-main.png"),
            "destroyed": PhotoImage(file="assets/img/alien-ship-destroyed.png"),
            "explosion": PhotoImage(file="assets/img/alien-ship-explosion.png")
            # Sprites generated using Canva's AI image generator Magic Media [https://www.canva.com/ai-image-generator/]
            # Input prompt "3D Cartoon 4K Animated and Futuristic Alien UFO. 2D view from the top of it. Place it on a black background."
            # Background removed using Canva's Magic Studio [https://www.canva.com/magic/].
            # Additional graphic "Cosmic explosion orange" Anna Kuz on Canva's free media library [https://www.canva.com/features/free-stock-photos/].
            # Further modifications made using Canva's image editor [https://canva.com].
            # Editable file available as view-only at https://www.canva.com/design/DAF0GJfd7jU/PrEOAQ9Z_rp3vRWcLYkN3Q/edit
        }

        # Properties of the alien ship
        self.current_sprite = "main"
        self.speed = speed
        self.width = 100
        self.height = 100

        # Create the alien ship
        self.create_alien_ship()

        # Properties for shooting lasers
        self.alien_lasers = []
        self.shoot_delay = 5000
        self.last_shot_time = 0

    def create_alien_ship(self):
        """The create_alien_ship method creates the alien ship on the canvas."""

        # Set the initial position of the alien ship randomly
        self.x = random.randint(75, constants.GAME_WIDTH - 75)
        self.y = random.randint(-900, 0)

        # Display the alien ship on the canvas and store it as an instance variable
        self.alien_ship_image = self.canvas.create_image(
            self.x,
            self.y,
            anchor="center",
            image=self.alien_ship_sprites[self.current_sprite])

    def move(self):
        """The move method moves the alien ship downwards."""

        # Move the alien ship downwards
        self.y += self.speed
        self.x += 2 * math.sin(self.y / 50)

        self.update_position()

        # Remove the alien ship if it goes beyond the bottom of the canvas
        if self.off_screen(constants.GAME_HEIGHT):
            self.destroyed_animation()

            # Update the lives of the player
            game.lives -= 1
            game.update_lives()

            # Remove the alien ship from the alien_ships array
            if self in game.alien_ships:
                game.alien_ships.remove(self)

        current_time = time.time() * 1000  # Convert to milliseconds

        # Check if it's time for the alien to shoot a laser
        if current_time - self.last_shot_time > self.shoot_delay and self.y > 0:
            self.shoot()
            self.last_shot_time = current_time

    def update_position(self):
        """The update_position method updates the position of the alien ship on the canvas."""
        self.canvas.coords(self.alien_ship_image, self.x, self.y)

    def shoot(self):
        """The shoot method shoots a laser from the alien ship."""

        # Create a laser at the current position of the alien ship
        alien_laser = Laser(self.canvas, self.x, self.y + 40, self.speed + 3, "down", "alt")

        self.alien_lasers.append(alien_laser)

    def move_lasers(self):
        """The move_lasers method moves the lasers in the list of lasers."""
        for alien_laser in self.alien_lasers:
            alien_laser.move()

            # Remove the laser if it goes beyond the bottom of the canvas
            if alien_laser.off_screen(constants.GAME_HEIGHT):
                self.alien_lasers.remove(alien_laser)

    def off_screen(self, height):
        """The off_screen method checks if the alien ship is off the screen."""
        return self.y >= height

    def destroyed_animation(self):
        """The destroyed_animation method animates the explosion of the alien ship."""

        # Stop the alien ship from moving
        self.speed = 0

        # Change the sprite of the alien ship to destroyed
        self.current_sprite = "destroyed"
        self.canvas.itemconfig(
            self.alien_ship_image,
            image=self.alien_ship_sprites[self.current_sprite])

        # Animate the explosion of the alien ship
        self.canvas.after(200, self.explosion_animation)

    def explosion_animation(self):
        """The explosion_animation method animates the explosion of the alien ship."""

        # Change the sprite of the alien ship to explosion
        self.current_sprite = "explosion"
        self.canvas.itemconfig(
            self.alien_ship_image,
            image=self.alien_ship_sprites[self.current_sprite])

        # Remove the alien ship after 200 milliseconds
        self.canvas.after(200, self.remove_alien_ship)

    def remove_alien_ship(self):
        """The remove_alien_ship method removes the alien ship from the canvas."""
        self.canvas.delete(self.alien_ship_image)

class Laser:
    """
    The Laser class represents the laser beam in the game.
    It manages the movement of the laser beam.
    It can be shot from the space fighter or the alien ship.
    """
    def __init__(self, canvas, x, y, speed = 10, direction = "up", sprite = "main"):
        self.canvas = canvas

        # Set the initial position of the laser
        self.x = x
        self.y = y

        # Speed and direction of the laser
        self.speed = speed
        self.direction = direction

        # Load and store the laser image as an instance variable
        self.laser_sprites = {
            "main": PhotoImage(file="assets/img/laser-beam.png"),
            "alt": PhotoImage(file="assets/img/laser-beam-alt.png")
        }
        # Laser graphic made by me (Jean Paul Fernandez) using Adobe Photoshop [https://adobe.com/products/photoshop/].

        # Properties of the laser
        self.current_sprite = sprite
        self.laser_image = self.laser_sprites[self.current_sprite]

        # Display the laser on the canvas and store it as an instance variable
        self.laser_beam = self.canvas.create_image(
            self.x,
            self.y,
            anchor="center",
            image=self.laser_image)

    # Define the move method to move the laser upwards
    def move(self):
        """The move method moves the laser beam upwards or downwards."""

        if self.direction == "up":
            self.y -= self.speed
        elif self.direction == "down":
            self.y += self.speed

        # Update the position of the laser on the canvas
        self.canvas.coords(self.laser_beam, self.x, self.y)

    def off_screen(self, height):
        """The off_screen method checks if the laser is off the screen."""
        if self.direction == "up":
            return self.y <= height

        if self.direction == "down":
            return self.y >= height

        return None

if __name__ == "__main__":
    def start_game(playing_keys, player_name):
        """The start_game function that starts a the game."""
        global game
        root.title(constants.GAME_TITLE)
        game = Game(root, playing_keys, player_name)

    root = Tk()
    start_menu = StartMenu(root, start_game)
    root.mainloop()
