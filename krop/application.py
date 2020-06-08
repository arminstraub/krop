# -*- coding: iso-8859-1 -*-

"""
krop: A tool to crop PDF files

You can use command line arguments in addition to (or, to a degree, instead of) the graphical interface.

For instance, to automatically undo 4 pages print onto a single page:
    krop --go --grid=2x2 file.pdf
To additionally trim each of these pages:
    krop --go --grid=2x2 --trim --trim-use=all file.pdf

Copyright (C) 2010-2020 Armin Straub, http://arminstraub.com
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
    parser = ArgumentParser(prog='krop', description=__doc__,
            formatter_class=RawTextHelpFormatter)

    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)

    parser.add_argument('file', nargs='?', help='PDF file to open')
    parser.add_argument('-o', '--output', help='where to save the cropped PDF')
    parser.add_argument('--whichpages', help='which pages (e.g. "1-5" or "1,3-") to include in cropped PDF (default: all)')
    parser.add_argument('--rotate', type=int, choices=[0,90,180,270], help='how much to rotate the cropped pdf clockwise (default: 0)')
    parser.add_argument('--optimize', choices=['gs', 'no'], help='whether to optimize the final PDF using ghostscript (default: previous choice)')

    parser.add_argument('--grid', help='if set to 2x3, for instance, creates a 2x3 grid of selections on initial page; if only one number is specified, the number of columns/rows is determined according to whether the page is landscape or portrait')

    parser.add_argument('--initialpage', help='which page to open initially (default: 1)')
    parser.add_argument('--selections', type=str, choices=['all', 'evenodd', 'individual'], help='to which pages should selections apply')
    parser.add_argument('--exceptions', help='pages (e.g. "1-5" or "1,3-") which require individual selections')

    parser.add_argument('--trim', action='store_true', help='if specified, will auto trim initial selections')
    parser.add_argument('--trim-use', type=str, choices=['initial', 'all'], help='whether to inspect only the initial page or all pages (slow!) when auto trimming (default: previous value)')
    parser.add_argument('--trim-padding', help='how much padding to include when auto trimming (default: previous value)')

    parser.add_argument('--go', action='store_true', help='output PDF without opening the krop GUI (using the choices supplied on the command line); if used in a script without X server access, you can run krop using xvfb-run')

    parser.add_argument('--no-kde', action='store_true', help='do not use KDE libraries (default: use if available)')
    parser.add_argument('--no-qt5', action='store_true', help='do not use PyQt5 instead of PyQt4 (default: use PyQt5 if available)')
    parser.add_argument('--no-PyPDF2', action='store_true', help='do not use PyPDF2 instead of pyPdf (default: use PyPDF2 if available)')

    args = parser.parse_args()

    # start the GUI
    if KDE:
        #TODO also use PyKDE5 once more easily available
        from PyKDE4.kdecore import ki18n, KCmdLineArgs, KAboutData
        from PyKDE4.kdeui import KApplication
        appName     = "krop"
        catalog     = ""
        programName = ki18n("krop")
         
        aboutData = KAboutData(appName, catalog, programName, __version__)
         
        KCmdLineArgs.init(aboutData)
        app = KApplication()
    else:
        from krop.qt import QApplication
        app = QApplication(sys.argv)
        app.setApplicationName("krop")

    app.setOrganizationName("arminstraub.com")
    app.setOrganizationDomain("arminstraub.com")

    from krop.mainwindow import MainWindow
    window=MainWindow()

    if args.file is not None:
        fileName = args.file
        try:
            fileName = fileName.decode(sys.stdin.encoding or sys.getdefaultencoding())
        except AttributeError:
            # not necessary (or possible) in python3, which uses unicode
            pass
        window.openFile(fileName)

    if args.output is not None:
        window.ui.editFile.setText(args.output)
    if args.whichpages is not None:
        window.ui.editWhichPages.setText(args.whichpages)
    if args.rotate is not None:
        window.ui.comboRotation.setCurrentIndex({0:0,90:2,180:3,270:1}[args.rotate])
    if args.optimize is not None:
        window.ui.checkGhostscript.setChecked(args.optimize == "gs")
    if args.selections is not None:
        if args.selections == "all":
            window.ui.radioSelAll.setChecked(True)
        elif args.selections == "evenodd":
            window.ui.radioSelEvenOdd.setChecked(True)
        elif args.selections == "individual":
            window.ui.radioSelIndividual.setChecked(True)
    if args.exceptions is not None:
        window.ui.editSelExceptions.setText(args.exceptions)
        window.slotSelExceptionsChanged()
    if args.initialpage is not None:
        window.ui.editCurrentPage.setText(args.initialpage)
        window.slotCurrentPageEdited(args.initialpage)
    if args.trim_use is not None:
        window.ui.checkTrimUseAllPages.setChecked(args.trim_use == "all")
    if args.trim_padding is not None:
        window.ui.editPadding.setText(args.trim_padding)

    # args.grid is specified as 2x3 for 2 cols, 3 rows
    if args.grid:
        window.createSelectionGrid(args.grid)

    if args.trim:
        window.slotTrimMarginsAll()

    # shut down on ctrl+c when pressed in terminal (not gracefully, though)
    # http://stackoverflow.com/questions/4938723/
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    if args.go:
        #  sys.stdout.write('kropping...\n')
        from krop.qt import QTimer
        QTimer.singleShot(0, window.slotKrop)
        QTimer.singleShot(0, window.close)
    else:
        window.show()
        window.slotFitInView(window.ui.actionFitInView.isChecked())

    # using exec_ because exec is a reserved keyword before python 3
    sys.exit(app.exec_())
