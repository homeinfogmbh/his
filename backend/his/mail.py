"""Emailing."""

from emaillib import Mailer

from his.config import CONFIG


__all__ = ['get_mailer']


def get_mailer():
    """Returns the HIS mailer."""

    return Mailer(
        CONFIG.get('mail', 'host'), CONFIG.getint('mail', 'port'),
        CONFIG.get('mail', 'user'), CONFIG.get('mail', 'passwd'))
