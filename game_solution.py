"""
Generate new docstring
"""

from tkinter import Tk, Canvas, PhotoImage
import os
import sys
import random
import math
import time
import constants
from leaderboard import LeaderboardManager
from menu_handler import StartMenu

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
        self.master.resizable(False, False)
        self.create_window()

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
        self.scroll_speed = 0
        self.playing_keys = playing_keys

        # Load and store the background image as an instance variable
        self.background_image = PhotoImage(file="assets/img/bg/background.png")
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
        if len(self.alien_ships) >= 0:
            for self.alien_ship in self.alien_ships:
                self.alien_ship = AlienShip(self.canvas, self.alien_ship_speed)

        # Create the space fighter
        self.space_fighter = SpaceFighter(self.canvas, playing_keys)

        # Create the player name label on the canvas
        self.canvas.create_text(
            20,
            30,
            text=f"Player: {self.player_name}",
            fill=constants.GAME_FONT_COLOR,
            font=(constants.GAME_SMALL_FONT),
            anchor="w",
            tag="player_name")

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
            constants.GAME_WIDTH - 20,
            70,
            text=f"Lives: {self.lives}",
            fill=constants.GAME_FONT_COLOR,
            font=(constants.GAME_SMALL_FONT),
            anchor="e",
            tag="lives")

        # Draw the lives bar on the canvas
        self.draw_lives_bar()

        # Create a leaderboard manager
        self.leaderboard_manager = LeaderboardManager("assets/db/leaderboard.txt")

        # Bind the key events to the corresponding methods
        self.canvas.bind("<B>", self.boss_key)
        self.canvas.bind("<b>", self.boss_key)
        self.canvas.bind("<P>", self.pause_resume_game)
        self.canvas.bind("<p>", self.pause_resume_game)

        # Set focus to the canvas
        self.canvas.focus_set()

        # Start the clock
        self.clock()

    def clock(self):
        """The clock method updates the game every frame."""
        # Check if the game is not yet over or paused
        if not self.game_over_status:
            self.scroll_speed = self.alien_ship_speed // 2
            self.update_screen()

            # Check if the player has destroyed an alien ship
            if len(self.alien_ships) == 0:
                self.level_up()

            self.check_collisions()

        self.master.after(1000 // constants.GAME_SPEED, self.clock)

    def create_window(self):
        """Create the game window."""
        # Get the screen width and height
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        # Calculate the x and y coordinates for the Tkinter window
        x = (screen_width - constants.GAME_WIDTH) // 2
        y = (screen_height - constants.GAME_HEIGHT) // 2

        # Set the window's position
        self.master.geometry(f"{constants.GAME_WIDTH}x{constants.GAME_HEIGHT}+{x}+{y}")

    def boss_key(self, _):
        """The boss_key method minimizes the game window."""
        self.master.iconify() # Minimize the game window

    def pause_resume_game(self, _):
        """The pause_resume_game method pauses or resumes the game."""
        if not self.paused:
            self.paused = True

            self.canvas.create_text(
                constants.GAME_WIDTH // 2,
                constants.GAME_HEIGHT // 2,
                text="GAME PAUSED",
                fill=constants.GAME_FONT_COLOR,
                font=(constants.GAME_LARGE_FONT_BOLD),
                anchor="center",
                tag="game_paused")

            self.canvas.create_text(
                constants.GAME_WIDTH // 2,
                constants.GAME_HEIGHT - 200,
                text="Press P to resume",
                fill=constants.GAME_FONT_COLOR,
                font=(constants.GAME_SMALL_FONT),
                anchor="center",
                tag="resume_game")

            print("Game paused")

        else:
            self.paused = False
            self.canvas.delete("game_paused")
            self.canvas.delete("resume_game")
            self.canvas.delete("save_game")
            print("Game resumed")

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
                        self.space_fighter.shot_animation() # Play the shot animation

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
                    self.space_fighter.shot_animation() # Play the shot animation

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
        if not self.paused:
            self.scroll_background(self.scroll_speed)

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

        self.destroy_lives_bar()

        self.draw_lives_bar()

        # Check if the player has no more lives
        if self.lives <= 0:
            self.game_over() # End the game

    def draw_lives_bar(self):
        """The draw_lives_bar method draws the lives bar on the canvas."""

        # Draw the lives bar on the canvas
        for i in range(self.lives):
            # Set the color of the lives bar
            lives_bar_color = constants.GAME_FONT_COLOR

            # Check the number of lives left and set the color of the lives bar accordingly
            match self.lives:
                case 1:
                    lives_bar_color = constants.GAME_FONT_COLOR_ERROR
                case 2:
                    lives_bar_color = constants.GAME_FONT_COLOR_WARNING
                case 3:
                    lives_bar_color = constants.GAME_FONT_COLOR_SUCCESS
                case _:
                    lives_bar_color = constants.GAME_FONT_COLOR

            # Draw the lives bar
            self.canvas.create_rectangle(
                constants.GAME_WIDTH - 20 - (i + 1) * 30,
                90,
                constants.GAME_WIDTH - 20 - i * 30,
                100,
                fill=lives_bar_color,
                outline=lives_bar_color,
                tag="lives-bar")

    def destroy_lives_bar(self):
        """The destroy_lives_bar method destroys the lives bar on the canvas."""

        # Destroy the lives bar on the canvas
        self.canvas.delete("lives-bar")

    def level_up(self):
        """The level_up method levels up the game and spawns more alien ships."""
        self.level += 1 # Increment the level by 1
        self.wave_length = int(self.level**0.7) + 2 # Calculate the wave length
        self.alien_ship_speed = int(self.level**0.6) + 1 # Calculate the alien ship speed
        self.space_fighter.speed = int(self.level**0.6)+14 # Calculate the space fighter speed

        if self.lives < 3:
            self.lives += 1 # Increment the lives by 1
            self.update_lives()

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

        # Wait for shot animation to finish before destroying the space fighter
        self.canvas.after(200, self.space_fighter.destroyed_animation)

        # Wait for the animation to finish before stopping the game
        self.canvas.after(800, self.stop_game)

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

        self.leaderboard_manager.print_leaderboard(self.canvas, sorted_leaderboard, self.player_name)

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

        # Set focus to the canvas
        self.canvas.focus_set()

    def return_to_menu(self, _):
        """The return_to_menu method returns to the start menu."""
        # Destroy the canvas
        self.canvas.destroy()

        os.execv(sys.executable, ['python'] + sys.argv)

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
        # Bounding box check
        if not (x1 < x2 + image2.width() and x1 + image1.width() > x2 and y1 < y2 + image2.height() and y1 + image1.height() > y2):
            return False  # No collision
        
        print(f"Checking collision between {image1} and {image2}")

        """The pixel_collision method checks if two images collide comparing its RGB values."""
        # Get the overlapping rectangle coordinates
        x_overlap = max(int(x1), int(x2))
        y_overlap = max(int(y1), int(y2))
        x_end = min(int(x1) + image1.width(), int(x2) + image2.width())
        y_end = min(int(y1) + image1.height(), int(y2) + image2.height())

        # Check for overlap within the rectangle
        for x in range(int(x_overlap), int(x_end)):
            for y in range(int(y_overlap), int(y_end)):
                # Get pixel values of the two images at the current position
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
            "main": PhotoImage(file="assets/img/chr/space-fighter-main.png"),
            "super": PhotoImage(file="assets/img/chr/space-fighter-super.png"),
            "shot": PhotoImage(file="assets/img/chr/space-fighter-shot.png"),
            "destroyed": PhotoImage(file="assets/img/chr/space-fighter-destroyed.png"),
            "explosion": PhotoImage(file="assets/img/chr/space-fighter-explosion.png")
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

        # Display the space fighter on the canvas and store it as an instance variable
        self.space_fighter_image = self.canvas.create_image(
            self.x,
            self.y,
            anchor="center",
            image=self.space_fighter_sprites[self.current_sprite])

    def update_sprite(self, _):
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

    def update_position(self, _):
        """The update_position method updates the position of the space fighter on the canvas."""
        self.canvas.coords(self.space_fighter_image, self.x, self.y)

    def shoot(self, _):
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

    def shot_animation(self):
        """The shot_animation method animates the space fighter when it gets hit by a laser."""

        self.current_sprite = "shot"
        self.canvas.itemconfig(
            self.space_fighter_image,
            image=self.space_fighter_sprites[self.current_sprite])

        # Animate the space fighter
        self.canvas.after(200, self.remove_shot_animation)

    def remove_shot_animation(self):
        """The remove_shot_animation method removes the space fighter from the canvas."""

        self.current_sprite = "main"
        self.canvas.itemconfig(
            self.space_fighter_image,
            image=self.space_fighter_sprites[self.current_sprite])

    def destroyed_animation(self):
        """The destroyed_animation method animates the space fighter when it gets destroyed."""

        self.current_sprite = "destroyed"
        self.canvas.itemconfig(
            self.space_fighter_image,
            image=self.space_fighter_sprites[self.current_sprite])

        # Animate the space fighter
        self.canvas.after(200, self.explosion_animation)

    def explosion_animation(self):
        """The explosion_animation method animates the explosion of the space fighter."""

        # Change the sprite of the space fighter to explosion
        self.current_sprite = "explosion"
        self.canvas.itemconfig(
            self.space_fighter_image,
            image=self.space_fighter_sprites[self.current_sprite])

        # Remove the space fighter after 200 milliseconds
        self.canvas.after(200, self.remove_space_fighter)

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

        # Load and store the alien ship sprites as a dictionary
        self.alien_ship_sprites = {
            "main": PhotoImage(file="assets/img/chr/alien-ship-main.png"),
            "destroyed": PhotoImage(file="assets/img/chr/alien-ship-destroyed.png"),
            "explosion": PhotoImage(file="assets/img/chr/alien-ship-explosion.png")
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

        # Create a list to store the lasers
        self.alien_lasers = []

        # Set the shoot delay and last shot time
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
            "main": PhotoImage(file="assets/img/clt/laser-beam.png"),
            "alt": PhotoImage(file="assets/img/clt/laser-beam-alt.png")
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

    def move(self):
        """The move method moves the laser beam upwards or downwards."""

        # Move the laser beam upwards or downwards according to its direction
        if self.direction == "up":
            self.y -= self.speed
        elif self.direction == "down":
            self.y += self.speed

        # Update the position of the laser on the canvas
        self.canvas.coords(self.laser_beam, self.x, self.y)

    def off_screen(self, height):
        """The off_screen method checks if the laser is off the screen."""
        # Check if the laser is off the screen according to its direction
        if self.direction == "up":
            return self.y <= height

        if self.direction == "down":
            return self.y >= height

        # If the direction is not up or down, return False
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
