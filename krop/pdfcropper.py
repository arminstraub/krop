# -*- coding: iso-8859-1 -*-

"""
Cropping functionality for krop.

Copyright (C) 2010-2020 Armin Straub, http://arminstraub.com
"""

"""
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.
"""

import copy
import sys

# Unless specified otherwise, use PyPDF2 instead of pyPdf if available.
usepypdf2 = '--no-PyPDF2' not in sys.argv
if usepypdf2:
    try:
        from PyPDF2 import PdfReader, PdfWriter
    except ImportError:
        usepypdf2 = False
if not usepypdf2:
    try:
        from pyPdf import PdfReader, PdfWriter
    except ImportError:
        _msg = "Please install PyPDF2 (or its predecessor pyPdf) first."\
            "\n\tOn recent versions of Ubuntu, the following should do the trick:"\
            "\n\tsudo apt-get install python-pypdf2"\
            "\n\t(or, if using python3) sudo apt-get install python3-pypdf2"
        raise RuntimeError(_msg)

class PdfEncryptedError(Exception):
    pass

class AbstractPdfFile:
    """Abstract class for loading a PDF document used in a corresponding
    PdfCropper class"""
    def loadFromStream(self, stream):
        pass
    def loadFromFile(self, filename):
        self.loadFromStream(open(filename, "rb"))

class AbstractPdfCropper:
    """Abstract class for writing a PDF documents composed of cropped pages
    from PdfFile instances"""
    def writeToStream(self, stream):
        pass
    def writeToFile(self, filename):
        stream = open(filename, "wb")
        self.writeToStream(stream)
        stream.close()
    def addPageCropped(self, pdffile, pagenumber, croplist, rotate=0):
        pass
    def copyDocumentRoot(self, pdffile):
        pass


class PyPdfFile(AbstractPdfFile):
    """Implementation of PdfFile using pyPdf"""
    def __init__(self):
        self.reader = None
    def loadFromStream(self, stream):
        if usepypdf2:
            self.reader = PdfReader(stream, strict=False)
        else:
            self.reader = PdfReader(stream)
        if self.reader.is_encrypted:
            try:
                if not self.reader.decrypt(''):
                    raise PdfEncryptedError
            except:
                raise PdfEncryptedError
    def getPage(self, nr):
        page = self.reader.pages[nr-1]

class PyPdfCropper(AbstractPdfCropper):
    """Implementation of PdfCropper using pyPdf"""
    def __init__(self):
        self.output = PdfWriter()
    def writeToStream(self, stream):
        # For certain large pdf files, PdfWriter.write() causes the error:
        #  maximum recursion depth exceeded while calling a Python object
        # This issue is present in pyPdf as well as PyPDF2 1.23
        # We therefore temporarily increase the recursion limit.
        old_reclimit = sys.getrecursionlimit()
        sys.setrecursionlimit(10000)
        self.output.write(stream)
        sys.setrecursionlimit(old_reclimit)
    def addPageCropped(self, pdffile, pagenumber, croplist, alwaysinclude, rotate=0):
        page = pdffile.reader.pages[pagenumber]
        if not croplist and alwaysinclude:
            self.output.add_page(page)
        for c in croplist:
            newpage = copy.copy(page)
            self.cropPage(newpage, c, rotate)
            self.output.add_page(newpage)
    def cropPage(self, page, crop, rotate):
        # Note that the coordinate system is up-side down compared with Qt.
        x0, y0 = page.cropbox.lower_left
        x1, y1 = page.cropbox.upper_right
        x0, y0, x1, y1 = float(x0), float(y0), float(x1), float(y1)
        x0, x1 = x0+crop[0]*(x1-x0), x1-crop[2]*(x1-x0)
        y0, y1 = y0+crop[3]*(y1-y0), y1-crop[1]*(y1-y0)
        # Update the various PDF boxes
        for box in (page.artbox, page.bleedbox, page.cropbox, page.mediabox, page.trimbox):
            box.lower_left = (x0, y0)
            box.upper_right = (x1, y1)
        if rotate != 0:
            page.rotate_clockwise(rotate)

    def copyDocumentRoot(self, pdffile):
        # Sounds promising in PyPDF2 (see PdfWriter.cloneDocumentFromReader),
        # but doesn't seem to produce a readable PDF:
        # self.output.cloneReaderDocumentRoot(pdffile.reader)
        # Instead, this copies at least the named destinations for links:
        for dest in pdffile.reader.named_destinations.values():
            self.output.add_named_destination_object(dest)


def optimizePdfGhostscript(oldfilename, newfilename):
    import subprocess
    subprocess.check_call(('gs', '-sDEVICE=pdfwrite', '-sOutputFile=' + newfilename,
        '-dNOPAUSE', '-dBATCH', oldfilename))

PdfFile = PyPdfFile
PdfCropper = PyPdfCropper

