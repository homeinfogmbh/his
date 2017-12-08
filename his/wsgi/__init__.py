"""HIS WSGI core services."""

from wsgilib import Application

from his.wsgi.account import list_accounts, get_account, add_account, \
    patch_account
from his.wsgi.customer import get_customer, get_logo
from his.wsgi.service import add_service
from his.wsgi.session import open_session, list_sessions, list_session, \
    refresh_session, close_session

__all__ = ['APPLICATION']


APPLICATION = Application('his', cors=True)
APPLICATION.route('/account', methods=['GET'])(list_accounts)
APPLICATION.route('/account/<name>', methods=['GET'])(get_account)
APPLICATION.route('/account', methods=['POST'])(add_account)
APPLICATION.route('/account/<name>', methods=['PATCH'])(patch_account)
APPLICATION.route('/customer/<customer>', methods=['GET'])(get_customer)
APPLICATION.route('/customer/logo', methods=['GET'])(get_logo)
APPLICATION.route('/service', methods=['POST'])(add_service)
APPLICATION.route('/session', methods=['POST'])(open_session)
APPLICATION.route('/session', methods=['GET'])(list_sessions)
APPLICATION.route('/session/<session_token>', methods=['GET'])(list_session)
APPLICATION.route('/session/<session_token>', methods=['PUT'])(refresh_session)
APPLICATION.route('/session/<session_token>', methods=['DELETE'])(
    close_session)
