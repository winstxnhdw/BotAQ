from bot.modes import Mode

class ChargeKindred(Mode):

    def main_loop(self):
        
        self.locate_templates.wait_until_clicked("skills_tab")
        self.locate_templates.wait_until_clicked("kindred_focus_button")