#! /usr/bin/env python3

from distutils.core import setup
from peewee import OperationalError

setup(
    name='homeinfo.his',
    version='0.0.1-indev',
    author='Richard Neumann, Nikos Zizopoulos',
    author_email='mail@richard-neumann.de',
    requires=['homeinfo',
              'homeinfo.crm',
              'pcp'],
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


try:
    from homeinfo.his.db import __tables__
except OperationalError:
    print('WARNING: No database access - Won\'t create any tables')
else:
    for table in __tables__:
        try:
            print('Creating table', table)
            table.create_table(fail_silently=True)
        except:
            print('Could not create table:', str(table))
