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
        if lib_crop == PYPDF2:
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

class PyMuPdfFile(AbstractPdfFile):
    """Implementation of PdfFile using PyMuPDF"""
    def __init__(self):
        self.reader = None
    def loadFromStream(self, stream):
        self.reader = fitz.open(stream)
        if self.reader.is_encrypted:
            raise PdfEncryptedError
    def getPage(self, nr):
        return self.reader[nr]

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
            self.doAddPage(page, rotate)
        else:
            box = self.pageGetCropBox(page)
            for crop in croplist:
                new_page = copy.copy(page)
                new_box = computeCropBoxCoords(box, crop)
                self.pageSetCropBox(new_page, new_box)
                self.doAddPage(new_page, rotate)
    def doAddPage(self, page, rotate):
        pass
    def pageGetCropBox(self, page):
        pass
    def pageSetCropBox(self, page, box):
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
    def doAddPage(self, page, rotate):
        if rotate != 0:
            page.rotate(rotate)
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
    def copyDocumentRoot(self, pdffile):
        # Copy the named destinations for links.
        # TODO: this worked for links in PyPDF2 but doesn't seem to work for pypdf
        for dest in pdffile.reader.named_destinations.values():
            self.output.add_named_destination_object(dest)

class PyPdfOldCropper(PyPdfCropper):
    """Implementation of PdfCropper using PyPDF2 or the old PyPdf"""
    def doAddPage(self, page, rotate):
        if rotate != 0:
            page.rotateClockwise(rotate)
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
    def copyDocumentRoot(self, pdffile):
        # Copy the named destinations for links.
        for dest in pdffile.reader.namedDestinations.values():
            self.output.addNamedDestinationObject(dest)


class PyMuPdfCropper(SemiAbstractPdfCropper):
    """Implementation of PdfCropper using PyMuPDF"""
    def __init__(self):
        self.output = fitz.open()
    def writeToStream(self, stream):
        self.output.save(stream)
    def addPageCropped(self, pdffile, pagenumber, croplist, alwaysinclude, rotate=0):
        def addPage():
            # https://pymupdf.readthedocs.io/en/latest/the-basics.html
            r = pdffile.reader[pagenumber].rotation + rotate
            self.output.insert_pdf(pdffile.reader, pagenumber, pagenumber, rotate=r)
        if not croplist and alwaysinclude:
            addPage()
            # self.output.insert_pdf(pdffile.reader, pagenumber, pagenumber, rotate=rotate)
        else:
            for crop in croplist:
                addPage()
                # self.output.insert_pdf(pdffile.reader, pagenumber, pagenumber, rotate=rotate)
                new_page = self.output[-1]
                box = self.pageGetCropBox(new_page)
                # MuPDF uses coordinates where (0,0) is the top-right point, unlike
                # PDF where (0,0) is the bottom-left.
                new_box = computeCropBoxCoords(box, crop, pdf_coords=False)
                self.pageSetCropBox(new_page, new_box)
                # if rotate != 0:
                #     self.pageRotateClockwise(new_page, rotate)
    def pageGetCropBox(self, page):
        return page.cropbox
    def pageSetCropBox(self, page, box):
        page.set_cropbox(box)
        page.set_artbox(page.cropbox)
        page.set_bleedbox(page.cropbox)
        # careful: mediabox in MuPDF is an exception and uses PDF coordinates
        # page.set_mediabox(page.cropbox)
        page.set_trimbox(page.cropbox)
    def copyDocumentRoot(self, pdffile):
        pass


class PikePdfCropper(SemiAbstractPdfCropper):
    """Implementation of PdfCropper using pikepdf"""
    def __init__(self):
        self.output = Pdf.new()
    def writeToStream(self, stream):
        self.output.save(stream)
    def doAddPage(self, page, rotate):
        if rotate != 0:
            page.rotate(rotate, relative=True)
        self.output.pages.append(page)
    def pageGetCropBox(self, page):
        try:
            # only page.MediaBox exists in pikepdf version 1.10.3 as currently in Ubuntu 20.04
            return page.cropbox
        except AttributeError:
            raise RuntimeError("Please install a more recent version of pikepdf.")
    def pageSetCropBox(self, page, box):
        page.cropbox = box
        page.mediabox = box
        page.trimbox = box
    def copyDocumentRoot(self, pdffile):
        pass


def computeCropBoxCoords(box, crop, pdf_coords=True):
    x0, y0, x1, y1 = box
    x0, y0, x1, y1 = float(x0), float(y0), float(x1), float(y1)
    # In PDF coordinates (0,0) is the bottom-left point; otherwise, as in
    # MuPDF or Qt, this would be the top-left point.
    if not pdf_coords:
        crop = (crop[0], crop[3], crop[2], crop[1])
    x0, x1 = x0+crop[0]*(x1-x0), x1-crop[2]*(x1-x0)
    y0, y1 = y0+crop[3]*(y1-y0), y1-crop[1]*(y1-y0)
    return x0, y0, x1, y1

def optimizePdfGhostscript(oldfilename, newfilename):
    import subprocess
    subprocess.check_call(('gs', '-sDEVICE=pdfwrite', '-sOutputFile=' + newfilename,
        '-dNOPAUSE', '-dBATCH', oldfilename))


# determine which of pypdf, PyPDF2, pyPdf, pikepdf, PyMuPDF to use
PYPDF1 = 1 # pyPdf (old)
PYPDF2 = 2 # PyPDF2
PYPDF = 3 # pydf
PYMUPDF = 4
PIKEPDF = 5
lib_crop = 0

# use PyMuPDF if requested
if '--use-pymupdf' in sys.argv:
    try:
        import fitz
        lib_crop = PYMUPDF
    except ImportError:
        print("PyMuPDF was requested but failed to load.", file=sys.stderr)

# use pikepdf if requested
if '--use-pikepdf' in sys.argv:
    try:
        from pikepdf import Pdf
        lib_crop = PIKEPDF
    except ImportError:
        print("pikepdf was requested but failed to load.", file=sys.stderr)

# use PyPDF2 if requested
if '--use-pypdf2' in sys.argv:
    try:
        from PyPDF2 import PdfFileReader as PdfReader, PdfFileWriter as PdfWriter
        lib_crop = PYPDF2
    except ImportError:
        print("PyPDF2 was requested but failed to load.", file=sys.stderr)

# by default use pypdf / PyPDF2
if not lib_crop:
    # if possible use the new pypdf
    try:
        from pypdf import PdfReader, PdfWriter
        lib_crop = PYPDF
    except ImportError:
        pass
    # otherwise use PyPDF2
    if not lib_crop:
        try:
            from PyPDF2 import PdfFileReader as PdfReader, PdfFileWriter as PdfWriter
            lib_crop = PYPDF2
        except ImportError:
            pass
    # or the very old pyPdf
    if not lib_crop:
        try:
            from pyPdf import PdfFileReader as PdfReader, PdfFileWriter as PdfWriter
            lib_crop = PYPDF1
        except ImportError:
            pass
    # try pikepdf
    if not lib_crop:
        try:
            from pikepdf import Pdf
            lib_crop = PIKEPDF
        except ImportError:
            pass
    # try PyMuPDF
    if not lib_crop:
        try:
            import fitz
            lib_crop = PYMUPDF
        except ImportError:
            pass
    # complain if no version is available
    if not lib_crop:
        _msg = "Please install pypdf (or its predecessor PyPDF2), PyMuPDF or a new version of pikepdf first."\
            "\n\tOn recent versions of Ubuntu, the following should do the trick:"\
            "\n\tsudo apt-get install python3-pypdf2"
        raise RuntimeError(_msg)

if lib_crop == PYMUPDF:
    PdfFile = PyMuPdfFile
    PdfCropper = PyMuPdfCropper
    print("Using PyMuPDF for cropping.", file=sys.stderr)
elif lib_crop == PIKEPDF:
    PdfFile = PikePdfFile
    PdfCropper = PikePdfCropper
    print("Using pikepdf for cropping.", file=sys.stderr)
elif lib_crop == PYPDF1 or lib_crop == PYPDF2:
    # PyPDF2 and the old pyPdf use a naming scheme different from the new pypdf
    PdfFile = PyPdfOldFile
    PdfCropper = PyPdfOldCropper
    print("Using " + (lib_crop == PYPDF2 and "PyPDF2" or "pyPdf") + " for cropping.", file=sys.stderr)
else:
    PdfFile = PyPdfFile
    PdfCropper = PyPdfCropper
    print("Using pypdf for cropping.", file=sys.stderr)
