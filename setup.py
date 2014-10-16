#! /usr/bin/env python3

from distutils.core import setup

setup(
	name='his',
	version='0.0.1-indev',
	author='Richard Neumann, Nikos Zizopoulos',
	author_email='mail@richard-neumann.de',
	packages=['his'],
	license=open('LICENSE.txt').read(),
	description='HOMEINFO Integrated Services',
	long_description=open('README.txt').read(),
)