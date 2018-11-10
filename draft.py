import random

from combat import fight
from models.characters import DWARF, ELF, HUMAN, Character
from models.corridor import Corridor
from models.items import Food, Item
from models.weapons import IRON_WEAPONS, Weapon
from text import get_str_from_rules, get_word_from_corpora


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
        get_word_from_corpora("first_names"), ELF, random.choice(IRON_WEAPONS)
    )


def create_human():
    return Character(
        get_word_from_corpora("first_names"), HUMAN, random.choice(IRON_WEAPONS)
    )


def create_dwarf():
    return Character(
        get_word_from_corpora("first_names"), DWARF, random.choice(IRON_WEAPONS)
    )


def run_corridor(corridor):
    for chapter in range(10):
        character = create_adventurer()

        print(f"\n\n## Chapter #{chapter} ({character.name})\n")

        character.intro()

        print(f"{character.name} slowly steps into the dark corridor to start their walk...\n")

        for challenge in corridor:
            if isinstance(challenge, Character):
                enemy = challenge
                print(f"{character.name} finds {enemy.name}, a {enemy.race} and get's ready for a fight.\n")

                character, enemy = fight(character, enemy)

                if not character.is_alive:
                    print(f"{character.name} dies\n")
                    corridor.add_item(character.weapon)
                    break
                else:
                    print(f"{enemy.name} dies\n")
                    print(f"{character.name} sighs in relief and continues...\n")

            elif isinstance(challenge, Item):
                print(f"{character.name} picks up the '{challenge}' triumphantly\n")
                return True

            elif isinstance(challenge, Food):
                print(f"{character.name} finds a {challenge} and gobbles it down.\n")
                character.eat(challenge)

            elif isinstance(challenge, Weapon):
                print(f"{character.name} finds a {challenge} and equips it.\n")
                character.equip(challenge)

            else:
                print("nothing happened :(\n")

            print(f"{character.name} takes a few more steps in the dark corridor\n")

        corridor.shuffle()


def epilogue(result):
    if result:
        print("\nThe corridor started crumbling and was reduced to dust\n")

    else:
        print("\nThe corridor remained unbeaten\n")


def main():
    """
    This is a draft structure for the book generator

    Intro
    Corridor Creation
    One Chapter per adventurer until someone gets to the end or a limit of runs is reached
    Epilogue
    """

    corridor = Corridor()

    print("\n## Introduction\n")
    print(intro(corridor.item))
    print()

    print("\n## The corridor\n")
    print(corridor.get_history())
    print()

    result = run_corridor(corridor)
    print()

    print("## Epilogue\n")
    epilogue(result)

    # print("## Appendix\n\n")
    # corridor.stats()


if __name__ == "__main__":
    main()

    # from combat import simulate_fight
    # simulate_fight(
    #     Character("A", "Human", WEAPONS["sword"], 30, 10, 10),
    #     Character("B", "Orc", WEAPONS["halberd"], 10, 10, 10),
    # )
