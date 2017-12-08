"""HIS session service."""

from json import loads

from flask import request, jsonify
from peewee import DoesNotExist
from wsgilib import crossdomain

from his.messages.account import NotAuthorized
from his.messages.session import NoSessionSpecified, NoSuchSession, \
    SessionExpired, MissingCredentials, InvalidCredentials
from his.orm import Account, Session

__all__ = [
    'open_session',
    'list_sessions',
    'list_session',
    'refresh_session',
    'close_session']


def get_duration(default=15):
    """Returns the repsective session duration in minutes."""

    return int(request.args.get('duration', default))


@crossdomain(origin='*')
def open_session():
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


@crossdomain(origin='*')
def list_sessions():
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


@crossdomain(origin='*')
def list_session(session_token):
    """Lists the respective session."""

    try:
        session = Session.get(Session.token == session_token)
    except DoesNotExist:
        raise NoSuchSession()

    if session.alive:
        return jsonify(session.to_dict())

    raise SessionExpired()


@crossdomain(origin='*')
def refresh_session(session_token):
    """Refreshes an existing session."""

    try:
        session = Session.get(Session.token == session_token)
    except DoesNotExist:
        raise NoSuchSession()

    if session.renew(duration=get_duration()):
        return jsonify(session.to_dict())

    raise SessionExpired()


@crossdomain(origin='*')
def close_session(session_token):
    """Tries to close a specific session identified by its token or
    all sessions for a certain account specified by its name.
    """

    try:
        session = Session.get(Session.token == session_token)
    except DoesNotExist:
        raise NoSuchSession()

    session.close()
    return jsonify({'closed': session.token})
