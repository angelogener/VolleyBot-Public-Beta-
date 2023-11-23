import random
from datetime import date

from player import Player
from team import Team


def generate_balanced(people: list[Player]) -> dict[str, Team]:
    """
    Generates a dictionary of balanced teams from a list of people attending a session.
    Accounts for elo when making the teams. Higher rated players are split amongst each other
    and algorithm continues as we proceed through the list.
    Captains will point to the teams. Similar to generate_teams(), we want random team captains.
    This is so better players aren't stuck being team captains all the time.
    :param people: A list of Players
    :return: A dict of Teams
    """
    teams = len(people) // 6
    team_dict: dict[str, Team] = {}
    temp_players = []
    counter = 0
    balance = sorted(people, key=lambda x: x.rating, reverse=True)

    # Prepares lists
    for i in range(teams):
        temp_list = []
        temp_players.append(temp_list)

    # Numbers players as so: 1, 2, 3, 1, 2, 3 (etc. if at least 3 teams are made)
    for person in balance:
        if counter == teams:
            counter = 0
        temp_players[counter].append(person)
        counter += 1

    # Now pick a random member as the captain and shuffle the order within teams
    # Makes each team feel dynamic
    for group in temp_players:
        curr_cap = random.choice(group)
        group.remove(curr_cap)
        team_dict[curr_cap.get_name()] = Team(curr_cap.get_name(), date_string())
        team_dict[curr_cap.get_name()].add_player(curr_cap)
        random.shuffle(group)
        for player in group:
            team_dict[curr_cap.get_name()].add_player(player)
    return team_dict


def generate_teams(people: list[Player]) -> dict[str, Team]:
    """
    Generates a dictionary of random teams from a list of people attending a session.
    Captains will point to the teams.
    :param people: A list of Players
    :return: A dict of Teams
    """
    teams = len(people) // 6
    team_dict = {}
    captains = []
    counter = 0
    # Randomizes list of players
    random.shuffle(people)

    # Get the team captains
    i = 0
    while i < teams:
        curr_cap = people[i].get_name()
        captains.append(curr_cap)
        team_dict[curr_cap] = Team(curr_cap, date_string())
        i += 1

    # Numbers players as so: 1, 2, 3, 1, 2, 3 (etc. if at least 3 teams are made)
    for person in people:
        if counter == teams:
            counter = 0
        team_dict[captains[counter]].add_player(person)
        counter += 1

    return team_dict


def team_string(teams: dict[str, Team]) -> str:
    formatted = f"The following teams on **{date_string()}** are: \n" + "\n"
    for team, players in teams.items():
        # We assume that the first person is a team captain, list the number of players (including them) and re-add
        temp_string = f"***Team {team.title()}***" + f": **({len(players.get_players())} Players)** \n"
        for player in players.get_players():

            if player == players.get_players()[0]:
                temp_string += f"***---------------***\n"
                temp_string += f" - {player.get_name().title()}\n"
            # Otherwise we just add them as normal
            else:
                temp_string = f" - {player.get_name().title()}\n"

            formatted += temp_string

            # If we are past the first team, add a new line character
            if player == players.get_players()[-1]:
                formatted += "\n"
    formatted += f"**Have fun!**"
    return formatted


def date_string() -> str:
    curr_date = date.today()
    to_format = curr_date.strftime("%A, %B %d")
    return to_format
