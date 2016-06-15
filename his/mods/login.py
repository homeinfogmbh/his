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
            account_name = self.query_dict['account']
            passwd = self.query_dict['passwd']
        except KeyError:
            return Error('No credentials specified.', status=400)
        else:
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
                        Session.open(account)
                        return OK('Session opened.')
                    else:
                        return Error('Invalid credentials.', status=400)
