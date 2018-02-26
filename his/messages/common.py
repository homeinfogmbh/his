"""HIS web API messages."""

from configparser import ConfigParser

from flask import request

from wsgilib import JSON

__all__ = ['MessageNotFound', 'LanguageNotFound', 'locales', 'Message']


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


def locales(filename):
    """Decorator to set the locales file."""

    parser = ConfigParser()
    parser.read(filename)
    return parser


class MetaMessage(type):
    """Metaclass for messages."""

    def __init__(cls, *args, **kwargs):
        """Sets the class's respective locales."""
        super().__init__(*args, **kwargs)

        try:
            del cls.ABSTRACT
        except AttributeError:
            try:
                cls.locales = cls.LOCALES[cls.__name__]
            except KeyError:
                raise MessageNotFound(cls.__name__)


class Message(JSON, metaclass=MetaMessage):
    """Indicates errors for the WebAPI."""

    LOCALES = locales('/etc/his.d/locale/his.ini')
    STATUS = 200
    ABSTRACT = True

    def __init__(self, *data, **fields):
        """Initializes the message."""
        try:
            message = self.__class__.locales[request.args.get('lang', 'de_DE')]
        except KeyError:
            raise LanguageNotFound(lang)

        if data:
            message = message.format(*data)

        dictionary = {'message': message}
        dictionary.update(fields)
        super().__init__(dictionary, status=self.__class__.STATUS)
