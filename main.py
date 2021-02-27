import pyautogui as autogui
import numpy as np
import time

class BotAQ:

    def __init__(self):
        
        templates = 'templates/'

        self.amboss = templates + 'amboss.png'
        self.db = templates + 'db.png'
        self.imbue = templates + 'imbue.png'
        self.menu = templates + 'menu.png'
        self.next = templates + 'next.png'
        self.skills = templates + 'skills.png'
        self.spells = templates + 'spells.png'

    def prep(self):
        pass

    def check_alive(self):

        if autogui.locateCenterOnScreen(self.next, grayscale=True, confidence=0.9):
            return True

        else:
            return False


def main():

    bot = BotAQ()
    delay = 5
    n = 0

    while True:
        ambosscoords = autogui.locateCenterOnScreen(bot.amboss, grayscale=True, confidence=0.9)

        while ambosscoords is False:
            time.sleep(delay)
        autogui.click(ambosscoords)

        # while autogui.locateCenterOnScreen(bot.amboss, grayscale=True, confidence=0.9) is False:
        #     time.sleep(delay)

        # if n == 0:
        #     bot.prep()

        time.sleep(delay)
        # n += 1

if __name__ == '__main__':
    main()