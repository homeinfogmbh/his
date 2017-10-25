#! /usr/bin/env python3
"""HIS core handler"""

from wsgilib import RestApp
from his.core import HISProxy

application = RestApp(HISProxy('his'), cors=True, debug=True)
