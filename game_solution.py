from tkinter import Tk, Canvas, PhotoImage
import random
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
        self.paused = False
        self.run = True
        self.lives = 3
        self.level = 1
        self.gameOver = False

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
        self.score_label = self.canvas.create_text(constants.GAME_WIDTH - 20, 30, text=f"Score: {self.score}", fill="white", font=("Helvetica", 16), anchor="e", tag="score")

        # Set focus to the canvas
        self.canvas.focus_set()

        # Start the clock
        self.clock()

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
            self.wave_length += 5
            self.alien_ship_speed += 2

            for i in range(self.wave_length):
                self.enemy = AlienShip(self.canvas, self.alien_ship_speed)
                self.alien_ships.append(self.enemy)

        # Move the alien ship and handle shooting
        for alien_ship in self.alien_ships:
            alien_ship.move()
            
            # Move and update the alien lasers
            for alien_laser in alien_ship.alien_lasers:
                alien_laser.move()

    def update_score(self):
        self.score += 1
        self.canvas.itemconfig(self.score_label, text=f"Score: {self.score}")
    
    # Define the scroll_background method to update the background images for infinite scrolling
    def scroll_background(self, speed):
        # Update the vertical position of the background images
        self.canvas.move(self.bgImage1, 0, speed) # Move the first background image down by 4 pixels
        self.canvas.move(self.bgImage2, 0, speed) # Move the second background image down by 4 pixels

        # Get the current y-coordinates of the background images
        _, y1, _, _ = self.canvas.bbox(self.bgImage1) # Get the y-coordinate of the first background image
        _, y2, _, _ = self.canvas.bbox(self.bgImage2) # Get the y-coordinate of the second background image

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
        # Store the canvas as an instance variable
        self.canvas = canvas

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
        self.currentSprite = "main" # Current sprite of the space fighter
        self.speed = 15 # Speed of the space fighter
        self.width = 150 # Width of the space fighter
        self.height = 150 # Height of the space fighter

        # Initial coordinates of the space fighter
        self.x = constants.GAME_WIDTH // 2 # Center of the canvas
        self.y = constants.GAME_HEIGHT - 90 # 90 pixels above the bottom of the canvas

        # Display the space fighter on the canvas and store it as an instance variable
        self.spaceFighterImage = self.canvas.create_image(self.x, self.y, anchor="center", image=self.spaceFighterSprites[self.currentSprite])

        # Create a list to store the lasers
        self.lasers = []

        # Bind the key events to the corresponding methods
        self.canvas.bind("<Left>", self.move_left) # Bind the left arrow key to the move_left method
        self.canvas.bind("<Right>", self.move_right) # Bind the right arrow key to the move_right method
        self.canvas.bind("<space>", self.shoot) # Bind the space bar to the shoot method
    
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

# Define the Laser class to represent the laser beam in the game
class Laser:
    # Define the constructor method of the Laser class
    def __init__(self, canvas, x, y):
        # Store the canvas as an instance variable
        self.canvas = canvas

        # Initial coordinates of the laser
        self.x = x # Same x-coordinate as the space fighter
        self.y = y - 40 # 40 pixels above the space fighter

        # Speed of the laser
        self.speed = 10  # Speed of the laser

        # Load and store the laser image as an instance variable
        self.laserImage = PhotoImage(file="assets/img/laser-beam.png")
        # Laser graphic made by me (Jean Paul Fernandez) using Adobe Photoshop [https://adobe.com/products/photoshop/].

        # Display the laser on the canvas and store it as an instance variable
        self.laserBeam = self.canvas.create_image(self.x, self.y, anchor="center", image=self.laserImage)

    # Define the move method to move the laser upwards
    def move(self):
        self.y -= self.speed  # Move the laser upwards
        self.canvas.coords(self.laserBeam, self.x, self.y) # Update the position of the laser on the canvas

        # Remove the laser if it goes beyond the top of the canvas
        if self.y < 0:
            self.canvas.delete(self.laserBeam)

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
        # Set the speed of the alien ship
        self.speed = speed
        self.width = 100
        self.height = 100

        # Create the alien ship
        self.create_alien_ship()

        # Properties for shooting lasers
        self.alien_lasers = []
        self.shoot_delay = 2000  # Delay between shots in milliseconds
        self.last_shot_time = 0  # Time of the last shot

    def create_alien_ship(self):
        # Create a new alien ship at a random position on the top of the canvas
        self.x = random.randint(75, constants.GAME_WIDTH - 75)
        self.y = random.randint(-900, 0)

        self.alienShipImage = self.canvas.create_image(self.x, self.y, anchor="center", image=self.alienSprites[self.currentSprite])        

    # Define the move method to move the alien ship downwards
    def move(self):
        self.y += self.speed  # Move the alien ship downwards
        self.canvas.coords(self.alienShipImage, self.x, self.y)  # Update the position of the alien ship on the canvas

        # Remove the alien ship if it goes beyond the bottom of the canvas
        if self.y > constants.GAME_HEIGHT:
            self.canvas.delete(self.alienShipImage)
            
            # Remove the alien ship from the alien_ships array
            if self in game.alien_ships:
                game.alien_ships.remove(self)
        
        # Check if it's time for the alien to shoot
        current_time = time.time() * 1000  # Convert to milliseconds
        if current_time - self.last_shot_time > self.shoot_delay:
            self.shoot()
            self.last_shot_time = current_time

    def shoot(self):
        # Create a laser at the current position of the alien ship
        alien_laser = AlienLaser(self.canvas, self.x, self.y)
        self.alien_lasers.append(alien_laser)

# Define the AlienLaser class to represent the laser beam of the alien ship in the game
class AlienLaser:
    def __init__(self, canvas, x, y):
        self.canvas = canvas

        # Initial coordinates of the alien laser
        self.x = x
        self.y = y

        # Speed of the alien laser
        self.speed = 10  # Adjust as needed

        # Load and store the alien laser image as an instance variable
        self.alienLaserImage = PhotoImage(file="assets/img/laser-beam.png")

        # Display the alien laser on the canvas and store it as an instance variable
        self.alienLaserObject = self.canvas.create_image(self.x, self.y, anchor="center", image=self.alienLaserImage)

    def move(self):
        self.y += self.speed  # Move the alien laser downwards
        self.canvas.coords(self.alienLaserImage, self.x, self.y)  # Update the position of the alien laser on the canvas


# MAIN PROGRAM
if __name__ == "__main__":
    root = Tk() # Create the root window
    game = Game(root) # Create the game instance
    root.mainloop() # Run the main loop