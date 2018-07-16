"""HIS cryptography library."""

try:
    from random import choices
except ImportError:
    from random import choice

    def choices(population, k=1):
        """Behaves similar to python 3.6's random.choices."""

        return [choice(population) for _ in range(k)]

from string import ascii_letters, digits, punctuation


__all__ = ['genpw']


def genpw(pool=ascii_letters+digits+punctuation, length=8):
    """Generates a password with the specified
    length from the character pool.
    """

    return ''.join(choices(pool, k=length))
