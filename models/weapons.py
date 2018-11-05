from dataclasses import dataclass
from typing import Any, List

from dragn.dice import *


@dataclass
class Material:
    name: str
    difficulty_modifier: int
    damage_modifier: int


@dataclass
class Weapon:
    name: str
    materials: List[Material]
    damage_modifier: int = 0
    difficulty_modifier: int = 0

    @property
    def difficulty(self):
        difficulty = 0
        for m in self.materials:
            difficulty += m.difficulty_modifier
        return difficulty + self.difficulty_modifier

    @property
    def damage(self) -> int:
        damage = 0
        for m in self.materials:
            damage += m.damage_modifier
        return damage + self.damage_modifier


IRON = Material("Iron", 2, 2)

SWORD = Weapon("Sword", [IRON])
HALBERD = Weapon("Halberd", [IRON], difficulty_modifier=4, damage_modifier=2)
