import os
import atexit
import json
import argparse
import pyautogui as auto
import math as m
import datetime as dt

from libs.termbar import print_progress_bar
from time import sleep

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
            json.dump(data, outfile, indent=4)

class BotAQ:

    def __init__(self):
        
        print("Initialising bot...")

        self.delay = 0.4
        self.threshold = 0.75
        self.blank = "\033[A                             \033[A"

    def path(self, name):

        templates = 'templates\\'
        imageformat = '.png'
        path = templates + name + imageformat

        return path

    def calc_cycles(self, level, cyclexp):

        # Source: https://docs.google.com/spreadsheets/d/1xyQeKtqsUkorgTEs8IBzDEQ3qIoBXYbI9KkX3CoP04U/edit#gid=0
        xpcap = m.ceil(990*(1.055**level + 8 + 1.055**(level**1.085)))
        cycles = m.ceil(xpcap / cyclexp)
        return cycles

    def standard_locate_click(self, template_name, clicks=1):

        while auto.locateOnScreen(self.path(template_name), grayscale=True, confidence=self.threshold) is None:
            print(self.blank)
            print(f"Finding {template_name.replace('_', ' ').title()}..")
            sleep(self.delay)

        coords = auto.locateCenterOnScreen(self.path(template_name), grayscale=True, confidence=self.threshold)
        auto.click(coords, clicks=clicks)

    def attack_locate_click(self, template_name, clicks=1):
        
        while auto.locateOnScreen(self.path(template_name), grayscale=True, confidence=self.threshold) is None:
            if self.is_dead():
                return

            print(self.blank)
            print(f"Finding {template_name.replace('_', ' ').title()}..")
            sleep(self.delay)

        coords = auto.locateCenterOnScreen(self.path(template_name), grayscale=True, confidence=self.threshold)
        auto.click(coords, clicks=clicks)

    def set_loadout(self):
        
        # Activate Imbue -> Enable Shield -> Equip Item -> Unequip Pet
        print("Entering preparation phase...")

        # Find and clicks skills tab
        self.standard_locate_click('skills_tab')

        # Find and clicks imbue buff
        self.standard_locate_click('imbue_with_lore')
        
        # Find and clicks menu to exit skills
        self.standard_locate_click('menu_button')

        # Find and enables shield ability
        self.standard_locate_click('celtic_wheel')

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
        return auto.locateCenterOnScreen(self.path('killed'), grayscale=True, confidence=self.threshold)

    def exceptions(self, level, cyclexp, maxcycles):

        # When player levels up
        if auto.locateOnScreen(self.path('levelled'), grayscale=True, confidence=self.threshold):
            levelledcoords = auto.locateCenterOnScreen(self.path('levelled'), grayscale=True, confidence=self.threshold)
            auto.click(levelledcoords)
            level = level + 1
            maxcycles = self.calc_cycles(level, cyclexp)

        # When player finds Z-Tokens
        elif auto.locateCenterOnScreen(self.path('killed'), grayscale=True, confidence=self.threshold):
            killedcoords = auto.locateCenterOnScreen(self.path('killed'), grayscale=True, confidence=self.threshold)
            auto.click(killedcoords)

        return maxcycles, level

def main(args):

    try:
        bot = BotAQ()
        e = Exit()

        try:
            with open('data\\bosses.json') as json_file:
                basexp = json.load(json_file)[args.boss]

        except SystemExit:
            raise Exception("There is no such boss. If this was intentional, please update the bosses.json file.")

        t = 0
        cyclexp = basexp + m.floor(0.1 * basexp)
        lastxp = 0
        prevcycles = 0
        x = 100 
        
        level = int(input("Adventurer Level (1 - 150)?: "))
        if level >= 1 and level <= 150:
            level = int(level)
            maxcycles = bot.calc_cycles(level, cyclexp)

        else:
            print("Incorrect input. Try again.\n\n")
            main(args)

        clrdata = str(input("Do you want to clear your user data? (y/n): ")).lower()
        if clrdata == 'y':
            pass

        elif clrdata == 'n':
            if not os.path.exists("data\\userdata.json"):
                with open('data\\userdata.json', 'w') as outfile:
                    data = {'lastxp': 0}
                    json.dump(data, outfile, indent=4)
            
            else:
                with open('data\\userdata.json') as json_file:
                    lastxp = json.load(json_file)['lastxp']
                    e.lastxp = lastxp
                    prevcycles = lastxp / cyclexp

        else:
            print("Incorrect input. Try again.\n\n")
            main(args)

        prepare = str(input("Prepare (y/n)?: ")).lower()
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
            while auto.locateOnScreen(bot.path(args.boss), grayscale=True, confidence=bot.threshold) is None:
                maxcycles, level = bot.exceptions(level, cyclexp, maxcycles)

                print(bot.blank)
                print("Finding boss...")
                auto.move(x, 0)
                x += 10
                sleep(bot.delay)

            bosscoords = auto.locateCenterOnScreen(bot.path(args.boss), grayscale=True, confidence=bot.threshold)
            auto.click(bosscoords)

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

            killedcoords = auto.locateCenterOnScreen(bot.path('killed'), grayscale=True, confidence=bot.threshold)
            auto.click(killedcoords)

            # Daily limit resets if system t is 1:00 P.M. GMT+8
            if t == 0 and n > 0:
                if dt.datetime.now().hour == 13:
                    n = -1
                    t = 1
            
            # Only check for daily limit reset once t is no longer 1:00 P.M.
            else:
                if dt.datetime.now().hour > 13:
                    t = 0
            
            # Exits if bot reaches daily limit
            if n >= maxcycles:
                atexit.register(e.exit_handler)
                exit()

            n += 1
            prevcycles = n

            # Update progress bar
            os.system('cls')
            print_progress_bar(n, maxcycles, prefix='Progress:', length=30)

            # Save current state
            e.n = n
            e.cyclexp = cyclexp

            atexit.register(e.exit_handler)
        
    except KeyboardInterrupt:
        atexit.register(e.exit_handler)

def parse_args():

    parser = argparse.ArgumentParser(description='Finds the name of the boss to attack')
    parser.add_argument('-b', '--boss', type=str, metavar='', required=True, help='Name of boss to attack')

    return parser.parse_known_args()

if __name__ == '__main__':
    args, _ = parse_args()
    main(args)
