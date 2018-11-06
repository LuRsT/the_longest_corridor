import tracery
from tracery.modifiers import base_english

from combat import fight
from models.characters import Character
from models.weapons import WEAPONS


def get_str_from_rules(rules, part):
    grammar = tracery.Grammar(rules)
    grammar.add_modifiers(base_english)
    return grammar.flatten(part)


def get_corpora(corpora_name):
    with open(f"corpora/{corpora_name}.txt", "r") as corpora_file:
        return [n.strip() for n in corpora_file.readlines()]


def write_intro(item):
    rules = {
        "introduction": "For years the corridor remained unexplored, until it was found out, that it held the precious #item#, from them on, countless adventurers ventured into the depths of the corridor, looking for fame and fortune.",
        "item": item,
    }
    return get_str_from_rules(rules, "#introduction#")


def create_item():
    rules = {
        "item": "#type# of #material#",
        "material": get_corpora("materials"),
        "type": get_corpora("objects"),
    }
    return get_str_from_rules(rules, "#item#")


def create_corridor():
    monsters = [Character("Ulfric", "Orc", WEAPONS['sword'], 10, 10, 10) for _ in range(5)]

    corridor_history = "The corridor was created by a God who laid out some creatures"
    return [*monsters], corridor_history


def create_character():
    return Character("Arnold", "Human", WEAPONS['magic_sword'], 10, 10, 10)


def run_corridor(corridor):
    while len(corridor) > 0:
        character = create_character()

        challenge = corridor.pop()

        if isinstance(challenge, Character):
            enemy = challenge
            character, enemy = fight(character, enemy)

            if not character.is_alive:
                print(f"{character.name} dies")
                break
            else:
                print(f"{enemy.name} dies")
                print(f"{character.name} sighs in relief and continues...")


def main():
    """
    This is a draft structure for the book generator

    Intro
    Corridor Creation
    One Chapter per adventurer until someone gets to the end or a limit of runs is reached
    Epilogue
    """

    item = f"'{create_item()}'"
    print(write_intro(item))

    corridor, corridor_history = create_corridor()
    print(corridor_history)

    print(run_corridor(corridor))


if __name__ == "__main__":
    main()
