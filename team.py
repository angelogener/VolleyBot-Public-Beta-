from player import Player


class Team:
    """
    A full Volleyball Team composed of Players.

    Attributes:
        name (str): The name of the Team.
        players (list[Player]): The list containing the Players in the team.
        record (int): The number of wins accumulated by this team.
    """
    def __init__(self, name: str, date: str):
        self.name = name
        self.date = date
        self.players = []
        self.record = 0

    def add_player(self, player: Player):
        """
        Adds a player to the team.
        :param player: The Player to be added to this Team.
        :return: Null
        """
        self.players.append(player)

    def remove_player(self, player: Player):
        """
        Removes a player from the team, if they are in the team.
        :param player: The Player to remove from this Team.
        :return: Null
        """
        if player in self.get_players():
            self.players.remove(player)

    def play_team(self, is_winner: bool, opponent: int):
        """
        Calculates the new rank of the Team's Players. Refer to Player.play().
        :param is_winner: True if Team won. False if the lost.
        :param opponent: The Elo Ranking of the opponent(s).
        :return: None.
        """
        self.record += 1
        for player in self.players:
            player.play(is_winner, opponent)

    def get_players(self) -> list[Player]:
        """
        Returns a list of the players in the team.
        :return: The Players in the team.
        """
        return self.players

    def get_team_name(self) -> str:
        """
        Returns a name of the team.
        :return: The team name
        """
        return self.name

    def get_record(self) -> int:
        """
        Returns the record of the team.
        :return: The number of wins by a team.
        """
        return self.record

    def average_rating(self) -> int:
        """
        Returns the average rating of the Team.
        :return: The average rating of all the Players.
        """
        if not self.players:
            return 0
        total_rating = sum(player.get_rating() for player in self.players)
        return total_rating // len(self.players)
