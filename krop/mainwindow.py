# -*- coding: iso-8859-1 -*-

"""
The main window of krop

Copyright (C) 2010-2018 Armin Straub, http://arminstraub.com
"""

"""
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.
"""

import sys
from os.path import exists, splitext
from distutils.spawn import find_executable
try:
    str_unicode = unicode
except:
    str_unicode = str


from krop.qt import *
from krop.config import PYQT5, KDE

if KDE:
    from PyKDE4.kdeui import KMainWindow as QKMainWindow
else:
    QKMainWindow = QMainWindow

if PYQT5:
    from krop.mainwindowui_qt5 import Ui_MainWindow
else:
    from krop.mainwindowui_qt4 import Ui_MainWindow

from krop.viewerselections import ViewerSelections, ViewerSelectionItem
from krop.vieweritem import ViewerItem
from krop.pdfcropper import PdfFile, PdfCropper, optimizePdfGhostscript


class DeviceType:
    def __init__(self, name, width, height):
        self.name = name
        self.width = width
        self.height = height

class DeviceTypeManager:

    types = []

    def __iter__(self):
        return iter(self.types)

    def addType(self, name, width, height):
        self.types.append(DeviceType(name, width, height))

    def getType(self, index):
        if index >= len(self.types):
            return None
        return self.types[index]

    def addDefaults(self):
        self.addType("Generic (don't break pages into parts)", 0, 0)
        self.addType("4:3 eReader", 4, 3)
        self.addType("4:3 eReader (widescreen)", 3, 4)
        self.addType("Nook 1st Ed.", 600, 730)
        self.addType("Nook 1st Ed. (widescreen)", 730, 600)
  
    def saveTypes(self, settings):
        settings.beginWriteArray("devicetypes")
        for i in range(len(self.types)):
            t = self.types[i]
            settings.setArrayIndex(i)
            settings.setValue("name", t.name)
            settings.setValue("width", t.width)
            settings.setValue("height", t.height)
        settings.endArray()
  
    def loadTypes(self, settings):
        count = settings.beginReadArray("devicetypes")
        for i in range(count):
            settings.setArrayIndex(i)
            name = settings.value("name")
            width = int(settings.value("width"))
            height = int(settings.value("height"))
            self.addType(name, width, height)
        settings.endArray()
        if count==0:
            self.addDefaults()


class MainWindow(QKMainWindow):

    fileName = None

    def __init__(self):
        QKMainWindow.__init__(self)

        self.devicetypes = DeviceTypeManager()

        self.selectedRect = None
        self._viewer = ViewerItem()

        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)

        # these options are awkwardly named and possibly confusing, so they are
        # not shown by default
        self.ui.labelAllowedChanges.hide()
        self.ui.editAllowedChanges.hide()
        self.ui.labelSensitivity.hide()
        self.ui.editSensitivity.hide()

        # self.ui.tabWidget.

        # http://standards.freedesktop.org/icon-naming-spec/icon-naming-spec-latest.html
        self.setWindowIcon(QIcon.fromTheme('edit-cut'))
        self.ui.actionOpenFile.setIcon(QIcon.fromTheme('document-open'))
        self.ui.actionKrop.setIcon(QIcon.fromTheme('face-smile'))
        self.ui.actionZoomIn.setIcon(QIcon.fromTheme('zoom-in'))
        self.ui.actionZoomOut.setIcon(QIcon.fromTheme('zoom-out'))
        self.ui.actionFitInView.setIcon(QIcon.fromTheme('zoom-fit-best'))
        self.ui.actionPreviousPage.setIcon(QIcon.fromTheme('go-previous'))
        self.ui.actionNextPage.setIcon(QIcon.fromTheme('go-next'))
        self.ui.actionFirstPage.setIcon(QIcon.fromTheme('go-first'))
        self.ui.actionLastPage.setIcon(QIcon.fromTheme('go-last'))
        self.ui.actionTrimMarginsAll.setIcon(QIcon.fromTheme('select-rectangular'))
        # self.ui.actionTrimMarginsAll.setIcon(QIcon.fromTheme('edit-select-all'))

        if QIcon.hasThemeIcon('document-open'):
            self.ui.buttonFileSelect.setIcon(QIcon.fromTheme('document-open'))
        else:
            self.ui.buttonFileSelect.setText('...')
            self.ui.buttonFileSelect.setAutoRaise(False)

        if QIcon.hasThemeIcon('go-first') and QIcon.hasThemeIcon('go-previous') \
                and QIcon.hasThemeIcon('go-next') and QIcon.hasThemeIcon('go-last'):
            self.ui.buttonFirst.setIcon(QIcon.fromTheme('go-first'))
            self.ui.buttonPrevious.setIcon(QIcon.fromTheme('go-previous'))
            self.ui.buttonNext.setIcon(QIcon.fromTheme('go-next'))
            self.ui.buttonLast.setIcon(QIcon.fromTheme('go-last'))
        else:
            self.ui.buttonFirst.setText('<<')
            self.ui.buttonPrevious.setText('<')
            self.ui.buttonNext.setText('>')
            self.ui.buttonLast.setText('>>')
            self.ui.buttonFirst.setFlat(False)
            self.ui.buttonPrevious.setFlat(False)
            self.ui.buttonNext.setFlat(False)
            self.ui.buttonLast.setFlat(False)


        self.ui.actionOpenFile.triggered.connect(self.slotOpenFile)
        self.ui.actionSelectFile.triggered.connect(self.slotSelectFile)
        self.ui.actionKrop.triggered.connect(self.slotKrop)
        self.ui.actionZoomIn.triggered.connect(self.slotZoomIn)
        self.ui.actionZoomOut.triggered.connect(self.slotZoomOut)
        self.ui.actionFitInView.toggled.connect(self.slotFitInView)
        self.ui.actionPreviousPage.triggered.connect(self.slotPreviousPage)
        self.ui.actionNextPage.triggered.connect(self.slotNextPage)
        self.ui.actionFirstPage.triggered.connect(self.slotFirstPage)
        self.ui.actionLastPage.triggered.connect(self.slotLastPage)
        self.ui.actionDeleteSelection.triggered.connect(self.slotDeleteSelection)
        self.ui.actionTrimMargins.triggered.connect(self.slotTrimMargins)
        self.ui.actionTrimMarginsAll.triggered.connect(self.slotTrimMarginsAll)
        self.ui.documentView.customContextMenuRequested.connect(self.slotContextMenu)
        self.ui.editCurrentPage.textEdited.connect(self.slotCurrentPageEdited)
        self.ui.radioSelAll.toggled.connect(self.slotSelectionMode)
        self.ui.radioSelEvenOdd.toggled.connect(self.slotSelectionMode)
        self.ui.radioSelIndividual.toggled.connect(self.slotSelectionMode)
        #  self.ui.editSelExceptions.editingFinished.connect(self.slotSelExceptionsChanged)
        self.ui.editSelExceptions.textEdited.connect(self.slotSelExceptionsEdited)
        self.ui.comboDevice.currentIndexChanged.connect(self.slotDeviceTypeChanged)
        self.ui.editAspectRatio.editingFinished.connect(self.slotAspectRatioChanged)

        self.pdfScene = QGraphicsScene(self.ui.documentView)
        self.pdfScene.setBackgroundBrush(self.pdfScene.palette().dark())
        self.pdfScene.addItem(self.viewer)

        self.readSettings()

        # populate combobox with device types
        for t in self.devicetypes:
            self.ui.comboDevice.addItem(t.name)
        self.ui.comboDevice.addItem("Custom")

        # disable Ghostscript option if gs is not available
        # once support for Python2 is dropped, we can simply call shutil.which('gs')
        if not find_executable('gs'):
            self.ui.checkGhostscript.setChecked(False)
            self.ui.checkGhostscript.setEnabled(False)

        self.ui.documentView.setScene(self.pdfScene)


    @property
    def viewer(self):
        return self._viewer

    @property
    def selections(self):
        return self.viewer.selections

    def readSettings(self):
        settings = QSettings()
        self.ui.editPadding.setText(
                settings.value("trim/padding", "2"))
        self.ui.editAllowedChanges.setText(
                settings.value("trim/allowedchanges", "0"))
        self.ui.editSensitivity.setText(
                settings.value("trim/sensitivity", "5"))
        self.ui.checkGhostscript.setChecked(settings.value("optimize", "gs") == "gs")

        self.devicetypes.loadTypes(settings)

    def writeSettings(self):
        settings = QSettings()
        settings.setValue("trim/padding",
                self.ui.editPadding.text())
        settings.setValue("trim/allowedchanges",
                self.ui.editAllowedChanges.text())
        settings.setValue("trim/sensitivity",
                self.ui.editSensitivity.text())
        settings.setValue("optimize", "gs" if
                self.ui.checkGhostscript.isChecked() else "")

        self.devicetypes.saveTypes(settings)

    def openFile(self, fileName):
        if fileName:
            self.viewer.load(fileName)
            if not self.viewer.isEmpty():
                self.fileName = fileName
                outputFileName = "%s-cropped.pdf" % splitext(str_unicode(fileName))[0]
                self.slotFitInView(self.ui.actionFitInView.isChecked())
            else:
                self.fileName = ''
                outputFileName = ''
                self.showWarning(self.tr("Something got in our way"),
                        self.tr("The PDF file couldn't be read. "
                            "Please check the file and its permissions."))
            self.ui.actionKrop.setEnabled(not self.viewer.isEmpty())
            self.ui.actionTrimMarginsAll.setEnabled(not self.viewer.isEmpty())
            self.ui.editFile.setText(outputFileName)
            self.updateControls()

    def slotOpenFile(self):
        fileName = QFileDialog.getOpenFileName(self,
             self.tr("Open PDF"), "", self.tr("PDF Files (*.pdf)"));
        # in PyQt5, getOpenFileName is what used to be
        # getOpenFileNameAndFilter
        if PYQT5:
            fileName = fileName[0]
        self.openFile(fileName)

    def slotSelectFile(self):
        fileName = QFileDialog.getSaveFileName(self,
                self.tr("Save cropped PDF to ..."), "", self.tr("PDF Files (*.pdf)"))
                # None, QFileDialog.DontConfirmOverwrite)
        self.ui.editFile.setText(fileName)

    def showWarning(self, title, text):
        # if krop is called with parameter --go, then the main window is never
        # shown; in that case, we output the warning to the shell
        if self.isVisible():
            QMessageBox.warning(self, title, text)
        else:
            sys.stderr.write(self.tr('WARNING: ') + title + '\n' + text + '\n')

    def str2pages(self, s):
        pages = []
        intervals = [ [ n.strip() for n in i.split('-') ]
                for i in s.split(',') ]
        for i in intervals:
            a,b = i[0], i[-1]
            if a:
                if not b: b = self.viewer.numPages()
                pages.extend(range(int(a)-1,int(b))) # subtract 1 because pages are counted from 0 internally
        return pages

    def slotKrop(self):
        # file names
        inputFileName = str_unicode(self.fileName)
        outputFileName = str_unicode(self.ui.editFile.text())

        # which pages
        s = str(self.ui.editWhichPages.text())
        if not s:
            pages = range(0, self.viewer.numPages())
        else:
            pages = self.str2pages(s)

        # rotate
        rotation = [0, 270, 90, 180][self.ui.comboRotation.currentIndex()]

        # Done when selecting filename.
        # if exists(outputFileName):
        #     self.showWarning(self.tr("Overwrite File?"),
        #             self.tr("A file named \"...\" already exists. Are you sure you want to overwrite it?"))
        #     return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            pdf = PdfFile()
            pdf.loadFromFile(inputFileName)
            cropper = PdfCropper()
            for nr in pages:
                c = self.viewer.cropValues(nr)
                cropper.addPageCropped(pdf, nr, c, rotate=rotation)
            if self.ui.checkGhostscript.isChecked():
                import tempfile, os
                with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as fp:
                    cropper.writeToStream(fp.file)
                    # we close the file because it depends on the platform
                    # whether it can be read a second time while still open
                    fp.close()
                    optimizePdfGhostscript(fp.name, outputFileName)
                    os.remove(fp.name)
            else:
                cropper.writeToFile(outputFileName)
            QApplication.restoreOverrideCursor()
        except IOError as err:
            QApplication.restoreOverrideCursor()
            self.showWarning(self.tr("Could not write cropped PDF"),
                    self.tr("An error occured while writing the cropped PDF. "
                        "Please make sure that you have permission to write to "
                        "the selected file."
                        "\n\nThe official error is:\n\n{0}").format(err))
        except Exception as err:
            QApplication.restoreOverrideCursor()
            self.showWarning(self.tr("Something got in our way"),
                    self.tr("The following unexpected error has occured:"
                    "\n\n{0}").format(err))
            raise err

    def slotZoomIn(self):
        self.ui.actionFitInView.setChecked(False)
        self.ui.documentView.scale(1.2, 1.2)

    def slotZoomOut(self):
        self.ui.actionFitInView.setChecked(False)
        self.ui.documentView.scale(1/1.2, 1/1.2)

    def slotFitInView(self, checked):
        if checked:
            self.ui.documentView.fitInView(self.pdfScene.sceneRect(),
                    Qt.KeepAspectRatio)

    def slotPreviousPage(self):
        self.viewer.previousPage()
        self.updateControls()

    def slotNextPage(self):
        self.viewer.nextPage()
        self.updateControls()

    def slotFirstPage(self):
        self.viewer.firstPage()
        self.updateControls()

    def slotLastPage(self):
        self.viewer.lastPage()
        self.updateControls()

    def slotCurrentPageEdited(self, text):
        try:
            n = int(text)
            self.viewer.currentPageIndex = n-1
            self.updateControls()
        except ValueError:
            pass

    def updateControls(self):
        cur = ''
        num = ''
        if not self.viewer.isEmpty():
            cur = str(self.viewer.currentPageIndex+1)
            num = str(self.viewer.numPages())
        self.ui.editCurrentPage.setText(cur)
        self.ui.editMaxPage.setText(num)

    def slotSelectionMode(self, checked):
        if checked:
            enableExceptions = True
            if self.ui.radioSelAll.isChecked():
                self.selections.selectionMode = ViewerSelections.all
            elif self.ui.radioSelEvenOdd.isChecked():
                self.selections.selectionMode = ViewerSelections.evenodd
            elif self.ui.radioSelIndividual.isChecked():
                enableExceptions = False
                self.selections.selectionMode = ViewerSelections.individual
            self.ui.editSelExceptions.setEnabled(enableExceptions)

    def slotSelExceptionsChanged(self):
        s = str(self.ui.editSelExceptions.text())
        pages = self.str2pages(s)
        self.selections.selectionExceptions = pages

    def slotSelExceptionsEdited(self, text):
        try:
            pages = self.str2pages(str(text))
            self.selections.selectionExceptions = pages
        except ValueError:
            pass

    def aspectRatioChanged(self, aspectRatio):
        self.selections.aspectRatio = aspectRatio

    def readAspectRatio(self):
        try:
            a = self.ui.editAspectRatio.text().split(":")
            if len(a) == 1:
                w, h = a[0], 1
            else:
                w, h = a[0], a[-1]
            aspectRatio = float(w)/float(h)
            if aspectRatio <= 0:
                aspectRatio = None
        except:
            aspectRatio = None
        return aspectRatio

    def slotAspectRatioChanged(self):
        self.aspectRatioChanged(self.readAspectRatio())

    def slotDeviceTypeChanged(self, index):
        t = self.devicetypes.getType(index)
        ar = t and "%s : %s" % (t.width, t.height) or "w : h"
        self.ui.editAspectRatio.setEnabled(t is None)
        self.ui.editAspectRatio.setText(ar)
        self.slotAspectRatioChanged()

    def slotContextMenu(self, pos):
        item = self.ui.documentView.itemAt(pos)
        try:
            self.selectedRect = item.selection
            popMenu = QMenu()
            popMenu.addAction(self.ui.actionDeleteSelection)
            popMenu.addAction(self.ui.actionTrimMargins)
            popMenu.exec_(self.ui.documentView.mapToGlobal(pos))
        except AttributeError:
            pass

    def slotDeleteSelection(self):
        if self.selectedRect is not None:
            self.pdfScene.removeItem(self.selectedRect)
            self.selectedRect = None
            self.pdfScene.update()

    def getPadding(self):
        """Return [top, right, bottom, left] tuple specifying padding for trimming margins."""
        try:
            # padding can be specified as in CSS (using one to four values):
            # top, right, bottom, left
            # top, right+left, bottom
            # top+bottom, right+left
            # top+bottom+right+left
            padding = [ float(a) for a in self.ui.editPadding.text().split(',') if a ]
            if len(padding) == 0:
                return [0,0,0,0]
            if len(padding) == 1:
                return 4*padding
            if len(padding) == 2:
                return 2*padding
            if len(padding) == 3:
                return padding + [padding[1]]
            if len(padding) == 4:
                return padding
            raise ValueError
        except ValueError:
            self.showWarning(self.tr("Bad value for padding"), self.tr("The value of padding "
                "(under settings for trimming margins) must be a list of one to four floats, "
                "separated by a comma."
                "\n\nAs in CSS, options are: "
                "\n(four values) top, right, bottom, left"
                "\n(three values) top, right+left, bottom"
                "\n(two values) top+bottom, right+left"))
            return [0,0,0,0]

    def slotTrimMarginsAll(self):
        # trim margins of all selections on the current page
        noSelections = True
        for sel in self.selections.items:
            if sel.isVisible():
                noSelections = False
                self.trimMarginsSelection(sel)
        # if there is no selections, then create one
        if noSelections and not self.viewer.isEmpty():
            sel = ViewerSelectionItem(self.viewer)
            self.trimMarginsSelection(sel)
        self.pdfScene.update()

    def slotTrimMargins(self):
        if self.selectedRect is not None:
            self.trimMarginsSelection(self.selectedRect)
            self.pdfScene.update()

    def trimMarginsSelection(self, sel):
        # calculate values for trimming
        img = self.viewer.getImage(self.viewer.currentPageIndex)
        r = sel.mapRectToImage(sel.rect).toRect()
        rt = QRectF(self.doTrimMargins(img, QRect(r)))
        # adjust for padding
        dtop, dright, dbottom, dleft = self.getPadding()
        rt.adjust(-dleft, -dtop, dright, dbottom)
        rt = rt.intersected(QRectF(r)) # but don't overadjust
        # set selection to new values
        rt = sel.mapRectFromImage(rt)
        sel.setBoundingRect(rt.topLeft(), rt.bottomRight())

    def doTrimMargins(self, img, r):
        def pixAt(x, y):
            return qGray(img.pixel(x, y))
        def isFilled(L):
            changes = 0
            y = L[0]
            for x in L:
                if abs(x-y) > sensitivity:
                    changes += 1
                y = x
            return changes > allowedchanges
        sensitivity = float(self.ui.editSensitivity.text())
        allowedchanges = float(self.ui.editAllowedChanges.text())
        while r.height() > 10:
            L = [ pixAt(x, r.top()) for x in range(r.left(), r.right()) ]
            if isFilled(L): break
            r.setTop(r.top()+1)
        while r.height() > 10:
            L = [ pixAt(x, r.bottom()) for x in range(r.left(), r.right()) ]
            if isFilled(L): break
            r.setBottom(r.bottom()-1)
        while r.width() > 10:
            L = [ pixAt(r.left(), y) for y in range(r.top(), r.bottom()) ]
            if isFilled(L): break
            r.setLeft(r.left()+1)
        while r.width() > 10:
            L = [ pixAt(r.right(), y) for y in range(r.top(), r.bottom()) ]
            if isFilled(L): break
            r.setRight(r.right()-1)
        return r

    def resizeEvent(self, event):
        self.slotFitInView(self.ui.actionFitInView.isChecked())

    def closeEvent(self, event):
        self.writeSettings()
