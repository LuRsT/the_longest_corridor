import random

from models.characters import ORC, Character, GOBLIN
from models.items import Item, Food
from models.weapons import NORMAL_WEAPONS
from text import get_corpora, get_str_from_rules


class Corridor:
    def __init__(self):
        self.item = create_item()

        monsters = [create_enemy() for _ in range(15)]
        food = [create_food() for _ in range(3)]

        stuff_in_corridor = [*monsters, *food]
        random.shuffle(stuff_in_corridor)

        self.corridor = [*stuff_in_corridor, self.item][::-1]
        self.index = len(self.corridor)

    def get_history(self):
        corridor_history = f"The corridor was created by a God who laid out some creatures, a bit of food, and finally, left the {self.item}"
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
    enemy = random.choice([
        create_orc,
        create_goblin,
    ])
    return enemy()

def create_orc():
    return Character(
        random.choice(get_corpora("enemy_names")), ORC, random.choice(NORMAL_WEAPONS)
    )

def create_goblin():
    return Character(
        random.choice(get_corpora("enemy_names")), GOBLIN, random.choice(NORMAL_WEAPONS)
    )

def create_item():
    return Item(
        random.choice(get_corpora("objects")), random.choice(get_corpora("materials"))
    )

def create_food():
    return Food(
        random.choice(get_corpora("food")), random.randint(1, 30)
    )
