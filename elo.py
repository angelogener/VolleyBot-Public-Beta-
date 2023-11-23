from math import pow


def calculate_elo(my_rating: int, their_rating: int, games: int, is_winner: bool) -> int:
    """
    Precondition: win = 0 or 1
    Uses Elo's Formula to calculate a players new rating. Accounts for
    the difference in skill rating between the two players.


    :param my_rating: Player's Elo Rating
    :param their_rating: Another Player's Elo Rating or another
    Team's Average Rating
    :param games: The number of games the current Player has played.
    Determines the value to be gained/lost (k in formula)
    :param is_winner: True if the Player won. False if the Player lost.
    :return: The Player's new rank rating
    """
    if games > 5:
        k = 50
    else:
        k = 100

    den = 1 + pow(10, (their_rating - my_rating) / 400)
    estimate = 1 / den
    if is_winner:
        new_rating = my_rating + round(k*(1 - estimate))
    else:
        new_rating = my_rating - round(k * estimate)
    return new_rating
