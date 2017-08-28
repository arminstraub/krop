try:
    import sip
    PYQT5 = False
    try:
        import PyQt5
        PYQT5 = True
        #  PYQT5 = False
    except ImportError:
        pass
    if not PYQT5:
        import PyQt4
except ImportError:
    _msg = "Please install PyQt4 or PyQt5 first."
    raise RuntimeError(_msg)

sip.setapi('QString', 2)
sip.setapi('QVariant', 2)

# use KDE unless not available or specified otherwise
import sys
if '--no-kde' in sys.argv:
    KDE = False
else:
    try:
        import PyKDE4
        KDE = True
        del PyKDE4
    except ImportError:
        KDE = False
