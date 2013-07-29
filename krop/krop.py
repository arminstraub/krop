#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

"""
Krop: A tool to crop PDF files, with an eye towards eReaders

Copyright (C) 2010-2013 Armin Straub, http://arminstraub.com
"""

"""
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.
"""

import sys

from PyQt4.QtGui import QApplication

from version import __version__
from mainwindow import MainWindow


def main():
    from argparse import ArgumentParser, RawTextHelpFormatter
    parser = ArgumentParser(description=__doc__, version=__version__,
            formatter_class=RawTextHelpFormatter)
    parser.add_argument('file', nargs='?')

    args = parser.parse_args()

    # start the GUI
    app = QApplication(sys.argv)

    QApplication.setOrganizationName("arminstraub.com")
    QApplication.setOrganizationDomain("arminstraub.com")
    QApplication.setApplicationName("krop")

    window=MainWindow()

    if args.file is not None:
        window.openFile(args.file)

    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
