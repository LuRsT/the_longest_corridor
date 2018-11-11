def fight(char1, char2):
    # TODO Determine who starts

    attacker, defender = char1, char2
    messages = []
    while char1.is_alive and char2.is_alive:
        result = attacker.attack(defender)
        if result:
            messages.append(
                f"{attacker.name} {attacker.weapon.hit_str} {defender.name}\n"
            )
        else:
            messages.append(f"{attacker.name} misses\n")
        attacker, defender = defender, attacker

    if char1.is_alive:
        leveled_up = char1.gain_exp(char2)
        if leveled_up:
            messages.append(f"{char1.name} feels stronger\n")
        char1.weapon.register_kill(char2)
    else:
        leveled_up = char2.gain_exp(char1)
        if leveled_up:
            messages.append(f"{char2.name} feels stronger\n")
        char2.weapon.register_kill(char1)

    return char1, char2, messages
