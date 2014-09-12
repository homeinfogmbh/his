"""
Common Real Estate API, Modified
"""
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'

from openimmofs import ITF as OpenImmoFS

#===============================================================================
# Main index method
#===============================================================================
def index(req): 
    with open('/var/www/de/homeinfo/api/openimmo-data_127.xml', 'r', 
              encoding='latin1') as oi_xml:
        xmldata = oi_xml.read()