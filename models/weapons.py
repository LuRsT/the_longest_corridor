import random
from typing import Any, List

from dragn.dice import *

from dataclasses import dataclass


@dataclass
class Material:
    name: str
    difficulty_modifier: int
    damage_modifier: int

    def __str__(self):
        return self.name


@dataclass
class WeaponKind:
    name: str
    damage_modifier: Any
    difficulty_modifier: int
    hit_choices: List[str]

    def __str__(self) -> str:
        return self.name


@dataclass
class Weapon:
    kind: WeaponKind
    material: Material

    def __post_init__(self):
        self.kills = {}
        self.name = ""

    def register_kill(self, killed_char):
        race = str(killed_char.race)
        if race in self.kills:
            self.kills[race] += 1
        else:
            self.kills[race] = 1

        number_of_kills = sum([k for k in self.kills.values()])
        if number_of_kills > 3:
            self.name = "The thricekiller"

    @property
    def difficulty(self) -> int:
        return self.material.difficulty_modifier + self.kind.difficulty_modifier

    @property
    def damage(self) -> int:
        return self.material.damage_modifier + self.kind.damage_modifier()

    def __str__(self) -> str:
        if self.name:
            return f"{self.name}"
        else:
            return f"{self.material} {self.kind}"

    @property
    def hit_str(self):
        return random.choice(self.kind.hit_choices)

    @property
    def value(self):
        return self.material.damage_modifier + self.kind.damage_modifier.max_value


IRON = Material("Iron", 2, 2)
STEEL = Material("Steel", 3, 4)
MITHRIL = Material("Mithril", 1, 8)

SWORD = WeaponKind("Sword", D4, 1, ["slashes"])
GREATSWORD = WeaponKind("Greatsword", D20, 6, ["slashes"])
MACE = WeaponKind("Mace", D12, 4, ["whacks"])
HALBERD = WeaponKind("Halberd", D6, 4, ["slices"])

IRON_WEAPONS = (
    Weapon(SWORD, IRON),
    Weapon(HALBERD, IRON),
    Weapon(SWORD, IRON),
    Weapon(GREATSWORD, IRON),
)
STEEL_WEAPONS = (
    Weapon(SWORD, STEEL),
    Weapon(HALBERD, STEEL),
    Weapon(SWORD, STEEL),
    Weapon(GREATSWORD, STEEL),
)
MITHRIL_WEAPONS = (
    Weapon(SWORD, MITHRIL),
    Weapon(HALBERD, MITHRIL),
    Weapon(SWORD, MITHRIL),
    Weapon(GREATSWORD, MITHRIL),
)
