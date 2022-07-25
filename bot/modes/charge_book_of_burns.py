from bot.modes import Mode

class ChargeBookOfBurns(Mode):

    def main_loop(self):
        
        self.locate_templates.wait_until_clicked("attack_tab")
        self.locate_templates.wait_until_clicked("stoke_the_flames")