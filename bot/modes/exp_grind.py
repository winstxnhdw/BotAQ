from bot.modes import Grind

class ExperienceGrind(Grind):

    def get_experience_cap(self) -> float:

        return self.get_gold_cap() * 3

    def main_loop(self):
        
        self.progress = self.get_character_details().get("dailyExp")/self.get_experience_cap()
        super().main_loop()