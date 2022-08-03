from bot.console import log, underscore_to_title

from time import sleep
from pyautogui import locateOnScreen, center, click
from typing_extensions import Self

class LocateOnScreen:

    log_action = lambda _, template_name: log(f"Finding {underscore_to_title(template_name)}..")

    def __init__(self, template_directory, template_format, confidence, delay, grayscale=True):

        self.template_directory = template_directory
        self.template_format = template_format
        self.confidence = confidence
        self.delay = delay
        self.grayscale = grayscale

    def located(self, template_name) -> tuple[float, float, float, float] | None:
        
        sleep(self.delay)

        return locateOnScreen(
            f"{self.template_directory}{template_name}{self.template_format}",
            confidence=self.confidence,
            grayscale=self.grayscale
        )

    def wait_until_clicked(self, template_name, clicks=1) -> Self:

        coordinates = None
        
        while not coordinates:
            coordinates = self.located(template_name)
            self.log_action(template_name)

        else:
            self.click_centre(coordinates, clicks)

        return self

    def click_if_located(self, template_name, clicks=1) -> bool:

        self.log_action(template_name)
        coordinates = self.located(template_name)
        
        return self.click_centre(coordinates, clicks)

    def click_centre(self, coordinates, clicks) -> bool:

        if coordinates:
            click(center(coordinates), clicks=clicks)

        return bool(coordinates)