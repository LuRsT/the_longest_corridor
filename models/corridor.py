import random

from models.characters import Character
from models.items import Item
from models.weapons import NORMAL_WEAPONS
from text import get_corpora, get_str_from_rules


class Corridor:
    def __init__(self):
        self.item = create_item()

        monsters = [create_enemy() for _ in range(5)]

        self.corridor = [*monsters, self.item][::-1]
        self.index = len(self.corridor)

    def get_history(self):
        corridor_history = f"The corridor was created by a God who laid out some creatures, and finally, left the {self.item}"
        return corridor_history

    # def get_corridor(self):
    #    return self.corridor[::-1]

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == 0:
            raise StopIteration
        self.index -= 1
        return self.corridor[self.index]

    def shuffle(self):
        for c in self.corridor:
            if isinstance(c, Character):
                c.resurrect()
        self.index = len(self.corridor)


def create_enemy():
    return Character(
        random.choice(get_corpora("enemy_names")),
        "Orc",
        random.choice(NORMAL_WEAPONS),
        10,
        10,
        10,
    )


def create_item():
    return Item(
        random.choice(get_corpora("objects")), random.choice(get_corpora("materials"))
    )
