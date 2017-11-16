#! /usr/bin/env python3
"""HIS core handler"""

from wsgilib import RestApp
from his.core import mk_router

application = RestApp(mk_router('his'), cors=True, debug=True)
