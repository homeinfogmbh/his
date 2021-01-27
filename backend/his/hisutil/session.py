"""Session management."""

from logging import getLogger

from his.orm import Session


__all__ = ['cleanup']


LOGGER = getLogger('hisutil')


def cleanup():
    """Cleans up orphaned sessions."""

    count = Session.cleanup()

    if count:
        LOGGER.info('Deleted %i orphaned sessions.', count)
    else:
        LOGGER.info('Nothing to do.')
