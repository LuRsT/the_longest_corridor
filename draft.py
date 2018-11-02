import tracery
from tracery.modifiers import base_english


def get_str_from_rules(rules, part):
    grammar = tracery.Grammar(rules)
    grammar.add_modifiers(base_english)
    return grammar.flatten(part)


def get_corpora(corpora_name):
    with open(f'corpora/{corpora_name}.txt', 'r') as corpora_file:
        return [n.strip() for n in corpora_file.readlines()]


def write_intro(item):
    rules = {
        "introduction": "For years the corridor remained unexplored, until it was found out, that it held the precious #item#, from them on, countless adventurers ventured into the depths of the corridor, looking for fame and fortune. ",
        "item": item,
    }
    return get_str_from_rules(rules, "#introduction#")


def create_item():
    rules = {
        "item": "#type# of #material#",
        "material": ['bronze', 'iron', 'stone', 'quartz'],
        "type": get_corpora('objects'),
    }
    return get_str_from_rules(rules, "#item#")


def main():
    """
    This is a draft structure for the book generator

    Intro
    One Chapter per adventurer until someone gets to the end or a limit of runs is reached
    Epilogue
    """

    item = f"'{create_item()}'"
    print(write_intro(item))


if __name__ == "__main__":
    main()
