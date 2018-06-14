"""HIS web API messages."""

from configparser import ConfigParser

from flask import request

from wsgilib import JSON

__all__ = ['MessageNotFound', 'LanguageNotFound', 'Message']


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


class MetaMessage(type):
    """Metaclass for messages."""

    def __init__(cls, *args, **kwargs):
        """Sets the class's respective locales."""
        super().__init__(*args, **kwargs)

        try:
            locales = cls.LOCALES
        except AttributeError:
            pass
        else:
            if isinstance(locales, str):
                cls.LOCALES = ConfigParser()
                cls.LOCALES.read(locales)

    @property
    def locales(cls):
        """Returns the class' locales."""
        try:
            return cls.LOCALES[cls.__name__]
        except KeyError:
            raise MessageNotFound(cls.__name__)


class Message(JSON, metaclass=MetaMessage):
    """Indicates errors for the WebAPI."""

    STATUS = 200

    def __init__(self, *data, status=None, **fields):
        """Initializes the message."""
        language = request.args.get('lang', 'de_DE')

        try:
            message = self.__class__.locales[language]  # Class property!
        except KeyError:
            raise LanguageNotFound(language)

        if status is None:
            status = self.__class__.STATUS

        if data:
            message = message.format(*data)

        dictionary = {'message': message}
        dictionary.update(fields)
        super().__init__(dictionary, status=status)
