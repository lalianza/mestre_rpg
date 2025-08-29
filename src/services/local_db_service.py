import json
import os

class LocalDbService:
    def __init__(self):

        self.db_file = "player_db.json"


        if not os.path.exists(self.db_file):
            with open(self.db_file, "w") as f:
                json.dump({}, f)

    def get_player_data(self, player_id: str) -> dict:

        try:
            with open(self.db_file, "r") as f:
                data = json.load(f)
                return data.get(player_id)
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def save_player_data(self, player_id: str, player_data: dict):

        with open(self.db_file, "r+") as f:
            data = json.load(f)
            data[player_id] = player_data
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
