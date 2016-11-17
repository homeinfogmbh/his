#! /usr/bin/env python3
"""HIS core handler"""

from homeinfo.lib.rest import RestApp
from his.core import HISProxy, SessionCleaner

sc = SessionCleaner()
sc.start()
application = RestApp(HISProxy('his'), cors=True, debug=True)
