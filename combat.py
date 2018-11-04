from dragn.dice import D6, D4, D20

from models.characters import Character
from models.weapons import SWORD, HALBERD


def simulate_fight(char1, char2):
    # TODO Determine who starts
    attacker, defender = char1, char_2
    while char1.is_alive and char_2.is_alive:
        attacker.attack(defender)
        attacker, defender = defender, attacker

    if not char1.is_alive:
        print(f"{char1.name} dies")
    else:
        print(f"{char_2.name} dies")


if __name__ == "__main__":
    simulate_fight(
        Character("Human", HALBERD, 30, 10, 10)
        Character("Orc", SWORD, 10, 10, 10)
    )
