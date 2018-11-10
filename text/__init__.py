import random

import tracery
from tracery.modifiers import base_english


def get_corpora(corpora_name):
    with open(f"corpora/{corpora_name}.txt", "r") as corpora_file:
        return [n.strip() for n in corpora_file.readlines()]


def get_str_from_rules(rules, part):
    grammar = tracery.Grammar(rules)
    grammar.add_modifiers(base_english)
    return grammar.flatten(part)


def get_word_from_corpora(corpora_name):
    return random.choice(get_corpora(corpora_name))
