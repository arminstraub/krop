# -*- coding: iso-8859-1 -*-

"""
User-created selections used in ViewerItem.

Copyright (C) 2010-2020 Armin Straub, http://arminstraub.com
"""

"""
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.
"""

from math import ceil

from krop.qt import *


class ViewerSelections(object):
    """A collection of user-created selections"""

    # possible selection modes
    all = 0
    evenodd = 1
    individual = 2

    def __init__(self, viewer):
        self.viewer = viewer
        self._selections = []
        self._currentSelection = None
        self._distributeAspectRatio = None
        self._selectionMode = ViewerSelections.all
        self._selectionExceptions = [] # list of page numbers which require individual selections
        self.lastPos = None

    @property
    def items(self):
        """Returns a list of the selections."""
        # the list equals self.viewer.childItems() except for the ordering:
        # we preserve the order in which the selections were created, whereas
        # childItems() gets reordered when stackBefore (or setZValue are
        # called)
        return self._selections

    def addSelection(self, rect=None):
        s = ViewerSelectionItem(self.viewer, rect)
        self._selections.append(s)
        s.setAsCurrent()
        return s

    def deleteSelection(self, s):
        self._selections.remove(s)
        s.scene().removeItem(s)
        if s is self.currentSelection:
            self.currentSelection = None
            self.autoSetCurrentSelection()

    def deleteSelections(self):
        for s in self.items:
            self.deleteSelection(s)

    def getCurrentSelection(self):
        return self._currentSelection

    def setCurrentSelection(self, currentSelection):
        self._currentSelection = currentSelection
        if currentSelection:
            for s in self.items:
                if s is not currentSelection:
                    s.stackBefore(currentSelection)
            currentSelection.setFocus()
        self.viewer.scene().update()
        self.currentSelectionUpdated()

    currentSelection = property(getCurrentSelection, setCurrentSelection)

    def autoSetCurrentSelection(self):
        s = self.currentSelection
        idx = self.viewer.currentPageIndex
        # check if currentSelection is visible
        if s and not s.selectionVisibleOnPage(idx):
            s = None
        # if currentSelection is None, we auto select if possible
        if s is None:
            for i in reversed(self.items):
                if i.selectionVisibleOnPage(idx):
                    s = i
                    break
        self.currentSelection = s

    def currentSelectionUpdated(self):
        self.viewer.mainwindow.currentSelectionUpdated()

    def getDistributeAspectRatio(self):
        return self._distributeAspectRatio

    def setDistributeAspectRatio(self, distributeAspectRatio):
        self._distributeAspectRatio = distributeAspectRatio
        self.viewer.update()

    distributeAspectRatio = property(getDistributeAspectRatio, setDistributeAspectRatio)

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

    def updateSelectionVisibility(self):
        idx = self.viewer.currentPageIndex
        for s in self.items:
            s.setVisible(s.selectionVisibleOnPage(idx))
        self.autoSetCurrentSelection()

    def cropValues(self, idx):
        return [ c for s in self.items if s.selectionVisibleOnPage(idx)
                for c in s.cropValues() ]

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.pos()
            rect = QRectF(pos, QSizeF())
            self.currentSelection = self.addSelection(rect)
            self.lastPos = pos

    def mouseMoveEvent(self, event):
        if self.lastPos is not None:
            pos2 = event.pos()
            self.currentSelection.setBoundingRect(self.lastPos, pos2)

    def mouseReleaseEvent(self, event):
        self.lastPos = None


class ViewerSelectionItem(QGraphicsItem):

    handleColor = QColor(0,0,128)
    handleColorCurrent = QColor(0,128,0)

    """An individual user-created selection"""
    def __init__(self, parent, rect=None):
        QGraphicsItem.__init__(self, parent)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsFocusable)

        if rect is None:
            rect = self.mapRectFromParent(self.viewer.irect)

        self.rect = rect
        self._aspectRatioData = None
        self._aspectRatio = None
        self.minWidth = 1
        self.minHeight = 1
        self.pageIndex = self.viewer.currentPageIndex
        self.lastPos = None
        SelectionHandleItem(self, SelectionHandleItem.LeftHandle)
        SelectionHandleItem(self, SelectionHandleItem.RightHandle)
        SelectionHandleItem(self, SelectionHandleItem.TopHandle)
        SelectionHandleItem(self, SelectionHandleItem.BottomHandle)
        SelectionCornerHandleItem(self, 0, 0)
        SelectionCornerHandleItem(self, 0, 1)
        SelectionCornerHandleItem(self, 1, 0)
        SelectionCornerHandleItem(self, 1, 1)
        self.adjustBoundingRect()

        self.setCursor(Qt.CursorShape.OpenHandCursor)


    @property
    def selection(self):
        # this is used in mainwindow.slotContextMenu
        return self

    @property
    def viewer(self):
        return self.parentItem()

    @property
    def selections(self):
        return self.viewer.selections


    def isCurrent(self):
        return self is self.selections.currentSelection

    def setAsCurrent(self):
        self.selections.currentSelection = self


    @property
    def orderIndex(self):
        nr = 1
        for c in self.selections.items:
            if c is self:
                return nr
            if c.isVisible():
                nr += 1


    @property
    def aspectRatio(self):
        return self._aspectRatio

    def getAspectRatioData(self):
        return self._aspectRatioData or [0, ""]

    def setAspectRatioData(self, data):
        index, s = data
        # index=0: flexible
        if index == 0:
            self._aspectRatio = None
            data[1] = ""
        else:
            self._aspectRatio = aspectRatioFromStr(s)
        self._aspectRatioData = data
        self.adjustBoundingRect()
        for c in self.childItems():
            if isinstance(c, SelectionHandleItem):
                c.setVisible(self._aspectRatio is None)

    aspectRatioData= property(getAspectRatioData, setAspectRatioData)


    @property
    def distributeAspectRatio(self):
        return self.selections.distributeAspectRatio


    def selectionVisibleOnPage(self, pageIndex):
        """Determines if this selection is visible on a given page."""
        mode = self.selections.selectionMode
        exceptions = self.selections.selectionExceptions
        if pageIndex in exceptions or self.pageIndex in exceptions or mode == ViewerSelections.individual:
            return pageIndex == self.pageIndex
        if mode == ViewerSelections.all:
            return True
        if mode == ViewerSelections.evenodd:
            return (pageIndex - self.pageIndex) % 2 == 0


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


    def adjustBoundingRect(self, dx1=0, dy1=0, dx2=0, dy2=0):
        orect = self.mapRectToParent(self.rect)
        prect = self.viewer.irect
        nrect = orect.adjusted(dx1, dy1, dx2, dy2)

        # make sure we are still inside the parent
        if nrect.left() < prect.left():
            nrect.setLeft(prect.left())
        if nrect.right() > prect.right():
            nrect.setRight(prect.right())
        if nrect.top() < prect.top():
            nrect.setTop(prect.top())
        if nrect.bottom() > prect.bottom():
            nrect.setBottom(prect.bottom())
        # similar but not quite the same...
        # nrect = nrect.normalized().intersected(prect)

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

        # enforce aspectRatio r = w/h if set
        if self.aspectRatio:
            r, w, h = self.aspectRatio, nrect.width(), nrect.height()
            nw, nh = min(w, h*r), min(h, w/r)
            if dx1==0 and dx2!=0:
                # move right side
                nrect.adjust(0, 0, nw-w, 0)
            elif dx2==0 and dx1!=0:
                # move left side
                nrect.adjust(w-nw, 0, 0, 0)
            else:
                # center horizontally
                nrect.adjust((w-nw)/2, 0, -(w-nw)/2, 0)
            if dy1==0 and dy2!=0:
                # move bottom side
                nrect.adjust(0, 0, 0, nh-h)
            elif dy2==0 and dy1!=0:
                # move top side
                nrect.adjust(0, h-nh, 0, 0)
            else:
                # center vertically
                nrect.adjust(0, (h-nh)/2, 0, -(h-nh)/2)

        # store parent rect for comparison (when cropping later)
        self.parentrect = self.mapRectFromParent(self.viewer.irect)

        # change size of boundingRect
        self.prepareGeometryChange()
        self.rect = self.mapRectFromParent(nrect)
        self.selections.currentSelectionUpdated()

        return [nrect.left()-orect.left(), nrect.top()-orect.top(),
                nrect.right()-orect.right(), nrect.bottom()-orect.bottom() ]


    def moveBoundingRect(self, dx, dy):
        """moves boundingRect but never changes its size"""
        orect = self.mapRectToParent(self.rect)
        prect = self.viewer.irect
        if dx < 0:
            dx = max(dx, prect.left() - orect.left())
        if dx > 0:
            dx = min(dx, prect.right() - orect.right())
        if dy < 0:
            dy = max(dy, prect.top() - orect.top())
        if dy > 0:
            dy = min(dy, prect.bottom() - orect.bottom())
        self.adjustBoundingRect(dx, dy, dx, dy)


    def distributeRect(self):
        r = self.distributeAspectRatio
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
        outerPen.setStyle(Qt.PenStyle.DashLine)
        painter.setPen(QColorConstants.White)
        painter.drawRect(rect)
        painter.setPen(outerPen)
        painter.drawRect(rect)

        def drawLine(pt1, pt2):
            painter.setPen(QColorConstants.White)
            painter.drawLine(pt1, pt2)
            painter.setPen(outerPen)
            painter.drawLine(pt1, pt2)

        # distributed rectangles
        even = True
        brush = QBrush()
        brush.setColor(QColor(0,0,0,50))
        for r in self.distributeRect():
            brush.setStyle(even and Qt.BrushStyle.BDiagPattern or Qt.BrushStyle.FDiagPattern)
            painter.setBrush(brush)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRect(r)
            if r.top() > self.rect.top():
                drawLine(r.topLeft(),r.topRight())
            if r.bottom() < self.rect.bottom():
                drawLine(r.bottomLeft(),r.bottomRight())
            even = not even

        # inner number
        font = QFont()
        font.setPointSize(20)
        font.setWeight(700)
        painter.setPen(QColor(0,0,0,155))
        painter.setFont(font)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, str(self.orderIndex))

    def mousePressEvent(self, event):
        # happens after right-click (trim margins) and then clicking
        # somewhere in the document
        if not self.boundingRect().contains(event.pos()):
            self.lastPos = None
            # event.ignore()
        elif event.button() == Qt.MouseButton.LeftButton:
            pos = event.pos()
            self.lastPos = pos
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
            self.setAsCurrent()

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
        self.setCursor(Qt.CursorShape.OpenHandCursor)

    def keyPressEvent(self, event):
        accepted = False
        if event.modifiers() == Qt.KeyboardModifier.ShiftModifier:
            accepted = True
            if event.key() == Qt.Key.Key_Left:
                self.moveBoundingRect(-1, 0)
            elif event.key() == Qt.Key.Key_Right:
                self.moveBoundingRect(1, 0)
            elif event.key() == Qt.Key.Key_Down:
                self.moveBoundingRect(0, 1)
            elif event.key() == Qt.Key.Key_Up:
                self.moveBoundingRect(0, -1)
            else:
                accepted = False
        if accepted:
            event.accept()
        else:
            event.ignore()


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

        if self.role==SelectionHandleItem.LeftHandle or self.role==SelectionHandleItem.RightHandle:
            self.setCursor(Qt.CursorShape.SizeHorCursor)
        elif self.role==SelectionHandleItem.TopHandle or self.role==SelectionHandleItem.BottomHandle:
            self.setCursor(Qt.CursorShape.SizeVerCursor)

    @property
    def selection(self):
        return self.parentItem()

    @property
    def handleColor(self):
        if self.selection.isCurrent():
            return self.selection.handleColorCurrent
        return self.selection.handleColor

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
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.pos()
            self.lastPos = pos
            self.selection.setAsCurrent()

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

        self.setCursor((Qt.CursorShape.SizeFDiagCursor, Qt.CursorShape.SizeBDiagCursor)[(lr+tb)%2])

    @property
    def selection(self):
        return self.parentItem()

    @property
    def handleColor(self):
        if self.selection.isCurrent():
            return self.selection.handleColorCurrent
        return self.selection.handleColor

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
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.pos()
            self.lastPos = pos
            self.selection.setAsCurrent()

    def mouseMoveEvent(self, event):
        if self.lastPos:
            mov = event.pos() - self.lastPos
            d = self.selection.adjustBoundingRect(*self.direction(mov))
            self.lastPos = self.lastPos + self.corner(QRectF().adjusted(*d))

    def mouseReleaseEvent(self, event):
        self.lastPos = None


def aspectRatioFromStr(s):
    try:
        a = [float(x) for x in s.split(":")]
        if len(a) == 1:
            aspectRatio = a[0]
        else:
            aspectRatio = a[0] / a[1]
        if aspectRatio <= 0:
            aspectRatio = None
    except:
        aspectRatio = None
    return aspectRatio
