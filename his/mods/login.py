"""HIS login handler"""

from homeinfo.lib.wsgi import Error

from his.api import HISService
from his.orm import Account, Session
from his.crypto import load


class Service(HISService):
    """Handles logins"""

    def get(self):
        """Logs in the user"""
        try:
            account_name = self.qd['account']
        except KeyError:
            return Error('No account specified.', status=400)

        try:
            passwd = self.qd['passwd']
        except KeyError:
            return Error('No password specified.', status=400)

        try:
            account = Account.get(Account.name == account_name)
        except DoesNotExist:
            return Error('Invalid credentials.', status=400)
        else:
            if Session.exists(account):
                return Error('Already logged in.', status=400)
            else:
                # Verify credentials
                pwmgr = load()

                if pwmgr.verify(passwd, account.pwhash, account.salt):
                    Session.open(account, duration=duration)
                    return OK('Session opened.')
                else:
                    return Error('Invalid credentials.', status=400)
