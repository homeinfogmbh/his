"""HIS WSGI core services."""

from flask import Flask

from his.wsgi.account import *
from his.wsgi.customer import *
from his.wsgi.service import *
from his.wsgi.session import *

__all__ = ['APPLICATION']


APPLICATION = Flask('his')
