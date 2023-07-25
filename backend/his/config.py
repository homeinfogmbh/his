"""HIS configuration."""

from functools import cache, partial

from configlib import load_config


__all__ = [
    "CONFIG_FILE",
    "CORS_FILE",
    "RECAPTCHA_FILE",
    "get_config",
    "get_cors",
    "get_recaptcha",
]


CONFIG_FILE = "his.d/his.conf"
CORS_FILE = "his.d/cors.json"
RECAPTCHA_FILE = "his.d/recaptcha.json"

load_config = cache(load_config)
get_config = partial(load_config, CONFIG_FILE)
get_cors = partial(load_config, CORS_FILE)
get_recaptcha = partial(load_config, RECAPTCHA_FILE)
