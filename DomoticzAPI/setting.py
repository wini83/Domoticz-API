#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json


class Setting:

    _type_settings = "settings"

    SETTING_AUTHENTICATION_METHOD_LOGIN_PAGE = 0
    SETTING_AUTHENTICATION_METHOD_BASIC_AUTH = 1
    SETTING_AUTHENTICATION_METHODS = [
        SETTING_AUTHENTICATION_METHOD_LOGIN_PAGE,
        SETTING_AUTHENTICATION_METHOD_BASIC_AUTH,
    ]

    SETTING_CHECKBOX_UNCHECKED = 0
    SETTING_CHECKBOX_CHECKED = 1
    SETTING_CHECKBOX_VALUES = [
        SETTING_CHECKBOX_UNCHECKED,
        SETTING_CHECKBOX_CHECKED,
    ]

    SETTING_CM113_DISPLAY_TYPE_AMPERE = 0
    SETTING_CM113_DISPLAY_TYPE_WATT = 1
    SETTING_CM113_DISPLAY_TYPES = [
        SETTING_CM113_DISPLAY_TYPE_AMPERE,
        SETTING_CM113_DISPLAY_TYPE_WATT,
    ]

    SETTTING_DASHBOARD_TYPE_NORMAL = 0
    SETTTING_DASHBOARD_TYPE_COMPACT = 1
    SETTTING_DASHBOARD_TYPE_MOBILE = 2
    SETTTING_DASHBOARD_TYPE_FLOORPLAN = 3
    SETTTING_DASHBOARD_TYPES = [
        SETTTING_DASHBOARD_TYPE_NORMAL,
        SETTTING_DASHBOARD_TYPE_COMPACT,
        SETTTING_DASHBOARD_TYPE_MOBILE,
        SETTTING_DASHBOARD_TYPE_FLOORPLAN,
    ]

    SETTING_MOBILE_TYPE_MOBILE = 0
    SETTING_MOBILE_TYPE_DASHBOARD = 1
    SETTING_MOBILE_TYPES = [
        SETTING_MOBILE_TYPE_MOBILE,
        SETTING_MOBILE_TYPE_DASHBOARD,
    ]

    SETTING_SMARTMETER_TYPE_WITH_DECIMALS = 0
    SETTING_SMARTMETER_TYPE_NO_DECIMALS = 1
    SETTING_SMARTMETER_TYPES = [
        SETTING_SMARTMETER_TYPE_WITH_DECIMALS,
        SETTING_SMARTMETER_TYPE_NO_DECIMALS,
    ]

    SETTING_TEMP_UNIT_CELSIUS = 0
    SETTING_TEMP_UNIT_FAHRENHEIT = 1
    SETTING_TEMP_UNITS = [
        SETTING_TEMP_UNIT_CELSIUS,
        SETTING_TEMP_UNIT_FAHRENHEIT,
    ]

    SETTING_WEIGHT_UNIT_KILOGRAMS = 0
    SETTING_WEIGHT_UNIT_POUNDS = 1
    SETTING_WEIGHT_UNITS = [
        SETTING_WEIGHT_UNIT_KILOGRAMS,
        SETTING_WEIGHT_UNIT_POUNDS,
    ]

    SETTING_WIND_UNIT_MS = 0
    SETTING_WIND_UNIT_KMH = 1
    SETTING_WIND_UNIT_MPH = 2
    SETTING_WIND_UNIT_KNOTS = 3
    SETTING_WIND_UNIT_BEAUFORT = 4
    SETTING_WIND_UNITS = [
        SETTING_WIND_UNIT_MS,
        SETTING_WIND_UNIT_KMH,
        SETTING_WIND_UNIT_MPH,
        SETTING_WIND_UNIT_KNOTS,
        SETTING_WIND_UNIT_BEAUFORT,
    ]

    def __init__(self, server):
        self._settings = {}
        self._server = server
        self._getSettings()

    def __str__(self):
        txt = "{}(\"{}\")".format(self.__class__.__name__, self._server)
        return txt

    # ..........................................................................
    # Private methods
    # ..........................................................................
    def _getSettings(self):
        # /json.htm?type=settings
        # Not required yet. Perhaps in the near future to be sure that ALL setting are available for use.
        self._server._api.querystring = "type={}".format(self._type_settings)
        self._server._api.call()
        if self._server._api.status == self._server._api.OK:
            self._settings = self._server._api.data
        else:
            self._settings = {}

    # ..........................................................................
    # Public method
    # ..........................................................................
    def value(self, key):
        if key not in (self._server._api.STATUS, self._server._api.TITLE):
            return self._settings.get(key)
        else:
            return None
