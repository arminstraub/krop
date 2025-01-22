from krop.config import PYQT6

if PYQT6:
    from PyQt6.QtCore import *
    from PyQt6.QtGui import *
    from PyQt6.QtWidgets import *
else:
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *
