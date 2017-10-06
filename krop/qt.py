from krop.config import PYQT5

if PYQT5:
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    # QApplication now resides in the new QtWidgets
    from PyQt5.QtWidgets import *
else:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
