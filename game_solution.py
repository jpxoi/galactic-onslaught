from tkinter import Tk, Canvas, PhotoImage
import random

# GLOBAL SCOPE CONSTANTS AND VARIABLES
GAME_TITLE = "Space Invaders 3D" # Game title
GAME_WIDTH = 1440 # Game window width
GAME_HEIGHT = 900 # Game window height
GAME_SPEED = 240 # Game speed (FPS)

# CLASS DEFINITIONS
# Define the Game class to represent the game window and its contents
class Game:
    # Define the constructor method of the Game class
    def __init__(self, master):
        # Store the root window as an instance variable
        self.master = master
        self.master.title(GAME_TITLE) # Set the title of the window to the game title (GAME_TITLE)
        self.master.geometry(f"{GAME_WIDTH}x{GAME_HEIGHT}+0+0") # Set the size of the window to the game size (GAME_WIDTH x GAME_HEIGHT) and position it at the top-left corner of the screen (+0+0)

        # Create the canvas widget and pack it to the root window
        self.canvas = Canvas(master, bg="black", width=GAME_WIDTH, height=GAME_HEIGHT) # Create the canvas widget with a black background and the game size (GAME_WIDTH x GAME_HEIGHT)
        self.canvas.pack()

        # Load and store the background image as an instance variable
        self.backgroundImage = PhotoImage(file="assets/img/background.png")
        # Background graphic made by me (Jean Paul Fernandez) using Canva's image editor [https://www.canva.com].
        # Additional graphic "Space with small elements. Minimal starry night sky background. Few stars space background." by Rostik Solonenko on Canva's free media library [https://www.canva.com/features/free-stock-photos/].
        # Editable file available as view-only at https://www.canva.com/design/DAF0EFDjc3g/cApy-RMGI9pTI6kQi9Xrmg/edit.

        # Create two background images for seamless scrolling
        self.bgImage1 = self.canvas.create_image(0, 0, anchor="nw", image=self.backgroundImage) # Create the first background image at the top-left corner of the canvas
        self.bgImage2 = self.canvas.create_image(0, -GAME_HEIGHT, anchor="nw", image=self.backgroundImage) # Create the second background image above the first background image

        # Initialize score
        self.score = 0

        # Create the score label on the canvas
        self.score_label = self.canvas.create_text(GAME_WIDTH - 20, 30, text=f"Score: {self.score}", fill="white", font=("Helvetica", 16), anchor="e", tag="score")

        # Create the space fighter
        self.spaceFighter = SpaceFighter(self.canvas)

        # Create the alien ship
        self.alienShip = AlienShip(self.canvas)

        # Set focus to the canvas
        self.canvas.focus_set()

        # Schedule the update_background method to run inmediately
        self.master.after(0, self.update_screen)

    def update_screen(self):
        # Update the background images for infinite scrolling
        self.scroll_background()

        # Move the lasers
        self.spaceFighter.move_lasers()

        # Move the alien ship
        self.alienShip.move()

        # Schedule the update_screen method to run again (recursion) after (1000 // GAME_SPEED) milliseconds (1000 milliseconds = 1 second)
        self.master.after(1000 // GAME_SPEED, self.update_screen)

    def update_score(self):
        self.score += 1
        self.canvas.itemconfig(self.score_label, text=f"Score: {self.score}")
    
    # Define the scroll_background method to update the background images for infinite scrolling
    def scroll_background(self):
        # Update the vertical position of the background images
        self.canvas.move(self.bgImage1, 0, 4) # Move the first background image down by 4 pixels
        self.canvas.move(self.bgImage2, 0, 4) # Move the second background image down by 4 pixels

        # Get the current y-coordinates of the background images
        _, y1, _, _ = self.canvas.bbox(self.bgImage1) # Get the y-coordinate of the first background image
        _, y2, _, _ = self.canvas.bbox(self.bgImage2) # Get the y-coordinate of the second background image

        # Check if the first background image is out of the canvas
        if y1 >= GAME_HEIGHT:
            # Reset its position above the second background image
            self.canvas.move(self.bgImage1, 0, -2 * GAME_HEIGHT)

        # Check if the second background image is out of the canvas
        if y2 >= GAME_HEIGHT:
            # Reset its position above the first background image
            self.canvas.move(self.bgImage2, 0, -2 * GAME_HEIGHT)

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
        self.x = GAME_WIDTH // 2 # Center of the canvas
        self.y = GAME_HEIGHT - 90 # 90 pixels above the bottom of the canvas

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
        if self.x < GAME_WIDTH - (self.width / 2 + 15):
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

class AlienShip:
    def __init__(self, canvas):
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
        self.speed = 5
        self.width = 100
        self.height = 100

        # Create the alien ship
        self.create_alien_ship()

    def create_alien_ship(self):
        # Create a new alien ship at a random position on the top of the canvas
        self.x = random.randint(0, GAME_WIDTH)
        self.y = 0

        self.alienShipImage = self.canvas.create_image(self.x, self.y, anchor="center", image=self.alienSprites[self.currentSprite])

        # Recursively call the create_alien_ship method after random time intervals
        self.canvas.after(random.randint(1000, 5000), self.create_alien_ship)

    # Define the move method to move the alien ship downwards
    def move(self):
        self.y += self.speed  # Move the alien ship downwards
        self.canvas.coords(self.alienShipImage, self.x, self.y)  # Update the position of the alien ship on the canvas

        # Remove the alien ship if it goes beyond the bottom of the canvas
        if self.y > GAME_HEIGHT:
            self.canvas.delete(self.alienShipImage)

# MAIN PROGRAM
if __name__ == "__main__":
    root = Tk() # Create the root window
    game = Game(root) # Create the game instance
    root.mainloop() # Run the main loop