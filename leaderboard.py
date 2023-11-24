"""
Galactic Onslaught - Leaderboard Module
Author: Jean Paul Fernandez
Date: 2023-11-24
Version: 1.0
Language: Python 3.11.2
IDE: Visual Studio Code 1.84.2
Development Platform: MacOs Sonoma 14.1

Description:
This module contains the leaderboard manager class, which manages the leaderboard file.
The leaderboard file contains the top scores of the players who have played the game.
The leaderboard manager class allows appending, updating, reading, and sorting of entries
in the leaderboard file.

Implementation:
This module is imported by the main game module. The leaderboard manager class is
instantiated in the main game module and is used to manage the leaderboard file.
"""

# Import modules
import constants

class LeaderboardManager:
    """
    Class to manage the leaderboard file
    It allows appending, updating, reading, and sorting of entries
    In the leaderboard file, each line contains a player name and a score
    A leaderboard entry is represented by a dictionary with keys "playerName" and "score"
    """
    def __init__(self, scores_file):
        self.scores_file = scores_file

    def append_leaderboard(self, new_entry):
        """Append a new entry to the leaderboard file"""
        with open(self.scores_file, 'a', encoding="utf-8") as file:
            line = f"{new_entry['playerName']} {new_entry['score']}\n"
            file.write(line)

    def update_leaderboard(self, update_entry):
        """Update an existing entry in the leaderboard file"""
        with open(self.scores_file, 'r', encoding="utf-8") as file:
            lines = file.readlines()

        with open(self.scores_file, 'w', encoding="utf-8") as file:
            for line in lines:
                parts = line.split()
                if len(parts) == 2:
                    name, _ = parts
                    if name == update_entry['playerName']:
                        line = f"{update_entry['playerName']} {update_entry['score']}\n"
                file.write(line)

    def read_leaderboard(self):
        """Read the leaderboard file and return a list of dictionaries"""
        leaderboard = []
        with open(self.scores_file, 'r', encoding="utf-8") as file:
            for line in file:
                parts = line.split()
                if len(parts) == 2:
                    name, score = parts
                    leaderboard.append({"playerName": name, "score": int(score)})

        return leaderboard

    def sort_leaderboard(self, leaderboard):
        """Sort the leaderboard by score"""
        leaderboard.sort(key=lambda x: x['score'], reverse=True)

        # Keep only the top 10 entries
        leaderboard = leaderboard[:10]
        return leaderboard

    def print_leaderboard(self, canvas, sorted_leaderboard, player_name):
        """Print the leaderboard to the screen"""

        # Print Leaderboard on a table
        canvas.create_rectangle(
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
        canvas.create_text(
            constants.GAME_WIDTH // 2,
            constants.GAME_HEIGHT // 2 - 350,
            text="LEADERBOARD",
            fill=constants.GAME_FONT_COLOR,
            font=(constants.GAME_LARGE_FONT_BOLD),
            anchor="center",
            tag="leaderboard-title")

        # Create the leaderboard table headers on the canvas
        canvas.create_text(
            constants.GAME_WIDTH // 2 - 125,
            constants.GAME_HEIGHT // 2 - 250,
            text="Rank",
            fill=constants.GAME_FONT_COLOR,
            font=(constants.GAME_SMALL_FONT_BOLD),
            anchor="center",
            tag="leaderboard-rank")

        canvas.create_text(
            constants.GAME_WIDTH // 2 - 50,
            constants.GAME_HEIGHT // 2 - 250,
            text="Name",
            fill=constants.GAME_FONT_COLOR,
            font=(constants.GAME_SMALL_FONT_BOLD),
            anchor="w",
            tag="leaderboard-name")

        canvas.create_text(
            constants.GAME_WIDTH // 2 + 125,
            constants.GAME_HEIGHT // 2 - 250,
            text="Score",
            fill=constants.GAME_FONT_COLOR,
            font=(constants.GAME_SMALL_FONT_BOLD),
            anchor="center",
            tag="leaderboard-score")

        # Create the leaderboard entries on the canvas
        for i, entry in enumerate(sorted_leaderboard):
            if entry["playerName"] == player_name:
                font_size = constants.GAME_SMALL_FONT_BOLD
                font_color = constants.GAME_FONT_COLOR_SUCCESS
            else:
                font_size = constants.GAME_SMALL_FONT
                font_color = constants.GAME_FONT_COLOR

            canvas.create_text(
                constants.GAME_WIDTH // 2 - 125,
                constants.GAME_HEIGHT // 2 - 200 + (i * 50),
                text=f"{i + 1}",
                fill=font_color,
                font=(font_size),
                anchor="center",
                tag="leaderboard-entry-rank")

            canvas.create_text(
                constants.GAME_WIDTH // 2 - 50,
                constants.GAME_HEIGHT // 2 - 200 + (i * 50),
                text=f"{entry['playerName']}",
                fill=font_color,
                font=(font_size),
                anchor="w",
                tag="leaderboard-entry-name")

            canvas.create_text(
                constants.GAME_WIDTH // 2 + 125,
                constants.GAME_HEIGHT // 2 - 200 + (i * 50),
                text=f"{entry['score']}",
                fill=font_color,
                font=(font_size),
                anchor="center",
                tag="leaderboard-entry-score")
