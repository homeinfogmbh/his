"""ReCAPTCHA related messages."""

from his.messages.facility import HIS_MESSAGE


__all__ = [
    'NO_RESPONSE_PROVIDED',
    'NO_SITE_KEY_PROVIDED',
    'SITE_NOT_CONFIGURED',
    'INVALID_RESPONSE']


NO_RESPONSE_PROVIDED = HIS_MESSAGE(
    'No ReCAPTCHA response provided.', status=400)
NO_SITE_KEY_PROVIDED = HIS_MESSAGE(
    'No ReCAPTCHA site key provided.', status=400)
SITE_NOT_CONFIGURED = HIS_MESSAGE('Invalid ReCAPTCHA site key.', status=400)
INVALID_RESPONSE = HIS_MESSAGE('Invalid ReCAPTCHA response.', status=401)
