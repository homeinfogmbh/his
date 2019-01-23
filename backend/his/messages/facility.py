"""HIS web API messages."""

from wsgilib import MessageFacility


__all__ = ['HIS_MESSAGE_FACILITY', 'HIS_MESSAGE']


HIS_MESSAGE_FACILITY = MessageFacility('/usr/local/etc/his.d/locales')
HIS_MESSAGE_DOMAIN = HIS_MESSAGE_FACILITY.domain('his')
HIS_MESSAGE = HIS_MESSAGE_DOMAIN.message
