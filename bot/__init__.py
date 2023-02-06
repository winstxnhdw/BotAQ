from bot.modes import Mode, SkipDialogue
from bot.modes import ExperienceGrind, GoldGrind
from bot.modes import ChargeKindred, ChargeBookOfBurns

from bot.console import warn, incorrect_input, clear_console

def get_bot_mode(modes: list[str]) -> str:

    while True:
        for i, mode in enumerate(modes):
            print(f"[{i}] {mode}")

        try:
            mode_index = int(input(f"\nSelect mode (0 - {len(modes) - 1}): "))
            return modes[mode_index]

        except (ValueError, IndexError):
            incorrect_input()

def main():

    clear_console()

    modes: dict[str, Mode] = {
        "EXP Grind": ExperienceGrind,
        "Gold Grind": GoldGrind,
        "Charge Kindred": ChargeKindred,
        "Charge Book of Burns": ChargeBookOfBurns,
        "Skip Dialogue": SkipDialogue
    }

    try:
        mode = get_bot_mode(list(modes.keys()))
        modes[mode]().start()

    except KeyboardInterrupt:
        warn("\nManual exit detected.")

    finally:
        warn("Exiting..")
