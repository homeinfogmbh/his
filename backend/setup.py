#! /usr/bin/env python3

from distutils.core import setup


setup(
    name='his',
    version='latest',
    author='Richard Neumann',
    requires=[
        'argon2', 'configlib', 'docopt', 'emaillib', 'filedb', 'flask',
        'functoolsplus', 'mdb', 'peewee', 'peeweeplus', 'recaptcha',
        'werkzeug', 'wsgilib'],
    packages=[
        'his',
        'his.messages',
        'his.wsgi',
        'his.wsgi.service'],
    scripts=['files/hisutil', 'files/his-session-cleanup'],
    data_files=[('/usr/local/etc/his.d', ['files/pwreset.html'])],
    description='HOMEINFO Integrated Services.')
