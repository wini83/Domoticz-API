#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ast import literal_eval

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


class Color:
    # Color Modes
    MODE_NONE = 0  # Illegal
    MODE_WHITE = 1  # White. Valid fields: none
    MODE_TEMP = 2  # White with color temperature. Valid fields: t
    MODE_RGB = 3  # Color. Valid fields: r, g, b.
    # Custom (color + white). Valid fields: r, g, b, cw, ww, depending on device capabilities
    MODE_CUSTOM = 4
    #
    _ColorModeFirst = MODE_NONE
    _ColorModeLast = MODE_CUSTOM

    def __init__(self, **kwargs):
        self._m = 0
        self._t = 0
        self._r = 0
        self._g = 0
        self._b = 0
        self._cw = 0
        self._ww = 0
        myDict = literal_eval(kwargs.get("color"))
        #  myDict = kwargs.get("color")
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

    def __str__(self):
        return "{}(m: {}, t: {}, r: {}, g: {}, b: {}, cw: {}, ww: {})".format(self.__class__.__name__,
                                                                              self._m,
                                                                              self._t,
                                                                              self._r,
                                                                              self._g,
                                                                              self._b,
                                                                              self._cw,
                                                                              self._ww
                                                                              )

    # ..........................................................................
    # Private methods
    # ..........................................................................
    def _minmax(self, v):
        return int(min(max(v, 0), 255))

    # ..........................................................................
    # Public methods
    # ..........................................................................

   # ..........................................................................
    # Properties
    # ..........................................................................

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
            self._m = self.MODE_NONE
        if self._m == self.MODE_NONE or self._m == self.MODE_WHITE:
            self._t = 0
            self._r = 0
            self._g = 0
            self._b = 0
            self._cw = 0
            self._ww = 0
        elif self._m == self.MODE_TEMP:
            self._r = 0
            self._g = 0
            self._b = 0
            self._cw = 0
            self._ww = 0
        elif self._m == self.MODE_RGB:
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
        if self._m == self.MODE_TEMP:
            self._t = self._minmax(temperature)
        else:
            self._t = 0

    @property
    def r(self):
        return self._r

    @r.setter
    def r(self, red):
        if self._m in (self.MODE_RGB, self.MODE_CUSTOM):
            self._r = self._minmax(red)
        else:
            self._r = 0

    @property
    def g(self):
        return self._g

    @g.setter
    def g(self, green):
        if self._m in (self.MODE_RGB, self.MODE_CUSTOM):
            self._g = self._minmax(green)
        else:
            self._g = 0

    @property
    def b(self):
        return self._b

    @b.setter
    def b(self, blue):
        if self._m in (self.MODE_RGB, self.MODE_CUSTOM):
            self._b = self._minmax(blue)
        else:
            self._b = 0

    @property
    def cw(self):
        return self._cw

    @cw.setter
    def cw(self, cold):
        if self._m == self.MODE_CUSTOM:
            self._cw = self._minmax(cold)
        else:
            self._cw = 0

    @property
    def ww(self):
        return self._ww

    @ww.setter
    def ww(self, warm):
        if self._m == self.MODE_CUSTOM:
            self._ww = self._minmax(warm)
        else:
            self._ww = 0
