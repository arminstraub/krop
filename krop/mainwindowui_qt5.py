# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Fri May 29 08:40:50 2020
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(949, 736)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName("splitter")
        self.tabWidget = QtWidgets.QTabWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName("tabWidget")
        self.tabBasic = QtWidgets.QWidget()
        self.tabBasic.setObjectName("tabBasic")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tabBasic)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.groupSaveTo = QtWidgets.QGroupBox(self.tabBasic)
        self.groupSaveTo.setObjectName("groupSaveTo")
        self.gridLayout = QtWidgets.QGridLayout(self.groupSaveTo)
        self.gridLayout.setObjectName("gridLayout")
        self.editFile = QtWidgets.QLineEdit(self.groupSaveTo)
        self.editFile.setObjectName("editFile")
        self.gridLayout.addWidget(self.editFile, 0, 0, 1, 1)
        self.buttonFileSelect = QtWidgets.QToolButton(self.groupSaveTo)
        self.buttonFileSelect.setText("")
        self.buttonFileSelect.setAutoRaise(True)
        self.buttonFileSelect.setObjectName("buttonFileSelect")
        self.gridLayout.addWidget(self.buttonFileSelect, 0, 1, 1, 1)
        self.verticalLayout_4.addWidget(self.groupSaveTo)
        self.groupPDFOperations = QtWidgets.QGroupBox(self.tabBasic)
        self.groupPDFOperations.setFlat(False)
        self.groupPDFOperations.setObjectName("groupPDFOperations")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.groupPDFOperations)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.comboRotation = QtWidgets.QComboBox(self.groupPDFOperations)
        self.comboRotation.setObjectName("comboRotation")
        self.comboRotation.addItem("")
        self.comboRotation.addItem("")
        self.comboRotation.addItem("")
        self.comboRotation.addItem("")
        self.verticalLayout_8.addWidget(self.comboRotation)
        self.checkGhostscript = QtWidgets.QCheckBox(self.groupPDFOperations)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkGhostscript.sizePolicy().hasHeightForWidth())
        self.checkGhostscript.setSizePolicy(sizePolicy)
        self.checkGhostscript.setChecked(True)
        self.checkGhostscript.setObjectName("checkGhostscript")
        self.verticalLayout_8.addWidget(self.checkGhostscript)
        self.verticalLayout_4.addWidget(self.groupPDFOperations)
        self.groupWhichPages = QtWidgets.QGroupBox(self.tabBasic)
        self.groupWhichPages.setObjectName("groupWhichPages")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupWhichPages)
        self.verticalLayout.setObjectName("verticalLayout")
        self.editWhichPages = QtWidgets.QLineEdit(self.groupWhichPages)
        self.editWhichPages.setObjectName("editWhichPages")
        self.verticalLayout.addWidget(self.editWhichPages)
        self.labelWhichPagesEg = QtWidgets.QLabel(self.groupWhichPages)
        self.labelWhichPagesEg.setWordWrap(True)
        self.labelWhichPagesEg.setObjectName("labelWhichPagesEg")
        self.verticalLayout.addWidget(self.labelWhichPagesEg)
        self.checkIncludePagesWithoutSelections = QtWidgets.QCheckBox(self.groupWhichPages)
        self.checkIncludePagesWithoutSelections.setChecked(True)
        self.checkIncludePagesWithoutSelections.setObjectName("checkIncludePagesWithoutSelections")
        self.verticalLayout.addWidget(self.checkIncludePagesWithoutSelections)
        self.verticalLayout_4.addWidget(self.groupWhichPages)
        self.groupSelectionMode = QtWidgets.QGroupBox(self.tabBasic)
        self.groupSelectionMode.setFlat(False)
        self.groupSelectionMode.setObjectName("groupSelectionMode")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupSelectionMode)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.radioSelAll = QtWidgets.QRadioButton(self.groupSelectionMode)
        self.radioSelAll.setChecked(True)
        self.radioSelAll.setObjectName("radioSelAll")
        self.gridLayout_2.addWidget(self.radioSelAll, 0, 0, 1, 2)
        self.radioSelEvenOdd = QtWidgets.QRadioButton(self.groupSelectionMode)
        self.radioSelEvenOdd.setObjectName("radioSelEvenOdd")
        self.gridLayout_2.addWidget(self.radioSelEvenOdd, 1, 0, 1, 2)
        self.radioSelIndividual = QtWidgets.QRadioButton(self.groupSelectionMode)
        self.radioSelIndividual.setObjectName("radioSelIndividual")
        self.gridLayout_2.addWidget(self.radioSelIndividual, 2, 0, 1, 2)
        self.labelSelExceptions = QtWidgets.QLabel(self.groupSelectionMode)
        self.labelSelExceptions.setObjectName("labelSelExceptions")
        self.gridLayout_2.addWidget(self.labelSelExceptions, 3, 0, 1, 1)
        self.editSelExceptions = QtWidgets.QLineEdit(self.groupSelectionMode)
        self.editSelExceptions.setObjectName("editSelExceptions")
        self.gridLayout_2.addWidget(self.editSelExceptions, 3, 1, 1, 1)
        self.verticalLayout_4.addWidget(self.groupSelectionMode)
        spacerItem = QtWidgets.QSpacerItem(20, 484, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem)
        self.tabWidget.addTab(self.tabBasic, "")
        self.tabAdvanced = QtWidgets.QWidget()
        self.tabAdvanced.setObjectName("tabAdvanced")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.tabAdvanced)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.groupCurrentSel = QtWidgets.QGroupBox(self.tabAdvanced)
        self.groupCurrentSel.setEnabled(False)
        self.groupCurrentSel.setObjectName("groupCurrentSel")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupCurrentSel)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.labelSelAspectRatio = QtWidgets.QLabel(self.groupCurrentSel)
        self.labelSelAspectRatio.setObjectName("labelSelAspectRatio")
        self.gridLayout_4.addWidget(self.labelSelAspectRatio, 0, 0, 1, 1)
        self.editSelAspectRatio = QtWidgets.QLineEdit(self.groupCurrentSel)
        self.editSelAspectRatio.setObjectName("editSelAspectRatio")
        self.gridLayout_4.addWidget(self.editSelAspectRatio, 0, 1, 1, 1)
        self.checkSelLockAspectRatio = QtWidgets.QCheckBox(self.groupCurrentSel)
        self.checkSelLockAspectRatio.setToolTip("")
        self.checkSelLockAspectRatio.setChecked(True)
        self.checkSelLockAspectRatio.setObjectName("checkSelLockAspectRatio")
        self.gridLayout_4.addWidget(self.checkSelLockAspectRatio, 1, 0, 1, 2)
        self.verticalLayout_5.addWidget(self.groupCurrentSel)
        self.groupTrimMargins = QtWidgets.QGroupBox(self.tabAdvanced)
        self.groupTrimMargins.setObjectName("groupTrimMargins")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupTrimMargins)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.checkTrimUseAllPages = QtWidgets.QCheckBox(self.groupTrimMargins)
        self.checkTrimUseAllPages.setChecked(True)
        self.checkTrimUseAllPages.setObjectName("checkTrimUseAllPages")
        self.gridLayout_3.addWidget(self.checkTrimUseAllPages, 0, 0, 1, 2)
        self.labelPadding = QtWidgets.QLabel(self.groupTrimMargins)
        self.labelPadding.setObjectName("labelPadding")
        self.gridLayout_3.addWidget(self.labelPadding, 1, 0, 1, 1)
        self.editPadding = QtWidgets.QLineEdit(self.groupTrimMargins)
        self.editPadding.setText("")
        self.editPadding.setObjectName("editPadding")
        self.gridLayout_3.addWidget(self.editPadding, 1, 1, 1, 1)
        self.labelTrimMarginsEg = QtWidgets.QLabel(self.groupTrimMargins)
        self.labelTrimMarginsEg.setWordWrap(True)
        self.labelTrimMarginsEg.setObjectName("labelTrimMarginsEg")
        self.gridLayout_3.addWidget(self.labelTrimMarginsEg, 2, 0, 1, 2)
        self.labelAllowedChanges = QtWidgets.QLabel(self.groupTrimMargins)
        self.labelAllowedChanges.setEnabled(True)
        self.labelAllowedChanges.setObjectName("labelAllowedChanges")
        self.gridLayout_3.addWidget(self.labelAllowedChanges, 3, 0, 1, 1)
        self.editAllowedChanges = QtWidgets.QLineEdit(self.groupTrimMargins)
        self.editAllowedChanges.setEnabled(True)
        self.editAllowedChanges.setObjectName("editAllowedChanges")
        self.gridLayout_3.addWidget(self.editAllowedChanges, 3, 1, 1, 1)
        self.labelSensitivity = QtWidgets.QLabel(self.groupTrimMargins)
        self.labelSensitivity.setEnabled(True)
        self.labelSensitivity.setObjectName("labelSensitivity")
        self.gridLayout_3.addWidget(self.labelSensitivity, 4, 0, 1, 1)
        self.editSensitivity = QtWidgets.QLineEdit(self.groupTrimMargins)
        self.editSensitivity.setEnabled(True)
        self.editSensitivity.setObjectName("editSensitivity")
        self.gridLayout_3.addWidget(self.editSensitivity, 4, 1, 1, 1)
        self.verticalLayout_5.addWidget(self.groupTrimMargins)
        self.groupDevice = QtWidgets.QGroupBox(self.tabAdvanced)
        self.groupDevice.setObjectName("groupDevice")
        self.formLayout = QtWidgets.QFormLayout(self.groupDevice)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.comboDevice = QtWidgets.QComboBox(self.groupDevice)
        self.comboDevice.setEditable(False)
        self.comboDevice.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContentsOnFirstShow)
        self.comboDevice.setObjectName("comboDevice")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.comboDevice)
        self.labelAspectRatio = QtWidgets.QLabel(self.groupDevice)
        self.labelAspectRatio.setObjectName("labelAspectRatio")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.labelAspectRatio)
        self.editAspectRatio = QtWidgets.QLineEdit(self.groupDevice)
        self.editAspectRatio.setObjectName("editAspectRatio")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.editAspectRatio)
        self.labelDeviceHelp = QtWidgets.QLabel(self.groupDevice)
        self.labelDeviceHelp.setWordWrap(True)
        self.labelDeviceHelp.setObjectName("labelDeviceHelp")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.SpanningRole, self.labelDeviceHelp)
        self.verticalLayout_5.addWidget(self.groupDevice)
        spacerItem1 = QtWidgets.QSpacerItem(20, 339, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem1)
        self.tabWidget.addTab(self.tabAdvanced, "")
        self.tabHelp = QtWidgets.QWidget()
        self.tabHelp.setObjectName("tabHelp")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tabHelp)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.labelHelp = QtWidgets.QLabel(self.tabHelp)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelHelp.sizePolicy().hasHeightForWidth())
        self.labelHelp.setSizePolicy(sizePolicy)
        self.labelHelp.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.labelHelp.setBaseSize(QtCore.QSize(0, 0))
        self.labelHelp.setTextFormat(QtCore.Qt.AutoText)
        self.labelHelp.setWordWrap(True)
        self.labelHelp.setOpenExternalLinks(True)
        self.labelHelp.setObjectName("labelHelp")
        self.verticalLayout_3.addWidget(self.labelHelp)
        spacerItem2 = QtWidgets.QSpacerItem(20, 524, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem2)
        self.labelHelpLicense = QtWidgets.QLabel(self.tabHelp)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelHelpLicense.sizePolicy().hasHeightForWidth())
        self.labelHelpLicense.setSizePolicy(sizePolicy)
        self.labelHelpLicense.setTextFormat(QtCore.Qt.AutoText)
        self.labelHelpLicense.setWordWrap(True)
        self.labelHelpLicense.setOpenExternalLinks(True)
        self.labelHelpLicense.setObjectName("labelHelpLicense")
        self.verticalLayout_3.addWidget(self.labelHelpLicense)
        self.tabWidget.addTab(self.tabHelp, "")
        self.frame = QtWidgets.QFrame(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.documentView = QtWidgets.QGraphicsView(self.frame)
        self.documentView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.documentView.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.documentView.setObjectName("documentView")
        self.verticalLayout_2.addWidget(self.documentView)
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.buttonFirst = QtWidgets.QPushButton(self.frame_2)
        self.buttonFirst.setMinimumSize(QtCore.QSize(24, 24))
        self.buttonFirst.setMaximumSize(QtCore.QSize(24, 24))
        self.buttonFirst.setFocusPolicy(QtCore.Qt.NoFocus)
        self.buttonFirst.setText("")
        self.buttonFirst.setFlat(True)
        self.buttonFirst.setObjectName("buttonFirst")
        self.horizontalLayout_2.addWidget(self.buttonFirst)
        self.buttonPrevious = QtWidgets.QPushButton(self.frame_2)
        self.buttonPrevious.setMinimumSize(QtCore.QSize(24, 24))
        self.buttonPrevious.setMaximumSize(QtCore.QSize(24, 24))
        self.buttonPrevious.setFocusPolicy(QtCore.Qt.NoFocus)
        self.buttonPrevious.setText("")
        self.buttonPrevious.setFlat(True)
        self.buttonPrevious.setObjectName("buttonPrevious")
        self.horizontalLayout_2.addWidget(self.buttonPrevious)
        self.editCurrentPage = QtWidgets.QLineEdit(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editCurrentPage.sizePolicy().hasHeightForWidth())
        self.editCurrentPage.setSizePolicy(sizePolicy)
        self.editCurrentPage.setMinimumSize(QtCore.QSize(40, 23))
        self.editCurrentPage.setMaximumSize(QtCore.QSize(40, 16777215))
        self.editCurrentPage.setInputMask("")
        self.editCurrentPage.setAlignment(QtCore.Qt.AlignCenter)
        self.editCurrentPage.setObjectName("editCurrentPage")
        self.horizontalLayout_2.addWidget(self.editCurrentPage)
        self.label = QtWidgets.QLabel(self.frame_2)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.editMaxPage = QtWidgets.QLineEdit(self.frame_2)
        self.editMaxPage.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editMaxPage.sizePolicy().hasHeightForWidth())
        self.editMaxPage.setSizePolicy(sizePolicy)
        self.editMaxPage.setMinimumSize(QtCore.QSize(40, 23))
        self.editMaxPage.setMaximumSize(QtCore.QSize(40, 16777215))
        self.editMaxPage.setAutoFillBackground(False)
        self.editMaxPage.setInputMask("")
        self.editMaxPage.setFrame(True)
        self.editMaxPage.setAlignment(QtCore.Qt.AlignCenter)
        self.editMaxPage.setReadOnly(True)
        self.editMaxPage.setObjectName("editMaxPage")
        self.horizontalLayout_2.addWidget(self.editMaxPage)
        self.buttonNext = QtWidgets.QPushButton(self.frame_2)
        self.buttonNext.setMinimumSize(QtCore.QSize(24, 24))
        self.buttonNext.setMaximumSize(QtCore.QSize(24, 24))
        self.buttonNext.setFocusPolicy(QtCore.Qt.NoFocus)
        self.buttonNext.setText("")
        self.buttonNext.setFlat(True)
        self.buttonNext.setObjectName("buttonNext")
        self.horizontalLayout_2.addWidget(self.buttonNext)
        self.buttonLast = QtWidgets.QPushButton(self.frame_2)
        self.buttonLast.setMinimumSize(QtCore.QSize(24, 24))
        self.buttonLast.setMaximumSize(QtCore.QSize(24, 24))
        self.buttonLast.setFocusPolicy(QtCore.Qt.NoFocus)
        self.buttonLast.setText("")
        self.buttonLast.setFlat(True)
        self.buttonLast.setObjectName("buttonLast")
        self.horizontalLayout_2.addWidget(self.buttonLast)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.verticalLayout_2.addWidget(self.frame_2)
        self.verticalLayout_7.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 949, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        self.toolBar.setMovable(True)
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonFollowStyle)
        self.toolBar.setFloatable(False)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionZoomIn = QtWidgets.QAction(MainWindow)
        self.actionZoomIn.setObjectName("actionZoomIn")
        self.actionZoomOut = QtWidgets.QAction(MainWindow)
        self.actionZoomOut.setObjectName("actionZoomOut")
        self.actionPreviousPage = QtWidgets.QAction(MainWindow)
        self.actionPreviousPage.setObjectName("actionPreviousPage")
        self.actionNextPage = QtWidgets.QAction(MainWindow)
        self.actionNextPage.setObjectName("actionNextPage")
        self.actionOpenFile = QtWidgets.QAction(MainWindow)
        self.actionOpenFile.setObjectName("actionOpenFile")
        self.actionFitInView = QtWidgets.QAction(MainWindow)
        self.actionFitInView.setCheckable(True)
        self.actionFitInView.setObjectName("actionFitInView")
        self.actionKrop = QtWidgets.QAction(MainWindow)
        self.actionKrop.setEnabled(False)
        self.actionKrop.setObjectName("actionKrop")
        self.actionDeleteSelection = QtWidgets.QAction(MainWindow)
        self.actionDeleteSelection.setObjectName("actionDeleteSelection")
        self.actionFirstPage = QtWidgets.QAction(MainWindow)
        self.actionFirstPage.setObjectName("actionFirstPage")
        self.actionLastPage = QtWidgets.QAction(MainWindow)
        self.actionLastPage.setObjectName("actionLastPage")
        self.actionTrimMargins = QtWidgets.QAction(MainWindow)
        self.actionTrimMargins.setObjectName("actionTrimMargins")
        self.actionSelectFile = QtWidgets.QAction(MainWindow)
        self.actionSelectFile.setObjectName("actionSelectFile")
        self.actionTrimMarginsAll = QtWidgets.QAction(MainWindow)
        self.actionTrimMarginsAll.setEnabled(False)
        self.actionTrimMarginsAll.setObjectName("actionTrimMarginsAll")
        self.toolBar.addAction(self.actionOpenFile)
        self.toolBar.addAction(self.actionKrop)
        self.toolBar.addAction(self.actionZoomIn)
        self.toolBar.addAction(self.actionZoomOut)
        self.toolBar.addAction(self.actionFitInView)
        self.toolBar.addAction(self.actionPreviousPage)
        self.toolBar.addAction(self.actionNextPage)
        self.toolBar.addAction(self.actionTrimMarginsAll)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.buttonPrevious.clicked.connect(self.actionPreviousPage.trigger)
        self.buttonNext.clicked.connect(self.actionNextPage.trigger)
        self.buttonFirst.clicked.connect(self.actionFirstPage.trigger)
        self.buttonLast.clicked.connect(self.actionLastPage.trigger)
        self.buttonFileSelect.clicked.connect(self.actionSelectFile.trigger)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "krop: A tool to crop your PDFs"))
        self.groupSaveTo.setTitle(_translate("MainWindow", "Save cropped PDF to"))
        self.editFile.setToolTip(_translate("MainWindow", "<p>This is where the cropped PDF will be saved after you choose <i>Krop!</i> in the menu.</p>"))
        self.buttonFileSelect.setToolTip(_translate("MainWindow", "<p>This is where the cropped PDF will be saved after you choose <i>Krop!</i> in the menu.</p>"))
        self.groupPDFOperations.setTitle(_translate("MainWindow", "Extra operations on the final PDF"))
        self.comboRotation.setItemText(0, _translate("MainWindow", "don\'t rotate"))
        self.comboRotation.setItemText(1, _translate("MainWindow", "rotate left (90° counterclockwise)"))
        self.comboRotation.setItemText(2, _translate("MainWindow", "rotate right (90° clockwise)"))
        self.comboRotation.setItemText(3, _translate("MainWindow", "upside down"))
        self.checkGhostscript.setToolTip(_translate("MainWindow", "<p>In order to use this option, Ghostscript must be installed and available as <i>gs</i>. Whether this option actually improves the file size depends on the PDF file.</p>"))
        self.checkGhostscript.setText(_translate("MainWindow", "Use Ghostscript to optimize"))
        self.groupWhichPages.setTitle(_translate("MainWindow", "Which pages to include"))
        self.labelWhichPagesEg.setText(_translate("MainWindow", "<p><i>Eg:</i> 1-5 for the first 5 pages\n"
"<br><i>Eg:</i> 2- for all but the first page\n"
"<br><i>Eg:</i> 1,4-5,7- to omit pages 2,3,6</p>"))
        self.checkIncludePagesWithoutSelections.setToolTip(_translate("MainWindow", "<p>If checked, pages without selections will be included in the output unchanged. Otherwise, such pages will be removed from the output.</p>"))
        self.checkIncludePagesWithoutSelections.setText(_translate("MainWindow", "Include pages without selections"))
        self.groupSelectionMode.setToolTip(_translate("MainWindow", "<p>Should all pages be cropped based on the same selections? Maybe you want to treat even and odd pages differently? For full control you can crop each page using individual selections.</p>"))
        self.groupSelectionMode.setTitle(_translate("MainWindow", "Selections apply to"))
        self.radioSelAll.setText(_translate("MainWindow", "all pages"))
        self.radioSelEvenOdd.setText(_translate("MainWindow", "even/odd pages"))
        self.radioSelIndividual.setText(_translate("MainWindow", "individual page"))
        self.labelSelExceptions.setToolTip(_translate("MainWindow", "<p>List pages which require individual selections.</p>"))
        self.labelSelExceptions.setText(_translate("MainWindow", "Exceptions:"))
        self.editSelExceptions.setToolTip(_translate("MainWindow", "<p>List pages which require individual selections.</p>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabBasic), _translate("MainWindow", "Basic"))
        self.groupCurrentSel.setTitle(_translate("MainWindow", "Current Selection"))
        self.labelSelAspectRatio.setText(_translate("MainWindow", "Aspect ratio:"))
        self.checkSelLockAspectRatio.setText(_translate("MainWindow", "Lock aspect ratio"))
        self.groupTrimMargins.setToolTip(_translate("MainWindow", "<p>Right-click a selection to automatically trim it.</p>"))
        self.groupTrimMargins.setTitle(_translate("MainWindow", "Settings for trimming margins"))
        self.checkTrimUseAllPages.setToolTip(_translate("MainWindow", "<p>If selected, all pages will be inspected (which can be very slow!) in order to determine the margins for auto trimming. Otherwise, only the current page is inspected.</p>"))
        self.checkTrimUseAllPages.setText(_translate("MainWindow", "Use all pages (slow!)"))
        self.labelPadding.setText(_translate("MainWindow", "Padding:"))
        self.labelTrimMarginsEg.setText(_translate("MainWindow", "<p><i>Eg:</i> 2 or 5,2 or 5,2,5,5 (interpreted as in CSS)</p>"))
        self.labelAllowedChanges.setText(_translate("MainWindow", "Allowed changes:"))
        self.labelSensitivity.setText(_translate("MainWindow", "Color sensitivity:"))
        self.groupDevice.setTitle(_translate("MainWindow", "Fit screen of device"))
        self.labelAspectRatio.setText(_translate("MainWindow", "Aspect ratio:"))
        self.labelDeviceHelp.setText(_translate("MainWindow", "<p><i>Eg:</i> 600:730 (ratio of width to height)</p>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabAdvanced), _translate("MainWindow", "Advanced"))
        self.labelHelp.setText(_translate("MainWindow", "<h3>Getting started</h3>\n"
"<p>Using your mouse, create one or more selections on the pdf document. These are the regions that will be included into the cropped file.</p>\n"
"<p>When you are done, click <i>Krop!</i> in the menu to create a cropped version of your document.</p>\n"
"<h3>Hints</h3>\n"
"<p>Right-click a selection to delete it.</p>\n"
"<p>You can choose to create individual selections for each page.</p>\n"
"<p>You can automatically trim the margins of your selections.</p>\n"
"<p>Examples and more information can be found at: <a href=\'http://arminstraub.com/software/krop\'>arminstraub.com</a></p>\n"
""))
        self.labelHelpLicense.setText(_translate("MainWindow", "<p>Copyright (C) 2010-2020 Armin Straub\n"
"<br><a href=\'http://arminstraub.com\'>http://arminstraub.com</a></p>\n"
"<p>This program is free software and available to you in the hope that it will be useful; but without any warranty. It is distributed under the terms of the GNU General Public License (GPLv3+). See the accompanying files for more information.</p>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabHelp), _translate("MainWindow", "Help"))
        self.label.setText(_translate("MainWindow", "of"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionZoomIn.setText(_translate("MainWindow", "Zoom In"))
        self.actionZoomIn.setShortcut(_translate("MainWindow", "Ctrl+="))
        self.actionZoomOut.setText(_translate("MainWindow", "Zoom Out"))
        self.actionZoomOut.setShortcut(_translate("MainWindow", "Ctrl+-"))
        self.actionPreviousPage.setText(_translate("MainWindow", "Previous Page"))
        self.actionPreviousPage.setShortcut(_translate("MainWindow", "Ctrl+Left"))
        self.actionNextPage.setText(_translate("MainWindow", "Next Page"))
        self.actionNextPage.setShortcut(_translate("MainWindow", "Ctrl+Right"))
        self.actionOpenFile.setText(_translate("MainWindow", "Open"))
        self.actionFitInView.setText(_translate("MainWindow", "Fit In View"))
        self.actionKrop.setText(_translate("MainWindow", "Krop!"))
        self.actionDeleteSelection.setText(_translate("MainWindow", "Delete Selection"))
        self.actionFirstPage.setText(_translate("MainWindow", "First Page"))
        self.actionLastPage.setText(_translate("MainWindow", "Last Page"))
        self.actionTrimMargins.setText(_translate("MainWindow", "Trim Margins"))
        self.actionSelectFile.setText(_translate("MainWindow", "Select File"))
        self.actionTrimMarginsAll.setText(_translate("MainWindow", "Trim Margins"))
        self.actionTrimMarginsAll.setToolTip(_translate("MainWindow", "Trim Margins"))

