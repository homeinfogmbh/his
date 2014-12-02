#! /usr/bin/env python3

from distutils.core import setup

setup(
    name='homeinfo-his',
    version='0.0.1-indev',
    author='Richard Neumann, Nikos Zizopoulos',
    author_email='mail@richard-neumann.de',
    requires=['homeinfo',
              'homeinfo.crm'],
    package_dir={'homeinfo': ''},
    packages=['homeinfo.his',
              'homeinfo.his.wsgi',
              'homeinfo.his.db',
              'homeinfo.his.lib',
              'homeinfo.his.services'],
    data_files=[('/usr/local/etc', ['files/etc/his.conf'])],
    license=open('LICENSE.txt').read(),
    description='HOMEINFO Integrated Services',
    long_description=open('README.txt').read(),
    )

from homeinfo.his.db import __tables__
for table in __tables__:
    print('Creating table', table)
    table.create_table(fail_silently=True)
