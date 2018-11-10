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

    @property
    def difficulty(self) -> int:
        return self.material.difficulty_modifier + self.kind.difficulty_modifier

    @property
    def damage(self) -> int:
        return self.material.damage_modifier + self.kind.damage_modifier()

    def __str__(self) -> str:
        return f"{self.material} {self.kind}"

    @property
    def hit_str(self):
        return random.choice(self.kind.hit_choices)


IRON = Material("Iron", 2, 2)
STEEL = Material("Steel", 3, 4)
MITHRIL = Material("Mithril", 1, 8)

SWORD = WeaponKind("Sword", D4, 1, ["slashes"])
GREATSWORD = WeaponKind("Greatsword", D20, 6, ["slashes"])
MACE = WeaponKind("Mace", D12, 4, ["whacks"])
HALBERD = WeaponKind("Halberd", D6, 4, ["slices"])

NORMAL_WEAPONS = (Weapon(SWORD, IRON), Weapon(HALBERD, IRON), Weapon(SWORD, IRON))
