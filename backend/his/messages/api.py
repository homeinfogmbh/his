"""HIS web API messages."""

from wsgilib import Message


__all__ = ['HISMessage']


class HISMessage(Message):
    """A Message from the HIS domain."""

    BASEDIR = '/usr/local/etc/his.d/locales'
    DOMAIN = 'his'
    DEFAULT = {'de_DE': 0.1}
