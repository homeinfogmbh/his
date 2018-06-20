#! /usr/bin/env python3

from distutils.core import setup


setup(
    name='his',
    version='latest',
    author='Richard Neumann',
    requires=['homeinfo.crm'],
    packages=['his', 'his.messages', 'his.wsgi'],
    scripts=['files/hisutil', 'files/his-session-cleanup'],
    data_files=[('/etc/his.d', ['files/pwreset.html'])],
    description='HOMEINFO Integrated Services.')
