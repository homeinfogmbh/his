"""Bug report related messages."""

from wsgilib import JSONMessage


__all__ = ['BUGREPORT_SENT']


BUGREPORT_SENT = JSONMessage('Bug report has been sent.', status=200)
