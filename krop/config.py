import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 1)

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
