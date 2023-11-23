from team import Team


class Game:
    """
    A Game between two Teams. Who will be the winner?

    Attributes:
        team_one(Team): The first team in the game.
        team_two(Team): The other team in the game.
        first_winner(bool): True if the team_one won. False if team_two won.
    """

    def __init__(self, team_one: Team, team_two: Team):
        self.team_one = team_one
        self.team_two = team_two
        self.first_winner = None

    def play_game(self, name: str):
        if name == self.team_one.get_team_name():
            self.first_winner = True
            self.team_one.play_team(True, self.team_two.average_rating())
            self.team_two.play_team(False, self.team_one.average_rating())

        elif name == self.team_two.get_team_name():
            self.first_winner = False
            self.team_one.play_team(False, self.team_two.average_rating())
            self.team_two.play_team(True, self.team_one.average_rating())

    def get_winner(self) -> Team:
        """
        Precondition: get_winner() is called only after a winner was decided,
        ex. self.first_winner != None
        :return: The Team that won
        """
        if self.first_winner:
            return self.team_one
        else:
            return self.team_two

    def get_teams(self) -> tuple[Team, Team]:
        return self.team_one, self.team_two

    def get_team_names(self) -> tuple[str, str]:
        return self.team_one.get_team_name(), self.team_two.get_team_name()
