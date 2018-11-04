from dataclasses import dataclass

from dragn.dice import D6, D4, D20
from typing import Any


@dataclass
class Weapon:
    type: str
    dificulty: int
    damage: Any


@dataclass
class Character:
    name: str
    weapon: Weapon
    health: int
    armor: int
    dex: int

    @property
    def is_alive(self):
        if self.health <= 0:
            return False
        return True

    def attack(self, other):
        if self.dex + D20() > other.armor:
            print(f"{self.name} hits {other.name} with their {self.weapon.type}")
            other.health -= self.weapon.damage()
        else:
            print(f"{self.name} fails to hit {other.name}")


def simulate_fight():
    sword = Weapon("Sword", 2, D6)
    halberd = Weapon("Halberd", 4, D4 * 2)

    one_character = Character("Human", sword, 10, 10, 10)
    second_character = Character("Orc", halberd, 10, 10, 10)

    attacker, defender = one_character, second_character
    while one_character.is_alive and second_character.is_alive:
        attacker.attack(defender)
        attacker, defender = defender, attacker

    if not one_character.is_alive:
        print("One dies")
    else:
        print("Two dies")


if __name__ == "__main__":
    simulate_fight()
