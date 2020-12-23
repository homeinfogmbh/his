"""Emailing."""

from emaillib import Mailer

from his.config import CONFIG


__all__ = ['MAILER', 'SENDER']


HOST = CONFIG.get('mail', 'host')
PORT = CONFIG.getint('mail', 'port')
USER = CONFIG.get('mail', 'user')
PASSWD = CONFIG.get('mail', 'passwd')
SENDER = CONFIG.get('mail', 'sender')
MAILER = Mailer(HOST, PORT, USER, PASSWD)
