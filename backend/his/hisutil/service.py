"""Handles services."""

from logging import getLogger
from sys import exit    # pylint: disable=W0622

from his.exceptions import ServiceExistsError
from his.orm import AccountService, CustomerService, Service


__all__ = ['add_service', 'add_customer_service', 'add_account_service']


LOGGER = getLogger('hisutil')


def add_service(args):
    """Adds a new service."""

    try:
        service = Service.add(
            args.name, description=args.description, promote=args.promote)
    except ServiceExistsError:
        LOGGER.error('Service already exists.')
        exit(1)

    service.save()
    LOGGER.info('Service added.')


def add_customer_service(args):
    """Adds a new customer-service mapping."""

    try:
        customer_service = CustomerService.get(
            (CustomerService.customer == args.customer) &
            (CustomerService.service == args.service))
    except CustomerService.DoesNotExist:
        customer_service = CustomerService.add(
            args.customer, args.service, begin=args.begin, end=args.end)
        customer_service.save()

    LOGGER.info('Added: %s', customer_service)


def add_account_service(args):
    """Adds a new account-service mapping."""

    try:
        account_service = AccountService.get(
            (AccountService.account == args.account) &
            (AccountService.service == args.service))
    except AccountService.DoesNotExist:
        account_service = AccountService.add(args.account, args.service)
        account_service.save()

    LOGGER.info('Added: %s', account_service)
