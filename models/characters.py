from dragn.dice import D20

from dataclasses import dataclass
from models.weapons import Weapon


@dataclass
class Race:
    name: str
    health: int
    armor: int
    dex: int


@dataclass
class Character:
    name: str
    race: Race
    weapon: Weapon
    exp: int = 0
    level: int = 1

    def __post_init__(self):
        self.health = self.race.health
        self.armor = self.race.armor
        self.dex = self.race.dex

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
            print(f"{self.name} {self.weapon.hit_str} {other.name}")
            other.health -= self.weapon.damage
        else:
            print(f"{self.name} misses")

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


HUMAN = Race("Human", 20, 10, 10)
DWARF = Race("Dwarf", 25, 12, 9)
ELF = Race("Dwarf", 18, 8, 13)

ORC = Race("Orc", 10, 10, 10)
