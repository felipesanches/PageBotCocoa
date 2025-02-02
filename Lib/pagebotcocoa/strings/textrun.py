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
#     textrun.py
#
from pagebot.toolbox.units import em, pt
from pagebot.toolbox.color import color
from pagebot.fonttoolbox.objects.font import findFont

from CoreText import (CTRunGetGlyphCount, CTRunGetStringRange,
        CTRunGetStringIndicesPtr, CTRunGetAdvances, CTRunGetStatus,
        CTRunGetPositions, CTRunGetGlyphs, CTRunGetAttributes,
        CTRunGetTextMatrix, CFRange)

class TextRun:
    """A TextRun object contains the chunk of text that combines a single
    style.

    Wraps the CoreText CTRun class, see also:

    https://developer.apple.com/documentation/coretext/ctrun-61n
    """

    def __init__(self, ctRun, runIndex):
        # Index of the run in the TextLine.
        self.runIndex = runIndex
        self._ctRun = ctRun

        # Property cash for constructed style from run parameters.
        self._style = None
        self.glyphCount = gc = CTRunGetGlyphCount(ctRun)

        # Reverse the style from
        attrs = CTRunGetAttributes(ctRun)
        self.nsFont = attrs['NSFont']

        # Initialize by calling the property self.font.
        self._font = None

        #self.fontDescriptor = f.fontDescriptor()
        self.nsColor = attrs['NSColor']
        # Initialize by calling self.color.
        self._fill = None
        self.nsParagraphStyle = attrs['NSParagraphStyle']
        # Save, in case the caller want to query other run parameters.
        self.attrs = attrs

        self.iStart, self.iEnd = CTRunGetStringRange(ctRun)
        self.string = ''

        # Hack for now to find the string in repr-string if self._ctLine.
        # TODO: Make a better conversion here, not relying on the format of the
        # repr-string.
        for index, part in enumerate(str(ctRun).split('"')[1].split('\\u')):
            if index == 0:
                self.string += part
            elif len(part) >= 4:
                self.string += chr(int(part[0:4], 16))
                self.string += part[4:]

        #print(gc, len(CTRunGetStringIndicesPtr(ctRun)), CTRunGetStringIndicesPtr(ctRun), ctRun)
        try:
            self.stringIndices = CTRunGetStringIndicesPtr(ctRun)[0:gc]
        except TypeError:
            self.stringIndices = [0]

        #CTRunGetStringIndices(ctRun._ctRun, CFRange(0, 5), None)[4]
        self.advances = CTRunGetAdvances(ctRun, CFRange(0, 5), None)
        #self.positions = CTRunGetPositionsPtr(ctRun)[0:gc]
        #CTRunGetPositions(ctRun, CFRange(0, 5), None)[4]
        #self.glyphFontIndices = CTRunGetGlyphsPtr(ctRun)[0:gc]
        #print(CTRunGetGlyphs(ctRun, CFRange(0, 5), None)[0:5])
        self.status = CTRunGetStatus(ctRun)

        # get all positions
        self.positions = CTRunGetPositions(ctRun, (0, gc), None)
        # get all glyphs
        self.glyphs = CTRunGetGlyphs(ctRun, (0, gc), None)

    def __len__(self):
        return self.glyphCount

    def __repr__(self):
        return '[TextRun #%d "%s"]' % (self.runIndex, self.string)

    def __getitem__(self, index):
        return self.string[index]

    def _get_style(self):
        """Answers the constructed style dictionary, with names that fit the
        standard PageBot style."""
        if self._style is None:
            self._style = dict(
                textFill=self.textFill,
                pl=self.headIndent,
                pr=self.tailIndent,
                fontSize=self.fontSize,
                font=self.font or self.fontName, # Answer Font object or font name.
                leading=self.leading
            )
        return self._style
    style = property(_get_style)

    def _get_textFill(self):
        if self._fill is None:
            self._fill = color(r=self.nsColor.redComponent(),
                    g=self.nsColor.greenComponent(),
                    b=self.nsColor.blueComponent(),
                    a=self.nsColor.alphaComponent())
        return self._fill
    textFill = fill = property(_get_textFill)

    # Font stuff

    def _get_displayName(self):
        return self.nsFont.displayName()
    displayName = property(_get_displayName)

    def _get_familyName(self):
        return self.nsFont.familyName()
    familyName = property(_get_familyName)

    def _get_fontName(self):
        return self.nsFont.fontName()
    fontName = font = property(_get_fontName)

    def _get_font(self):
        if self._font is None:
            self._font = findFont(self.fontName)
        return self._font
    font = property(_get_font)

    def _get_isVertical(self):
        return self.nsFont.isVertical()
    isVertical = property(_get_isVertical)

    def _get_isFixedPitch(self):
        return self.nsFont.isFixedPitch()
    isFixedPitch = property(_get_isFixedPitch)

    def _get_boundingRectForFont(self):
        (x, y), (w, h) = self.nsFont.boundingRectForFont()
        return x, y, w, h
    boundingRectForFont = property(_get_boundingRectForFont)

    def _get_renderingMode(self):
        return self.nsFont.renderingMode()
    renderingMode = property(_get_renderingMode)

    # Font metrics, based on self.nsFont. This can be different from
    # self.fontAscencender and self.fontDescender, etc. which are based on the
    # current setting in the FormattedString.

    def _get_ascender(self):
        fontSize = self.nsFont.pointSize()
        return em(self.nsFont.ascender()/fontSize, base=fontSize)
    ascender = property(_get_ascender)

    def _get_descender(self):
        fontSize = self.nsFont.pointSize()
        return em(self.nsFont.descender()/fontSize, base=fontSize)
    descender = property(_get_descender)

    def _get_capHeight(self):
        fontSize = self.nsFont.pointSize()
        return em(self.nsFont.capHeight()/fontSize, base=fontSize)
    capHeight = property(_get_capHeight)

    def _get_xHeight(self):
        fontSize = self.nsFont.pointSize()
        return em(self.nsFont.xHeight()/fontSize, base=fontSize)
    xHeight = property(_get_xHeight)

    def _get_italicAngle(self):
        return self.nsFont.italicAngle()
    italicAngle = property(_get_italicAngle)

    def _get_fontSize(self):
        return pt(self.nsFont.pointSize())
    fontSize = property(_get_fontSize)

    #def _get_leading(self):
    #    return self.nsFont.leading()
    #leading = property(_get_leading)

    def _get_fontMatrix(self):
        return self.nsFont.matrix()
    fontMatrix = property(_get_fontMatrix)

    def _get_textTransform(self):
        return self.nsFont.textTransform()
    textTransform = property(_get_textTransform)

    def _get_underlinePosition(self):
        fontSize = self.nsFont.pointSize()
        return em(self.nsFont.underlinePosition()/fontSize, base=fontSize)
    underlinePosition = property(_get_underlinePosition)

    def _get_underlineThickness(self):
        fontSize = self.nsFont.pointSize()
        return em(self.nsFont.underlineThickness()/fontSize, base=fontSize)
    underlineThickness = property(_get_underlineThickness)

    #   Paragraph attributes

    def _get_matrix(self):
        return CTRunGetTextMatrix(self._ctRun)
    matrix = property(_get_matrix)

    def _get_alignment(self):
        return self.nsParagraphStyle.alignment()
    alignment = property(_get_alignment)

    def _get_lineSpacing(self):
        fontSize = self.nsFont.pointSize()
        return em(self.nsParagraphStyle.lineSpacing()/fontSize, base=fontSize)
    lineSpacing = property(_get_lineSpacing)

    def _get_paragraphSpacing(self):
        fontSize = self.nsFont.pointSize()
        return em(self.nsParagraphStyle.paragraphSpacing()/fontSize, base=fontSize)
    paragraphSpacing = property(_get_paragraphSpacing)

    def _get_paragraphSpacingBefore(self):
        fontSize = self.nsFont.pointSize()
        return em(self.nsParagraphStyle.paragraphSpacingBefore()/fontSize, base=fontSize)
    paragraphSpacingBefore = property(_get_paragraphSpacingBefore)

    def _get_headIndent(self):
        fontSize = self.nsFont.pointSize()
        return em(self.nsParagraphStyle.headIndent()/fontSize, base=fontSize)
    headIndent = property(_get_headIndent)

    def _get_tailIndent(self):
        fontSize = self.nsFont.pointSize()
        return em(self.nsParagraphStyle.tailIndent()/fontSize, base=fontSize)
    tailIndent = property(_get_tailIndent)

    def _get_firstLineHeadIndent(self):
        fontSize = self.nsFont.pointSize()
        return em(self.nsParagraphStyle.firstLineHeadIndent()/fontSize, base=fontSize)
    firstLineHeadIndent = property(_get_firstLineHeadIndent)

    def _get_lineHeightMultiple(self):
        fontSize = self.nsFont.pointSize()
        return em(self.nsParagraphStyle.lineHeightMultiple()/fontSize, base=fontSize)
    lineHeightMultiple = property(_get_lineHeightMultiple)

    def _get_maximumLineHeight(self):
        fontSize = self.nsFont.pointSize()
        return em(self.nsParagraphStyle.maximumLineHeight()/fontSize, base=fontSize)
    maximumLineHeight = leading = property(_get_maximumLineHeight)

    def _get_minimumLineHeight(self):
        fontSize = self.nsFont.pointSize()
        return em(self.nsParagraphStyle.minimumLineHeight()/fontSize, base=fontSize)
    minimumLineHeight = property(_get_minimumLineHeight)
