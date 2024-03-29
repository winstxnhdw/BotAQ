from bot.utils import LocateOnScreen
from bot.console import clear_console, warn

class Mode:

    main_loop = lambda _: warn("Please implement the main loop.")

    def __init__(self):
        
        self.completed = False
        self.templates_directory = "templates/"
        self.format = ".png"
        self.confidence_threshold = 0.75
        self.locate_templates = LocateOnScreen(self.templates_directory, self.format, self.confidence_threshold, 0.2)

    def start(self):

        """
        This method should never be overriden. Please override main_loop() instead.
        """

        clear_console()

        while not self.completed:
            self.main_loop()

        print("Grind completed!")