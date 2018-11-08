from dragn.dice import D20

from dataclasses import dataclass
from models.weapons import Weapon


@dataclass
class Item:
    kind: str
    material: str

    def __str__(self):
        return f"{self.kind} of {self.material}"
