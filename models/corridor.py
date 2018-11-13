import random

from models.characters import Character, create_enemy
from models.items import Food, Item
from models.weapons import get_mithril_weapon
from text import get_word_from_corpora


class Corridor:
    def __init__(self):
        self.item = create_item()

        self.initial_creation()
        self.reset()
        self.index = len(self.corridor)
        self.stuff_to_remove = []

    def initial_creation(self):
        monsters = [create_enemy() for _ in range(15)]
        food = [create_food() for _ in range(3)]
        treasure = [get_mithril_weapon()]

        self.stuff_in_corridor = [*monsters, *food, *treasure]

    def reset(self):
        random.shuffle(self.stuff_in_corridor)
        self.corridor = [*self.stuff_in_corridor, self.item][::-1]

    def add_to_corridor(self, thing):
        self.stuff_in_corridor.append(thing)

    def remove_from_corridor(self, thing):
        self.stuff_to_remove.append(thing)

    def get_history(self):
        corridor_history = f"The corridor was created by a God who laid out some creatures, a bit of food, and finally, left the {self.item}"
        return corridor_history

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == 0:
            raise StopIteration
        self.index -= 1
        return self.corridor[self.index]

    def shuffle(self):
        for s in self.stuff_to_remove:
            self.stuff_in_corridor.remove(s)
        self.stuff_to_remove = []

        for c in self.stuff_in_corridor:
            if isinstance(c, Character):
                c.resurrect()
        self.index = len(self.corridor)

        self.reset()

    def stats(self):
        messages = []
        messages.append("The corridor contains:\n\n")
        for c in self.stuff_in_corridor:
            if isinstance(c, Character):
                messages.append(f"- {c.stats}\n")
            else:
                messages.append(f"- {c}\n")

        ## WEAPON STATS
        messages.append("\n### Weapon stats\n\n")
        weapons = sorted(
            [c.weapon for c in self.stuff_in_corridor if isinstance(c, Character)],
            key=lambda w: w.kind,
        )
        weapons = filter(lambda w: bool(w.kills), weapons)
        for w in weapons:
            messages.append(f"- {w} killed: {w.kills}\n")

        return messages


def create_item():
    return Item(get_word_from_corpora("objects"), get_word_from_corpora("materials"))


def create_food():
    return Food(get_word_from_corpora("food"), random.randint(1, 30))
