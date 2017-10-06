import sys

PYQT5 = False
try:
    import sip
    # use PyQt5 unless not available or specified otherwise
    if '--no-qt5' not in sys.argv:
        try:
            import PyQt5
            PYQT5 = True
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
KDE = False
if '--no-kde' not in sys.argv:
    if PYQT5:
        #TODO use PyKDE5 once more easily available
        pass
    else:
        try:
            import PyKDE4
            KDE = True
        except ImportError:
            pass
