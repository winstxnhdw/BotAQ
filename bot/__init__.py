from bot.modes import Mode, ExperienceGrind, GoldGrind, ChargeKindred
from bot.utils import warn, incorrect_input, clear_console

def get_bot_mode(modes: str) -> str:

    while True:
        [print(f"[{i}] {mode}") for i, mode in enumerate(modes)]

        try:
            mode_index = int(input(f"\nSelect mode (0 - {len(modes) - 1}): "))
            return list(modes)[mode_index]

        except (ValueError, IndexError):
            incorrect_input()
            continue

def main():

    clear_console()

    modes: dict[str, Mode] = {
        "EXP Grind": ExperienceGrind,
        "Gold Grind": GoldGrind,
        "Charge Kindred": ChargeKindred
    }

    mode = get_bot_mode(modes.keys())

    try:
        modes[mode]().start()

    except KeyboardInterrupt:
        warn("\nManual exit detected.")

    finally:
        warn("Exiting..")