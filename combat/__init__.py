from models.characters import Character


def simulate_fight(char1, char2):
    print(
        f"A {char1.race} yielding a {char1.weapon} attacks an {char2.race} who yields a {char2.weapon}..."
    )
    char1, char2 = fight(char1, char2)

    if not char1.is_alive:
        print(f"{char1.name} dies")
        print(f"{char2.name} ends up with {char2.health} HP")
    else:
        print(f"{char2.name} dies")
        print(f"{char1.name} ends up with {char1.health} HP")


def fight(char1, char2):
    # TODO Determine who starts
    attacker, defender = char1, char2
    while char1.is_alive and char2.is_alive:
        attacker.attack(defender)
        attacker, defender = defender, attacker

    if char1.is_alive:
        char1.gain_exp(char2)
        char1.weapon.register_kill(char2)
    elif char2.is_alive:
        char2.gain_exp(char1)
        char2.weapon.register_kill(char1)

    return char1, char2
