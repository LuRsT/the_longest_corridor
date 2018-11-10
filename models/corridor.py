import random

from models.characters import GOBLIN, OGRE, ORC, Character
from models.items import Food, Item
from models.weapons import NORMAL_WEAPONS
from text import get_str_from_rules, get_word_from_corpora


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
    enemy = random.choice([create_orc, create_goblin, create_ogre])
    return enemy()


def create_orc():
    return Character(create_enemy_name(), ORC, random.choice(NORMAL_WEAPONS))


def create_ogre():
    return Character(create_enemy_name(), OGRE, random.choice(NORMAL_WEAPONS))


def create_goblin():
    return Character(create_enemy_name(), GOBLIN, random.choice(NORMAL_WEAPONS))


def create_enemy_name():
    return get_word_from_corpora("enemy_names")


def create_item():
    return Item(get_word_from_corpora("objects"), get_word_from_corpora("materials"))


def create_food():
    return Food(get_word_from_corpora("food"), random.randint(1, 30))
