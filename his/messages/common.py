"""HIS web API messages."""

from configparser import ConfigParser

from wsgilib import JSON

__all__ = ['locales', 'Message']


DEFAULT_LANGUAGE = 'de_DE'


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

        # Exclude Message base class and protected (abstract) messages.
        print('MRO:', cls.__mro__, flush=True)
        if cls.__mro__[1] is JSON and not cls.__name__.startswith('_'):
            try:
                cls.locales = cls.LOCALES[cls.__name__]
            except KeyError:
                raise MessageNotFound(cls.__name__)


class Message(JSON, metaclass=MetaMessage):
    """Indicates errors for the WebAPI."""

    LOCALES = locales('/etc/his.d/locale/his.ini')
    STATUS = 200

    def __init__(self, *data, lang=DEFAULT_LANGUAGE, **fields):
        """Initializes the message."""
        try:
            message = self.__class__.locales[lang]  # Set by metaclass.
        except KeyError:
            raise LanguageNotFound(lang)

        if data:
            message = message.format(*data)

        dictionary = {'message': message}
        dictionary.update(fields)
        super().__init__(dictionary, status=self.__class__.STATUS)
