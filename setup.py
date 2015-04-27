#! /usr/bin/env python3

from distutils.core import setup
from homeinfo.lib.misc import GitInfo

version, author, author_email, *_ = GitInfo()

setup(
    name='homeinfo-his',
    version=version,
    author=author,
    author_email=author_email,
    requires=['pcp',
              'homeinfo.crm'],
    package_dir={'homeinfo': ''},
    packages=['homeinfo.his',
              'homeinfo.his.api',
              'homeinfo.his.db',
              'homeinfo.his.lib',
              'homeinfo.his.wsgi'],
    data_files=[('/usr/local/etc', ['files/etc/his.conf'])],
    license=open('LICENSE.txt').read(),
    description='Main library for the HOMEINFO Integrated Services',
    )
