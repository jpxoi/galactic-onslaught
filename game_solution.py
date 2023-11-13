from tkinter import Tk, Canvas, PhotoImage
import random

# GLOBAL SCOPE CONSTANTS
GAME_TITLE = "Space Invaders Redux"
GAME_WIDTH = 1440
GAME_HEIGHT = 900
GAME_SPEED = 60

class Game:
    def __init__(self, master):
        self.master = master
        self.master.title(GAME_TITLE)
        self.master.geometry(f"{GAME_WIDTH}x{GAME_HEIGHT}+0+0")

        BACKGROUND_IMAGE = PhotoImage(file="assets/img/background.png")
        # Photo by Ivana Cajina [https://unsplash.com/@von_co] on Unsplash [https://unsplash.com/photos/milky-way-asuyh-_ZX54]

        self.canvas = Canvas(master, bg="black", width=GAME_WIDTH, height=GAME_HEIGHT)
        self.canvas.pack()


if __name__ == "__main__":
    root = Tk()
    game = Game(root)
    root.mainloop()