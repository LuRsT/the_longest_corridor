from typing import Any

from dragn.dice import D20

from dataclasses import dataclass
from models.weapons import Weapon


@dataclass
class Item:
    kind: str
    material: str

    def __str__(self):
        return f"{self.kind} of {self.material}"


@dataclass
class Scroll:
    name: str
    action: Any
    description: str

    def apply(self, character):
        self.action(character)
        return self.description.format(character.name)

    def __str__(self):
        return f"{self.name}"


@dataclass
class Food:
    kind: str
    amount: int

    def get_amount_string(self):
        amount_per_string = {
            5: "a bit of",
            10: "some",
            15: "a portion of",
            20: "a big chunk of",
        }
        for amount, string in amount_per_string.items():
            if self.amount < amount:
                return string
        return "a banquet of"

    def __str__(self):
        return f"{self.get_amount_string()} {self.kind}".title()
