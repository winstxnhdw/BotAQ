from bot.modes import ExperienceGrind, GoldGrind, ChargeKindred
from bot.utils import warn, incorrect_input, clear_console

def get_bot_mode(modes: str) -> str:

    while True:
        [print(f"[{i}] {mode}") for i, mode in enumerate(modes)]

        try:
            return list(modes)[int(input(f"\nSelect mode (0 - {len(modes) - 1}): "))]

        except (ValueError, IndexError):
            incorrect_input()
            continue

def main():

    clear_console()

    modes = {
        "EXP Grind": ExperienceGrind,
        "Gold Grind": GoldGrind,
        "Charge Kindred": ChargeKindred
    }

    mode = get_bot_mode(modes.keys())

    try:
        modes.get(mode)().start()

    except KeyboardInterrupt:
        warn("\nManual exit detected.")

    finally:
        warn("Exiting..")