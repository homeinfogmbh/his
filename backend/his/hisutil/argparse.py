"""CLI arguments parsing."""

from argparse import ArgumentParser
from datetime import datetime

from mdb import Customer

from his.orm import Account, Service


__all__ = ['get_args']


def customer(string):
    """Returns the respective customer."""

    try:
        match, *excess = Customer.find(string)
    except ValueError:
        raise ValueError('No such customer.')

    if excess:
        raise ValueError('Ambiguous customer selection.')

    return match


def service(string):
    """Returns the respective service."""

    try:
        return Service.get(Service.name == string)
    except Service.DoesNotExist:
        raise ValueError('No such service.')


def account(string):
    """Returns the account."""

    try:
        ident = int(string)
    except ValueError:
        select = False
    else:
        select = Account.id == ident

    select |= Account.name == string
    select |= Account.email == string

    try:
        match, *excess = Account.select().where(select)
    except ValueError:
        raise ValueError('No such account.')

    if excess:
        raise ValueError('Ambiguous account selection.')

    return match


def dtime(string):
    """Parses a datetime."""

    return datetime.strptime(string, '%Y-%m-%dT%H:%M:%S')


def _add_account_parser(subparsers):
    """Adds a parser for handling accounts."""

    parser = subparsers.add_parser('account', help='manage accounts')
    subparsers_ = parser.add_subparsers(dest='action')
    add_parser = subparsers_.add_parser('add', help='add a new account')
    add_parser.add_argument('name', help='the login name')
    add_parser.add_argument('email', help='an email address')
    add_parser.add_argument('customer', type=customer, help='the customer')
    add_parser.add_argument('-n', '--full-name', help="the user's full name")
    add_parser.add_argument(
        '-p', '--password', action='store_true',
        help='manually specify a password')
    add_parser.add_argument(
        '-a', '--admin', action='store_true',
        help='make the account an administrator')
    add_parser.add_argument(
        '--root', action='store_true', help='make the account a root user')


def _add_service_parser(subparsers):
    """Adds a parser for handling services."""

    parser = subparsers.add_parser('service', help='manage services')
    subparsers_ = parser.add_subparsers(dest='action')
    add_parser = subparsers_.add_parser('add', help='add a new service')
    add_parser.add_argument('name', help='the service name')
    add_parser.add_argument('-d', '--description', help='a description')
    add_parser.add_argument(
        '-p', '--promote', action='store_true', help='promote the service')
    add_customer_parser = subparsers_.add_parser(
        'customer', help='add a customer to the service')
    add_customer_parser.add_argument(
        'service', type=service, help='the service name')
    add_customer_parser.add_argument(
        'customer', type=customer, help='the customer ID or name')
    add_customer_parser.add_argument(
        '-b', '--begin', type=dtime, help='the beginning of the usage period')
    add_customer_parser.add_argument(
        '-e', '--end', type=dtime, help='the end of the usage period')
    add_account_parser = subparsers_.add_parser(
        'account', help='add an account to the service')
    add_account_parser.add_argument(
        'service', type=service, help='the service name')
    add_account_parser.add_argument(
        'account', type=account, help='the account ID, name or email')


def get_args():
    """Returns the command line arguments."""

    parser = ArgumentParser(description='Manage HIS settings.')
    parser.add_argument(
        '-v', '--verbose', action='store_true', help='enable verbose logging')
    subparsers = parser.add_subparsers(dest='target')
    _add_account_parser(subparsers)
    _add_service_parser(subparsers)
    return parser.parse_args()
