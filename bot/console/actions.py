from os import system
from os import name as os_name

from bot.console import warn

def clear_console():

    system("cls") if os_name == 'nt' else system("clear")
    print("====== BotAQ ======\n")

def incorrect_input():

    clear_console()
    warn("Invalid input. Try again.\n")