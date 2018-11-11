import random
import uuid
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

    def __gt__(self, other):
        return self.name > other.name


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
        return (self.material.damage_modifier + self.kind.damage_modifier.max_value) - (
            self.kind.difficulty_modifier + self.material.difficulty_modifier
        )


IRON = Material("Iron", 2, 2)
STEEL = Material("Steel", 3, 4)
MITHRIL = Material("Mithril", 1, 8)


WEAPON_KINDS = [
    WeaponKind("Sword", D4, 1, ["slashes"]),
    WeaponKind("Greatsword", D20, 6, ["slashes"]),
    WeaponKind("Mace", D12, 4, ["whacks"]),
    WeaponKind("Halberd", D6, 4, ["slices"]),
]


def get_iron_weapon():
    return Weapon(random.choice(WEAPON_KINDS), IRON)


def get_steel_weapon():
    return Weapon(random.choice(WEAPON_KINDS), STEEL)


def get_mithril_weapon():
    return Weapon(random.choice(WEAPON_KINDS), MITHRIL)
