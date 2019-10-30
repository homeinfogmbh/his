"""ReCAPTCHA related messages."""

from wsgilib import JSONMessage


__all__ = [
    'NO_RESPONSE_PROVIDED',
    'NO_SITE_KEY_PROVIDED',
    'SITE_NOT_CONFIGURED',
    'INVALID_RESPONSE'
]


NO_RESPONSE_PROVIDED = JSONMessage(
    'No ReCAPTCHA response provided.', status=400)
NO_SITE_KEY_PROVIDED = JSONMessage(
    'No ReCAPTCHA site key provided.', status=400)
SITE_NOT_CONFIGURED = JSONMessage('Invalid ReCAPTCHA site key.', status=400)
INVALID_RESPONSE = JSONMessage('Invalid ReCAPTCHA response.', status=401)
