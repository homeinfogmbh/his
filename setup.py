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
        'his.mods'],
    scripts=['files/hisutil', 'files/his-session-cleanup'],
    data_files=[
        ('/etc/uwsgi/apps-available', ['files/his.ini']),
        ('/etc/his.d/locale', ['files/core.ini']),
        ('/usr/share/his', ['files/his.wsgi'])],
    description='HOMEINFO Integrated Services.')
