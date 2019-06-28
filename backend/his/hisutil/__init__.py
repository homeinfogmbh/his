"""HIS command line utility."""

from logging import DEBUG, INFO, basicConfig

from his.hisutil.account import add_account
from his.hisutil.argparse import get_args
from his.hisutil.service import add_account_service
from his.hisutil.service import add_customer_service
from his.hisutil.service import add_service


__all__ = ['main']


LOG_FORMAT = '[%(levelname)s] %(name)s: %(message)s'


def main():
    """Runs the HIS utility."""

    args = get_args()
    basicConfig(level=DEBUG if args.verbose else INFO, format=LOG_FORMAT)

    if args.target == 'account':
        if args.action == 'add':
            add_account(args)
    elif args.target == 'service':
        if args.action == 'add':
            add_service(args)
        elif args.action == 'customer':
            add_customer_service(args)
        elif args.action == 'account':
            add_account_service(args)
