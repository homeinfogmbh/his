#! /usr/bin/env python3
"""HIS core handler"""

from homeinfo.lib.rest import RestApp
from his.core import HISProxy

application = RestApp(HISProxy, cors=True, debug=True)
