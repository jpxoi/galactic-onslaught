"""
Galactic Onslaught - Constants Module
Author: Jean Paul Fernandez
Date: 2023-11-24
Version: 1.0
Language: Python 3.11.2
IDE: Visual Studio Code 1.84.2
Development Platform: MacOs Sonoma 14.1

Description:
This module contains the constants used in the game. The constants are used to
define the game window properties, font properties, font colors, and font styles.
"""

GAME_TITLE = "Galactic Onslaught" # Game title
GAME_WIDTH = 1440 # Game window width
GAME_HEIGHT = 900 # Game window height
GAME_SPEED = 60 # Game speed (FPS)

PLAYER_NAME_MAX_LENGTH = 10 # Maximum length of the player's name
PLAYER_NAME_MIN_LENGTH = 3 # Minimum length of the player's name

# Define font properties
GAME_FONT_FAMILY = "Trebuchet MS" # Font family
GAME_FONT_SIZE = (18, 24, 32, 48) # Font sizes

# Define font color constants
GAME_FONT_COLOR = "white"
GAME_FONT_COLOR_PRIMARY = "#5C8FFF" # Blue
GAME_FONT_COLOR_ERROR = "#F36A68" # Red
GAME_FONT_COLOR_WARNING = "#F9AE61" # Orange
GAME_FONT_COLOR_SUCCESS = "#84D792" # Green

# Define font style constants
GAME_FONT_STYLE_NORMAL = "normal" # Regular
GAME_FONT_STYLE_BOLD = "bold" # Bold

# Define font constants
GAME_SMALLEST_FONT = (GAME_FONT_FAMILY, GAME_FONT_SIZE[0], GAME_FONT_STYLE_NORMAL)
GAME_SMALL_FONT = (GAME_FONT_FAMILY, GAME_FONT_SIZE[1], GAME_FONT_STYLE_NORMAL)
GAME_MEDIUM_FONT = (GAME_FONT_FAMILY, GAME_FONT_SIZE[2], GAME_FONT_STYLE_NORMAL)
GAME_LARGE_FONT = (GAME_FONT_FAMILY, GAME_FONT_SIZE[3], GAME_FONT_STYLE_NORMAL)

GAME_SMALL_FONT_BOLD = (GAME_FONT_FAMILY, GAME_FONT_SIZE[1], GAME_FONT_STYLE_BOLD)
GAME_MEDIUM_FONT_BOLD = (GAME_FONT_FAMILY, GAME_FONT_SIZE[2], GAME_FONT_STYLE_BOLD)
GAME_LARGE_FONT_BOLD = (GAME_FONT_FAMILY, GAME_FONT_SIZE[3], GAME_FONT_STYLE_BOLD)
