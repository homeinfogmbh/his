#! /usr/bin/env python3

from distutils.core import setup

setup(
    name='homeinfo.his',
    version='0.0.1-indev',
    author='Richard Neumann, Nikos Zizopoulos',
    author_email='r.neumann@homeinfo.de',
    requires=['pcp',
              'homeinfo',
              'homeinfo.crm'],
    package_dir={'homeinfo': ''},
    packages=['homeinfo.his',
              'homeinfo.his.api',
              'homeinfo.his.db',
              'homeinfo.his.lib',
              'homeinfo.his.wsgi'],
    data_files=[('/usr/local/etc', ['files/etc/his.conf'])],
    license=open('LICENSE.txt').read(),
    description='HOMEINFO Integrated Services',
    long_description=open('README.txt').read(),
    )
