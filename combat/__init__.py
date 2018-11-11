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
