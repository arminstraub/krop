# -*- coding: iso-8859-1 -*-

"""
Cropping functionality for Krop.

Copyright (C) 2010-2013 Armin Straub, http://arminstraub.com
"""

"""
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.
"""

try:
    from pyPdf import PdfFileReader, PdfFileWriter, pdf
except ImportError:
    _msg = "Please install pyPdf first."\
        "\n\tOn recent versions of Ubuntu, the following should do the trick:\n\tsudo apt-get install python-pypdf"
    raise RuntimeError(_msg)


class AbstractPdfFile:
    """Abstract class for loading a PDF document used in a corresponding
    PdfCropper class"""
    def loadFromStream(self, stream):
        pass
    def loadFromFile(self, filename):
        self.loadFromStream(file(filename, "rb"))

class AbstractPdfCropper:
    """Abstract class for writing a PDF documents composed of cropped pages
    from PdfFile instances"""
    def writeToStream(self, stream):
        pass
    def writeToFile(self, filename):
        stream = file(filename, "wb")
        self.writeToStream(stream)
        stream.close()
    def addPageCropped(self, pdffile, pagenumber, croplist, rotate=0):
        pass


class PyPdfFile(AbstractPdfFile):
    """Implementation of PdfFile using pyPdf"""
    def __init__(self):
        self.reader = None
    def loadFromStream(self, stream):
        self.reader = PdfFileReader(stream)
    def getPage(self, nr):
        page = self.reader.getPage(nr-1)

class PyPdfCropper(AbstractPdfCropper):
    """Implementation of PdfCropper using pyPdf"""
    def __init__(self):
        self.output = PdfFileWriter()
    def writeToStream(self, stream):
        self.output.write(stream)
    def addPageCropped(self, pdffile, pagenumber, croplist, rotate=0):
        if not croplist:
            return
        page = pdffile.reader.getPage(pagenumber-1)
        # In order to use a page in more than one cropped version, we need to
        # create copies of it (the route via createBlankPage, though unpleasant
        # looking, works well enough).
        for c in croplist[:-1]:
            newpage = pdf.PageObject.createBlankPage(None,
                    page.mediaBox.getWidth(), page.mediaBox.getHeight())
            newpage.mergePage(page)
            newpage.compressContentStreams()
            self.cropPage(newpage, c, rotate)
            self.output.addPage(newpage)
        # Once we may use the original page and we do so, since it results in a
        # (little bit) smaller file and less work (especially, avoiding the
        # compression).
        self.cropPage(page, croplist[-1], rotate)
        self.output.addPage(page)
    def cropPage(self, page, crop, rotate):
        # Note that the coordinate system is up-side down compared with Qt.
        x0, y0 = page.mediaBox.lowerLeft
        x1, y1 = page.mediaBox.upperRight
        x0, y0, x1, y1 = float(x0), float(y0), float(x1), float(y1)
        x0, x1 = x0+crop[0]*(x1-x0), x1-crop[2]*(x1-x0)
        y0, y1 = y0+crop[3]*(y1-y0), y1-crop[1]*(y1-y0)
        page.mediaBox.lowerLeft = (x0, y0)
        page.mediaBox.upperRight = (x1, y1)
        if rotate != 0:
            page.rotateClockwise(rotate)

PdfFile = PyPdfFile
PdfCropper = PyPdfCropper

