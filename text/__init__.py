import random

import tracery
from tracery.modifiers import base_english

from combat import fight
from models.items import Food, Item
from models.weapons import get_iron_weapon, Weapon, get_steel_weapon


def _get_corpora(corpora_name):
    with open(f"corpora/{corpora_name}.txt", "r") as corpora_file:
        return [n.strip() for n in corpora_file.readlines()]


def get_str_from_rules(rules, part):
    grammar = tracery.Grammar(rules)
    grammar.add_modifiers(base_english)
    return grammar.flatten(part)


def get_word_from_corpora(corpora_name):
    return random.choice(_get_corpora(corpora_name))


def intro(item):
    rules = {
        "introduction": "For years the corridor remained unexplored, until it was found out, that it held the precious '#item#', from them on, countless adventurers ventured into the depths of the corridor, looking for fame and fortune.",
        "item": str(item),
    }
    return get_str_from_rules(rules, "#introduction#")


def run_corridor(corridor):
    from models.characters import create_adventurer

    messages = []
    for chapter in range(1):
        character = create_adventurer()

        messages.append(f"\n\n# Chapter #{chapter} ({character.name})\n")

        messages.append(character.intro())

        messages.append(
            f"{character.name} slowly steps into the dark corridor to start their walk...\n"
        )

        for challenge in corridor:
            challenge_messages = deal_with_challenge(challenge, character, corridor)
            messages.extend(challenge_messages)
            if not character.is_alive:
                break

        corridor.shuffle()
        messages.append("The corridor is shuffled and all creatures are ressurected.\n")

    return messages


def deal_with_challenge(challenge, character, corridor):
    from models.characters import Character, create_goblin, create_orc

    messages = [f"{character.name} takes a few more steps in the dark corridor\n"]
    if isinstance(challenge, Character):
        enemy = challenge
        messages.append(
            f"{character.name} finds {enemy.name}, a {enemy.race} and get's ready for a fight.\n"
        )

        character, enemy, fight_messages = fight(character, enemy)
        messages.extend(fight_messages)

        if not character.is_alive:
            messages.append(f"{character.name} dies\n")
            if character.level > 2:
                messages.append(
                    f"{character.name} gets ressurected by the corridor and becomes a part of it.\n"
                )
                corridor.add_to_corridor(character)
            else:
                messages.append(
                    f"{character.name} is not worthy for the corridor. Three goblins get spawned in their place."
                )
                corridor.add_to_corridor(create_goblin(character.weapon))
                corridor.add_to_corridor(create_goblin(get_iron_weapon()))
                corridor.add_to_corridor(create_goblin(get_iron_weapon()))
        else:
            messages.append(f"{enemy.name} dies\n")
            old_weapon = character.weapon

            equiped = character.loot(enemy.weapon)
            if equiped:
                messages.append(
                    f"{character.name} equips {character.weapon} from the corpse"
                )
                enemy.weapon = old_weapon

    elif isinstance(challenge, Item):
        messages.append(f"{character.name} picks up the '{challenge}' triumphantly\n")
        messages.append("The corridor zaps {character.name} with great might and creates:")

        messages.append("\n- One Orc with their weapon")
        corridor.add_to_corridor(create_orc(character.weapon))
        for _ in range(character.level):
            messages.append("\n- an Orc with a stronger weapon")
            corridor.add_to_corridor(create_orc(get_steel_weapon()))


    elif isinstance(challenge, Food):
        messages.append(f"{character.name} finds a {challenge} and gobbles it down.\n")
        character.eat(challenge)

    elif isinstance(challenge, Weapon):
        weapon = challenge
        messages.append(f"{character.name} finds a {weapon}.\n")

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

    return messages


def epilogue():
    messages = []
    messages.append("\nThe corridor started crumbling and was reduced to dust\n")
