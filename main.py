import os
import time
import atexit
import json
import argparse

import pyautogui as py
import math as m
import datetime as dt

from libs.termbar import *

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
        self.threshold = 0.7

    def path(self, name):

        templates = 'templates\\'
        imageformat = '.png'
        path = templates + name + imageformat

        return path

    def calc_cycles(self, level, cyclexp):

        cycles = m.ceil((990*(1.055**level + 8 + 1.055**(level**1.085))) / cyclexp)
        return cycles

    def set_loadout(self):
        
        # Activate Imbue -> Enable Shield -> Equip Item -> Unequip Pet

        print("Entering prepartion phase...")

        # Find and clicks skills tab
        while py.locateOnScreen(self.path('skills'), grayscale=True, confidence=self.threshold) is None:
            print ("\033[A                             \033[A")
            print("Finding skills tab...")
            time.sleep(self.delay)
        skillscoords = py.locateCenterOnScreen(self.path('skills'), grayscale=True, confidence=self.threshold)
        py.click(skillscoords)

        # Find and clicks imbue buff
        while py.locateOnScreen(self.path('imbue'), grayscale=True, confidence=self.threshold) is None:
            print ("\033[A                             \033[A")
            print("Finding imbue...")
            time.sleep(self.delay)
        imbuecoords = py.locateCenterOnScreen(self.path('imbue'), grayscale=True, confidence=self.threshold)
        py.click(imbuecoords)
        
        # Find and clicks menu to exit skills
        while py.locateOnScreen(self.path('menu'), grayscale=True, confidence=self.threshold) is None:
            print ("\033[A                             \033[A")
            print("Finding menu...")
            time.sleep(self.delay)
        menucoords = py.locateCenterOnScreen(self.path('menu'), grayscale=True, confidence=self.threshold)
        py.click(menucoords)

        # Find and enables shield ability
        while py.locateOnScreen(self.path('poseidon'), grayscale=True, confidence=self.threshold) is None:
            print ("\033[A                             \033[A")
            print("Finding shield...")
            time.sleep(self.delay)
        poseidoncoords = py.locateCenterOnScreen(self.path('poseidon'), grayscale=True, confidence=self.threshold)
        py.click(poseidoncoords)

        # Find and clicks pets tab
        while py.locateOnScreen(self.path('pets'), grayscale=True, confidence=self.threshold) is None:
            print ("\033[A                             \033[A")
            print("Finding pets tab...")
            time.sleep(self.delay)
        petscoords = py.locateCenterOnScreen(self.path('pets'), grayscale=True, confidence=self.threshold)
        py.click(petscoords)

        # Find and unequips item
        while py.locateOnScreen(self.path('hide'), grayscale=True, confidence=self.threshold) is None:
            print ("\033[A                             \033[A")
            print("Finding pet to hide...")
            time.sleep(self.delay)
        hidecoords = py.locateCenterOnScreen(self.path('hide'), grayscale=True, confidence=self.threshold)
        py.click(hidecoords, clicks=2)

    def prepare(self):

        # Find and clicks items tab
        while py.locateOnScreen(self.path('items'), grayscale=True, confidence=self.threshold) is None:
            print ("\033[A                             \033[A")
            print("Finding items tab...")
            time.sleep(self.delay)
        itemscoords = py.locateCenterOnScreen(self.path('items'), grayscale=True, confidence=self.threshold)
        py.click(itemscoords)

        # Find and equips item
        while py.locateOnScreen(self.path('sphere'), grayscale=True, confidence=self.threshold) is None:
            print ("\033[A                             \033[A")
            print("Finding item...")
            time.sleep(self.delay)
        spherecoords = py.locateCenterOnScreen(self.path('sphere'), grayscale=True, confidence=self.threshold)
        py.click(spherecoords, clicks=2)
        
    def attack(self):

        print ("\033[A                             \033[A")
        print("Attacking...")

         # Find and clicks spells tab
        while py.locateOnScreen(self.path('spells'), grayscale=True, confidence=self.threshold) is None:
            if self.check_death() == True:
                break

            print ("\033[A                             \033[A")
            print("Finding spells tab...")
            time.sleep(self.delay)
        spellscoords = py.locateCenterOnScreen(self.path('spells'), grayscale=True, confidence=self.threshold)
        py.click(spellscoords)

        # Find and clicks Destruction Burst
        while py.locateOnScreen(self.path('db'), grayscale=True, confidence=self.threshold) is None:
            if self.check_death() == True:
                break

            print ("\033[A                             \033[A")
            print("Finding spell...")
            time.sleep(self.delay)
        dbcoords = py.locateCenterOnScreen(self.path('db'), grayscale=True, confidence=self.threshold)
        py.click(dbcoords, clicks=2)

    def check_death(self):

        print ("\033[A                             \033[A")
        print("Finding vitality signals...")
        if py.locateCenterOnScreen(self.path('killed'), grayscale=True, confidence=self.threshold):
            return True

        else:
            return False

    def exceptions(self, level, cyclexp, maxcycles):

        # When player levels up
        if py.locateOnScreen(self.path('levelled'), grayscale=True, confidence=self.threshold):
            levelledcoords = py.locateCenterOnScreen(self.path('levelled'), grayscale=True, confidence=self.threshold)
            py.click(levelledcoords)
            level = level + 1
            maxcycles = self.calc_cycles(level, cyclexp)

        # When player finds Z-Tokens
        elif py.locateCenterOnScreen(self.path('killed'), grayscale=True, confidence=self.threshold):
            killedcoords = py.locateCenterOnScreen(self.path('killed'), grayscale=True, confidence=self.threshold)
            py.click(killedcoords)

        return maxcycles, level

def main(args):

    try:
        bot = BotAQ()

        with open('data\\bosses.json') as json_file:
            basexp = json.load(json_file)[args.boss]

        e = Exit()
        t = -1
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

        os.system('cls')
        printProgressBar(prevcycles, maxcycles, prefix='Progress:', length=30)

        while True:
            # Find and click on the boss
            while py.locateOnScreen(bot.path(args.boss), grayscale=True, confidence=bot.threshold) is None:
                maxcycles, level = bot.exceptions(level, cyclexp, maxcycles)

                print ("\033[A                             \033[A")
                print("Finding boss...")
                py.move(x, None)
                x += 10
                time.sleep(bot.delay)
            bosscoords = py.locateCenterOnScreen(bot.path(args.boss), grayscale=True, confidence=bot.threshold)
            py.click(bosscoords)

            if n == -1:
                bot.set_loadout()
                n = 0

            n = prevcycles

            bot.prepare()
            bot.attack()
            while bot.check_death() is False:
                print ("\033[A                             \033[A")
                print("Continuing to attack...")
                bot.attack()
                time.sleep(bot.delay)

            killedcoords = py.locateCenterOnScreen(bot.path('killed'), grayscale=True, confidence=bot.threshold)
            py.click(killedcoords)

            if t == -1 and n > 0:
                if dt.datetime.now().hour == 13 and dt.datetime.now().minute == 0:
                    n = 0
                    t += 1
            
            if n >= maxcycles:
                exit()
            n += 1
            prevcycles = n

            os.system('cls')
            printProgressBar(n, maxcycles, prefix='Progress:', length=30)

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