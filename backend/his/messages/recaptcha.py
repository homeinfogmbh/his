"""ReCAPTCHA related messages."""

from his.messages.api import HISMessage


__all__ = [
    'NO_RESPONSE_PROVIDED',
    'NO_SITE_KEY_PROVIDED',
    'SITE_NOT_CONFIGURED',
    'INVALID_RESPONSE']


NO_RESPONSE_PROVIDED = HISMessage(
    'No ReCAPTCHA response provided.', status=400)
NO_SITE_KEY_PROVIDED = HISMessage(
    'No ReCAPTCHA site key provided.', status=400)
SITE_NOT_CONFIGURED = HISMessage('Invalid ReCAPTCHA site key.', status=400)
INVALID_RESPONSE = HISMessage('Invalid ReCAPTCHA response.', status=401)
