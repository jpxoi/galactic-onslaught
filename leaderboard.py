"""
Module: leaderboard

This module defines the `LeaderboardManager` class, which provides functionality for
managing a leaderboard file. The leaderboard file is assumed to contain entries with
player names and corresponding scores.

Classes:
- LeaderboardManager: Manages the leaderboard file, allowing appending, updating,
                        reading, and sorting of entries.

Methods:
- __init__(self, scores_file): Initializes the LeaderboardManager instance with the
                                specified leaderboard file.
- append_leaderboard(self, new_entry): Appends a new entry to the leaderboard file.
- update_leaderboard(self, update_entry): Updates an existing entry in the leaderboard file.
- read_leaderboard(self): Reads the leaderboard file and returns a list of dictionaries
                            representing entries.
- sort_leaderboard(self, leaderboard): Sorts the given leaderboard by score in descending
                                        order and keeps only the top 10 entries.
"""

class LeaderboardManager:
    """Class to manage the leaderboard file"""
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
