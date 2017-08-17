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
    data_files=[
        ('/etc', ['files/etc/his.conf']),
        ('/etc/uwsgi/apps-available',
         ['files/etc/uwsgi/apps-available/his.ini']),
        ('/etc/his.d/locale', ['files/etc/his.d/locale/core.ini']),
        ('/usr/share/his', ['files/usr/share/his/his.wsgi']),
        ('/usr/local/bin', [
            'files/usr/bin/hisutil',
            'files/usr/bin/his-session-cleanup'])],
    description='HOMEINFO Integrated Services')
