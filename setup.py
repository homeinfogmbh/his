#! /usr/bin/env python3

from distutils.core import setup


setup(
    name='his',
    version='latest',
    author='Richard Neumann',
    requires=['homeinfo.crm'],
    packages=['his', 'his.messages', 'his.wsgi'],
    scripts=['files/hisutil', 'files/his-session-cleanup'],
    data_files=[('/etc/his.d/locale/his', [
        'files/locales/account.ini',
        'files/locales/customer.ini',
        'files/locales/data.ini',
        'files/locales/pwreset.ini',
        'files/locales/service.ini',
        'files/locales/session.ini'])],
    description='HOMEINFO Integrated Services.')
