from dragn.dice import D6, D4, D20

from models.characters import Character
from models.weapons import SWORD, HALBERD, MAGIC_SWORD


def simulate_fight(char1, char2):
    print(
        f"A {char1.race} yielding a {char1.weapon} attacks an {char2.race} who yields a {char2.weapon}..."
    )
    # TODO Determine who starts
    attacker, defender = char1, char2
    while char1.is_alive and char2.is_alive:
        attacker.attack(defender)
        attacker, defender = defender, attacker

    if not char1.is_alive:
        print(f"{char1.name} dies")
    else:
        print(f"{char2.name} dies")


if __name__ == "__main__":
    simulate_fight(
        Character("A", "Human", MAGIC_SWORD, 30, 10, 10),
        Character("B", "Orc", SWORD, 10, 10, 10),
    )
