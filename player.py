from elo import calculate_elo


class Player:
    """
    A Player playing Volleyball.

    Attributes:
        name (str): The name of the Player. In this case we take the name of the player as we
                    care more about their in-server name (Ex. Viborn#0420 -> Angelo)
        disc_id (int): A Player's unique Discord ID.
        rating (int): The calculated Elo rating of this Player.
        games_played (int): The running total of a Player's total number of games.
        wins (int): The Player's total wins to date.
    """

    def __init__(self, disc_id: int, name: str, rating: int, won: int, played: int):

        self.disc_id = disc_id
        self.name = name
        self.rating = rating
        self.wins = won
        self.games_played = played

    def play(self, is_winner: bool, opponent: int):
        """
        Calculates the new rank of the Player. Considers if the player won or not
        and the skill difference from two players. Adds result to the total
        games played and wins by the player
        :param is_winner: True if Player won. False if they lost.
        :param opponent: The Elo Ranking of the opponent(s).
        :return: None.
        """
        if is_winner:
            self.games_played += 1
            self.wins += 1
        else:
            self.games_played += 1

        self.rating = calculate_elo(self.rating, opponent, self.games_played, is_winner)

    def win_rate(self) -> float:
        """
        Returns the win percentage of the player given their games
        won vs games played.
        :return: The ratio of wins to total games played.
        """
        return self.wins / self.games_played

    def get_wins(self) -> int:
        """
        Returns the total wins to date.
        :return: The integer total of wins.
        """
        return self.wins

    def played_total(self) -> int:
        """
        Returns the total games played to date.
        :return: The integer total of games played.
        """
        return self.games_played

    def get_id(self) -> int:
        """
        Returns player's Discord ID.
        :return: Player's Discord ID.
        """
        return self.disc_id

    def get_name(self) -> str:
        """
        Returns player's current server name.
        :return: Player's current server name.
        """
        return self.name

    def get_rating(self) -> int:
        """
        Returns player's current elo rating.
        :return: Player's current elo rating.
        """
        return self.rating
