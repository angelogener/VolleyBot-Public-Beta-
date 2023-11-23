import asyncio
import discord

from game import Game
from player import Player
from discord.ext import commands

from team_builder import generate_teams, generate_balanced, team_string
from load_file import load_data, save_data

# Global Variables
FILE_NAME = 'player_data.csv'
TOKEN = ''  # Replace with your bot token
intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

all_players = {}  # All users in server
players = []  # Player ID's with their Names for team builder
teams = {}  # A list of Teams
curr_game = None
curr_guild = None
in_channel = None


@bot.event
async def on_ready():
    """
    Prepares the bot for use. Will load player data.
    :return: None
    """
    global all_players
    all_players = load_data(FILE_NAME)

    print(f'{bot.user} is now running!')


@bot.command()
async def shuffle(ctx):
    global teams
    # Specifically add Planners as the sole role capable of using this command
    role_access = discord.utils.get(ctx.guild.roles, name="Planners")

    if role_access not in ctx.author.roles:
        # Non-planners will get no response
        return

    if not players:
        await ctx.send(f"Please update first!")
        return
    # In the case we try to make teams with less than 12 players
    if len(players) < 12:
        await ctx.send(f"You currently have **{len(players)} players.**\n"
                               f"You will need **{12 - len(players)} more players** to make at least two teams!")
        return

    # Now create teams...
    curr_players = []
    for num in players:
        curr_players.append(all_players[num])

    teams = generate_teams(curr_players)
    result = team_string(teams)
    # Simulate typing! Makes bot look busy
    async with ctx.typing():
        await asyncio.sleep(2)

    await ctx.send(result)
    return


@bot.command()
async def balance(ctx):
    global teams
    # Specifically add Planners as the sole role capable of using this command
    role_access = discord.utils.get(ctx.guild.roles, name="Planners")

    if role_access not in ctx.author.roles:
        # Non-planners will get no response
        return

    if not players:
        await ctx.send(f"Please update first!")
        return
    # In the case we try to make teams with less than 12 players
    if len(players) < 12:
        await ctx.send(f"You currently have **{len(players)} players.**\n"
                               f"You will need **{12 - len(players)} more players** to make at least two teams!")
        return

    # Now create teams...
    curr_players = []
    for num in players:
        curr_players.append(all_players[num])

    teams = generate_balanced(curr_players)
    result = team_string(teams)
    # Simulate typing! Makes bot look busy
    async with ctx.typing():
        await asyncio.sleep(2)

    await ctx.send(result)
    return


@bot.command()
async def creategame(ctx, *, disc_teams: str):
    """
    Creates a Game object from the Two teams.
    :param ctx: The message
    :param disc_teams: The string containing the Teams to pit against.
    :return: None
    """
    global curr_game

    # Specifically add Planners as the sole role capable of using this command
    role_access = discord.utils.get(ctx.guild.roles, name="Planners")

    if role_access not in ctx.author.roles:
        # Non-planners will get no response
        return

    if not teams:
        await ctx.send("Please make teams first!")
        return

    opponents = disc_teams.lower().split(',')
    gamers = []

    # Handles case where there weren't exactly "teams" within the string
    if len(opponents) != 2:
        await ctx.send("Must input two valid team names!")
        return
    # Off case where both strings identical. Weird right?
    if opponents[0] == opponents[1]:
        await ctx.send("Can't have the team play itself! What?")
        return

    # Get the two Teams for the brawl! Checks if both teams exist in the current team dictionary
    if opponents[0].strip() in teams:
        gamers.append(teams[opponents[0].strip()])
    else:
        await ctx.send("Game could not be played. Please add two valid teams.")
        return

    if opponents[1].strip() in teams:
        gamers.append(teams[opponents[1].strip()])
    else:
        await ctx.send("Game could not be played. Please add two valid teams.")
        return

    curr_game = Game(gamers[0], gamers[1])
    # Simulate typing! Makes bot look busy
    async with ctx.typing():
        await asyncio.sleep(2)
    await ctx.send(f"Prepare for the following matchup: \n"
                           f"***Team {curr_game.team_one.get_team_name().title()}*** vs "
                           f"***Team {curr_game.team_two.get_team_name().title()}***")
    return


@bot.command()
async def update(ctx):
    """
    Get the players that have last RSVP'd to the latest session and update the current
    list of players.
    :param ctx: The Message
    :return: None
    """

    # Obtain the server that the message was sent in
    global curr_guild, in_channel, players
    curr_guild = ctx.guild

    # Obtain this server's instance of Polls and Teams
    for text in curr_guild.text_channels:
        if text.name.lower() == "polls":
            in_channel = curr_guild.get_channel(text.id)

    await ctx.send("Obtained players who RSVP'd! Thank you for doing that!")

    # Specifically add Planners as the sole role capable of using this command
    role_access = discord.utils.get(curr_guild.roles, name="Planners")

    if role_access not in ctx.author.roles:
        # Non-planners will get no response
        await ctx.send("You don't have the necessary permissions to use this command.")
        return

    try:
        # Instantiate the checkmark emoji
        checkmark = '\U00002705'  # Unicode for the checkmark emoji
        reacted = []

        # Parse through the most recent 50 messages
        async for msg in in_channel.history(limit=5):

            # Checks if each of the last 50 messages contains the checkmark emoji
            if checkmark in [reaction.emoji for reaction in msg.reactions]:

                # Now goes through each of the users that reacted
                async for user in msg.reactions[0].users():
                    reacted.append(user.id)
                # We obtain all the users who reacted and fetch nicknames (if they have any)
                # We then try to add them to our list of players
                await ctx.send(f"Updating player roster!")

                await update_players(reacted)
                players = reacted
                # Simulate typing! Makes bot look busy
                async with ctx.typing():
                    await asyncio.sleep(2)
                await ctx.send(f"Ready!")

                return
        else:
            await ctx.send("No recent reactions found with the specified emoji.")
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")


@bot.command()
async def clear(ctx, value: int):
    """
    Purges the last 20 messages.
    """

    # Specifically add Planners as the sole role capable of using this command
    role_access = discord.utils.get(ctx.guild.roles, name="Planners")

    if role_access not in ctx.author.roles:
        # Non-planners will get no response
        await ctx.send("You don't have the necessary permissions to use this command.")
        return
    assert isinstance(value, int), await ctx.send(f"Not a valid number!")
    assert 0 < value < 51, await ctx.send(f"Can only be between 1 and 50 messages!")

    await ctx.channel.purge(limit=value + 1)  # Limit is set to '20 + 1' to include the command message
    await ctx.send(f'Cleared the last {value} messages.',
                   delete_after=5)  # Delete the confirmation message after 5 seconds


@bot.command()
async def winner(ctx, champ: str):
    """
    Declares the winning team of the game! Ensures all players from each team
    gets their ratings updated
    :param ctx: The message.
    :param champ: The string representation of the winning team
    :return: None
    """
    global curr_game

    # Specifically add Planners as the sole role capable of using this command
    role_access = discord.utils.get(ctx.guild.roles, name="Planners")

    if role_access not in ctx.author.roles:
        # Non-planners will get no response
        return

    if not curr_game:
        await ctx.send("Please make a game first!")
        return

    if champ.lower() not in curr_game.get_team_names():
        await ctx.send(f"Please enter a valid winner!")
        return

    curr_game.play_game(champ.lower())
    # Simulate typing! Makes bot look busy // ADDS SUSPENSE MUAHHAAH
    async with ctx.typing():
        await asyncio.sleep(2)
    await ctx.send(f"Congratulations to ***{curr_game.get_winner().get_team_name().title()}*** for taking the "
                           f"cake!")
    # Game is done! So we have no more current game!
    curr_game = None

    # Now we update the .csv with the changes
    save_data(FILE_NAME, all_players)


@bot.command()
async def delete(ctx, to_delete: str):
    """
    Delete the specified team.
    :param ctx: The message
    :param to_delete: The string representation of the team to be deleted
    :return: None
    """
    global teams
    if to_delete.lower() not in teams:
        await ctx.send(f"Please enter a valid team")
        return

    del teams[to_delete.lower()]


@bot.command()
async def addplayer(ctx, *, ctx_input: str):

    # Specifically add Planners as the sole role capable of using this command
    role_access = discord.utils.get(ctx.guild.roles, name="Planners")

    if role_access not in ctx.author.roles:
        # Non-planners will get no response
        return

    # Avoid infinite loops by ignoring messages from the bot itself
    if ctx.author == bot.user:
        return

    if not teams:
        await ctx.send("Please make teams first!")
        return

    words = ctx_input.lower().split(',')

    # Handles case where there weren't exactly "teams" within the string
    if len(words) != 2:
        await ctx.send("Must input a player and a team!")
        return

    mentioned_users = ctx.message.mentions

    if not mentioned_users:
        await ctx.send("Please mention which user to add!")
        return
    elif len(mentioned_users) > 1:
        await ctx

    person = mentioned_users[0]
    # If they have not been instantiated in all_players
    if person.id not in all_players:
        await update_players([person.id])

    # If they forgot to RSVP
    if person.id not in players:
        players.append(person.id)

    to_team = words[1].lower().strip()
    if to_team not in teams:
        await ctx.send("Please enter valid team!")
        return

    teams[to_team].add_player(all_players[person.id])
    await ctx.send(f"**{all_players[person.id].get_name().title()}** "
                           f"has joined **Team {teams[to_team].get_team_name().title()}**!")
    return


@bot.command()
async def removeplayer(ctx, *, ctx_input: str):

    # Specifically add Planners as the sole role capable of using this command
    role_access = discord.utils.get(ctx.guild.roles, name="Planners")

    if role_access not in ctx.author.roles:
        # Non-planners will get no response
        return

    # Avoid infinite loops by ignoring messages from the bot itself
    if ctx.author == bot.user:
        return

    if not teams:
        await ctx.send("Please make teams first!")
        return

    words = ctx_input.lower().split(',')

    # Handles case where there weren't exactly "teams" within the string
    if len(words) != 2:
        await ctx.send("Must input a player and a team!")
        return

    mentioned_users = ctx.message.mentions

    if not mentioned_users:
        await ctx.send("Please mention which user to add!")
        return
    elif len(mentioned_users) > 1:
        await ctx.send("Please mention one user!")
        return

    person = mentioned_users[0]

    to_team = words[1].lower().strip()
    if to_team not in teams:
        await ctx.send("Please enter valid team!")
        return

    # Can you remove player?
    in_team = False
    for player in teams[to_team].get_players():
        if player.get_id() == person.id:
            in_team = True
    if not in_team:
        await ctx.send("Player is not in team!")
        return

    teams[to_team].remove_player(all_players[person.id])
    await ctx.send(f"**{all_players[person.id].get_name().title()}** "
                           f"has left **Team {teams[to_team].get_team_name().title()}**!")
    return


@bot.command()
async def show(ctx):
    """
    Returns current iteration of all Teams.
    :param ctx: The Message.
    :return: None
    """
    # Simulate typing! Makes bot look busy
    async with ctx.typing():
        await asyncio.sleep(2)

    await ctx.send(team_string(teams))
    return


async def update_players(ids: list[str]) -> None:
    """
    Creates a dict of Players who RSVP'd and compares them to the players in the .csv file
    (players = {}) to see if any changes are to be made.
    Changes are made IF:
        - The player has been saved but has changed their display name (1)
        - The player does not yet exist in the data (1)

    Runs data through clean() to ensure we get the best possible username for teams and sharing.

    :param ids: A list containing the id's of players.
    :return: None
    """

    global all_players
    updated = {}
    for reacted in ids:
        member = await curr_guild.fetch_member(reacted)

        # 1: The player has been saved but has changed their display name
        if member.id in all_players and member.display_name != all_players[member.id].name:
            if clean(member.display_name):
                # Changes all_players directly
                all_players[member.id].name = member.display_name.lower()

        # 2: The player does not yet exist in the data
        elif member.id not in all_players:
            if clean(member.display_name):
                updated[member.id] = Player(member.id, member.display_name.lower(), 1200, 0, 0)
            else:
                updated[member.id] = Player(member.id, member.name.lower(), 1200, 0, 0)

    all_players.update(updated)


def save_players() -> dict[Player]:
    """
    In the event that a game is played or the bot ends,
    write and save changes to a file.
    """
    return all_players


def clean(username: str) -> bool:
    """
    Checks if the username is a "clean" string that can be used in csv for saving
    :param username: The username to check
    :return: True if username can be used in csv
    """
    return isinstance(username, str) and all(ord(char) < 128 for char in username)


def run_bot():
    bot.run(TOKEN)
