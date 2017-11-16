#! /usr/bin/env python3
"""HIS core handler"""

from wsgilib import RestApp
from his.wsgi import ROUTER

application = RestApp(ROUTER, cors=True, debug=True)
