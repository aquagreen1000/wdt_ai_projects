"""Turn-order generation for debates."""

import random


def generate_turn_order(debater_names, turns_per_debater):
    """Generate a balanced order without consecutive turns when possible."""
    total_turns = len(debater_names) * turns_per_debater
    remaining = {name: turns_per_debater for name in debater_names}
    order = []
    last = None

    for _ in range(total_turns):
        candidates = [
            name for name in remaining
            if remaining[name] > 0 and name != last
        ]
        if not candidates:
            candidates = [name for name in remaining if remaining[name] > 0]

        choice = random.choice(candidates)
        order.append(choice)
        remaining[choice] -= 1
        last = choice

    return order