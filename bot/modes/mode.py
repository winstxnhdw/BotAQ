from bot.utils import LocateOnScreen

class Mode:

    def __init__(self):
        
        self.completed = False
        self.format = ".png"
        self.templates_directory = "templates/"
        self.threshold = 0.75
        self.locate_templates = LocateOnScreen(self.templates_directory, self.format, self.threshold, 0.2)

    def main_loop(self):
        pass

    def start(self):
        
        while not self.completed:
            self.main_loop()