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

from version import __version__
from config import KDE


def main():
    from argparse import ArgumentParser, RawTextHelpFormatter
    parser = ArgumentParser(description=__doc__, version=__version__,
            formatter_class=RawTextHelpFormatter)

    parser.add_argument('file', nargs='?', help='PDF file to open')
    parser.add_argument('--nokde', action='store_true', help='do not use KDE libraries (default: use if available)')

    args = parser.parse_args()

    # start the GUI
    if KDE:
        from PyKDE4.kdecore import ki18n, KCmdLineArgs, KAboutData
        from PyKDE4.kdeui import KApplication
        appName     = "krop"
        catalog     = ""
        programName = ki18n("krop")
         
        aboutData = KAboutData(appName, catalog, programName, __version__)
         
        KCmdLineArgs.init (sys.argv, aboutData)
        app = KApplication()
    else:
        from PyQt4.QtGui import QApplication
        app = QApplication(sys.argv)
        app.setApplicationName("krop")

    app.setOrganizationName("arminstraub.com")
    app.setOrganizationDomain("arminstraub.com")

    from mainwindow import MainWindow
    window=MainWindow()

    if args.file is not None:
        window.openFile(args.file)

    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
