import sys

PYQT5 = False

try:
    # use PyQt5 unless PyQt6 is specified
    if '--use-qt6' not in sys.argv:
        try:
            from PyQt5 import QtCore
            PYQT5 = True
        except ImportError:
            pass
    if not PYQT5:
        from PyQt6 import QtCore
except ImportError:
    _msg = "Please install PyQt5 or PyQt6 first."
    raise RuntimeError(_msg)