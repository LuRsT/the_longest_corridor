from dragn.dice import D6


def fight(char1, char2):
    if char1.dex + D6() > char2.dex + D6():
        attacker, defender = char1, char2
    else:
        defender, attacker = char1, char2

    messages = []
    while char1.is_alive and char2.is_alive:
        result = attacker.attack(defender)
        if result:
            messages.append(
                f"{attacker.name} {attacker.weapon.hit_str} {defender.name}"
            )
        else:
            messages.append(f"{attacker.name} misses")
        attacker, defender = defender, attacker

    if char1.is_alive:
        leveled_up = char1.gain_exp(char2)
        if leveled_up:
            messages.append(f"{char1.name} feels stronger")
        char1.weapon.register_kill(char2)
    else:
        leveled_up = char2.gain_exp(char1)
        if leveled_up:
            messages.append(f"{char2.name} feels stronger")
        char2.weapon.register_kill(char1)

    return char1, char2, messages
