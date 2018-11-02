import tracery
from tracery.modifiers import base_english


def write_intro(item):
    rules = {
        "introduction": "For years the corridor remained unexplored, until it was found out, that it held the precious #item#, from them on, countless adventurers ventured into the depths of the corridor, looking fame and fortune. ",
        "item": item,
    }

    grammar = tracery.Grammar(rules)
    grammar.add_modifiers(base_english)
    return grammar.flatten("#introduction#")


def main():
    """
    This is a draft structure for the book generator

    Intro
    One Chapter per adventurer until someone gets to the end or a limit of runs is reached
    Epilogue
    """

    item = "'Amulet of Whatever'"
    print(write_intro(item))


if __name__ == "__main__":
    main()
