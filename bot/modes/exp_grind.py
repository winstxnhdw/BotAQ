from bot.modes import Grind

class ExperienceGrind(Grind):

    get_experience_cap = lambda self: self.get_gold_cap() * 3

    def main_loop(self):
        
        self.progress = self.character_details["dailyExp"]/self.get_experience_cap()
        super().main_loop()