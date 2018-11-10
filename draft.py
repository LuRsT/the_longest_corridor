import random

from combat import fight
from models.characters import DWARF, ELF, HUMAN, Character
from models.corridor import Corridor
from models.items import Item
from models.weapons import NORMAL_WEAPONS
from text import get_corpora, get_str_from_rules


def intro(item):
    rules = {
        "introduction": "For years the corridor remained unexplored, until it was found out, that it held the precious '#item#', from them on, countless adventurers ventured into the depths of the corridor, looking for fame and fortune.",
        "item": str(item),
    }
    return get_str_from_rules(rules, "#introduction#")


def create_adventurer():
    creator = random.choice([create_dwarf, create_human, create_elf])
    return creator()


def create_elf():
    return Character(
        random.choice(get_corpora("first_names")), ELF, random.choice(NORMAL_WEAPONS)
    )


def create_human():
    return Character(
        random.choice(get_corpora("first_names")), HUMAN, random.choice(NORMAL_WEAPONS)
    )


def create_dwarf():
    return Character(
        random.choice(get_corpora("first_names")), DWARF, random.choice(NORMAL_WEAPONS)
    )


def run_corridor(corridor):
    for chapter in range(10):
        character = create_adventurer()

        print(f"\n\nChapter #{chapter} ({character.name})\n")

        for challenge in corridor:
            print(
                f"{character.name} slowly steps into the dark corridor to start their walk..."
            )

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

        corridor.shuffle()


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

    corridor = Corridor()

    print(intro(corridor.item))
    print()

    print(corridor.get_history())
    print()

    result = run_corridor(corridor)
    print()

    epilogue(result)


if __name__ == "__main__":
    main()

    # from combat import simulate_fight
    # simulate_fight(
    #     Character("A", "Human", WEAPONS["sword"], 30, 10, 10),
    #     Character("B", "Orc", WEAPONS["halberd"], 10, 10, 10),
    # )
