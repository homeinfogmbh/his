"""HIS session service."""

from json import load

from flask import request, jsonify, Flask
from peewee import DoesNotExist

from his.orm import Account, Session

__all__ = ['APPLICATION']


APPLICATION = Flask('session')


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
        return ('Missing user name and / or password.', 400)

    try:
        account = Account.get(Account.name == account)
    except DoesNotExist:
        pass
    else:
        if account.login(passwd):
            session = Session.open(account, duration=get_duration())
            return jsonify(session.to_dict())

    return ('Invalid user name and / or password.', 401)


@APPLICATION.route('/session', methods=['GET'])
def list_sessions():
    """Lists all sessions iff specified session is root."""

    try:
        session = request.args['session']
    except KeyError:
        return ('No session specified.', 400)

    try:
        session = Session.get(Session.token == session)
    except DoesNotExist:
        return ('No such session.', 404)

    if session.alive:
        if session.account.root:
            sessions = {
                session.token: session.to_dict() for session in Session}
            return jsonify(sessions)

        return ('Not authorized.', 403)

    return ('Session expired.', 410)


@APPLICATION.route('/session/<session_token>', methods=['GET'])
def list_session(session_token):
    """Lists the respective session."""

    try:
        session = Session.get(Session.token == session_token)
    except DoesNotExist:
        return ('No such session.', 404)

    if session.alive:
        return jsonify(session.to_dict())

    return ('Session expired.', 410)


@APPLICATION.route('/session/<session_token>', methods=['PUT'])
def refresh_session(session_token):
    """Refreshes an existing session."""

    try:
        session = Session.get(Session.token == session_token)
    except DoesNotExist:
        return ('No such session.', 404)

    if session.renew(duration=get_duration()):
        return jsonify(session.to_dict())

    return ('Session expired.', 410)


@APPLICATION.route('/session/<session_token>', methods=['DELETE'])
def delete(session_token):
    """Tries to close a specific session identified by its token or
    all sessions for a certain account specified by its name.
    """

    try:
        session = Session.get(Session.token == session_token)
    except DoesNotExist:
        return ('No such session.', 404)

    session.close()
    return jsonify({'closed': session.token})
