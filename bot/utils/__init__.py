from bot.utils.locate_onscreen import LocateOnScreen
from json import load

import os

warn = lambda text, **kwargs : print(f"\x1b[33;20m{text}\x1b[0m", **kwargs)

def clear_console():

    os.system("cls") if os.name == 'nt' else os.system("clear")
    print("====== BotAQ ======\n")

def incorrect_input():

    clear_console()
    warn("Invalid input. Try again.\n")

def get_data(name: str) -> dict[str, any]:
    
    with open(f"data/{name}.json") as json_file:
        return load(json_file)