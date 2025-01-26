import sys

PYQT6 = False

try:
    # use PyQt6 unless PyQt5 is specified
    if '--use-qt5' not in sys.argv:
        try:
            from PyQt6 import QtCore
            PYQT6 = True
        except ImportError:
            pass
    if not PYQT6:
        from PyQt5 import QtCore
except ImportError:
    _msg = "Please install PyQt6 (or PyQt5) first."
    raise RuntimeError(_msg)