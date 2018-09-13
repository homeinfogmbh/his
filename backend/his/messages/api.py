"""HIS web API messages."""

from gettext import translation

from flask import request

from wsgilib import JSON

__all__ = [
    'NoDomainSpecified',
    'MessageNotFound',
    'LanguageNotFound',
    'Message',
    'HISMessage']


LOCALES_DIR = '/etc/his.d/locales'


class NoDomainSpecified(Exception):
    """Indicates that no domain was specified."""

    def __init__(self, message):
        """Sets the message with the missing domain."""
        super().__init__(message)
        self.message = message


class MessageNotFound(Exception):
    """Indicates that the respective message could not be found."""

    def __init__(self, message):
        """Sets the respective message."""
        super().__init__(message)
        self.message = message


class LanguageNotFound(Exception):
    """Indicates that the respective language could not be found."""

    def __init__(self, lang):
        """Sets the respective language."""
        super().__init__(lang)
        self.lang = lang


class Message(JSON):
    """Messages returned by the respective web application."""

    STATUS = 200

    def __init__(self, *data, status=None, **fields):
        """Initializes the message."""
        try:
            domain = self.__class__.DOMAIN
        except AttributeError:
            raise NoDomainSpecified(self.__class__)

        language = request.args.get('lang', 'de_DE')

        try:
            locales = translation(domain, LOCALES_DIR, [language])
        except FileNotFoundError:
            raise LanguageNotFound(language)

        msgid = self.__class__.__name__
        message = locales.gettext(msgid)

        if message == msgid:
            raise MessageNotFound(msgid)

        if status is None:
            status = self.__class__.STATUS

        if data:
            message = message.format(*data)

        dictionary = {'message': message}
        dictionary.update(fields)
        super().__init__(dictionary, status=status)


class HISMessage(Message):
    """A message for the HIS domain."""

    DOMAIN = 'his'
