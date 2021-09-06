from libs.termbar import print_progress_bar

import os
import atexit
import json
import argparse
import pyautogui as auto
import math as m
import time as t
import datetime as dt

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

    def locate_equipment(self, item_name, clicks=1):

        while auto.locateOnScreen(self.path(item_name), grayscale=True, confidence=self.threshold) is None:
            print(self.blank)
            print(f"Finding {item_name}..")
            t.sleep(self.delay)

        coords = auto.locateCenterOnScreen(self.path(item_name), grayscale=True, confidence=self.threshold)
        auto.click(coords, clicks=clicks)

    def set_loadout(self):
        
        # Activate Imbue -> Enable Shield -> Equip Item -> Unequip Pet

        print("Entering preparation phase...")

        # Find and clicks skills tab
        self.set_equipment('skills')

        # Find and clicks imbue buff
        self.set_equipment('imbue')
        
        # Find and clicks menu to exit skills
        self.set_equipment('menu')

        # Find and enables shield ability
        self.set_equipment('shield')

        # Find and clicks pets tab
        self.set_equipment('pets')

        # Find and unequips item
        self.set_equipment('hide', 2)

    def prepare(self):

        # Find and clicks items tab
        self.set_equipment('items')

        # Find and equips item
        self.set_equipment('sphere', 2)
        
    def attack(self):

        print(self.blank)
        print("Attacking...")

         # Find and clicks spells tab
        while auto.locateOnScreen(self.path('spells'), grayscale=True, confidence=self.threshold) is None:
            if self.check_death() == True:
                break

            print(self.blank)
            print("Finding spells tab...")
            t.sleep(self.delay)

        spellscoords = auto.locateCenterOnScreen(self.path('spells'), grayscale=True, confidence=self.threshold)
        auto.click(spellscoords)

        # Find and clicks Destruction Burst
        while auto.locateOnScreen(self.path('db'), grayscale=True, confidence=self.threshold) is None:
            if self.check_death() == True:
                break

            print(self.blank)
            print("Finding spell...")
            t.sleep(self.delay)

        dbcoords = auto.locateCenterOnScreen(self.path('db'), grayscale=True, confidence=self.threshold)
        auto.click(dbcoords, clicks=2)

    def check_death(self):

        print(self.blank)
        print("Finding vitality signals...")
        if auto.locateCenterOnScreen(self.path('killed'), grayscale=True, confidence=self.threshold):
            return True

        else:
            return False

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
        
        level = input("Adventurer Level (1 - 150)?: ")
        if int(level) >= 1 and int(level) <= 150:
            level = int(level)
            maxcycles = bot.calc_cycles(level, cyclexp)

        else:
            print("Incorrect input. Try again.\n\n")
            main(args)

        clrdata = input("Do you want to clear your user data (y/n)?: ")
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

        prepare = input("Prepare (y/n)?: ")
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
                auto.move(x, None)
                x += 10
                t.sleep(bot.delay)

            bosscoords = auto.locateCenterOnScreen(bot.path(args.boss), grayscale=True, confidence=bot.threshold)
            auto.click(bosscoords)

            # Set Loadout
            if n == -1:
                bot.set_loadout()
                n = 0

            n = prevcycles

            bot.prepare()

            # Attack
            while bot.check_death() is False:
                print(bot.blank)
                print("Continuing to attack...")
                bot.attack()
                t.sleep(bot.delay)

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