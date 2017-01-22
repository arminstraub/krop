# -*- coding: iso-8859-1 -*-

"""
krop: A tool to crop PDF files

Copyright (C) 2010-2017 Armin Straub, http://arminstraub.com
"""

"""
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.
"""

import sys

from krop.version import __version__
from krop.config import KDE


def main():
    from argparse import ArgumentParser, RawTextHelpFormatter
    parser = ArgumentParser(description=__doc__,
            formatter_class=RawTextHelpFormatter)

    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)

    parser.add_argument('file', nargs='?', help='PDF file to open')
    parser.add_argument('-o', '--output', help='where to save the cropped PDF')
    parser.add_argument('--rotate', type=int, choices=[0,90,180,270], help='how much to rotate the cropped pdf clockwise (default: 0)')
    parser.add_argument('--whichpages', help='which pages (e.g. "1-5" or "1,3-") to include in cropped PDF (default: all)')
    parser.add_argument('--initialpage', help='which page to open initially (default: 1)')
    parser.add_argument('--autotrim', action='store_true', help='create a selection for the entire initial page minus blank margins')
    parser.add_argument('--selections', type=str, choices=['all','evenodd','individual'], help='to which pages should selections apply')
    parser.add_argument('--no-kde', action='store_true', help='do not use KDE libraries (default: use if available)')
    parser.add_argument('--no-PyPDF2', action='store_true', help='do not use PyPDF2 instead of pyPdf (default: use PyPDF2 if available)')

    args = parser.parse_args()

    # start the GUI
    if KDE:
        from PyKDE4.kdecore import ki18n, KCmdLineArgs, KAboutData
        from PyKDE4.kdeui import KApplication
        appName     = "krop"
        catalog     = ""
        programName = ki18n("krop")
         
        aboutData = KAboutData(appName, catalog, programName, __version__)
         
        KCmdLineArgs.init(aboutData)
        app = KApplication()
    else:
        from PyQt4.QtGui import QApplication
        app = QApplication(sys.argv)
        app.setApplicationName("krop")

    app.setOrganizationName("arminstraub.com")
    app.setOrganizationDomain("arminstraub.com")

    from krop.mainwindow import MainWindow
    window=MainWindow()

    if args.file is not None:
        fileName = args.file.decode(sys.stdin.encoding or sys.getdefaultencoding())
        window.openFile(fileName)
    if args.output is not None:
        window.ui.editFile.setText(args.output)
    if args.whichpages is not None:
        window.ui.editWhichPages.setText(args.whichpages)
    if args.rotate is not None:
        window.ui.comboRotation.setCurrentIndex({0:0,90:2,180:3,270:1}[args.rotate])
    if args.selections is not None:
        if args.selections == 'all':
            window.ui.radioSelAll.setChecked(True)
        elif args.selections == 'evenodd':
            window.ui.radioSelEvenOdd.setChecked(True)
        elif args.selections == 'individual':
            window.ui.radioSelIndividual.setChecked(True)
    if args.initialpage is not None:
        window.ui.editCurrentPage.setText(args.initialpage)
        window.slotCurrentPageEdited(args.initialpage)
    if args.autotrim:
        window.slotTrimMarginsAll()

    # shut down on ctrl+c when pressed in terminal (not gracefully, though)
    # http://stackoverflow.com/questions/4938723/
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    window.show()
    sys.exit(app.exec_())
