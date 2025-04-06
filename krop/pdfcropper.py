# -*- coding: iso-8859-1 -*-

"""
Cropping functionality for krop.

Copyright (C) 2010-2025 Armin Straub, http://arminstraub.com
"""

"""
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.
"""

import copy
import sys

from krop.config import PYQT6


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
        self.reader = self.PdfReader(stream)
        if self.reader.is_encrypted:
            try:
                if not self.reader.decrypt(''):
                    raise PdfEncryptedError
            except:
                raise PdfEncryptedError
    def getPage(self, nr):
        return self.reader.pages[nr]

class PyPdfOldFile(PyPdfFile):
    """Implementation of PdfFile using PyPDF2 (<2) which uses camelCase rather
    than snake_case"""
    def loadFromStream(self, stream):
        self.reader = self.PdfReader(stream, strict=False)
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
        self.reader = self.pymupdf.open(stream)
        if self.reader.is_encrypted:
            raise PdfEncryptedError
    def getPage(self, nr):
        return self.reader[nr]

class PikePdfFile(AbstractPdfFile):
    """Implementation of PdfFile using pikepdf"""
    def __init__(self):
        self.reader = None
    def loadFromStream(self, stream):
        self.reader = self.Pdf.open(stream)
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
        self.output = self.PdfWriter()
    def writeToStream(self, stream):
        # For certain large pdf files, PdfWriter.write() causes the error:
        #   maximum recursion depth exceeded while calling a Python object
        # This issue is present, for instance, in PyPDF2 1.23.
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
    """Implementation of PdfCropper using PyPDF2 (<2)"""
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
        self.output = self.pymupdf.open()
    def writeToStream(self, stream):
        self.output.save(stream)
    def addPageCropped(self, pdffile, pagenumber, croplist, alwaysinclude, rotate=0):
        def addPage():
            # https://pymupdf.readthedocs.io/en/latest/the-basics.html
            r = pdffile.reader[pagenumber].rotation + rotate
            self.output.insert_pdf(pdffile.reader, from_page=pagenumber, to_page=pagenumber, rotate=r)
        if not croplist and alwaysinclude:
            addPage()
        else:
            for crop in croplist:
                addPage()
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
        try:
            page.set_artbox(page.cropbox)
            page.set_bleedbox(page.cropbox)
            # careful: mediabox in MuPDF is an exception and uses PDF coordinates
            # page.set_mediabox(page.cropbox)
            page.set_trimbox(page.cropbox)
        except:
            # these functions did not exist prior to v1.19.4
            pass
    def copyDocumentRoot(self, pdffile):
        pass


class PikePdfCropper(SemiAbstractPdfCropper):
    """Implementation of PdfCropper using pikepdf"""
    def __init__(self):
        self.output = self.Pdf.new()
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


# In the following, we determine which cropping library to use.
# See lib_crop_options below for a list of the supported libraries.

def import_pymupdf():
    import fitz
    # note: since 1.24.3, one can use 'import pymupdf' instead but fitz is
    # promised to always be supported as well
    PyMuPdfFile.pymupdf = fitz
    PyMuPdfCropper.pymupdf = fitz
    return PyMuPdfFile, PyMuPdfCropper

def import_pikepdf():
    from pikepdf import Pdf
    PikePdfFile.Pdf = Pdf
    PikePdfCropper.Pdf = Pdf
    return PikePdfFile, PikePdfCropper

def import_pypdf():
    from pypdf import PdfReader, PdfWriter
    PyPdfFile.PdfReader = PdfReader
    PyPdfCropper.PdfWriter = PdfWriter
    return PyPdfFile, PyPdfCropper

def import_pypdf2():
    import PyPDF2
    # PyPDF2 (<2) uses camelCase while newer versions (just like pypdf) use snake_case
    if PyPDF2.__version__.startswith("1."):
        from PyPDF2 import PdfFileReader as PdfReader, PdfFileWriter as PdfWriter
        PdfFile = PyPdfOldFile
        PdfCropper = PyPdfOldCropper
    else:
        from PyPDF2 import PdfReader, PdfWriter
        PdfFile = PyPdfFile
        PdfCropper = PyPdfCropper
    PdfFile.PdfReader = PdfReader
    PdfCropper.PdfWriter = PdfWriter
    return PdfFile, PdfCropper

# for each cropping library: [name, import function, flag to request it]
lib_crop_options = [
        ['PyMuPDF', import_pymupdf, '--use-pymupdf'],
        ['pikepdf', import_pikepdf, '--use-pikepdf'],
        ['pypdf', import_pypdf, '--use-pypdf'],
        ['PyPDF2', import_pypdf2, '--use-pypdf2'],
        ]
# lib_crop will be set to the name of the cropping library in use
lib_crop = None

# We go through all options for libraries twice:
# during the first round, we load a library if it is specifically requested,
# and during the second round, we load the first available library.
for load_only_if_requested in [True, False]:
    for lib, import_func, flag in lib_crop_options:
        if not lib_crop and (not load_only_if_requested or (flag and flag in sys.argv)):
            try:
                PdfFile, PdfCropper = import_func()
                lib_crop = lib
                print(f"Using {lib} for cropping.", file=sys.stderr)
            except ImportError:
                if load_only_if_requested:
                    print(f"{lib} was requested but failed to load.", file=sys.stderr)

# complain if no library could be imported
if not lib_crop:
    _msg = "Please install one of the supported cropping libraries first (PyMuPDF, pypdf, or pikepdf)."
    if PYQT6:
        _msg += "\n\tFor instance, on recent versions of Ubuntu, the following should do the trick:"\
            "\n\tsudo apt-get install python3-pymupdf"
    else:
        _msg += "\n\tFor instance, on versions of Ubuntu such as 22.04, one of the following should do the trick:"\
            "\n\tsudo apt install python3-fitz"\
            "\n\tsudo apt-get install python3-pypdf2"
    raise RuntimeError(_msg)

