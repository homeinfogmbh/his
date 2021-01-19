"""Session management."""

from logging import getLogger

from his.orm import Session


__all__ = ['cleanup']


LOGGER = getLogger('hisutil')


def cleanup():
    """Cleans up orphaned sessions."""

    count = 0

    for count, session in enumerate(Session.cleanup(), start=1):
        LOGGER.info('Removing session: %s', session)

    if count:
        LOGGER.info('Deleted %i orphaned sessions.', count)
    else:
        LOGGER.info('Nothing to do.')
