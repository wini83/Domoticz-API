#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .settings import Settings
import urllib.request as request
import urllib.parse as parse


class Setting:

    _type_settings = "settings"

    _url = "storesettings.webem"

    def __init__(self, server):
        """Settings class, to get Domoticz settings

        Args:
            server (:obj:`Server`): Domoticz server object where to maintain the device            
        """
        self._server = server

    def __str__(self):
        txt = "{}(\"{}\")".format(self.__class__.__name__, self._server)
        return txt

    # ..........................................................................
    # Public methods
    # ..........................................................................
    def get_value(self, key):
        """Retrieve the value from a Domoticz setting

        Args:
            key (str): key from a setting, eg. "AcceptNewHardware", "SecPassword", etc
        """
        # Requery settings
        # /json.htm?type=settings
        # Not required yet. Perhaps in the near future to be sure that ALL setting are available for use.
        if key in Settings.KEYS:
            self._settings = {}
            if self._server.exists():
                self._server._api.querystring = "type={}".format(
                    self._type_settings)
                self._server._api.call()
                return self._server._api.data.get(key)
            else:
                return None
        else:
            return None

    def set_value(self, key, value):
        if key in Settings.KEYS:
            url = "{}{}".format(
                self._server._api.endpoint,
                self._url
            )
            d = {}
            d[key] = value
            data = parse.urlencode(d).encode("utf-8")
            req = request.Request(url, data=data)
            resp = request.urlopen(req)
