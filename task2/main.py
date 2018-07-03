import string
import random
from collections import Counter

"""
    In fact of no restricions based on time and memory cost the
    solution maintain clean and readable code.

    Probably Python not the best way to solve such tasks.
"""

LIMIT = int(1e6)


def generate_sequence():
    return ''.join(
        [random.choice(string.ascii_lowercase) for _ in range(LIMIT)]
    )


def check_sequence(sequence):
    limits = [40000, 2000, 100]
    sequence_lenght = len(sequence)
    for offset, limit in enumerate(limits, start=1):
        result = Counter(
            tuple(sequence[i:i + offset]) for i in range(sequence_lenght)
        )
        if max(result.values()) >= limit:
            return False
    return True


def get_specific_sequence():
    while True:
        sequence = generate_sequence()
        if not check_sequence(sequence):
            continue
        return sequence


if __name__ == '__main__':
    sequence = get_specific_sequence()
