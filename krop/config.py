# use KDE unless not available or specified otherwise
import sys
if '--nokde' in sys.argv:
    KDE = False
else:
    try:
        import PyKDE4
        KDE = True
        del PyKDE4
    except ImportError:
        KDE = False
