import sys

PYQT5 = False
try:
    # use PyQt5 unless not available or specified otherwise
    if '--no-qt5' not in sys.argv:
        try:
            from PyQt5 import QtCore
            PYQT5 = True
        except ImportError:
            pass
    if not PYQT5:
        from PyQt4 import QtCore
except ImportError:
    _msg = "Please install PyQt4 or PyQt5 first."
    raise RuntimeError(_msg)