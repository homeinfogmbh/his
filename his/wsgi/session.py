"""HIS session service."""

from json import loads

from flask import request, jsonify
from peewee import DoesNotExist

from his.messages import NotAuthorized, NoSessionSpecified, NoSuchSession, \
    SessionExpired, MissingCredentials, InvalidCredentials
from his.orm import Account, Session

__all__ = ['ENDPOINTS']

DURATION = 15


def get_duration():
    """Returns the repsective session duration in minutes."""

    return int(request.args.get('duration', DURATION))


def login():
    """Opens a new session for the respective account."""

    json = loads(request.get_data().decode())
    account = json.get('account')
    passwd = json.get('passwd')

    if not account or not passwd:
        raise MissingCredentials()

    try:
        account = Account.get(Account.name == account)
    except DoesNotExist:
        pass
    else:
        if account.login(passwd):
            session = Session.open(account, duration=get_duration())
            return jsonify(session.to_dict())

    raise InvalidCredentials()


def lst():
    """Lists all sessions iff specified session is root."""

    try:
        session = request.args['session']
    except KeyError:
        raise NoSessionSpecified()

    try:
        session = Session.get(Session.token == session)
    except DoesNotExist:
        raise NoSuchSession()

    if session.alive:
        if session.account.root:
            sessions = {
                session.token: session.to_dict() for session in Session}
            return jsonify(sessions)

        raise NotAuthorized()

    raise SessionExpired()


def get(session_token):
    """Lists the respective session."""

    try:
        session = Session.get(Session.token == session_token)
    except DoesNotExist:
        raise NoSuchSession()

    if session.alive:
        return jsonify(session.to_dict())

    raise SessionExpired()


def refresh(session_token):
    """Refreshes an existing session."""

    try:
        session = Session.get(Session.token == session_token)
    except DoesNotExist:
        raise NoSuchSession()

    if session.renew(duration=get_duration()):
        return jsonify(session.to_dict())

    raise SessionExpired()


def close(session_token):
    """Tries to close a specific session identified by its token or
    all sessions for a certain account specified by its name.
    """

    try:
        session = Session.get(Session.token == session_token)
    except DoesNotExist:
        raise NoSuchSession()

    session.close()
    return jsonify({'closed': session.token})


ENDPOINTS = {
    'login': ('POST', '/session', login),
    'list_sessions': ('GET', '/session', lst),
    'get_session': ('GET', '/session/<session_token>', get),
    'refresh_session': ('PUT', '/session/<session_token>', refresh),
    'close_session': ('DELETE', '/session/<session_token>', close)}
