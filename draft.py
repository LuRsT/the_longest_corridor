import random

from combat import fight
from models.characters import Character
from models.items import Item
from models.weapons import WEAPONS
from text import get_corpora, get_str_from_rules


def intro(item):
    rules = {
        "introduction": "For years the corridor remained unexplored, until it was found out, that it held the precious '#item#', from them on, countless adventurers ventured into the depths of the corridor, looking for fame and fortune.",
        "item": str(item),
    }
    return get_str_from_rules(rules, "#introduction#")


def create_item():
    return Item(
        random.choice(get_corpora("objects")), random.choice(get_corpora("materials"))
    )


def create_character():
    return Character(
        random.choice(get_corpora("first_names")),
        "Human",
        WEAPONS["magic_sword"],
        10,
        10,
        10,
    )


def create_enemy():
    return Character(
        random.choice(get_corpora("enemy_names")), "Orc", WEAPONS["sword"], 10, 10, 10
    )


def create_corridor(item):
    monsters = [create_enemy() for _ in range(5)]

    corridor = [*monsters, item]
    corridor_history = "The corridor was created by a God who laid out some creatures"
    return corridor[::-1], corridor_history


def run_corridor(corridor):
    for _ in range(10):
        character = create_character()

        while len(corridor) > 0:
            print(
                f"{character.name} slowly steps into the dark corridor to start their walk..."
            )

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

            elif isinstance(challenge, Item):
                print(f"{character.name} picks up the '{challenge}' triumphantly")
                return True

            else:
                print("nothing happened :(")


def epilogue(result):
    if result:
        print("The corridor started crumbling and was reduced to dust")

    else:
        print("The corridor remained unbeaten")


def main():
    """
    This is a draft structure for the book generator

    Intro
    Corridor Creation
    One Chapter per adventurer until someone gets to the end or a limit of runs is reached
    Epilogue
    """

    item = create_item()
    print(intro(item))

    corridor, corridor_history = create_corridor(item)
    print(corridor_history)

    result = run_corridor(corridor)

    epilogue(result)


if __name__ == "__main__":
    main()

    # from combat import simulate_fight
    # simulate_fight(
    #     Character("A", "Human", WEAPONS["sword"], 30, 10, 10),
    #     Character("B", "Orc", WEAPONS["halberd"], 10, 10, 10),
    # )
