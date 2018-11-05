from dataclasses import dataclass
from typing import Any, List

from dragn.dice import *


@dataclass
class Material:
    name: str
    difficulty_modifier: int
    damage_modifier: int

    def __str__(self):
        return self.name


@dataclass
class Weapon:
    kind: str
    materials: List[Material]
    damage_modifier: Any
    difficulty_modifier: int = 0

    @property
    def difficulty(self) -> int:
        difficulty = 0
        for m in self.materials:
            difficulty += m.difficulty_modifier
        return difficulty + self.difficulty_modifier

    @property
    def damage(self) -> int:
        damage = 0
        for m in self.materials:
            damage += m.damage_modifier
        return damage + self.damage_modifier()

    def __str__(self) -> str:
        return f"{self.kind} made of {self.materials[0]}"


IRON = Material("Iron", 2, 2)
STEEL = Material("Steel", 3, 4)
MITHRIL = Material("Mithril", 1, 8)

SWORD = Weapon("Sword", [IRON], D4)
HALBERD = Weapon("Halberd", [IRON], difficulty_modifier=4, damage_modifier=D6)
MAGIC_SWORD = Weapon("Magic Sword", [MITHRIL], difficulty_modifier=4, damage_modifier=D6)
