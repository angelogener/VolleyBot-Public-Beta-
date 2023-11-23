import csv
from typing import Any
from player import Player


def load_data(file: str) -> dict[Player] | dict[Any, Any]:
    """
    :param file: The string name of the .csv file to be read.
    Instantiates Players and creates a dictionary of them.
    :return: A dictionary with Player ID's pointing to the Player.
    """
    try:
        players = {}
        with open(file, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader, None)
            for row in csv_reader:
                player_num = int(row[0])
                player_name = row[1]
                player_ranking = int(row[2]) if row[2] else 0
                player_wins = int(row[3]) if row[3] else 0
                player_games = int(row[4]) if row[4] else 0
                new_player = Player(player_num, player_name, player_ranking, player_wins, player_games)
                players[player_num] = new_player
        return players
    except FileNotFoundError:
        return {}


def save_data(file: str, players: dict[Player]):
    try:
        with open(file, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['Player ID', 'Player Names', 'Elo Rating', 'Wins', 'Total Games Played'])

            for key, values in players.items():
                csv_writer.writerow([key, values.name, values.rating, values.wins, values.games_played])

    except FileNotFoundError:
        print("File not Found")
