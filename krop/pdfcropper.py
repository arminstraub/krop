# -*- coding: iso-8859-1 -*-

"""
Cropping functionality for krop.

Copyright (C) 2010-2023 Armin Straub, http://arminstraub.com
"""

"""
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.
"""

import copy
import sys


class PdfEncryptedError(Exception):
    pass


class AbstractPdfFile:
    """Abstract class for loading a PDF document used in a corresponding
    PdfCropper class"""
    def loadFromStream(self, stream):
        pass
    def loadFromFile(self, filename):
        self.loadFromStream(open(filename, "rb"))

class PyPdfFile(AbstractPdfFile):
    """Implementation of PdfFile using the new pypdf"""
    def __init__(self):
        self.reader = None
    def loadFromStream(self, stream):
        self.reader = PdfReader(stream)
        if self.reader.is_encrypted:
            try:
                if not self.reader.decrypt(''):
                    raise PdfEncryptedError
            except:
                raise PdfEncryptedError
    def getPage(self, nr):
        return self.reader.pages[nr]

class PyPdfOldFile(PyPdfFile):
    """Implementation of PdfFile using PyPDF2 or the old PyPdf"""
    def loadFromStream(self, stream):
        if pypdf_version == 2:
            self.reader = PdfReader(stream, strict=False)
        else:
            self.reader = PdfReader(stream)
        if self.reader.isEncrypted:
            try:
                if not self.reader.decrypt(''):
                    raise PdfEncryptedError
            except:
                raise PdfEncryptedError
    def getPage(self, nr):
        return self.reader.getPage(nr)

class PikePdfFile(AbstractPdfFile):
    """Implementation of PdfFile using pikepdf"""
    def __init__(self):
        self.reader = None
    def loadFromStream(self, stream):
        self.reader = Pdf.open(stream)
        if self.reader.is_encrypted:
            raise PdfEncryptedError
    def getPage(self, nr):
        return self.reader.pages[nr]


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

class SemiAbstractPdfCropper(AbstractPdfCropper):
    """An extension of AbstractPdfCropper that implements the basic logic
    breaking it down to certain functions on pages"""
    def addPageCropped(self, pdffile, pagenumber, croplist, alwaysinclude, rotate=0):
        page = pdffile.getPage(pagenumber)
        if not croplist and alwaysinclude:
            self.doAddPage(page)
        else:
            box = self.pageGetCropBox(page)
            for crop in croplist:
                new_page = copy.copy(page)
                new_box = computeCropBoxCoords(box, crop)
                self.pageSetCropBox(new_page, new_box)
                if rotate != 0:
                    self.pageRotateClockwise(new_page, rotate)
                self.doAddPage(new_page)
    def doAddPage(self, page):
        pass
    def pageGetCropBox(self, page):
        pass
    def pageSetCropBox(self, page, box):
        pass
    def pageRotateClockwise(self, page, rotate):
        pass

class PyPdfCropper(SemiAbstractPdfCropper):
    """Implementation of PdfCropper using pypdf"""
    def __init__(self):
        self.output = PdfWriter()
    def writeToStream(self, stream):
        # For certain large pdf files, PdfWriter.write() causes the error:
        #   maximum recursion depth exceeded while calling a Python object
        # This issue is present in pyPdf as well as PyPDF2 1.23
        # We therefore temporarily increase the recursion limit.
        old_reclimit = sys.getrecursionlimit()
        sys.setrecursionlimit(10000)
        self.output.write(stream)
        sys.setrecursionlimit(old_reclimit)
    def doAddPage(self, page):
        self.output.add_page(page)
    def pageGetCropBox(self, page):
        x0, y0 = page.cropbox.lower_left
        x1, y1 = page.cropbox.upper_right
        return x0, y0, x1, y1
    def pageSetCropBox(self, page, box):
        x0, y0, x1, y1 = box
        for page_box in (page.artbox, page.bleedbox, page.cropbox, page.mediabox, page.trimbox):
            page_box.lower_left = (x0, y0)
            page_box.upper_right = (x1, y1)
    def pageRotateClockwise(self, page, rotate):
        page.rotate_clockwise(rotate)
    def copyDocumentRoot(self, pdffile):
        # Sounds promising in PyPDF2 (see PdfWriter.cloneDocumentFromReader),
        # but doesn't seem to produce a readable PDF:
        # self.output.cloneReaderDocumentRoot(pdffile.reader)
        # Instead, this copies at least the named destinations for links:
        for dest in pdffile.reader.named_destinations.values():
            self.output.add_named_destination_object(dest)

class PyPdfOldCropper(PyPdfCropper):
    """Implementation of PdfCropper using PyPDF2 or the old PyPdf"""
    def doAddPage(self, page):
        self.output.addPage(page)
    def pageGetCropBox(self, page):
        x0, y0 = page.cropBox.lowerLeft
        x1, y1 = page.cropBox.upperRight
        return x0, y0, x1, y1
    def pageSetCropBox(self, page, box):
        x0, y0, x1, y1 = box
        for page_box in (page.artBox, page.bleedBox, page.cropBox, page.mediaBox, page.trimBox):
            page_box.lowerLeft = (x0, y0)
            page_box.upperRight = (x1, y1)
    def pageRotateClockwise(self, page, rotate):
        page.rotateClockwise(rotate)
    def copyDocumentRoot(self, pdffile):
        # Sounds promising in PyPDF2 (see PdfWriter.cloneDocumentFromReader),
        # but doesn't seem to produce a readable PDF:
        # self.output.cloneReaderDocumentRoot(pdffile.reader)
        # Instead, this copies at least the named destinations for links:
        for dest in pdffile.reader.namedDestinations.values():
            self.output.addNamedDestinationObject(dest)


class PikePdfCropper(SemiAbstractPdfCropper):
    """Implementation of PdfCropper using pikepdf"""
    def __init__(self):
        self.output = Pdf.new()
    def writeToStream(self, stream):
        self.output.save(stream)
    def doAddPage(self, page):
        self.output.pages.append(page)
    def pageGetCropBox(self, page):
        try:
            # only page.MediaBox exists in pikepdf version 1.10.3 as currently in Ubuntu 20.04
            return page.cropbox
        except AttributeError:
            raise RuntimeError("Please install a more recent version of pikepdf.")
    def pageSetCropBox(self, page, box):
        page.mediabox = box
        page.cropbox = box
        page.trimbox = box
    def pageRotateClockwise(self, page, rotate):
        page.rotate(rotate, relative=True)
    def copyDocumentRoot(self, pdffile):
        pass


def computeCropBoxCoords(box, crop):
    x0, y0, x1, y1 = box
    x0, y0, x1, y1 = float(x0), float(y0), float(x1), float(y1)
    # Note that the coordinate system is up-side down compared with Qt.
    x0, x1 = x0+crop[0]*(x1-x0), x1-crop[2]*(x1-x0)
    y0, y1 = y0+crop[3]*(y1-y0), y1-crop[1]*(y1-y0)
    return x0, y0, x1, y1

def optimizePdfGhostscript(oldfilename, newfilename):
    import subprocess
    subprocess.check_call(('gs', '-sDEVICE=pdfwrite', '-sOutputFile=' + newfilename,
        '-dNOPAUSE', '-dBATCH', oldfilename))


# determine which of pypdf, PyPDF2, pyPdf, pikepdf to use
use_pikepdf = False
pypdf_version = 0 # 3 = new pypdf, 2 = PyPDF2, 1 = old pyPdf, 0 = none

# use pikepdf if requested
if '--use-pikepdf' in sys.argv:
    try:
        from pikepdf import Pdf
        use_pikepdf = True
    except ImportError:
        print("pikepdf was requested but failed to load.", file=sys.stderr)

# use PyPDF2 if requested
if '--use-pypdf2' in sys.argv:
    try:
        from PyPDF2 import PdfFileReader as PdfReader, PdfFileWriter as PdfWriter
        pypdf_version = 2
    except ImportError:
        print("PyPDF2 was requested but failed to load.", file=sys.stderr)

# by default use pypdf / PyPDF2
if not use_pikepdf and not pypdf_version:
    # if possible use the new pypdf
    try:
        from pypdf import PdfReader, PdfWriter
        pypdf_version = 3
    except ImportError:
        pass
    # otherwise use PyPDF2
    if not pypdf_version:
        try:
            from PyPDF2 import PdfFileReader as PdfReader, PdfFileWriter as PdfWriter
            pypdf_version = 2
        except ImportError:
            pass
    # or the very old pyPdf
    if not pypdf_version:
        try:
            from pyPdf import PdfFileReader as PdfReader, PdfFileWriter as PdfWriter
            pypdf_version = 1
        except ImportError:
            pass
    # try pikepdf
    if not pypdf_version:
        try:
            from pikepdf import Pdf
            use_pikepdf = True
        except ImportError:
            pass
    # complain if no version is available
    if not pypdf_version and not use_pikepdf:
        _msg = "Please install pypdf (or its predecessor PyPDF2) or a new version of pikepdf first."\
            "\n\tOn recent versions of Ubuntu, the following should do the trick:"\
            "\n\tsudo apt-get install python3-pypdf2"
        raise RuntimeError(_msg)

if use_pikepdf:
    PdfFile = PikePdfFile
    PdfCropper = PikePdfCropper
    print("pikepdf loaded.", file=sys.stderr)
elif pypdf_version < 3:
    # PyPDF2 and the old pyPdf use a naming scheme different from the new pypdf
    PdfFile = PyPdfOldFile
    PdfCropper = PyPdfOldCropper
    print(pypdf_version == 2 and "PyPDF2 loaded." or "pyPdf loaded.", file=sys.stderr)
else:
    PdfFile = PyPdfFile
    PdfCropper = PyPdfCropper
    print("pypdf loaded.", file=sys.stderr)
