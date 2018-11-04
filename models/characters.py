from dataclasses import dataclass

from dragn.dice import D20

from models.weapons import Weapon


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
            print(f"{self.name} hits {other.name} with their {self.weapon.name}")
            other.health -= self.weapon.damage
        else:
            print(f"{self.name} fails to hit {other.name}")
