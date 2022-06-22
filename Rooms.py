import random
import json


class Room:
    def __init__(self, players, judge, n_game):
        self.players = [players]
        self.judge = [judge]
        self.n_game = n_game
        self.all_usersInRoom = self.players + self.judge
        self.names = []

        for i in self.players:
            self.names.append(i[1])

        self.rols = ["Мирный житель", "Мирный житель", "Мирный житель", "Мирный житель", "Мирный житель",
                     "Мирный житель", "Мафия", "Мафия", "Дон", "Шериф"]  # Роли которые есть в игре
        random.shuffle(self.rols)

        # API
        self.mafia_api = {
            "mafia_players": self.names,
            "mafia_judge": self.judge[0][1],
            "mafia_number_game": self.n_game,
            "mafia_start_game": False,
            "mafia_event":
                {
                    "mafia_rols": self.rols,
                    "mafia_night": 0,
                    "mafia_day": 0,
                    "mafia_kill": 0,
                    "mafia_don": 0,
                    "mafia_sherif": 0
                }
        }

    def prossesing_dataroom(self):
        for p in self.all_usersInRoom:
            p[0].data = json.loads(p[0].data)
            p[0].data["lobby_room"]["mafia_api"] = self.mafia_api
            p[0].data = json.dumps(p[0].data)
