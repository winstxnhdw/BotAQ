import pyautogui as py
import math as m
import datetime as dt
import os, time, atexit, json

from libs.termbar import *
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

def main():

    bot = BotAQ()
    newlevel = 0
    t = -1
    basexp = 19600
    cyclexp = basexp + (0.1 * basexp)
    lastxp = 0
    x = 100 
    
    level = input("Adventurer Level (1 - 150)?: ")
    if int(level) >= 1 and int(level) <= 150:
        maxcycles = m.ceil((3 * 1.055**int(level) + 24 + 3 * 1.055**(int(level)**1.085) * 200 * 1.1) / cyclexp)

    else:
        print("Incorrect input. Try again.\n\n")
        main()

    clrdata = input("Do you want to clear your user data (y/n)?: ")
    if clrdata == 'y':
        pass

    elif clrdata == 'n':
        with open('usr\\userdata.json', 'w') as outfile:
            data = {'lastxp': 0}
            json.dump(data, outfile, indent=4)

        with open('usr\\userdata.json') as json_file:
            lastxp = json.load(json_file)['lastxp']
            maxcycles = m.ceil(((3 * 1.055**int(level) + 24 + 3 * 1.055**(int(level)**1.085) * 200 * 1.1) - lastxp) / cyclexp)

    else:
        print("Incorrect input. Try again.\n\n")
        main()

    prepare = input("Prepare (y/n)?: ")
    if prepare == 'y':
        n = -1

    elif prepare == 'n':
        n = 0

    else:
        print("Incorrect input. Try again.\n\n")
        main()

    os.system('cls')
    if n == -1:
        printProgressBar(0, maxcycles, prefix='Progress:', suffix='Complete', length=30)

    else:
        firstprogress = lastxp / cyclexp
        printProgressBar(firstprogress, maxcycles, prefix='Progress:', suffix='Complete', length=30)

    while True:
        # Find and click on Am-Boss
        while py.locateOnScreen(bot.path('amboss'), grayscale=True, confidence=bot.threshold) is None:
            # When player levels up
            if py.locateOnScreen(bot.path('levelled'), grayscale=True, confidence=bot.threshold):
                levelledcoords = py.locateCenterOnScreen(bot.path('levelled'), grayscale=True, confidence=bot.threshold)
                py.click(levelledcoords)
                newlevel = int(level) + 1 + newlevel
                maxcycles = m.ceil((3 * 1.055**newlevel + 24 + 3 * 1.055**(newlevel**1.085) * 200 * 1.1) / cyclexp)

            # When player finds Z-Tokens
            elif py.locateCenterOnScreen(bot.path('killed'), grayscale=True, confidence=bot.threshold):
                killedcoords = py.locateCenterOnScreen(bot.path('killed'), grayscale=True, confidence=bot.threshold)
                py.click(killedcoords)

            print ("\033[A                             \033[A")
            print("Finding Am-Boss...")
            py.move(x, None)
            x += 10
            time.sleep(bot.delay)
        ambosscoords = py.locateCenterOnScreen(bot.path('amboss'), grayscale=True, confidence=bot.threshold)
        py.click(ambosscoords)

        if n == -1:
            bot.set_loadout()
            n = 0

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
            if dt.datetime.now().hour >= 1:
                n = 0
                t += 1
        
        if n >= maxcycles:
            exit()
        n += 1

        os.system('cls')
        printProgressBar(n, maxcycles, prefix='Progress:', suffix='Complete', length=30)

    atexit.unregister(exit_handler)
    atexit.register(exit_handler, n, cyclexp, lastxp)

def exit_handler(n, cyclexp, lastxp=0):

    print("Bot is shutting down...")
    print(n)
    totalxp = (n * cyclexp) + lastxp
    data = {'lastxp': totalxp}

    with open('usr\\userdata.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)

if __name__ == '__main__':
    if not os.path.exists('usr'):
        os.makedirs('usr')

    main()