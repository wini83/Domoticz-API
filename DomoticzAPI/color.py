#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ast import literal_eval
from .const import(COLOR_MODE_CUSTOM, COLOR_MODE_NONE,
                  COLOR_MODE_RGB, COLOR_MODE_TEMP, COLOR_MODE_WHITE,
                  NUM_MAX, NUM_MIN)

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

    _ColorModeFirst = COLOR_MODE_NONE
    _ColorModeLast = COLOR_MODE_CUSTOM

    def __init__(self, **kwargs):
        self._m = NUM_MIN
        self._t = NUM_MIN
        self._r = NUM_MIN
        self._g = NUM_MIN
        self._b = NUM_MIN
        self._cw = NUM_MIN
        self._ww = NUM_MIN
        myDict = literal_eval(kwargs.get("color"))
        #  myDict = kwargs.get("color")
        if myDict is not None:
            self.m = myDict.get("m", NUM_MIN)
            self.t = myDict.get("t", NUM_MIN)
            self.r = myDict.get("r", NUM_MIN)
            self.g = myDict.get("g", NUM_MIN)
            self.b = myDict.get("b", NUM_MIN)
            self.cw = myDict.get("cw", NUM_MIN)
            self.ww = myDict.get("ww", NUM_MIN)
        else:
            self.m = kwargs.get("m", NUM_MIN)
            self.t = kwargs.get("t", NUM_MIN)
            self.r = kwargs.get("r", NUM_MIN)
            self.g = kwargs.get("g", NUM_MIN)
            self.b = kwargs.get("b", NUM_MIN)
            self.cw = kwargs.get("cw", NUM_MIN)
            self.ww = kwargs.get("ww", NUM_MIN)

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
        return int(min(max(v, NUM_MIN), NUM_MAX))

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
            self._m = COLOR_MODE_NONE
        if self._m == COLOR_MODE_NONE or self._m == COLOR_MODE_WHITE:
            self._t = NUM_MIN
            self._r = NUM_MIN
            self._g = NUM_MIN
            self._b = NUM_MIN
            self._cw = NUM_MIN
            self._ww = NUM_MIN
        elif self._m == COLOR_MODE_TEMP:
            self._r = NUM_MIN
            self._g = NUM_MIN
            self._b = NUM_MIN
            self._cw = NUM_MIN
            self._ww = NUM_MIN
        elif self._m == COLOR_MODE_RGB:
            self._t = NUM_MIN
            self._cw = NUM_MIN
            self._ww = NUM_MIN
        else:
            self._t = NUM_MIN

    @property
    def t(self):
        return self._t

    @t.setter
    def t(self, temperature):
        if self._m == COLOR_MODE_TEMP:
            self._t = self._minmax(temperature)
        else:
            self._t = NUM_MIN

    @property
    def r(self):
        return self._r

    @r.setter
    def r(self, red):
        if self._m in (COLOR_MODE_RGB, COLOR_MODE_CUSTOM):
            self._r = self._minmax(red)
        else:
            self._r = NUM_MIN

    @property
    def g(self):
        return self._g

    @g.setter
    def g(self, green):
        if self._m in (COLOR_MODE_RGB, COLOR_MODE_CUSTOM):
            self._g = self._minmax(green)
        else:
            self._g = NUM_MIN

    @property
    def b(self):
        return self._b

    @b.setter
    def b(self, blue):
        if self._m in (COLOR_MODE_RGB, COLOR_MODE_CUSTOM):
            self._b = self._minmax(blue)
        else:
            self._b = NUM_MIN

    @property
    def cw(self):
        return self._cw

    @cw.setter
    def cw(self, cold):
        if self._m == COLOR_MODE_CUSTOM:
            self._cw = self._minmax(cold)
        else:
            self._cw = NUM_MIN

    @property
    def ww(self):
        return self._ww

    @ww.setter
    def ww(self, warm):
        if self._m == COLOR_MODE_CUSTOM:
            self._ww = self._minmax(warm)
        else:
            self._ww = NUM_MIN
