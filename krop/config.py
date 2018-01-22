try:
    import PyQt5
except ImportError:
    _msg = "Please install PyQt5 first."
    raise RuntimeError(_msg)
