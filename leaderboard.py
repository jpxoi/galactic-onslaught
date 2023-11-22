class LeaderboardManager:
    def __init__(self, scores_file):
        self.scores_file = scores_file

    def append_leaderboard(self, new_entry):
        with open(self.scores_file, 'a') as file:
            line = f"{new_entry['playerName']} {new_entry['score']}\n"
            file.write(line)

    def update_leaderboard(self, update_entry):
        with open(self.scores_file, 'r') as file:
            lines = file.readlines()

        with open(self.scores_file, 'w') as file:
            for line in lines:
                parts = line.split()
                if len(parts) == 2:
                    name, score = parts
                    if name == update_entry['playerName']:
                        line = f"{update_entry['playerName']} {update_entry['score']}\n"
                file.write(line)

    def read_leaderboard(self):
        leaderboard = []
        with open(self.scores_file, 'r') as file:
            for line in file:
                parts = line.split()
                if len(parts) == 2:
                    name, score = parts
                    leaderboard.append({"playerName": name, "score": int(score)})

        return leaderboard
        
    def sort_leaderboard(self, leaderboard):
        leaderboard.sort(key=lambda x: x['score'], reverse=True)
        # Keep only the top 10 entries
        leaderboard = leaderboard[:10]
        return leaderboard