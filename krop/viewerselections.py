# -*- coding: iso-8859-1 -*-

"""
User-created selections used in ViewerItem.

Copyright (C) 2010-2017 Armin Straub, http://arminstraub.com
"""

"""
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.
"""

from math import ceil

from PyQt4.QtCore import *
from PyQt4.QtGui import *


class ViewerSelections(object):
    """A collection of user-created selections"""

    # possible selection modes
    all = 0
    evenodd = 1
    individual = 2

    def __init__(self, viewer):
        self.viewer = viewer
        self._aspectRatio = None
        self._selectionMode = ViewerSelections.all
        self._selectionExceptions = [] # list of page numbers which require individual selections
        self.activepdfrect = None
        self.lastPos = None

    def getAspectRatio(self):
        return self._aspectRatio

    def setAspectRatio(self, aspectRatio):
        self._aspectRatio = aspectRatio
        self.viewer.update()

    aspectRatio = property(getAspectRatio, setAspectRatio)

    def getSelectionMode(self):
        return self._selectionMode

    def setSelectionMode(self, mode):
        self._selectionMode = mode
        self.updateSelectionVisibility()

    selectionMode = property(getSelectionMode, setSelectionMode)

    def getSelectionExceptions(self):
        return self._selectionExceptions

    def setSelectionExceptions(self, exceptions):
        self._selectionExceptions = exceptions
        self.updateSelectionVisibility()

    selectionExceptions = property(getSelectionExceptions, setSelectionExceptions)

    def selectionVisibleOnPage(self, selection, idx):
        """Determines if this selection is visible on a given page."""
        mode = self.selectionMode
        selPageIndex = selection.pageIndex
        if idx in self.selectionExceptions or selPageIndex in self.selectionExceptions or mode == ViewerSelections.individual:
            return idx == selPageIndex
        if mode == ViewerSelections.all:
            return True
        if mode == ViewerSelections.evenodd:
            return (idx - selPageIndex) % 2 == 0

    @property
    def items(self):
        """Returns a list of the actual selections."""
        return self.viewer.childItems()

    def deleteSelections(self):
        for s in self.items:
            s.scene().removeItem(s)

    def updateSelectionVisibility(self):
        idx = self.viewer.currentPageIndex
        for s in self.items:
            s.setVisible(self.selectionVisibleOnPage(s, idx))

    def cropValues(self, idx):
        return [ c for s in self.items if self.selectionVisibleOnPage(s, idx)
                for c in s.cropValues() ]

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            pos = event.pos()
            rect = QRectF(pos, QSizeF())
            pdfrect = ViewerSelectionItem(self.viewer, rect)
            self.activepdfrect = pdfrect
            self.lastPos = pos

    def mouseMoveEvent(self, event):
        if self.lastPos is not None:
            pos2 = event.pos()
            self.activepdfrect.setBoundingRect(self.lastPos, pos2)

    def mouseReleaseEvent(self, event):
        self.lastPos = None


class ViewerSelectionItem(QGraphicsItem):
    """An individual user-created selection"""
    def __init__(self, parent, rect=None):
        QGraphicsItem.__init__(self, parent)

        if rect is None:
            rect = self.mapRectFromParent(self.viewer.irect)

        self.rect = rect
        self.minWidth = 1
        self.minHeight = 1
        self.pageIndex = self.viewer.currentPageIndex
        self.lastPos = None
        self.handleColor = QColor(0,0,128)
        SelectionHandleItem(self, SelectionHandleItem.LeftHandle)
        SelectionHandleItem(self, SelectionHandleItem.RightHandle)
        SelectionHandleItem(self, SelectionHandleItem.TopHandle)
        SelectionHandleItem(self, SelectionHandleItem.BottomHandle)
        SelectionCornerHandleItem(self, 0, 0)
        SelectionCornerHandleItem(self, 0, 1)
        SelectionCornerHandleItem(self, 1, 0)
        SelectionCornerHandleItem(self, 1, 1)
        self.adjustBoundingRect(0,0,0,0)

        self.setCursor(Qt.OpenHandCursor)

    @property
    def viewer(self):
        return self.parentItem()

    @property
    def selection(self):
        return self

    @property
    def orderIndex(self):
        nr = 1
        for c in self.viewer.selections.items:
            if c == self: break
            if c.isVisible(): nr += 1
        return nr

    @property
    def aspectRatio(self):
        return self.viewer.selections.aspectRatio

    def boundingRect(self):
        return self.rect

    def setBoundingRect(self, pt1, pt2):
        orect = self.rect
        nrect = QRectF(pt1, pt2).normalized()
        self.adjustBoundingRect(
                nrect.left()-orect.left(),
                nrect.top()-orect.top(),
                nrect.right()-orect.right(),
                nrect.bottom()-orect.bottom())

    def adjustBoundingRect(self, dx1, dy1, dx2, dy2):
        orect = self.mapRectToParent(self.rect)
        nrect = orect.adjusted(dx1, dy1, dx2, dy2)
        # make sure we are still inside the parent
        prect = self.viewer.irect
        if nrect.left() < prect.left():
            nrect.setLeft(prect.left())
        if nrect.right() > prect.right():
            nrect.setRight(prect.right())
        if nrect.top() < prect.top():
            nrect.setTop(prect.top())
        if nrect.bottom() > prect.bottom():
            nrect.setBottom(prect.bottom())
        # ensure minimum size
        extra = self.minWidth - nrect.width()
        if extra > 0:
            if dx1 == 0:
                nrect.setRight(nrect.right()+extra)
            elif dx2 == 0:
                nrect.setLeft(nrect.left()-extra)
            else:
                nrect.setLeft(nrect.left()-extra/2)
                nrect.setRight(nrect.right()+extra/2)
        extra = self.minHeight - nrect.height()
        if extra > 0:
            if dy1 == 0:
                nrect.setBottom(nrect.bottom()+extra)
            elif dy2 == 0:
                nrect.setTop(nrect.top()-extra)
            else:
                nrect.setTop(nrect.top()-extra/2)
                nrect.setBottom(nrect.bottom()+extra/2)
        # store parent rect for comparison (when cropping later)
        self.parentrect = self.mapRectFromParent(self.viewer.irect)
        # enlarge
        self.prepareGeometryChange()
        self.rect = self.mapRectFromParent(nrect)
        return [nrect.left()-orect.left(), nrect.top()-orect.top(),
                nrect.right()-orect.right(), nrect.bottom()-orect.bottom() ]

    def distributeRect(self):
        r = self.aspectRatio
        if r is None:
            return [ self.rect ]
        x0,y0,x1,y1 = self.rect.getCoords()
        h = (x1-x0) / r # height of each piece
        # how many pieces?
        nr = int(ceil((y1-y0) / h))
        if nr == 1:
            return [ self.rect ]
        o = (nr*h - (y1-y0)) / float(nr-1) # overlap
        return [ QRectF(x0, y0+i*(h-o), x1-x0, h) for i in range(nr) ]

    def cropValues(self):
        p = self.parentrect
        def cV(r):
            return ((r.left()-p.left())/p.width(),
                    (r.top()-p.top())/p.height(),
                    (p.right()-r.right())/p.width(),
                    (p.bottom()-r.bottom())/p.height())
        return [ cV(r) for r in self.distributeRect() ]

    def mapRectToImage(self, r):
        m = self.mapRectToParent(r)
        return self.viewer.mapRectToImage(m)

    def mapRectFromImage(self, r):
        m = self.viewer.mapRectFromImage(r)
        return self.mapRectFromParent(m)

    def paint(self, painter, option, widget):
        rect = self.boundingRect()

        # outer dashed rectangle
        outerPen = QPen()
        outerPen.setStyle(Qt.DashLine)
        painter.setPen(Qt.white)
        painter.drawRect(rect)
        painter.setPen(outerPen)
        painter.drawRect(rect)

        def drawLine(pt1, pt2):
            painter.setPen(Qt.white)
            painter.drawLine(pt1, pt2)
            painter.setPen(outerPen)
            painter.drawLine(pt1, pt2)

        # distributed rectangles
        even = True
        brush = QBrush()
        brush.setColor(QColor(0,0,0,50))
        for r in self.distributeRect():
            brush.setStyle(even and Qt.BDiagPattern or Qt.FDiagPattern)
            painter.setBrush(brush)
            painter.setPen(Qt.NoPen)
            painter.drawRect(r)
            if r.top() > self.rect.top():
                drawLine(r.topLeft(),r.topRight())
            if r.bottom() < self.rect.bottom():
                drawLine(r.bottomLeft(),r.bottomRight())
            even = not even

        # inner number
        font = QFont()
        font.setPointSize(20)
        font.setWeight(QFont.Bold)
        painter.setPen(QColor(0,0,0,155))
        painter.setFont(font)
        painter.drawText(rect, Qt.AlignCenter, str(self.orderIndex))

    def mousePressEvent(self, event):
        # happens after right-click (trim margins) and then clicking
        # somewhere in the document
        if not self.boundingRect().contains(event.pos()):
            self.lastPos = None
            # event.ignore()
        elif event.button() == Qt.LeftButton:
            pos = event.pos()
            self.lastPos = pos
            self.setCursor(Qt.ClosedHandCursor)

    def mouseMoveEvent(self, event):
        if self.lastPos:
            newPos = event.pos()
            mov = newPos - self.lastPos
            nrect = self.mapRectToParent(self.boundingRect().translated(mov))
            prect = self.viewer.irect
            if nrect.left() < prect.left():
                newPos.setX(newPos.x() - nrect.left() + prect.left())
            if nrect.right() > prect.right():
                newPos.setX(newPos.x() - nrect.right() + prect.right())
            if nrect.top() < prect.top():
                newPos.setY(newPos.y() - nrect.top() + prect.top())
            if nrect.bottom() > prect.bottom():
                newPos.setY(newPos.y() - nrect.bottom() + prect.bottom())
            mov = newPos - self.lastPos
            r = self.boundingRect().translated(mov)
            self.setBoundingRect(r.topLeft(), r.bottomRight())
            self.lastPos = newPos

    def mouseReleaseEvent(self, event):
        self.lastPos = None
        self.setCursor(Qt.OpenHandCursor)


class SelectionHandleItem(QGraphicsItem):
    LeftHandle = 1
    RightHandle = 2
    TopHandle = 3
    BottomHandle = 4

    def __init__(self, parent, role):
        QGraphicsItem.__init__(self, parent)

        self.role = role
        self.lastPos = None
        # arrow width and height (half, that is)
        self.aw = 8
        self.ah = 4
        # arrow center (0 means centered on boundary)
        self.ac = self.ah

        self.handleColor = parent.handleColor

        if self.role==SelectionHandleItem.LeftHandle or self.role==SelectionHandleItem.RightHandle:
            self.setCursor(Qt.SizeHorCursor)
        elif self.role==SelectionHandleItem.TopHandle or self.role==SelectionHandleItem.BottomHandle:
            self.setCursor(Qt.SizeVerCursor)

    @property
    def selection(self):
        return self.parentItem()

    def boundingRect(self):
        rect = self.selection.boundingRect()
        pt = rect.center()
        if self.role==SelectionHandleItem.LeftHandle:
            pt.setX(rect.left()-self.ac)
            return QRectF(pt-QPointF(self.ah,self.aw),
                    QSizeF(2*self.ah,2*self.aw))
        if self.role==SelectionHandleItem.RightHandle:
            pt.setX(rect.right()+self.ac)
            return QRectF(pt-QPointF(self.ah,self.aw),
                    QSizeF(2*self.ah,2*self.aw))
        if self.role==SelectionHandleItem.TopHandle:
            pt.setY(rect.top()-self.ac)
            return QRectF(pt-QPointF(self.aw,self.ah),
                    QSizeF(2*self.aw,2*self.ah))
        if self.role==SelectionHandleItem.BottomHandle:
            pt.setY(rect.bottom()+self.ac)
            return QRectF(pt-QPointF(self.aw,self.ah),
                    QSizeF(2*self.aw,2*self.ah))

    def paint(self, painter, option, widget):
        rect = self.boundingRect()
        pt = rect.center()
        if self.role==SelectionHandleItem.LeftHandle:
            pts = [QPointF(-self.ah,0), QPointF(self.ah,-self.aw),
                    QPointF(self.ah,self.aw)]
        if self.role==SelectionHandleItem.RightHandle:
            pts = [QPointF(self.ah,0), QPointF(-self.ah,-self.aw),
                    QPointF(-self.ah,self.aw)]
        if self.role==SelectionHandleItem.TopHandle:
            pts = [QPointF(0,-self.ah), QPointF(self.aw,self.ah),
                    QPointF(-self.aw,self.ah)]
        if self.role==SelectionHandleItem.BottomHandle:
            pts = [QPointF(0,self.ah), QPointF(self.aw,-self.ah),
                    QPointF(-self.aw,-self.ah)]
        painter.setPen(self.handleColor)
        painter.setBrush(self.handleColor)
        painter.drawConvexPolygon(QPolygonF([pt+p for p in pts]))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            pos = event.pos()
            self.lastPos = pos

    def mouseMoveEvent(self, event):
        if self.lastPos:
            pos2 = event.pos()
            mov = pos2 - self.lastPos
            if self.role==SelectionHandleItem.LeftHandle:
                d = self.selection.adjustBoundingRect(mov.x(),0,0,0)[0]
                pos2.setX(self.lastPos.x() + d)
            if self.role==SelectionHandleItem.RightHandle:
                d = self.selection.adjustBoundingRect(0,0,mov.x(),0)[2]
                pos2.setX(self.lastPos.x() + d)
            if self.role==SelectionHandleItem.TopHandle:
                d = self.selection.adjustBoundingRect(0,mov.y(),0,0)[1]
                pos2.setY(self.lastPos.y() + d)
            if self.role==SelectionHandleItem.BottomHandle:
                d = self.selection.adjustBoundingRect(0,0,0,mov.y())[3]
                pos2.setY(self.lastPos.y() + d)
            self.lastPos = pos2

    def mouseReleaseEvent(self, event):
        self.lastPos = None


class SelectionCornerHandleItem(QGraphicsItem):
    def __init__(self, parent, lr, tb):
        QGraphicsItem.__init__(self, parent)

        self.lr = lr
        self.tb = tb
        self.lastPos = None
        # size (half, that is)
        self.bs = 4

        self.handleColor = parent.handleColor

        self.setCursor((Qt.SizeFDiagCursor, Qt.SizeBDiagCursor)[(lr+tb)%2])

    @property
    def selection(self):
        return self.parentItem()

    def corner(self, rect):
        c = rect.getCoords()
        return QPointF(c[2*self.lr], c[2*self.tb+1])

    def direction(self, pt):
        d = [0,0,0,0]
        d[2*self.lr] = pt.x()
        d[2*self.tb+1] = pt.y()
        return d

    def boundingRect(self):
        pt = self.corner(self.selection.boundingRect())
        rect = QRectF(0,0,2*self.bs,2*self.bs)
        rect.moveCenter(pt)
        return rect

    def paint(self, painter, option, widget):
        rect = self.boundingRect()
        painter.setPen(self.handleColor)
        painter.setBrush(self.handleColor)
        painter.drawRect(rect)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            pos = event.pos()
            self.lastPos = pos

    def mouseMoveEvent(self, event):
        if self.lastPos:
            mov = event.pos() - self.lastPos
            d = self.selection.adjustBoundingRect(*self.direction(mov))
            self.lastPos = self.lastPos + self.corner(QRectF().adjusted(*d))

    def mouseReleaseEvent(self, event):
        self.lastPos = None

