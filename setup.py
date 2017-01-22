#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

"""
Copyright (C) 2014-2017 Armin Straub, http://arminstraub.com
"""

"""
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.
"""

from distutils.core import setup


# Automatically determine version from first line of ChangeLog file
import re
with open('ChangeLog') as f:
    s = f.readline()
    version = re.search('\((.*)\)', s).group(1)

# Update version in version.py
with open('krop/version.py', 'w') as f:
    f.write("__version__ = '%s'\n" % (version,))

# For reading long_description from README file (stolen from setup.py documentation)
import os
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
        name = 'krop',
        version = version,
        author = 'Armin Straub',
        author_email = 'mail@arminstraub.com',
        url = 'http://arminstraub.com/software/krop',
        description = 'A tool to crop PDF files',
        long_description = read('README'),
        keywords = 'pdf crop ereader',
        packages = ['krop'],
        scripts = ['bin/krop'],
        classifiers = [
            'Development Status :: 3 - Alpha',
            'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
            'Topic :: Utilities',
            'Intended Audience :: End Users/Desktop',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 3',
            'Environment :: X11 Applications :: Qt',
        ],
)
