import random

from combat import fight
from models.corridor import Corridor
from text import epilogue, intro, run_corridor


def simulate_fight(char1, char2):
    print(
        f"A {char1.race} yielding a {char1.weapon} attacks an {char2.race} who yields a {char2.weapon}..."
    )
    char1, char2 = fight(char1, char2)

    if not char1.is_alive:
        print(f"{char1.name} dies")
        print(f"{char2.name} ends up with {char2.health} HP")
    else:
        print(f"{char2.name} dies")
        print(f"{char1.name} ends up with {char1.health} HP")


def main():
    """
    This is a draft structure for the book generator

    Intro
    Corridor Creation
    One Chapter per adventurer
    Epilogue
    """

    corridor = Corridor()

    print("\n## Introduction\n")
    print(intro(corridor.item))
    print()

    print("\n## The corridor\n")
    print(corridor.get_history())
    print()

    messages = run_corridor(corridor)
    for m in messages:
        print(m)
    print()

    print("\n## Epilogue\n")
    epilogue()

    print("\n## Appendix\n\n")
    for s in corridor.stats():
        print(s)


if __name__ == "__main__":
    main()

    # from combat import simulate_fight
    # simulate_fight(
    #     Character("A", "Human", WEAPONS["sword"], 30, 10, 10),
    #     Character("B", "Orc", WEAPONS["halberd"], 10, 10, 10),
    # )
