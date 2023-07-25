"""Account actions."""

from argparse import Namespace
from logging import getLogger
from sys import exit  # pylint: disable=W0622

from peewee import IntegrityError

from his.crypto import genpw, read_passwd
from his.orm.account import Account


__all__ = ["add_account"]


LOGGER = getLogger("hisutil")


def add_account(args: Namespace):
    """Adds the respective account."""

    if args.password:
        try:
            passwd = read_passwd()
        except KeyboardInterrupt:
            LOGGER.error("Aborted by user.")
            exit(1)
    else:
        passwd = genpw()
        LOGGER.info("Generated password: %s", passwd)

    try:
        account = Account.add(
            args.customer,
            args.name,
            args.email,
            passwd=passwd,
            full_name=args.full_name,
            admin=args.admin,
            root=args.root,
        )
    except IntegrityError as error:
        LOGGER.error("%i: %s", *error.args)
        exit(2)

    account.save()  # Account.add() does not perform save().
    LOGGER.info("Added %s", account)
