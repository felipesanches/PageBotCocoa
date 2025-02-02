#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     canvascontext.py
#

from pagebot.contexts.base.basecontext import BaseContext
from pagebot.toolbox.units import upt, point2D
from pagebotcocoa.contexts.canvas.canvasbuilder import CanvasBuilder

class CanvasContext(BaseContext):

    def __init__(self):
        super().__init__()
        self.b = CanvasBuilder()
        self.name = self.__class__.__name__

    #   D O C U M E N T

    def newPage(self, width, height):
        return self.b.newPage(width, height)

    def update(self):
        self.b.update()

    def setStyles(self, styles):
        pass

    def fill(self, c):
        pass

    def stroke(self, c, w=None):
        pass

    def shadow(self, shadow):
        pass

    def linearGradient(self, gradient, origin, w, h, e=None):
        pass

    cmykFill = fill
    cmykStroke = stroke
    cmykShadow = shadow
    cmykLinearGradient = linearGradient
    radialGradient = linearGradient
    cmykRadialGradient = radialGradient

    #   P A T H

    def newPath(self):
        self.b.newPath()

    def moveTo(self, pt):
        ppt = upt(point2D(pt))
        self.b.moveTo(ppt)

    def lineTo(self, pt):
        ppt = upt(point2D(pt))
        self.b.lineTo(ppt)

    def curveTo(self, bcp1, bcp2, pt):
        b1pt = upt(point2D(bcp1))
        b2pt = upt(point2D(bcp2))
        ppt = upt(point2D(pt))
        self.b.curveTo(b1pt, b2pt, ppt)

    def stroke(self, c):
        if c is None:
            self.b.stroke(None)
        else:
            r, g, b = c.rgb
            self.b.stroke(r, g, b, a=c.a)

        self.strokeWidth(0.5)

    def strokeWidth(self, w):
        wpt = upt(w)
        self.b.strokeWidth(wpt)

    def getFlattenedPath(self, path=None):
        pass

    def getFlattenedContours(self, path=None):
        pass

    def getGlyphPath(self, glyph, p=None, path=None):
        pass
