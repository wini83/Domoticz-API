#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Domoticz Color class

    Domoticz color format:

    Example: color={"m":3,"t":0,"r":0,"g":0,"b":50,"cw":0,"ww":0}

        Color {
          m:  # Above color mode 0 .. 4
          t:  # Range: 0 .. 255, Color temperature (warm / cold ratio, 0 is coldest, 255 is warmest)
          r:  # Range: 0 .. 255, Red level
          g:  # Range: 0 .. 255, Green level
          b:  # Range: 0 .. 255, Blue level
          cw: # Range: 0 .. 255, Cold white level
          ww: # Range: 0 .. 255, Warm white level (also used as level for monochrome white)
        }
"""
import ast


class Color:
    # Color Modes
    _ColorModeNone = 0  # Illegal
    _ColorModeWhite = 1  # White. Valid fields: none
    _ColorModeTemp = 2  # White with color temperature. Valid fields: t
    _ColorModeRGB = 3  # Color. Valid fields: r, g, b.
    _ColorModeCustom = 4  # Custom (color + white). Valid fields: r, g, b, cw, ww, depending on device capabilities
    _ColorModeFirst = _ColorModeNone
    _ColorModeLast = _ColorModeCustom

    def __init__(self, **kwargs):
        self._m = 0
        self._t = 0
        self._r = 0
        self._g = 0
        self._b = 0
        self._cw = 0
        self._ww = 0
        myDict = ast.literal_eval(kwargs.get("color"))
        if myDict is not None:
            self.m = myDict.get("m", 0)
            self.t = myDict.get("t", 0)
            self.r = myDict.get("r", 0)
            self.g = myDict.get("g", 0)
            self.b = myDict.get("b", 0)
            self.cw = myDict.get("cw", 0)
            self.ww = myDict.get("ww", 0)
        else:
            self.m = kwargs.get("m", 0)
            self.t = kwargs.get("t", 0)
            self.r = kwargs.get("r", 0)
            self.g = kwargs.get("g", 0)
            self.b = kwargs.get("b", 0)
            self.cw = kwargs.get("cw", 0)
            self.ww = kwargs.get("ww", 0)

    @property
    def color(self):
        return "{" + "\"m\":{},\"t\":{},\"r\":{},\"g\":{},\"b\":{},\"cw\":{},\"ww\":{}".format(self._m,
                                                                                               self._t,
                                                                                               self._r,
                                                                                               self._g,
                                                                                               self._b,
                                                                                               self._cw,
                                                                                               self._ww) + "}"

    @property
    def m(self):
        return self._m

    @m.setter
    def m(self, mode):
        if mode >= self._ColorModeFirst and mode <= self._ColorModeLast:
            self._m = int(mode)
        else:
            self._m = self._ColorModeNone
        if self._m == self._ColorModeNone or self._m == self._ColorModeWhite:
            self._t = 0
            self._r = 0
            self._g = 0
            self._b = 0
            self._cw = 0
            self._ww = 0
        elif self._m == self._ColorModeTemp:
            self._r = 0
            self._g = 0
            self._b = 0
            self._cw = 0
            self._ww = 0
        elif self._m == self._ColorModeRGB:
            self._t = 0
            self._cw = 0
            self._ww = 0
        else:
            self._t = 0

    @property
    def t(self):
        return self._t

    @t.setter
    def t(self, temperature):
        if self._m == self._ColorModeTemp and 0 <= temperature <= 255:
            self._t = int(temperature)
        else:
            self._t = 0

    @property
    def r(self):
        return self._r

    @r.setter
    def r(self, red):
        if self._m in (self._ColorModeRGB, self._ColorModeCustom) and 0 <= red <= 255:
            self._r = int(red)
        else:
            self._r = 0

    @property
    def g(self):
        return self._g

    @g.setter
    def g(self, green):
        if self._m in (self._ColorModeRGB, self._ColorModeCustom) and 0 <= green <= 255:
            self._g = int(green)
        else:
            self._g = 0

    @property
    def b(self):
        return self._b

    @b.setter
    def b(self, blue):
        if self._m in (self._ColorModeRGB, self._ColorModeCustom) and 0 <= blue <= 255:
            self._b = int(blue)
        else:
            self._b = 0

    @property
    def cw(self):
        return self._cw

    @cw.setter
    def cw(self, cold):
        if self._m == self._ColorModeCustom and 0 <= cold <= 255:
            self._cw = int(cold)
        else:
            self._cw = 0

    @property
    def ww(self):
        return self._ww

    @ww.setter
    def ww(self, warm):
        if self._m == self._ColorModeCustom and 0 <= warm <= 255:
            self._ww = int(warm)
        else:
            self._ww = 0
