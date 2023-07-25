#! /usr/bin/env python3
"""Install scipt."""

from setuptools import setup


setup(
    name="his",
    use_scm_version={
        "root": "..",
        "relative_to": __file__,
        "local_scheme": "node-and-timestamp",
    },
    setup_requires=["setuptools_scm"],
    install_requires=[
        "argon2_cffi",
        "configlib",
        "emaillib",
        "filedb",
        "flask",
        "mdb",
        "peewee",
        "peeweeplus",
        "recaptcha",
        "setuptools",
        "werkzeug",
        "wsgilib",
    ],
    author="HOMEINFO - Digitale Informationssysteme GmbH",
    author_email="<info@homeinfo.de>",
    maintainer="Richard Neumann",
    maintainer_email="<r.neumann@homeinfo.de>",
    packages=["his", "his.hisutil", "his.orm", "his.wsgi", "his.wsgi.service"],
    entry_points={"console_scripts": ["hisutil = his.hisutil:main"]},
    data_files=[
        ("/usr/local/etc/his.d", ["files/pwreset.html", "files/bugreport.html"])
    ],
    description="HOMEINFO Integrated Services.",
)
