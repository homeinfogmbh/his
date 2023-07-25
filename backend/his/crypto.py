"""HIS cryptography library."""

from getpass import getpass
from secrets import choice
from string import ascii_letters, digits
from sys import stderr


__all__ = ["genpw", "read_passwd"]


def genpw(length: int = 16, *, pool: str = ascii_letters + digits) -> str:
    """Generates a safe, radom password."""

    return "".join(choice(pool) for _ in range(length))


def read_passwd() -> str:
    """Reads a password."""

    while True:
        try:
            passwd = getpass("Password: ")
        except EOFError:
            continue

        try:
            repeat = getpass("Repeat password: ")
        except EOFError:
            continue

        if passwd and passwd == repeat:
            return passwd

        print("Passwords do not match.", file=stderr)
        continue
