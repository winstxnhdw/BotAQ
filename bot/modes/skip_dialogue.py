from bot.modes import Mode
from bot.utils import LocateOnScreen, reset_cursor

class SkipDialogue(Mode):

    def __init__(self):

        super().__init__()
        self.locate_templates = LocateOnScreen(self.templates_directory, self.format, 0.8, 0)

    def main_loop(self):

        if self.locate_templates.click_if_located("win_button"):
            return

        elif self.locate_templates.click_if_located("more_button"):
            reset_cursor()
