from dragn.dice import D20

from dataclasses import dataclass
from models.weapons import Weapon


@dataclass
class Character:
    name: str
    race: str
    weapon: Weapon
    health: int
    armor: int
    dex: int
    exp: int = 0
    level: int = 1

    def __post_init__(self):
        self._original_health = self.health

    def resurrect(self):
        self.health = self._original_health

    @property
    def is_alive(self):
        if self.health <= 0:
            return False
        return True

    def attack(self, other):
        if self.dex + D20() > other.armor:
            print(f"{self.name} hits {other.name} with their {self.weapon}")
            other.health -= self.weapon.damage
        else:
            print(f"{self.name} fails to hit {other.name}")

    @property
    def value(self):
        return 5

    def gain_exp(self, other):
        self.exp += other.value
        self.maybe_level_up()

    def maybe_level_up(self):
        lvl_by_xp = {2: 10, 3: 50, 4: 100, 5: 250}
        for lvl, xp in lvl_by_xp.items():
            if self.level >= lvl:
                continue

            if self.exp >= xp:
                self.level = lvl
                self.level_up()
                break

    def level_up(self):
        print("###### LEVEL UP!! #####")
        self.dex += 1
        self.armor += 1
        self.health += 5

    @property
    def stats(self):
        print(
            f"DEX: {self.dex} ARMOR: {self.armor} "
            f"HP: {self.health} WEAPON: {self.weapon}"
            f"LEVEL: {self.level}"
        )
