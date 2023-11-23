import bot
import atexit

from load_file import save_data

# Boots up bot!

if __name__ == '__main__':
    bot.run_bot()
    atexit.register(lambda: save_data('player_data.csv', bot.save_players()))
