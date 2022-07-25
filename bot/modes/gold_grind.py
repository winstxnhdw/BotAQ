from bot.modes import Grind

class GoldGrind(Grind):

    def main_loop(self):
        
        self.progress = self.character_details["dailyGold"]/self.get_gold_cap()
        super().main_loop()