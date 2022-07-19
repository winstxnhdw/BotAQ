import os

from libs.termbar import print_progress_bar
from pyautogui import locateCenterOnScreen, locateOnScreen, click, move
from atexit import register
from time import sleep
from json import load, dump
from math import floor, ceil
from argparse import ArgumentParser
from datetime import datetime as dt

class Exit:
    
    def __init__(self):

        self.n = 0
        self.cyclexp = 0
        self.lastxp = 0

    def exit_handler(self):

        print("Bot is shutting down...")
        totalxp = (self.n * self.cyclexp) + self.lastxp
        data = {'lastxp': totalxp}

        with open('data\\userdata.json', 'w') as outfile:
            dump(data, outfile, indent=4)

class BotAQ:

    def __init__(self, is_x_guardian):
        
        print("Initialising bot..")

        self.is_x_guardian = is_x_guardian

        self.delay = 0.4
        self.threshold = 0.75
        self.blank = "\033[A                             \033[A"

    def path(self, name):

        templates = 'templates\\'
        imageformat = '.png'
        path = templates + name + imageformat

        return path

    def calculate_total_cycles(self, level, cyclexp):

        """
        If player has reached the maximum level, the max daily gold cap is used instead.
        Source: https://adventurequestwiki.fandom.com/wiki/Big_List_of_AQ_Formulas#EXP/Gold_Caps

        :param level:       (int) Player's current level
        :param cyclexp:     (float) Player's current cyclexp

        :return cycles:     (int) Player's max cycles
        """

        multiplier = (1485 if self.is_x_guardian else 1350) if level < 150 else (495 if self.is_x_guardian else 450)
        cap = multiplier * (1.055**level + 1.055**(level**1.085) + 8)
        cycles = ceil(cap / cyclexp)

        return cycles

    def standard_locate_click(self, template_name, clicks=1):

        while locateOnScreen(self.path(template_name), grayscale=True, confidence=self.threshold) is None:
            print(self.blank)
            print(f"Finding {template_name.replace('_', ' ').title()}..")
            sleep(self.delay)

        coords = locateCenterOnScreen(self.path(template_name), grayscale=True, confidence=self.threshold)
        click(coords, clicks=clicks)

    def attack_locate_click(self, template_name, clicks=1):
        
        while locateOnScreen(self.path(template_name), grayscale=True, confidence=self.threshold) is None:
            if self.is_dead():
                return

            print(self.blank)
            print(f"Finding {template_name.replace('_', ' ').title()}..")
            sleep(self.delay)

        coords = locateCenterOnScreen(self.path(template_name), grayscale=True, confidence=self.threshold)
        click(coords, clicks=clicks)

    def set_loadout(self):
        
        # Unequips Pet
        print("Entering preparation phase...")

        # Find and clicks pets tab
        self.standard_locate_click('pets_tab')

        # Find and unequips item
        self.standard_locate_click('hide_button', 2)

    def prepare(self):

        # Find and clicks items tab
        self.standard_locate_click('items_tab')

        # Find and equips item
        self.standard_locate_click('oblivion_sphere', 2)
        
    def attack(self):

        print(self.blank)
        print("Attacking...")

        # Find and clicks spells tab
        self.attack_locate_click('spells_tab')

        # Find and clicks Destruction Burst
        self.attack_locate_click('destruction_burst', 2)

    def is_dead(self):

        print(self.blank)
        print("Finding vitality signals...")
        return locateCenterOnScreen(self.path('killed'), grayscale=True, confidence=self.threshold)

    def exceptions(self, level, cyclexp, maxcycles):

        # When player levels up
        if locateOnScreen(self.path('levelled'), grayscale=True, confidence=self.threshold):
            levelledcoords = locateCenterOnScreen(self.path('levelled'), grayscale=True, confidence=self.threshold)
            click(levelledcoords)
            level = level + 1
            maxcycles = self.calculate_total_cycles(level, cyclexp)

        # When player finds Z-Tokens
        elif locateCenterOnScreen(self.path('killed'), grayscale=True, confidence=self.threshold):
            killedcoords = locateCenterOnScreen(self.path('killed'), grayscale=True, confidence=self.threshold)
            click(killedcoords)

        return maxcycles, level

def incorrect_input():

    print("Incorrect input. Try again.\n\n")

def get_adventurer_level():

    level = int(input("Adventurer Level (1 - 150)?: "))

    if level < 1 or level > 150:
        incorrect_input()
        get_adventurer_level()

    return level

def get_userdata():

    clrdata = str(input("Do you want to clear your user data? (y/N): ")).lower()

    if clrdata == 'y':
        return True

    elif clrdata == 'n':
        if not os.path.exists("data\\userdata.json"):
            with open('data\\userdata.json', 'w') as outfile:
                data = {'lastxp': 0}
                dump(data, outfile, indent=4)

    else:
        incorrect_input()
        get_userdata()

    return False

def main(args):

    e = Exit()

    try:
        bot = BotAQ(True)

        try:
            with open('data\\bosses.json') as json_file:
                basexp = load(json_file)[args.boss]

        except SystemExit:
            raise Exception("There is no such boss. If this was intentional, please update the bosses.json file.")

        t = 0
        cyclexp = basexp + floor(0.1 * basexp)
        lastxp = 0
        prevcycles = 0
        x = 100 
        
        level = get_adventurer_level()
        maxcycles = bot.calculate_total_cycles(level, cyclexp)

        if not get_userdata():
            with open('data\\userdata.json') as json_file:
                lastxp = load(json_file)['lastxp']
                e.lastxp = lastxp
                prevcycles = lastxp / cyclexp

        prepare = str(input("Prepare (y/N)?: ")).lower()
        if prepare == 'y':
            n = -1

        elif prepare == 'n':
            n = 0

        else:
            print("Incorrect input. Try again.\n\n")
            main(args)

        # Initialise progress bar
        os.system('cls')
        print_progress_bar(prevcycles, maxcycles, prefix='Progress:', length=30)

        while True:
            # Find and click on the boss
            while locateOnScreen(bot.path(args.boss), grayscale=True, confidence=bot.threshold) is None:
                maxcycles, level = bot.exceptions(level, cyclexp, maxcycles)

                print(bot.blank)
                print("Finding boss...")
                move(x, 0)
                x += 10
                sleep(bot.delay)

            bosscoords = locateCenterOnScreen(bot.path(args.boss), grayscale=True, confidence=bot.threshold)
            click(bosscoords)

            # Set Loadout
            if n == -1:
                bot.set_loadout()
                n = 0

            n = prevcycles

            bot.prepare()

            # Attack
            while not bot.is_dead():
                print(bot.blank)
                print("Continuing to attack...")
                bot.attack()
                sleep(bot.delay)

            killedcoords = locateCenterOnScreen(bot.path('killed'), grayscale=True, confidence=bot.threshold)
            click(killedcoords)

            # Daily limit resets if system t is 1:00 P.M. GMT+8
            if t == 0 and n > 0:
                if dt.now().hour == 13:
                    n = -1
                    t = 1
            
            # Only check for daily limit reset once t is no longer 1:00 P.M.
            else:
                if dt.now().hour > 13:
                    t = 0
            
            # Exits if bot reaches daily limit
            if n >= maxcycles:
                register(e.exit_handler)
                exit()

            n += 1
            prevcycles = n

            # Update progress bar
            os.system('cls')
            print_progress_bar(n, maxcycles, prefix='Progress:', length=30)

            # Save current state
            e.n = n
            e.cyclexp = cyclexp

            register(e.exit_handler)
        
    except KeyboardInterrupt:
        print("\nManual exit detected.")

    finally:
        register(e.exit_handler)
        pass

def parse_args():

    parser = ArgumentParser(description='Finds the name of the boss to attack')
    parser.add_argument('-b', '--boss', type=str, metavar='', required=True, help='Name of boss to attack')

    return parser.parse_known_args()

if __name__ == '__main__':
    args, _ = parse_args()
    main(args)
