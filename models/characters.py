from dataclasses import dataclass

from dragn.dice import D20

from models.weapons import Weapon


@dataclass
class Character:
    name: str
    race: str
    weapon: Weapon
    health: int
    armor: int
    dex: int
    race: str

    @property
    def is_alive(self):
        if self.health <= 0:
            return False
        return True

    def attack(self, other):
        if self.dex + D20() > other.armor:
            print(f"{self.race} hits {other.race} with their {self.weapon.kind}")
            other.health -= self.weapon.damage
        else:
            print(f"{self.race} fails to hit {other.race}")
