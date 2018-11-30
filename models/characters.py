import random

from dragn.dice import D4, D20

from dataclasses import dataclass
from models.weapons import Weapon, get_iron_weapon, get_mithril_weapon
from text import get_word_from_corpora


@dataclass
class Race:
    name: str
    health: int
    armor: int
    dex: int

    def __str__(self):
        return self.name


@dataclass
class Character:
    name: str
    race: Race
    weapon: Weapon
    exp: int = 0
    level: int = 1
    bonus_health: int = 0
    bonus_dex: int = 0
    bonus_armor: int = 0

    def __post_init__(self):
        self.health = self.race.health + self.bonus_health
        self.armor = self.race.armor + self.bonus_armor
        self.dex = self.race.dex + self.bonus_dex

        self._max_health = self.health
        self.is_zombie = False
        self.characteristics = [
            get_word_from_corpora("characteristics") for _ in range(3)
        ]

    def resurrect(self):
        if not self.is_alive:
            self.make_zombie()
            self.health = self._max_health

    def make_zombie(self):
        self.is_zombie = True
        self.dex -= 4
        self.armor -= 4

    def __str__(self):
        return self.name

    @property
    def full_description(self):
        zombie = "zombie " if self.is_zombie else ""
        characteristics = (
            ", ".join(self.characteristics[:2]) + " and " + self.characteristics[-1]
        )
        return f"{self.name} is a {zombie}{self.race}, yielding a {self.weapon}. They are {characteristics}"

    @property
    def is_alive(self):
        if self.health <= 0:
            return False
        return True

    def attack(self, other):
        if self.dex + D20() > other.armor:
            other.take_damage(self.weapon.damage)
            return True
        return False

    @property
    def value(self):
        return (self.exp * self.level) + self.dex + self._max_health + self.armor

    def gain_exp(self, other):
        self.exp += other.value
        return self.maybe_level_up()

    def maybe_level_up(self):
        lvl_by_xp = {2: 50, 3: 100, 4: 200, 5: 400, 6: 600, 7: 830, 8: 1000}
        for lvl, xp in lvl_by_xp.items():
            if self.level >= lvl:
                continue

            if self.exp >= xp:
                self.level = lvl
                self.level_up()
                return True

        return False

    def level_up(self):
        self.dex += 1
        self.armor += 1
        self.health += 5
        self._max_health += 5

    def eat(self, food):
        self.heal(food.amount)

    def heal(self, amount):
        self.health += amount
        if self.health > self._max_health:
            self.health = self._max_health

    def loot(self, weapon: Weapon):
        if self.weapon.value < weapon.value:
            self.weapon = weapon
            return True
        return False

    def take_damage(self, damage):
        self.health -= damage

    @property
    def name_and_link(self):
        if self.is_adventurer:
            return f"[{self.name}](#{self.name.replace(' ', '-')})"
        else:
            return self.name

    @property
    def is_adventurer(self):
        return self.race not in (ORC, GOBLIN, OGRE)

    @property
    def stats(self):
        zombie = "zombie " if self.is_zombie else ""
        return (
            f"{self.name_and_link}: a {zombie}{self.race} yielding a {self.weapon}, "
            f"DEX: {self.dex} ARMOR: {self.armor} "
            f"HP: {self._max_health} LVL: {self.level}"
        )


HUMAN = Race("Human", 20, 10, 10)
DWARF = Race("Dwarf", 25, 12, 9)
ELF = Race("Dwarf", 18, 8, 13)

ORC = Race("Orc", 10, 10, 10)
GOBLIN = Race("Goblin", 5, 8, 13)
OGRE = Race("Ogre", 30, 14, 7)


def create_adventurer():
    creator = random.choice([_create_dwarf, _create_human, _create_elf])
    return creator(get_iron_weapon())


def _create_adventurer(race, weapon):
    name = " ".join(
        [get_word_from_corpora("first_names"), get_word_from_corpora("last_names")]
    )
    if random.choice([True, False]):
        # May get a second last name
        name += get_word_from_corpora("last_names")

    return Character(
        name, race, weapon, bonus_health=D4(), bonus_armor=D4(), bonus_dex=D4()
    )


def _create_elf(weapon):
    return _create_adventurer(ELF, weapon)


def _create_human(weapon):
    return _create_adventurer(HUMAN, weapon)


def _create_dwarf(weapon):
    return _create_adventurer(DWARF, weapon)


def create_enemy(zombie=False):
    enemy = random.choice([create_orc, create_goblin])
    return enemy(get_iron_weapon(), zombie)


def create_orc(weapon, zombie=False):
    return _create_enemy(weapon, ORC, zombie)


def create_ogre():
    weapon = get_iron_weapon()
    return _create_enemy(weapon, OGRE, False)


def create_goblin(weapon=None, zombie=False):
    if not weapon:
        weapon = get_iron_weapon()
    return _create_enemy(weapon, GOBLIN, zombie)


def _create_enemy(weapon, race, zombie):
    character = Character(create_enemy_name(), race, weapon)
    if zombie:
        character.make_zombie()
    return character


def create_enemy_name():
    return get_word_from_corpora("enemy_names")
