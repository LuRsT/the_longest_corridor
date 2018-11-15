import random

from dragn.dice import D20

from dataclasses import dataclass
from models.weapons import Weapon, get_iron_weapon
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

    def __post_init__(self):
        self.health = self.race.health
        self.armor = self.race.armor
        self.dex = self.race.dex

        self._max_health = self.health
        self.is_zombie = False

    def resurrect(self):
        if not self.is_alive:
            self.is_zombie = True
            self.health = self._max_health

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
        lvl_by_xp = {2: 50, 3: 100, 4: 200, 5: 400}
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
        return (
            f"{self.name_and_link}: a {self.race} wielding a {self.weapon}, "
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
    return Character(name, race, weapon)


def _create_elf(weapon):
    return _create_adventurer(ELF, weapon)


def _create_human(weapon):
    return _create_adventurer(HUMAN, weapon)


def _create_dwarf(weapon):
    return _create_adventurer(DWARF, weapon)


def create_enemy(zombie=False):
    enemy = random.choice([create_orc, create_goblin, _create_ogre])
    return enemy(get_iron_weapon(), zombie)


def create_orc(weapon, zombie=False):
    return _create_enemy(weapon, ORC, zombie)


def _create_ogre(weapon, zombie=False):
    return _create_enemy(weapon, OGRE, zombie)


def create_goblin(weapon, zombie=False):
    return _create_enemy(weapon, GOBLIN, zombie)


def _create_enemy(weapon, race, zombie):
    character = Character(create_enemy_name(), race, weapon)
    if zombie:
        character.is_zombie = True
    return character


def create_enemy_name():
    return get_word_from_corpora("enemy_names")
