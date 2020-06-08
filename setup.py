#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

"""
Copyright (C) 2014-2020 Armin Straub, http://arminstraub.com
"""

"""
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.
"""

from setuptools import setup


# Automatically determine version from first line of ChangeLog file
import re
with open('ChangeLog') as f:
    s = f.readline()
    version = re.search('\((.*)\)', s).group(1)

# Update version in version.py
with open('krop/version.py', 'w') as f:
    f.write("__version__ = '%s'\n" % (version,))


setup(
        name = 'krop',
        version = version,
        author = 'Armin Straub',
        author_email = 'mail@arminstraub.com',
        url = 'http://arminstraub.com/software/krop',
        description = 'A tool to crop PDF files',
        long_description = 'krop is a simple graphical tool to crop the pages of PDF files. It is written in Python and relies on PyQT, python-poppler-qt5 and PyPDF2 for its functionality. A unique feature of krop is its ability to automatically split pages into subpages to fit the limited screen size of devices such as eReaders. This is particularly useful, if your eReader does not support convenient scrolling.',
        keywords = 'pdf crop ereader',
        packages = ['krop'],
        entry_points = {
            'console_scripts': ['krop = krop.__main__:main']
        },
        # https://pypi.org/classifiers/
        classifiers = [
            'Development Status :: 4 - Beta',
            'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
            'Topic :: Utilities',
            'Intended Audience :: End Users/Desktop',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 3',
            'Environment :: X11 Applications :: Qt',
        ],
)
