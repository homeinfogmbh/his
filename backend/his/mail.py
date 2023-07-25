"""Emailing."""

from emaillib import Mailer

from his.config import get_config


__all__ = ["get_mailer"]


def get_mailer():
    """Returns the HIS mailer."""

    return Mailer(
        (config := get_config()).get("mail", "host"),
        config.getint("mail", "port"),
        config.get("mail", "user"),
        config.get("mail", "passwd"),
    )
