import random

import tracery
from tracery.modifiers import base_english

from combat import fight
from models.items import Food, Item, Scroll
from models.weapons import get_iron_weapon, Weapon, get_steel_weapon


NUMBER_OF_RUNS = 10

def _get_corpora(corpora_name):
    with open(f"corpora/{corpora_name}.txt", "r") as corpora_file:
        return [n.strip() for n in corpora_file.readlines()]


def get_str_from_rules(rules, part):
    grammar = tracery.Grammar(rules)
    grammar.add_modifiers(base_english)
    return grammar.flatten(part)


def get_word_from_corpora(corpora_name):
    return random.choice(_get_corpora(corpora_name))


def intro(corridor):
    rules = {
        "introduction": f"For years the {corridor.name} remained unexplored, until it was found out that it held the precious '#item#', from them on, countless adventurers ventured into the depths of the {corridor.name}, looking for fame and fortune.",
        "item": str(corridor.boss),
    }
    return get_str_from_rules(rules, "#introduction#")


def run_corridor(corridor):
    from models.characters import create_adventurer, Character

    messages = {}
    for chapter in range(1, NUMBER_OF_RUNS + 1):
        messages[chapter] = []
        msgs = messages[chapter]

        # If the corridor has changed, this chapter will be about it
        if corridor.has_changed:
            msgs.append(f"# The {corridor.name}")
            msgs.append(
                f"The {corridor.name} contains a {corridor.boss} in the end of it."
            )

            msgs.append(f"The {corridor.name} also contains:")
            for c in corridor.stuff_in_corridor:
                if isinstance(c, Character):
                    msgs.append(f"- {c.full_description}")
            corridor.has_changed = False
            continue

        character = create_adventurer()

        msgs.append(f"# {character.name} {{#{character.name.replace(' ', '-')}}}")

        msgs.append(
            f"{character.name} is a {character.race} from a town nearby, they heard of the rumours and came to see the {corridor.name} for themselves."
        )
        msgs.append(
            f"{character.name} slowly steps into the dark {corridor.name} to start their walk..."
        )

        for challenge in corridor:
            challenge_messages = deal_with_challenge(challenge, character, corridor)
            msgs.extend(challenge_messages)
            if not character.is_alive:
                break

        msgs.extend(corridor.update())

    return messages


def deal_with_challenge(challenge, character, corridor):
    from models.characters import Character, create_goblin

    messages = [f"{character.name} takes a few more steps in the dark {corridor.name}"]
    if isinstance(challenge, Character):
        enemy = challenge
        messages.append(
            f"{character.name} finds {enemy.name}, a {enemy.race} and get's ready for a fight."
        )

        character, enemy, fight_messages = fight(character, enemy)
        messages.extend(fight_messages)

        if not enemy.is_alive:
            messages.append(f"{enemy.name} dies")
            old_weapon = character.weapon

            equiped = character.loot(enemy.weapon)
            if equiped:
                messages.append(
                    f"{character.name} equips {character.weapon} from the corpse"
                )
                enemy.weapon = old_weapon

    elif isinstance(challenge, Item):
        item = challenge
        messages.append(f"{character.name} picks up the '{item}' triumphantly.")
        messages.append(
            f"The {character.name} gets corrupted by {item} and becomes the {corridor.name} master."
        )

        corridor.update_boss(character)
        messages.extend(dm_creates_creatures(corridor))

    elif isinstance(challenge, Scroll):
        messages.append(f"{character.name} finds a dusty scroll and reads it.")
        scroll = challenge
        messages.append(scroll.apply(character))
        corridor.remove_from_corridor(scroll)
        messages.append(f"...the scroll crumbles into dust")

    elif isinstance(challenge, Food):
        messages.append(f"{character.name} finds a {challenge} and gobbles it down.")
        character.eat(challenge)

    elif isinstance(challenge, Weapon):
        weapon = challenge
        messages.append(f"{character.name} finds a {weapon}.")

        old_weapon = character.weapon
        equiped = character.loot(challenge)
        if equiped:
            messages.append(f"{character.name} equips {weapon}")
            corridor.add_to_corridor(old_weapon)
            corridor.remove_from_corridor(weapon)
        else:
            messages.append(
                f"After some inspection, {character.name} decides not to take {weapon}"
            )

    #### #### #### #### ####
    if not character.is_alive:
        messages.append(f"{character.name} dies")
        if character.level > 2:
            messages.append(
                f"{character.name} gets ressurected by the {corridor.name} and becomes a part of it."
            )
            corridor.add_to_corridor(character)
        else:
            messages.append(
                f"{character.name} is not worthy for the {corridor.name}. Three goblins get spawned in their place."
            )
            corridor.add_to_corridor(create_goblin(character.weapon))
            corridor.add_to_corridor(create_goblin(get_iron_weapon()))
            corridor.add_to_corridor(create_goblin(get_iron_weapon()))

    elif challenge == corridor.boss:
        messages.append(f"The {character.name} becomes the new {corridor.name} master.")

        corridor.update_boss(character)
        messages.extend(dm_creates_creatures(corridor))

    return messages


def dm_creates_creatures(corridor):
    from models.characters import create_orc

    messages = []
    messages.append(f"{corridor.boss.name} calls forth the help of more creatures.")

    for _ in range(corridor.boss.level):
        creature = create_orc(get_steel_weapon())
        messages.append(f"- {creature.full_description}")
        corridor.add_to_corridor(creature)
    return messages


def epilogue(corridor):
    return f"This is the story of the {corridor.name}. Time will tell when the next adventurer dares to enter it."
