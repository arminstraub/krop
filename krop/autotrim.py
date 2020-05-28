# -*- coding: iso-8859-1 -*-

"""
Cropping functionality for krop.

Copyright (C) 2010-2020 Armin Straub, http://arminstraub.com
"""

"""
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.
"""

from krop.qt import *


def autoTrimMargins(img, r, sensitivity, allowedchanges):
    """Given a QImage img and a QRect r, automatically trims the margins of
    that rectangle according to the parameters."""
    def pixAt(x, y):
        return qGray(img.pixel(x, y))
    def isTrimmable(L):
        changes = 0
        y = L[0]
        for x in L:
            if abs(x-y) > sensitivity:
                changes += 1
                if changes > allowedchanges:
                    return False
            y = x
        return True
    mindim = 10
    while r.height() > mindim:
        L = [ pixAt(x, r.top()) for x in range(r.left(), r.right()) ]
        if not isTrimmable(L): break
        r.setTop(r.top()+1)
    while r.height() > mindim:
        L = [ pixAt(x, r.bottom()) for x in range(r.left(), r.right()) ]
        if not isTrimmable(L): break
        r.setBottom(r.bottom()-1)
    while r.width() > mindim:
        L = [ pixAt(r.left(), y) for y in range(r.top(), r.bottom()) ]
        if not isTrimmable(L): break
        r.setLeft(r.left()+1)
    while r.width() > mindim:
        L = [ pixAt(r.right(), y) for y in range(r.top(), r.bottom()) ]
        if not isTrimmable(L): break
        r.setRight(r.right()-1)
    return r

