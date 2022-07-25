from bot.modes import Mode
from bot.utils import LocateOnScreen, incorrect_input, clear_console, get_data, warn

from urllib.request import Request, urlopen
from urllib.error import HTTPError
from math import ceil
from json import loads
from os import listdir
from os.path import isfile, join

from pyautogui import moveTo

class Grind(Mode):

    def __init__(self):

        super().__init__()
        self.progress = 0.0
        self.character_id = get_data("userdata")["character_id"]
        self.character_details = self.get_character_details()
        self.is_x_guardian = True if self.character_details["type"] == "X-Guardian" else False

        boss_template_directory = f"{self.templates_directory}/bosses/"
        self.boss_name = self.get_boss_name(boss_template_directory)
        self.locate_bosses = LocateOnScreen(boss_template_directory, self.format, self.threshold, 1)

    def get_character_details(self) -> dict[str, any]:

        request = Request(f"https://account.battleon.com/charpage/details?id={self.character_id}", headers={"User-Agent": "Mozilla/5.0"})
        
        try:
            with urlopen(request) as response:
                return loads(response.read())["details"]

        except (HTTPError, KeyError):
            warn("Could not retrieve character details from the battleon API.")
            warn("Please check if the following URL endpoint is accessible: https://account.battleon.com/charpage/details?id=10")
            raise

    def get_gold_cap(self) -> float:

        level: int = self.character_details["level"]
        cap: float = ceil((1.055**level + 1.055**(level**1.085) + 8) * 450)
        
        return cap if not self.is_x_guardian else cap * 1.1

    def get_boss_name(self, boss_template_directory: str) -> str:

        clear_console()
        boss_names = [file.split('.')[0] for file in listdir(boss_template_directory) if isfile(join(boss_template_directory, file))]
        max_boss_index = len(boss_names) - 1

        while True:
            [print(f"[{i}] {boss_name}") for i, boss_name in enumerate(boss_names)]

            try:
                boss_index = int(input(f"\nBoss index (0 - {max_boss_index}): "))
                return boss_names[boss_index]

            except (ValueError, IndexError):
                incorrect_input()
                continue

    def print_progress_bar(self, progress, length=100):
        
        clear_console()
        filled_length = int(length * progress)
        bar = f"{'█'*filled_length}{'-'*(length - filled_length)}"
        print(f"Progress: |{bar}| {progress*100:.2f}\n")

    def prepare_buffs(self):
        
        print("Preparing buffs..")
        self.locate_templates.wait_until_clicked("items_tab")
        self.locate_templates.wait_until_clicked("oblivion_sphere", 2)

    def attack(self):

        print("Attacking..")
        self.locate_templates.wait_until_clicked("spells_tab")
        self.locate_templates.wait_until_clicked("destruction_burst", 2)

    def main_loop(self):

        self.print_progress_bar(self.progress)
        self.completed = self.progress >= 100.0
        fight_end_template = "killed_button"

        while not self.locate_bosses.located(self.boss_name):
            moveTo(50, 50)
            self.locate_bosses.log_action(self.boss_name)

            # Check if dead or has levelled up
            self.locate_templates.click_if_located(fight_end_template)
            self.locate_templates.click_if_located("level_up_button")

        self.locate_bosses.click_if_located(self.boss_name)
        self.prepare_buffs()

        while not self.locate_templates.located(fight_end_template):
            self.attack()

        self.locate_templates.click_if_located(fight_end_template)
        self.character_details = self.get_character_details()