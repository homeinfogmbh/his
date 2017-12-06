"""HIS web API messages."""

from configparser import ConfigParser

from wsgilib import JSON

__all__ = ['Message']


DEFAULT_LANGUAGE = 'de_DE'


def locales(filename):
    """Decorator to set the locales file."""

    parser = ConfigParser()
    parser.read(filename)
    return parser


class Message(JSON):
    """Indicates errors for the WebAPI."""

    STATUS = 200
    LOCALES = locales('/etc/his.d/locale/core.ini')

    def __init__(self, *data, lang=DEFAULT_LANGUAGE, **fields):
        """Initializes the message."""
        dictionary = {'message': self.message(lang, data=data)}
        dictionary.update(fields)
        super().__init__(dictionary, status=self.STATUS)

    @property
    def locales(self):
        """Returns the classes locales."""
        try:
            return self.__class__.LOCALES[self.__class__.__name__]
        except KeyError:
            return {}

    def message(self, lang, data=None):
        """Returns the respective message."""
        try:
            message = self.locales[lang]
        except KeyError:
            return 'Could not get locale: {}.'.format(lang)

        if data:
            return message.format(*data)

        return message
