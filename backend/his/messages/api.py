"""HIS web API messages."""

from gettext import translation

from wsgilib import LANGUAGES, JSON

__all__ = [
    'NoDomainSpecified',
    'MessageNotFound',
    'LanguageNotFound',
    'Message',
    'HISMessage']


LOCALES_DIR = '/etc/his.d/locales'
DEFAULT_LANGS = {'de_DE': 0.1}


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


def _key_lang(language):
    """Returns a key for the respective language."""

    language, quality = language
    return (1-quality, language)


def get_locales(domain):
    """Returns the fist best locale."""

    languages = dict(DEFAULT_LANGS)
    languages.update(dict(LANGUAGES))
    lang_list = [lang for lang, _ in sorted(languages.items(), key=_key_lang)]

    print('LANGUAGES:', [(lang, languages[lang]) for lang in lang_list],
          flush=True)

    try:
        return translation(domain, LOCALES_DIR, lang_list)
    except FileNotFoundError:
        raise LanguageNotFound(languages)


class Message(JSON):
    """Messages returned by the respective web application."""

    STATUS = 200

    def __init__(self, *data, status=None, **fields):
        """Initializes the message."""
        try:
            domain = self.__class__.DOMAIN
        except AttributeError:
            raise NoDomainSpecified(self.__class__)

        msgid = self.__class__.__name__
        message = get_locales(domain).gettext(msgid)

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
