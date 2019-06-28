"""Account actions."""

from logging import getLogger
from sys import exit    # pylint: disable=W0622

from his.crypto import genpw, read_passwd
from his.exceptions import AccountExistsError
from his.orm import Account


__all__ = ['add_account']


LOGGER = getLogger('hisutil')


def add_account(args):
    """Adds the respective account."""

    if args.passwd:
        try:
            passwd = read_passwd()
        except KeyboardInterrupt:
            LOGGER.error('Aborted by user.')
            exit(1)
    else:
        passwd = genpw()
        LOGGER.info('Generated password: %s', passwd)

    try:
        account = Account.add(
            args.customer, args.name, args.email, passwd=passwd,
            admin=args.admin, root=args.root)
    except AccountExistsError as account_exists:
        LOGGER.error(
            'Account already exists for field "%s".', account_exists.field)
        exit(2)

    account.save()  # Account.add() does not perform save().
    LOGGER.info('Added %s', account)
