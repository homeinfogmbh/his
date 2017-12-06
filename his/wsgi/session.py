"""HIS session service."""

from json import load

from flask import request, jsonify
from peewee import DoesNotExist

from his.messages.account import NotAuthorized
from his.messages.session import NoSessionSpecified, NoSuchSession, \
    SessionExpired, MissingCredentials, InvalidCredentials
from his.orm import Account, Session
from his.wsgi import APPLICATION

__all__ = [
    'open_session',
    'list_sessions',
    'list_session',
    'refresh_session',
    'close_session']


def get_duration(default=15):
    """Returns the repsective session duration in minutes."""

    return int(request.args.get('duration', default))


@APPLICATION.route('/session', methods=['POST'])
def open_session():
    """Opens a new session for the respective account."""

    json = load(request.get_data())
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


@APPLICATION.route('/session', methods=['GET'])
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


@APPLICATION.route('/session/<session_token>', methods=['GET'])
def list_session(session_token):
    """Lists the respective session."""

    try:
        session = Session.get(Session.token == session_token)
    except DoesNotExist:
        raise NoSuchSession()

    if session.alive:
        return jsonify(session.to_dict())

    raise SessionExpired()


@APPLICATION.route('/session/<session_token>', methods=['PUT'])
def refresh_session(session_token):
    """Refreshes an existing session."""

    try:
        session = Session.get(Session.token == session_token)
    except DoesNotExist:
        raise NoSuchSession()

    if session.renew(duration=get_duration()):
        return jsonify(session.to_dict())

    raise SessionExpired()


@APPLICATION.route('/session/<session_token>', methods=['DELETE'])
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
