# -*- coding: iso-8859-1 -*-

"""
Viewer for krop used to display PDF files.

Copyright (C) 2010-2017 Armin Straub, http://arminstraub.com
"""

"""
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *

try:
    from popplerqt4 import Poppler
except ImportError:
    _msg = "Please install popplerqt4 first."\
        "\n\tOn recent versions of Ubuntu, the following should do the trick:"\
        "\n\tsudo apt-get install python-poppler-qt4"\
        "\n\t(or, if using python3) sudo apt-get install python3-poppler-qt4"
    raise RuntimeError(_msg)

from krop.viewerselections import ViewerSelections


class AbstractViewerItem(QGraphicsItem):
    """Abstract class for displaying a PDF document and for allowing the user
    to create selections."""
    def __init__(self):
        QGraphicsItem.__init__(self)
        self.selections = ViewerSelections(self)
        self.reset()

    def reset(self):
        self._currentPageIndex = 0
        self.brect = QRectF()
        self.irect = QRectF()
        self._images = []
        self.selections.deleteSelections()

    def boundingRect(self):
        return self.brect

    def paint(self, painter, option, widget):
        img = self.getImage(self.currentPageIndex)
        if img is None:
            return
        painter.drawRect(self.irect.adjusted(-1,-1,1,1))
        painter.drawImage(self.irect, img)

    def mapRectToImage(self, r):
        return r.translated(-self.irect.left(), -self.irect.top())

    def mapRectFromImage(self, r):
        return r.translated(self.irect.left(), self.irect.top())

    def getCurrentPageIndex(self):
        return self._currentPageIndex

    def setCurrentPageIndex(self, idx):
        if idx >= self.numPages():
            idx = self.numPages()-1
        if idx < 0:
            idx = 0
        self._currentPageIndex = idx

        img = self.getImage(idx)
        if img is None:
            return
        self.selections.updateSelectionVisibility()

        self.prepareGeometryChange()
        rect = QRectF(img.rect())
        # inflate slightly so that bounding rect will be visible
        padding = 5
        self.brect = QRectF(0,0,rect.width()+2*padding,rect.height()+2*padding)
        self.irect = QRectF(padding,padding,rect.width(),rect.height())
        self.scene().setSceneRect(self.brect)

    currentPageIndex = property(getCurrentPageIndex, setCurrentPageIndex)

    def previousPage(self):
        self.currentPageIndex = self.currentPageIndex-1

    def nextPage(self):
        self.currentPageIndex = self.currentPageIndex+1

    def firstPage(self):
        self.currentPageIndex = 0

    def lastPage(self):
        self.currentPageIndex = self.numPages()-1

    def getImage(self, idx):
        if idx < 0 or idx >= self.numPages():
            return None
        if self._images[idx] is None:
            self._images[idx] = self.cacheImage(idx)
        return self._images[idx]        

    def mousePressEvent(self, event):
        self.selections.mousePressEvent(event)

    def mouseMoveEvent(self, event):
        self.selections.mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.selections.mouseReleaseEvent(event)

    def load(self, filename):
        self.reset()
        self.doLoad(filename)
        self._images = [None for i in range(self.numPages())]
        self.firstPage()

    # To be implemented in deriving classes:

    def doLoad(self, filename):
        pass

    def numPages(self):
        return 0

    def isEmpty(self):
        return self.numPages() <= 0

    def cacheImage(self, idx):        
        return None

    def cropValues(self, idx):
        return self.selections.cropValues(idx)


class PopplerViewerItem(AbstractViewerItem):
    """Viewer implementation which uses Poppler to display PDF documents."""
    def reset(self):
        AbstractViewerItem.reset(self)
        self._pdfdoc = None

    def doLoad(self, filename):
        self._pdfdoc = Poppler.Document.load(filename)
        if self._pdfdoc:
            self._pdfdoc.setRenderHint(Poppler.Document.Antialiasing and
                    Poppler.Document.TextAntialiasing)

    def numPages(self):
        if self._pdfdoc is None:    
            return 0
        else:
            return self._pdfdoc.numPages()

    def cacheImage(self, idx):        
        page = self._pdfdoc.page(idx)
        return page.renderToImage(96.0, 96.0)
        # return page.renderToImage()

    def cropValues(self, idx):
        def adjustForOrientation(cv):
            if o == page.Landscape:
                return [ cv[1], cv[2], cv[3], cv[0] ]
            elif o == page.UpsideDown:
                return [ cv[2], cv[3], cv[0], cv[1] ]
            elif o == page.Seascape:
                return [ cv[3], cv[0], cv[1], cv[2] ]
            else: # o == page.Portrait
                return cv
        page = self._pdfdoc.page(idx)
        o = page.orientation()
        return [ adjustForOrientation(cv)
                for cv in self.selections.cropValues(idx) ]


ViewerItem = PopplerViewerItem
