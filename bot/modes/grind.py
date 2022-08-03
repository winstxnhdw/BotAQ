from bot.modes import Mode
from bot.utils import LocateOnScreen, reset_cursor

from bot.console import incorrect_input, clear_console, log
from bot.console import warn, underscore_to_title

from urllib.request import Request, urlopen
from urllib.error import HTTPError
from json import load, loads, dump
from json.decoder import JSONDecodeError

from os import listdir
from os.path import isfile
from math import ceil

class Grind(Mode):

    def __init__(self):

        super().__init__()
        self.get_character_detail_url = lambda id: f"https://account.battleon.com/charpage/details?id={id}"
        self.fight_end_template = "win_button"
        self.userdata_path = "data/userdata.json"
        self.progress = 0.0

        self.character_id = self.get_character_id()
        self.character_details = self.get_character_details()
        self.is_x_guardian = self.character_details["type"] == "X-Guardian"

        boss_template_directory = f"{self.templates_directory}/bosses/"
        self.boss_name = self.get_boss_name(boss_template_directory)
        self.locate_bosses = LocateOnScreen(boss_template_directory, self.format, self.confidence_threshold, 0.5)


    def get_character_id(self):

        clear_console()

        if isfile(self.userdata_path):
            with open(self.userdata_path) as json_file:
                try:
                    return int(load(json_file).get("character_id"))

                except (JSONDecodeError, ValueError, TypeError):
                    warn(
                        f"{self.userdata_path} is found but the data has been corrupted.",
                        "Recreating JSON data..\n"
                    )

        while True:
            try:
                character_id = int(input("Enter your Character ID: "))

            except ValueError:
                incorrect_input()

            else:
                with open(self.userdata_path, "w") as json_file:
                    dump({"character_id": character_id}, json_file, indent=2)
                    return character_id

    def get_character_details(self) -> dict[str, int | str]:

        request = Request(self.get_character_detail_url(self.character_id), headers={
            "User-Agent": "Mozilla/5.0"
        })
        
        try:
            with urlopen(request) as response:
                return loads(response.read())["details"]

        except (HTTPError, KeyError):
            warn(
                "Could not retrieve character details from the battleon API.",
                f"Please check if the following URL endpoint is accessible: {self.get_character_detail_url(10)}"
            )
            raise

    def get_gold_cap(self) -> float:

        # Source: https://github.com/nivp/aq_classic_launcher/blob/master/index.js
        level: int = self.character_details["level"]
        cap = ceil((1.055**level + 1.055**(level**1.085) + 8) * 450)
        
        return cap if not self.is_x_guardian else cap * 1.1

    def get_boss_name(self, boss_template_directory: str) -> str:

        clear_console()
        
        boss_names = [file.split('.')[0] for file in listdir(boss_template_directory) if isfile(f"{boss_template_directory}/{file}")]
        max_boss_index = len(boss_names) - 1

        while True:
            [print(f"[{i}] {underscore_to_title(boss_name)}") for i, boss_name in enumerate(boss_names)]

            try:
                boss_index = int(input(f"\nBoss index (0 - {max_boss_index}): "))
                return boss_names[boss_index]

            except (ValueError, IndexError):
                incorrect_input()

    def print_progress_bar(self, progress, length=50):
        
        filled_length = int(length * progress)
        bar = f"{'█'*filled_length}{'-'*(length - filled_length)}"

        print(f"Progress: |{bar}| {progress*100:.2f}%\n")

    def prepare_buffs(self):
        
        log("Preparing buffs..")

        (
            self.locate_templates.wait_until_clicked("items_tab")
                                 .wait_until_clicked("oblivion_sphere", 2)
        )

    def attack(self):

        log("Attacking..")
        self.locate_templates.click_if_located("spells_tab")
        self.locate_templates.click_if_located("destruction_burst", 2)

    def main_loop(self):

        clear_console()
        self.print_progress_bar(self.progress)
        self.completed = self.progress >= 100.0

        while not self.locate_bosses.located(self.boss_name):
            reset_cursor()
            self.locate_bosses.log_action(self.boss_name)
            self.locate_templates.click_if_located(self.fight_end_template) # if player got z-token
            self.locate_templates.click_if_located("level_up_button") # if the player is dead or has levelled up

        self.locate_bosses.click_if_located(self.boss_name)
        self.prepare_buffs()
    
        while not self.locate_templates.located(self.fight_end_template):
            self.attack()

        self.locate_templates.wait_until_clicked(self.fight_end_template)
        self.character_details = self.get_character_details()