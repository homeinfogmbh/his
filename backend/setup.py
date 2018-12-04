#! /usr/bin/env python3

from distutils.core import setup


setup(
    name='his',
    version='latest',
    author='Richard Neumann',
    requires=['mdb'],
    packages=[
        'his',
        'his.cache',
        'his.messages',
        'his.wsgi',
        'his.wsgi.service'],
    scripts=['files/hisutil', 'files/his-session-cleanup'],
    data_files=[('/etc/his.d', ['files/pwreset.html'])],
    description='HOMEINFO Integrated Services.')
