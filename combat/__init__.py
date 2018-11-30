from dragn.dice import D6


def fight(char1, char2):
    if char1.dex + D6() > char2.dex + D6():
        attacker, defender = char1, char2
    else:
        defender, attacker = char1, char2

    fight_messages = []
    while char1.is_alive and char2.is_alive:
        messages = []
        if fight_messages:
            messages.append(
                f"{attacker.name} grips their {attacker.weapon} and attempts to strike {defender.name} again"
            )
        else:
            messages.append(
                f"{attacker.name} pulls out their {attacker.weapon} and tries to strike {defender.name}"
            )
        result = attacker.attack(defender)
        if result:
            messages.append(f"They easily {attacker.weapon.hit_str} their foe.")
        else:
            messages.append(f"they miss.")
        attacker, defender = defender, attacker

        fight_messages.append(", ".join(messages))

    if char1.is_alive:
        leveled_up = char1.gain_exp(char2)
        if leveled_up:
            fight_messages.append(f"{char1.name} feels stronger.")
        char1.weapon.register_kill(char2)
    else:
        leveled_up = char2.gain_exp(char1)
        if leveled_up:
            fight_messages.append(f"{char2.name} feels stronger.")
        char2.weapon.register_kill(char1)

    return char1, char2, " ".join(fight_messages)
