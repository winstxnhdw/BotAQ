from bot.utils import LocateOnScreen
from bot.console import clear_console, warn

class Mode:

    def __init__(self):
        
        self.completed = False
        self.templates_directory = "templates/"
        self.format = ".png"
        self.confidence_threshold = 0.75
        self.locate_templates = self.set_locate_templates(self.templates_directory, self.format, self.confidence_threshold, 0.2)

    def main_loop(self):
        
        warn("Main loop is not implemented.")

    def start(self):
        
        clear_console()

        while not self.completed:
            self.main_loop()

    def set_locate_templates(self, templates_directory: str, format: str, confidence_threshold: float, timeout: float):
        
        return LocateOnScreen(templates_directory, format, confidence_threshold, 0.2)