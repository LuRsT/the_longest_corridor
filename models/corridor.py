import random

from models.characters import Character, create_enemy
from models.items import Food, Item, Scroll
from models.weapons import Weapon, get_mithril_weapon
from text import get_word_from_corpora


class Corridor:
    def __init__(self):
        self.boss = create_item()
        self.name = "corridor"

        self.initial_creation()
        self.reset()
        self.index = len(self.corridor)
        self.stuff_to_remove = []
        self.archive = []
        self.has_changed = True

    def initial_creation(self):
        self.stuff_in_corridor = []

        self._add_treasure(1)
        self._add_enemies(5)
        self._add_food(3)
        self._add_scrolls(2)

    def reset(self):
        random.shuffle(self.stuff_in_corridor)
        self.corridor = [*self.stuff_in_corridor, self.boss][::-1]

    def add_to_corridor(self, thing):
        self.stuff_in_corridor.append(thing)

    def remove_from_corridor(self, thing):
        self.stuff_to_remove.append(thing)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == 0:
            raise StopIteration
        self.index -= 1
        return self.corridor[self.index]

    def update_boss(self, new_boss):
        new_boss.heal(100)
        self.boss = new_boss
        self.has_changed = True

    def new_corridor_name(self):
        possible_names = ["corridor", "tomb", "crypt", "dungeon", "lair"]
        return random.choice([n for n in possible_names if n != self.name])

    def update(self):
        messages = []
        if self.has_changed:
            new_name = self.new_corridor_name()
            messages.append(
                f"The {self.name} becomes a {new_name}. It is shuffled and all creatures are ressurected."
            )
            self.name = new_name
            messages.append("Five zombies are added.")
            self._add_zombies(5)
        else:
            messages.append(
                f"The {self.name} is shuffled and all creatures are ressurected."
            )
            messages.append("Two scrolls are added.")
            self._add_scrolls(2)
        self._shuffle()
        return messages

    def _get_number_of_zombies(self):
        characters = [c for c in self.stuff_in_corridor if isinstance(c, Character)]
        zombies = [c for c in characters if c.is_zombie]
        return len(zombies)

    def _shuffle(self):
        self._ressurect_creatures()
        self._remove_things()

        self._add_food(int(len(self.stuff_in_corridor) / 10))
        self.reset()

        self.index = len(self.corridor)

    def _ressurect_creatures(self):
        for c in self.stuff_in_corridor:
            if isinstance(c, Character):
                if c.is_zombie and not c.is_alive:
                    self.stuff_in_corridor.append(c.weapon)
                    self.stuff_to_remove.append(c)
                else:
                    c.resurrect()

    def _add_food(self, amount):
        food = [create_food() for _ in range(amount)]
        self.stuff_in_corridor.extend(food)

    def _add_scrolls(self, amount):
        scrolls = [create_scroll() for _ in range(amount)]
        self.stuff_in_corridor.extend(scrolls)

    def _add_enemies(self, amount):
        monsters = [create_enemy() for _ in range(amount)]
        self.stuff_in_corridor.extend(monsters)

    def _add_zombies(self, amount):
        monsters = [create_enemy(zombie=True) for _ in range(amount)]
        self.stuff_in_corridor.extend(monsters)

    def _add_treasure(self, amount):
        treasure = [get_mithril_weapon() for _ in range(amount)]
        self.stuff_in_corridor.extend(treasure)

    def _remove_things(self):
        for s in self.stuff_in_corridor:
            if isinstance(s, Food):
                self.stuff_to_remove.append(s)
            elif isinstance(s, Weapon):
                if s.kills == {}:
                    self.stuff_to_remove.append(s)

        for s in self.stuff_to_remove:
            if isinstance(s, Character):
                self.archive.append(s)

        self.stuff_in_corridor = [
            s for s in self.stuff_in_corridor if s not in self.stuff_to_remove
        ]
        self.stuff_to_remove = []

    def stats(self):
        messages = []
        messages.append(f"\n## The {self.name} contains:\n")
        for c in self.stuff_in_corridor:
            if isinstance(c, Character):
                messages.append(f"- {c.stats}")
            else:
                messages.append(f"- {c}")
        messages.append(f"- {self.boss.stats}")

        messages.append("\n## Notable characters that died permanently:\n")
        for c in self.archive:
            if c.level > 1:
                messages.append(f"- {c.name_and_link}: a {c.race} of level {c.level}")

        ## WEAPON STATS
        messages.append("\n## Weapon stats\n")
        weapons = sorted(
            [c.weapon for c in self.stuff_in_corridor if isinstance(c, Character)],
            key=lambda w: w.kind,
        )
        weapons.extend([w for w in self.stuff_in_corridor if isinstance(w, Weapon)])
        weapons = filter(lambda w: bool(w.kills), weapons)
        for w in weapons:
            messages.append(f"- {w} killed: {w.kills}")

        return messages


def create_item():
    return Item(get_word_from_corpora("objects"), get_word_from_corpora("materials"))


def create_food():
    return Food(get_word_from_corpora("food"), random.randint(1, 30))


def create_scroll():
    scrolls = [
        Scroll("Scroll of healing", lambda c: c.heal(5), "{} feels better."),
        Scroll("Scroll of pain", lambda c: c.take_damage(5), "{} feels awful."),
        Scroll(
            "Scroll of uselessness", lambda c: None, "100 butterflies suddenly appear."
        ),
    ]
    return random.choice(scrolls)
