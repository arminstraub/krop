# -*- coding: iso-8859-1 -*-

"""
The main window of krop

Copyright (C) 2010-2020 Armin Straub, http://arminstraub.com
"""

"""
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.
"""

import sys
from os.path import exists, splitext

try:
    from shutil import which
except:
    # shutil is not available in python2; instead we use the following:
    from distutils.spawn import find_executable as which

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

from krop.viewerselections import ViewerSelections, aspectRatioFromStr
from krop.vieweritem import ViewerItem
from krop.pdfcropper import PdfFile, PdfCropper, PdfEncryptedError, optimizePdfGhostscript
from krop.autotrim import autoTrimMargins


class AspectRatioType:
    def __init__(self, name, width, height):
        self.name = name
        self.width = width
        self.height = height

class AspectRatioTypeManager:

    def __init__(self):
        self.types = []

    def __iter__(self):
        return iter(self.types)

    def addType(self, name, width, height):
        self.types.append(AspectRatioType(name, width, height))

    def getType(self, index):
        if index >= len(self.types):
            return None
        return self.types[index]

    def addDefaults(self):
        pass

    def settingsCaption(self):
        pass
  
    def saveTypes(self, settings):
        settings.beginWriteArray(self.settingsCaption())
        for i in range(len(self.types)):
            t = self.types[i]
            settings.setArrayIndex(i)
            settings.setValue("Name", t.name)
            settings.setValue("Width", t.width)
            settings.setValue("Height", t.height)
        settings.endArray()
  
    def loadTypes(self, settings):
        count = settings.beginReadArray(self.settingsCaption())
        for i in range(count):
            settings.setArrayIndex(i)
            name = settings.value("Name")
            width = int(settings.value("Width"))
            height = int(settings.value("Height"))
            self.addType(name, width, height)
        settings.endArray()
        if count==0:
            self.addDefaults()

class SelAspectRatioTypeManager(AspectRatioTypeManager):

    def settingsCaption(self):
        return "SelAspectRatios"

    def addDefaults(self):
        self.addType("Flexible aspect ratio", 0, 0)
        self.addType("Letter", 216, 279)

class DeviceTypeManager(AspectRatioTypeManager):

    def settingsCaption(self):
        return "DeviceTypes"

    def addDefaults(self):
        self.addType("No fitting", 0, 0)
        self.addType("4:3 eReader", 4, 3)
        self.addType("4:3 eReader (widescreen)", 3, 4)
        self.addType("Nook 1st Ed.", 600, 730)
        self.addType("Nook 1st Ed. (widescreen)", 730, 600)


class MainWindow(QKMainWindow):

    fileName = None

    def __init__(self):
        QKMainWindow.__init__(self)

        self.selAspectRatioTypes = SelAspectRatioTypeManager()
        self.deviceTypes = DeviceTypeManager()

        self._viewer = ViewerItem(self)

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

        # we need to add the action to a widget in order for keyboard shortcuts to work
        self.addAction(self.ui.actionDeleteSelection)
        self.addAction(self.ui.actionFirstPage)
        self.addAction(self.ui.actionLastPage)

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
        self.ui.comboSelAspectRatioType.currentIndexChanged.connect(self.slotSelAspectRatioTypeChanged)
        self.ui.editSelAspectRatio.editingFinished.connect(self.slotSelAspectRatioChanged)
        self.ui.comboDistributeDevice.currentIndexChanged.connect(self.slotDeviceTypeChanged)
        self.ui.editDistributeAspectRatio.editingFinished.connect(self.slotDistributeAspectRatioChanged)
        self.ui.splitter.splitterMoved.connect(self.slotSplitterMoved)

        self.pdfScene = QGraphicsScene(self.ui.documentView)
        self.pdfScene.setBackgroundBrush(self.pdfScene.palette().dark())
        self.pdfScene.addItem(self.viewer)

        self.readSettings()

        # populate combobox with aspect ratio types
        for t in self.selAspectRatioTypes:
            self.ui.comboSelAspectRatioType.addItem(t.name)
        self.ui.comboSelAspectRatioType.addItem("Custom")
        # populate combobox with device types
        for t in self.deviceTypes:
            self.ui.comboDistributeDevice.addItem(t.name)
        self.ui.comboDistributeDevice.addItem("Custom")

        # disable Ghostscript option if gs is not available
        if not which('gs'):
            self.ui.checkGhostscript.setChecked(False)
            self.ui.checkGhostscript.setEnabled(False)

        self.ui.documentView.setScene(self.pdfScene)
        self.ui.documentView.setFocus()


    @property
    def viewer(self):
        return self._viewer

    @property
    def selections(self):
        return self.viewer.selections

    def currentSelectionUpdated(self):
        sel = self.selections.currentSelection
        if sel:
            r = sel.boundingRect()
            self.ui.groupCurrentSel.setEnabled(True)
            index, s = sel.aspectRatioData
            self.ui.comboSelAspectRatioType.setCurrentIndex(index)
            self.ui.editSelAspectRatio.setText(s)
            if index == 0:
                w, h = int(r.width()), int(r.height())
                self.ui.editSelAspectRatio.setText("{} : {}".format(w, h))
        else:
            self.ui.comboSelAspectRatioType.setCurrentIndex(0)
            self.ui.editSelAspectRatio.setText("")
            self.ui.groupCurrentSel.setEnabled(False)

    def readSettings(self):
        settings = QSettings()
        geometry = settings.value("Window/Geometry", "")
        if geometry:
            self.restoreGeometry(geometry)
        splitter = settings.value("Window/Splitter", "")
        if splitter:
            self.ui.splitter.restoreState(splitter)
        self.ui.actionFitInView.setChecked(settings.value("Window/FitInView", "") == "true")

        self.ui.checkTrimUseAllPages.setChecked(settings.value("Trim/UseAllPages", "") == "true")
        self.ui.editPadding.setText(
                settings.value("Trim/Padding", "2"))
        self.ui.editAllowedChanges.setText(
                settings.value("Trim/AllowedChanges", "0"))
        self.ui.editSensitivity.setText(
                settings.value("Trim/Sensitivity", "5"))

        self.ui.checkGhostscript.setChecked(settings.value("PDF/Optimize", "gs") == "gs")
        self.ui.checkIncludePagesWithoutSelections.setChecked(
                settings.value("PDF/IncludePagesWithoutSelections", "") == "true")

        self.selAspectRatioTypes.loadTypes(settings)
        self.deviceTypes.loadTypes(settings)

    def writeSettings(self):
        settings = QSettings()
        settings.setValue("Window/Geometry", self.saveGeometry())
        settings.setValue("Window/Splitter", self.ui.splitter.saveState())
        settings.setValue("Window/FitInView", "true" if
                self.ui.actionFitInView.isChecked() else "false")

        settings.setValue("Trim/UseAllPages", "true" if
                self.ui.checkTrimUseAllPages.isChecked() else "false")
        settings.setValue("Trim/Padding",
                self.ui.editPadding.text())
        settings.setValue("Trim/AllowedChanges",
                self.ui.editAllowedChanges.text())
        settings.setValue("Trim/Sensitivity",
                self.ui.editSensitivity.text())

        settings.setValue("PDF/Optimize", "gs" if
                self.ui.checkGhostscript.isChecked() else "no")
        settings.setValue("PDF/IncludePagesWithoutSelections", "true" if
                self.ui.checkIncludePagesWithoutSelections.isChecked() else "false")

        #TODO
        self.deviceTypes.saveTypes(settings)

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
        try:
            self.ui.editFile.setText(fileName)
        except TypeError:
            # new versions of Qt return a tuple (fileName, selectedFilter)
            self.ui.editFile.setText(fileName[0])

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
            pages = range(self.viewer.numPages())
        else:
            pages = self.str2pages(s)

        alwaysinclude = self.ui.checkIncludePagesWithoutSelections.isChecked()

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
                cropper.addPageCropped(pdf, nr, c, alwaysinclude, rotation)
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
        except PdfEncryptedError as err:
            QApplication.restoreOverrideCursor()
            self.showWarning(self.tr("PDF is encrypted"),
                    self.tr("This PDF needs to be decrypted before cropping. "
                        "You could try to do that using qpdf:"
                        "\nqpdf --password='hello' --decrypt encrypted.pdf decrypted.pdf"))
            raise err
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

    def slotSplitterMoved(self, pos, idx):
        self.slotFitInView(self.ui.actionFitInView.isChecked())

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


    def slotSelAspectRatioChanged(self):
        sel = self.selections.currentSelection
        if sel:
            index = self.ui.comboSelAspectRatioType.currentIndex()
            # index=0: flexible
            # index=last: custom
            s = self.ui.editSelAspectRatio.text()
            sel.aspectRatioData = [index, s]

    def slotSelAspectRatioTypeChanged(self, index):
        sel = self.selections.currentSelection
        t = self.selAspectRatioTypes.getType(index)
        # index=0: flexible
        # t=None: custom
        # ar = t and "%s : %s" % (t.width, t.height) or "w : h"
        ar = ""
        if index == 0 or t is None:
            if sel:
                r = sel.boundingRect()
                w, h = int(r.width()), int(r.height())
                ar = "{} : {}".format(w, h)
        elif t is not None:
            ar = "{} : {}".format(t.width, t.height)
        # self.ui.editSelAspectRatio.setEnabled(index == 0 or t is None)
        self.ui.editSelAspectRatio.setEnabled(t is None)
        self.ui.editSelAspectRatio.setText(ar)
        if sel:
            s = self.ui.editSelAspectRatio.text()
            sel.aspectRatioData = [index, s]


    def distributeAspectRatioChanged(self, aspectRatio):
        self.selections.distributeAspectRatio = aspectRatio

    def slotDistributeAspectRatioChanged(self):
        self.selections.distributeAspectRatio = aspectRatioFromStr(self.ui.editDistributeAspectRatio.text())

    def slotDeviceTypeChanged(self, index):
        t = self.deviceTypes.getType(index)
        ar = t and "%s : %s" % (t.width, t.height) or "w : h"
        self.ui.editDistributeAspectRatio.setEnabled(t is None)
        self.ui.editDistributeAspectRatio.setText(ar)
        self.slotDistributeAspectRatioChanged()

    def slotContextMenu(self, pos):
        item = self.ui.documentView.itemAt(pos)
        try:
            self.selections.currentSelection = item.selection
        except AttributeError:
            return
        popMenu = QMenu()
        popMenu.addAction(self.ui.actionDeleteSelection)
        popMenu.addAction(self.ui.actionTrimMargins)
        popMenu.exec_(self.ui.documentView.mapToGlobal(pos))

    def slotDeleteSelection(self):
        if self.selections.currentSelection is not None:
            self.selections.deleteSelection(self.selections.currentSelection)

    def createSelectionGrid(self, cols=1, rows=1):
        for j in range(rows):
            for i in range(cols):
                sel = self.selections.addSelection()
                r = sel.boundingRect()
                w = r.width()/cols
                h = r.height()/rows
                p0 = QPointF(r.left()+i*w, r.top()+j*h)
                sel.setBoundingRect(p0, p0 + QPointF(w, h))
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
            sel = self.selections.addSelection()
            self.trimMarginsSelection(sel)
        self.pdfScene.update()

    def slotTrimMargins(self):
        if self.selections.currentSelection is not None:
            self.trimMarginsSelection(self.selections.currentSelection)
            self.pdfScene.update()

    def trimMarginsSelection(self, sel):
        sensitivity = float(self.ui.editSensitivity.text())
        allowedchanges = float(self.ui.editAllowedChanges.text())

        # if requested, use all pages for trimming; otherwise, just the current page
        pages = [self.viewer.currentPageIndex]
        if self.ui.checkTrimUseAllPages.isChecked():
            pages = [i for i in range(self.viewer.numPages()) if sel.selectionVisibleOnPage(i)]

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            # r is the original selection, rt is the trimmed version
            r = sel.mapRectToImage(sel.rect)
            rt = QRectF()
            for idx in pages:
                # calculate values for trimming
                img = self.viewer.getImage(idx)
                rt = rt.united(autoTrimMargins(img, r, sensitivity, allowedchanges))

            # adjust for padding
            dtop, dright, dbottom, dleft = self.getPadding()
            rt.adjust(-dleft, -dtop, dright, dbottom)
            rt = rt.intersected(r) # but don't overadjust
            # set selection to new values
            rt = sel.mapRectFromImage(rt)
            sel.setBoundingRect(rt.topLeft(), rt.bottomRight())
        finally:
            QApplication.restoreOverrideCursor()

    def resizeEvent(self, event):
        self.slotFitInView(self.ui.actionFitInView.isChecked())

    def closeEvent(self, event):
        self.writeSettings()
