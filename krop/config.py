import sys

try:
    # the following is only needed in python2
    # for PyQt5 >=5.11 and PyQt4 >= 4.12.2, PyQt uses a private copy of sip
    # that can be included as: from PyQt4 import sip
    # however, we don't need sip.setapi except in the old python2 setup
    import sip
    sip.setapi('QString', 2)
    sip.setapi('QVariant', 2)
except ImportError:
    pass

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
