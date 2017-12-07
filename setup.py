#! /usr/bin/env python3

from distutils.core import setup


setup(
    name='his',
    version='latest',
    author='Richard Neumann',
    requires=['homeinfo.crm'],
    packages=[
        'his',
        'his.api',
        'his.wsgi'],
    scripts=['files/hisd', 'files/hisutil', 'files/his-session-cleanup'],
    data_files=[
        ('/usr/lib/systemd/system', ['files/his.service'])
        ('/etc/his.d/locale', ['files/his.ini'])],
    description='HOMEINFO Integrated Services.')
