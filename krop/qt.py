from krop.config import PYQT5

if PYQT5:
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    # QApplication now resides in the new QtWidgets
    from PyQt5.QtWidgets import *
    # we also import QtCore and QtGui for use in mainwindowui.py
    from PyQt5 import QtCore, QtGui
else:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
    from PyQt4 import QtCore, QtGui
