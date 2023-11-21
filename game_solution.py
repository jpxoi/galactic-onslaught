from tkinter import Tk, Canvas, PhotoImage
import random
import math
import time
import constants

# Define the Game class to represent the game window and its contents
class Game:
    # Define the constructor method of the Game class
    def __init__(self, master):
        # Store the root window as an instance variable
        self.master = master
        self.master.title(constants.GAME_TITLE) # Set the title of the window to the game title (constants.GAME_TITLE)
        self.master.geometry(f"{constants.GAME_WIDTH}x{constants.GAME_HEIGHT}+0+0") # Set the size of the window to the game size (constants.GAME_WIDTH x constants.GAME_HEIGHT) and position it at the top-left corner of the screen (+0+0)

        # Create the canvas widget and pack it to the root window
        self.canvas = Canvas(master, bg="black", width=constants.GAME_WIDTH, height=constants.GAME_HEIGHT) # Create the canvas widget with a black background and the game size (constants.GAME_WIDTH x constants.GAME_HEIGHT)
        self.canvas.pack()

        # Define game variables
        self.score = 0
        self.lives = 3
        self.paused = False
        self.run = True
        self.level = 1
        self.gameOver = False
        self.lostCount = 0

        # Load and store the background image as an instance variable
        self.backgroundImage = PhotoImage(file="assets/img/background.png")
        # Background graphic made by me (Jean Paul Fernandez) using Canva's image editor [https://www.canva.com].
        # Additional graphic "Space with small elements. Minimal starry night sky background. Few stars space background." by Rostik Solonenko on Canva's free media library [https://www.canva.com/features/free-stock-photos/].
        # Editable file available as view-only at https://www.canva.com/design/DAF0EFDjc3g/cApy-RMGI9pTI6kQi9Xrmg/edit.

        # Create two background images for seamless scrolling
        self.bgImage1 = self.canvas.create_image(0, 0, anchor="nw", image=self.backgroundImage) # Create the first background image at the top-left corner of the canvas
        self.bgImage2 = self.canvas.create_image(0, -constants.GAME_HEIGHT, anchor="nw", image=self.backgroundImage) # Create the second background image above the first background image

        # Store Enemy objects in a list
        self.alien_ships = []
        self.wave_length = 0
        self.alien_ship_speed = 2
        
        # Create the alien ship
        for self.alien_ship in self.alien_ships:
            self.alien_ship = AlienShip(self.canvas, self.alien_ship_speed)

        # Create the space fighter
        self.spaceFighter = SpaceFighter(self.canvas)

        # Create the score label on the canvas
        self.score_label = self.canvas.create_text(constants.GAME_WIDTH - 20, 30, text=f"Score: {self.score}", fill=constants.GAME_FONT_COLOR, font=(constants.GAME_SMALL_FONT), anchor="e", tag="score")

        # Create the lives label on the canvas
        self.lives_label = self.canvas.create_text(constants.GAME_WIDTH - 20, 70, text=f"Lives: {self.lives}", fill=constants.GAME_FONT_COLOR, font=(constants.GAME_SMALL_FONT), anchor="e", tag="lives")
        # Bind the key events to the corresponding methods
        self.canvas.bind("<B>", self.boss_key)

        # Set focus to the canvas
        self.canvas.focus_set()

        # Start the clock
        self.clock()

    def boss_key(self, event):
        # Minimize the window
        self.master.iconify()

    def clock(self):
        # Update the screen
        self.update_screen()

        self.master.after(1000 // constants.GAME_SPEED, self.clock)

    def update_screen(self):
        # Update the background images for infinite scrolling
        self.scroll_background(self.alien_ship_speed // 2)
        
        # Move the lasers
        self.spaceFighter.move_lasers()

        if len(self.alien_ships) == 0:
            self.level += 1
            self.wave_length += 3
            self.alien_ship_speed += 2

            for i in range(self.wave_length):
                self.enemy = AlienShip(self.canvas, self.alien_ship_speed)
                self.alien_ships.append(self.enemy)

        # Move the alien ship and handle shooting
        for alien_ship in self.alien_ships:
            alien_ship.move()
            alien_ship.move_lasers()

    def update_score(self):
        self.score += 1
        self.canvas.itemconfig(self.score_label, text=f"Score: {self.score}")

    def update_lives(self):
        self.canvas.itemconfig(self.lives_label, text=f"Lives: {self.lives}")

        if self.lives <= 0:
            self.game_over()

    def game_over(self):
        self.gameOver = True
        self.canvas.create_text(constants.GAME_WIDTH // 2, constants.GAME_HEIGHT // 2, text="GAME OVER", fill=constants.GAME_FONT_COLOR, font=(constants.GAME_LARGE_FONT_BOLD), anchor="center", tag="game_over")
    
    # Define the scroll_background method to update the background images for infinite scrolling
    def scroll_background(self, speed):
        # Update the vertical position of the background images
        self.canvas.move(self.bgImage1, 0, speed) # Move the first background image down by 4 pixels
        self.canvas.move(self.bgImage2, 0, speed) # Move the second background image down by 4 pixels

        # The bbox method returns a tuple containing the coordinates (x, y, width, height) of the specified item on the canvas.
        _, y1, _, _ = self.canvas.bbox(self.bgImage1)
        _, y2, _, _ = self.canvas.bbox(self.bgImage2)

        # Check if the first background image is out of the canvas
        if y1 >= constants.GAME_HEIGHT:
            # Reset its position above the second background image
            self.canvas.move(self.bgImage1, 0, -2 * constants.GAME_HEIGHT)

        # Check if the second background image is out of the canvas
        if y2 >= constants.GAME_HEIGHT:
            # Reset its position above the first background image
            self.canvas.move(self.bgImage2, 0, -2 * constants.GAME_HEIGHT)

# Define the SpaceFighter class to represent the space fighter in the game
class SpaceFighter:
    # Define the constructor method of the SpaceFighter class
    def __init__(self, canvas):
        self.canvas = canvas
        self.x = constants.GAME_WIDTH // 2 # Center of the canvas
        self.y = constants.GAME_HEIGHT - 90 # 90 pixels above the bottom of the canvas

        # Load and store the space fighter sprites as a dictionary
        self.spaceFighterSprites = {
            "main": PhotoImage(file="assets/img/space-fighter-main.png"), # Main sprite - default
            "super": PhotoImage(file="assets/img/space-fighter-super.png") # Super sprite - power-up
            # Sprites generated using Canva's AI image generator Magic Media [https://www.canva.com/ai-image-generator/]
            # Input prompt "3D 4K Animated and Futuristic Space Fighter. 2D view from the top of it. Place it on a black background."
            # Background removed using Canva's Magic Studio [https://www.canva.com/magic/].
            # Further modifications made using Canva's image editor [https://canva.com].
            # Editable file available as view-only at https://www.canva.com/design/DAF0D65NA5U/6-y7e9e_xXZK_j7Iaaq5TQ/edit.
        }

        # Properties of the space fighter
        self.currentSprite = "main"
        self.speed = 15
        self.width = 150
        self.height = 150

        # Create the space fighter
        self.create_space_fighter()

        # Create a list to store the lasers
        self.lasers = []

        # Bind the key events to the corresponding methods
        self.canvas.bind("<F>", self.update_sprite)
        self.canvas.bind("<Left>", self.move_left)
        self.canvas.bind("<Right>", self.move_right)
        self.canvas.bind("<space>", self.shoot)

    def create_space_fighter(self):
        self.spaceFighterImage = self.canvas.create_image(self.x, self.y, anchor="center", image=self.spaceFighterSprites[self.currentSprite])
    
    # Define the update_sprite method to update the sprite of the space fighter
    def update_sprite(self, event):
        # Check if the space fighter is in its main sprite
        if self.currentSprite == "main":
            # Change the sprite of the space fighter to super
            self.currentSprite = "super"
            # Change the image of the space fighter to the super sprite
            self.canvas.itemconfig(self.spaceFighterImage, image=self.spaceFighterSprites[self.currentSprite])
        # Check if the space fighter is in its super sprite
        elif self.currentSprite == "super":
            # Change the sprite of the space fighter to main
            self.currentSprite = "main"
            # Change the image of the space fighter to the main sprite
            self.canvas.itemconfig(self.spaceFighterImage, image=self.spaceFighterSprites[self.currentSprite])

        self.canvas.focus_set()

    # Define the move_left method to move the space fighter to the left
    def move_left(self, event):
        # Check if the space fighter is not yet at the leftmost part of the canvas
        if self.x > self.width / 2 + 15:
            self.x -= self.speed # Move the space fighter to the left by the speed of the space fighter
            self.update_position() # Update the position of the space fighter on the canvas

    # Define the move_right method to move the space fighter to the right
    def move_right(self, event):
        # Check if the space fighter is not yet at the rightmost part of the canvas
        if self.x < constants.GAME_WIDTH - (self.width / 2 + 15):
            self.x += self.speed # Move the space fighter to the right by the speed of the space fighter
            self.update_position() # Update the position of the space fighter on the canvas

    # Update the position of the space fighter on the canvas
    def update_position(self):
        self.canvas.coords(self.spaceFighterImage, self.x, self.y)

    def shoot(self, event):
        # Create a laser at the current position of the space fighter
        laser = Laser(self.canvas, self.x, self.y)
        self.lasers.append(laser)

    def move_lasers(self):
        # Move all the lasers in the list
        for laser in self.lasers:
            laser.move()

# Define the SlienShip class to represent the alien ship in the game
class AlienShip:
    def __init__(self, canvas, speed):
        self.canvas = canvas
        self.x = 0
        self.y = 0

        self.alienSprites = {
            "main": PhotoImage(file="assets/img/alien-ship-main.png"), # Main sprite - default
            "destroyed": PhotoImage(file="assets/img/alien-ship-destroyed.png"), # Destroyed sprite - when hit by a laser
            "explosion": PhotoImage(file="assets/img/alien-ship-explosion.png") # Explosion sprite - when destroyed
            # Sprites generated using Canva's AI image generator Magic Media [https://www.canva.com/ai-image-generator/]
            # Input prompt "3D Cartoon 4K Animated and Futuristic Alien UFO. 2D view from the top of it. Place it on a black background."
            # Background removed using Canva's Magic Studio [https://www.canva.com/magic/].
            # Additional graphic "Cosmic explosion orange" Anna Kuz on Canva's free media library [https://www.canva.com/features/free-stock-photos/].
            # Further modifications made using Canva's image editor [https://canva.com].
            # Editable file available as view-only at https://www.canva.com/design/DAF0GJfd7jU/PrEOAQ9Z_rp3vRWcLYkN3Q/edit
        }

        # Properties of the alien ship
        self.currentSprite = "main"
        self.speed = speed
        self.width = 100
        self.height = 100

        # Create the alien ship
        self.create_alien_ship()

        # Properties for shooting lasers
        self.alien_lasers = []
        self.shoot_delay = 4000  # Delay between shots in milliseconds
        self.last_shot_time = 0  # Time of the last shot

    def create_alien_ship(self):
        self.x = random.randint(75, constants.GAME_WIDTH - 75)
        self.y = random.randint(-900, 0)

        self.alienShipImage = self.canvas.create_image(self.x, self.y, anchor="center", image=self.alienSprites[self.currentSprite])        

    # Define the move method to move the alien ship downwards
    def move(self):
        self.y += self.speed  # Move the alien ship downwards
        self.x += 2 * math.sin(self.y / 50)  # Move the alien ship sideways
        self.update_position()  # Update the position of the alien ship on the canvas

        # Remove the alien ship if it goes beyond the bottom of the canvas
        if self.y > constants.GAME_HEIGHT:
            # Remove the alien ship from the canvas
            self.canvas.delete(self.alienShipImage)

            # Update the lives of the player
            game.lives -= 1
            game.update_lives()
            
            # Remove the alien ship from the alien_ships array
            if self in game.alien_ships:
                game.alien_ships.remove(self)
        
        # Check if it's time for the alien to shoot
        current_time = time.time() * 1000  # Convert to milliseconds
        
        if current_time - self.last_shot_time > self.shoot_delay:
            self.shoot()
            self.last_shot_time = current_time

    def update_position(self):
        self.canvas.coords(self.alienShipImage, self.x, self.y)

    def shoot(self):
        # Create a laser at the current position of the alien ship
        alien_laser = Laser(self.canvas, self.x, self.y, self.speed + 3, "down")
        self.alien_lasers.append(alien_laser)

    def move_lasers(self):
        for alien_laser in self.alien_lasers:
            alien_laser.move()

# Define the Laser class to represent the laser beam in the game
class Laser:
    # Define the constructor method of the Laser class
    def __init__(self, canvas, x, y, speed = 10, direction = "up"):
        self.canvas = canvas
        self.x = x
        self.y = y - 40

        # Speed of the laser
        self.speed = 10  # Speed of the laser
        self.direction = direction

        self.laserImage = PhotoImage(file="assets/img/laser-beam.png")
        # Laser graphic made by me (Jean Paul Fernandez) using Adobe Photoshop [https://adobe.com/products/photoshop/].

        # Display the laser on the canvas and store it as an instance variable
        self.laserBeam = self.canvas.create_image(self.x, self.y, anchor="center", image=self.laserImage)

    # Define the move method to move the laser upwards
    def move(self):
        if self.direction == "up":
            self.y -= self.speed
        elif self.direction == "down":
            self.y += self.speed

        # Update the position of the laser on the canvas
        self.canvas.coords(self.laserBeam, self.x, self.y)

    def off_screen(self, height):
        return self.y <= height and self.y >= 0
    
    def collision(self, obj):
        return collide(self, obj)

# MAIN PROGRAM
if __name__ == "__main__":
    # Create the root window, and pass it to the Game class
    root = Tk()
    game = Game(root)

    # Run the main loop
    root.mainloop()