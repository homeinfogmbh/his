"""Emailing."""

from emaillib import Mailer

from his.config import CONFIG


__all__ = ['MAIL_CFG', 'MAILER']


MAIL_CFG = CONFIG['mail']
MAILER = Mailer(
    MAIL_CFG['host'], int(MAIL_CFG['port']), MAIL_CFG['user'],
    MAIL_CFG['passwd'])
