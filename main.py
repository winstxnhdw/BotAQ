import pyautogui as py
import math as m
import os

from datetime import time, datetime
class BotAQ:

    def __init__(self):

        print("Initialising bot...")
        
        self.delay = 0.4
        self.threshold = 0.8

    def path(self, name):

        templates = 'templates\\'
        imageformat = '.png'
        path = templates + name + imageformat

        return path

    def set_loadout(self):
        
        # Activate Imbue -> Enable Shield -> Equip Item -> Unequip Pet

        print("Entering prepartion phase...")

        # Find and clicks skills tab
        while py.locateOnScreen(self.path('skills'), grayscale=True, confidence=self.threshold) is None:
            os.system('cls')
            print("Finding skills tab...")
            time.sleep(self.delay)
        skillscoords = py.locateCenterOnScreen(self.path('skills'), grayscale=True, confidence=self.threshold)
        py.click(skillscoords)

        # Find and clicks imbue buff
        while py.locateOnScreen(self.path('imbue'), grayscale=True, confidence=self.threshold) is None:
            os.system('cls')
            print("Finding imbue...")
            time.sleep(self.delay)
        imbuecoords = py.locateCenterOnScreen(self.path('imbue'), grayscale=True, confidence=self.threshold)
        py.click(imbuecoords)
        
        # Find and clicks menu to exit skills
        while py.locateOnScreen(self.path('menu'), grayscale=True, confidence=self.threshold) is None:
            os.system('cls')
            print("Finding menu...")
            time.sleep(self.delay)
        menucoords = py.locateCenterOnScreen(self.path('menu'), grayscale=True, confidence=self.threshold)
        py.click(menucoords)

        # Find and enables shield ability
        while py.locateOnScreen(self.path('poseidon'), grayscale=True, confidence=self.threshold) is None:
            os.system('cls')
            print("Finding shield...")
            time.sleep(self.delay)
        poseidoncoords = py.locateCenterOnScreen(self.path('poseidon'), grayscale=True, confidence=self.threshold)
        py.click(poseidoncoords)

        # Find and clicks pets tab
        while py.locateOnScreen(self.path('pets'), grayscale=True, confidence=self.threshold) is None:
            os.system('cls')
            print("Finding pets tab...")
            time.sleep(self.delay)
        petscoords = py.locateCenterOnScreen(self.path('pets'), grayscale=True, confidence=self.threshold)
        py.click(petscoords)

        # Find and unequips item
        while py.locateOnScreen(self.path('hide'), grayscale=True, confidence=self.threshold) is None:
            os.system('cls')
            print("Finding pet to hide...")
            time.sleep(self.delay)
        hidecoords = py.locateCenterOnScreen(self.path('hide'), grayscale=True, confidence=self.threshold)
        py.click(hidecoords, clicks=2)

    def prepare(self):

        # Find and clicks items tab
        while py.locateOnScreen(self.path('items'), grayscale=True, confidence=self.threshold) is None:
            os.system('cls')
            print("Finding items tab...")
            time.sleep(self.delay)
        itemscoords = py.locateCenterOnScreen(self.path('items'), grayscale=True, confidence=self.threshold)
        py.click(itemscoords)

        # Find and equips item
        while py.locateOnScreen(self.path('sphere'), grayscale=True, confidence=self.threshold) is None:
            os.system('cls')
            print("Finding item...")
            time.sleep(self.delay)
        spherecoords = py.locateCenterOnScreen(self.path('sphere'), grayscale=True, confidence=self.threshold)
        py.click(spherecoords, clicks=2)
        
    def attack(self):
        os.system('cls')
        print("Attacking...")

         # Find and clicks spells tab
        while py.locateOnScreen(self.path('spells'), grayscale=True, confidence=self.threshold) is None:
            if self.check_death() == True:
                break

            os.system('cls')
            print("Finding spells tab...")
            time.sleep(self.delay)
        spellscoords = py.locateCenterOnScreen(self.path('spells'), grayscale=True, confidence=self.threshold)
        py.click(spellscoords)

        # Find and clicks Destruction Burst
        while py.locateOnScreen(self.path('db'), grayscale=True, confidence=self.threshold) is None:
            if self.check_death() == True:
                break

            os.system('cls')
            print("Finding spell...")
            time.sleep(self.delay)
        dbcoords = py.locateCenterOnScreen(self.path('db'), grayscale=True, confidence=self.threshold)
        py.click(dbcoords, clicks=2)

    def check_death(self):
        os.system('cls')
        print("Finding vitality signals...")
        if py.locateCenterOnScreen(self.path('killed'), grayscale=True, confidence=self.threshold):
            return True

        else:
            return False

def main():

    bot = BotAQ()
    xp = 19600
    totalxp = xp + (0.1 * xp)
    t = -1

    level = input("Adventurer Level (1 - 150)?: ")
    if int(level) >= 1 and int(level) <= 150:
        maxcycles = m.ceil(3 * 1.055**int(level) + 24 + 3 * 1.055**(int(level)**1.085) * 200 * 1.1 / totalxp)

    else:
        print("Incorrect input. Try again.\n")
        main()

    prepare = input("Prepare (y/n)?: ")
    if prepare == 'y':
        n = -1

    elif prepare == 'n':
        n = 0

    else:
        print("Incorrect input. Try again.\n")
        main()

    while True:
        # Find and click on Am-Boss
        while py.locateOnScreen(bot.path('amboss'), grayscale=True, confidence=bot.threshold) is None:
            if py.locateOnScreen(bot.path('levelled'), grayscale=True, confidence=bot.threshold):
                levelledcoords = py.locateCenterOnScreen(bot.path('levelled'), grayscale=True, confidence=bot.threshold)
                py.click(levelledcoords)
            os.system('cls')
            print("Finding Am-Boss...")
            time.sleep(bot.delay)
        ambosscoords = py.locateCenterOnScreen(bot.path('amboss'), grayscale=True, confidence=bot.threshold)
        py.click(ambosscoords)

        if n == -1:
            bot.set_loadout()

        bot.prepare()

        bot.attack()
        while bot.check_death() is False:
            os.system('cls')
            print("Continuing to attack...")
            bot.attack()

        killedcoords = py.locateCenterOnScreen(bot.path('killed'), grayscale=True, confidence=bot.threshold)
        py.click(killedcoords)
        
        if n >= maxcycles:
            exit()
        n += 1

        if t == -1:
            if datetime.now >= time(hour=1):
                n = 0
                t += 1

if __name__ == '__main__':
    main()