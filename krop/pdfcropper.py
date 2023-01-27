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
from pikepdf import Pdf


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


class PyPdfFile(AbstractPdfFile):
    """Implementation of PdfFile using pyPdf"""
    def __init__(self):
        self.reader = None
    def loadFromStream(self, stream):
        self.reader = Pdf.open(stream)
        if self.reader.is_encrypted:
            raise PdfEncryptedError


class PyPdfCropper(AbstractPdfCropper):
    """Implementation of PdfCropper using pyPdf"""
    def __init__(self):
        self.pdf = Pdf.new()

    def writeToStream(self, stream):
        # For certain large pdf files, PdfFileWriter.write() causes the error:
        #  maximum recursion depth exceeded while calling a Python object
        # This issue is present in pyPdf as well as PyPDF2 1.23
        # We therefore temporarily increase the recursion limit.
        old_reclimit = sys.getrecursionlimit()
        sys.setrecursionlimit(10000)
        self.pdf.save(stream)
        sys.setrecursionlimit(old_reclimit)

    def addPageCropped(self, pdffile, pagenumber, croplist, alwaysinclude, rotate=0):
        page = pdffile.reader.pages[pagenumber]
        if not croplist and alwaysinclude:
            self.pdf.pages.append(page)
        for c in croplist:
            new_box = self.getCropPageParm(page, c)
            # Update the various PDF boxes
            new_page = copy.copy(page)
            new_page.mediabox = new_box
            new_page.cropbox = new_box
            new_page.trimbox = new_box
            if rotate != 0:
                new_page.rotate(rotate, True)
            self.pdf.pages.append(new_page)

    def getCropPageParm(self, page, crop):
        # Note that the coordinate system is up-side down compared with Qt.
        x0, y0, x1, y1 = page.cropbox
        x0, y0, x1, y1 = float(x0), float(y0), float(x1), float(y1)
        x0, x1 = x0+crop[0]*(x1-x0), x1-crop[2]*(x1-x0)
        y0, y1 = y0+crop[3]*(y1-y0), y1-crop[1]*(y1-y0)
        return [x0, y0, x1, y1]


def optimizePdfGhostscript(oldfilename, newfilename):
    import subprocess
    subprocess.check_call(('gs', '-sDEVICE=pdfwrite', '-sOutputFile=' + newfilename,
        '-dNOPAUSE', '-dBATCH', oldfilename))

PdfFile = PyPdfFile
PdfCropper = PyPdfCropper
