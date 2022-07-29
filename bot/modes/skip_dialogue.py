from bot.modes import Mode
from bot.utils import LocateOnScreen, reset_cursor

class SkipDialogue(Mode):

    def __init__(self):

        super().__init__()
        self.locate_templates = LocateOnScreen(self.templates_directory, self.format, self.confidence_threshold, 0)

    def main_loop(self):

        self.locate_templates.wait_until_clicked("more_button")
        reset_cursor()
