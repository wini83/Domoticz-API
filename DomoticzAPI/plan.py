#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .server import Server

"""
    Domoticz (Room)Plan class
"""

class Plan:

    _type_plans = "plans"

    # _param_get_plan_devices = "getplandevices"

    def __init__(self, server, idx):
        if isinstance(server, Server) and server.exists():
            self._server = server
        else:
            self._server = None
        self._idx = idx
        self._initPlan()

    def __str__(self):
        return "{}({}, {}: \"{}\")".format(self.__class__.__name__, str(self._server), self._idx, self._Name)

    # ..........................................................................
    # Private methods
    # ..........................................................................

    def _initPlan(self):
        # /json.htm?type=plans
        querystring = "type={}".format(self._type_plans)
        self._api_querystring = querystring
        res = self._server._call_api(querystring)
        self._set_status(res)
        myDict = {}
        if self._api_status == self._server._return_ok:
            if res.get("result"):
                for resDict in res["result"]:
                    if self._idx is not None and int(resDict.get("idx")) == self._idx:
                        myDict = resDict
                        break
        self._Devices = myDict.get("Devices")
        self._Name = myDict.get("Name")
        self._Order = myDict.get("Order")

    def _set_status(self, r):
        self._api_message = r.get("message", self._server._return_empty)
        self._api_status = r.get("status", self._server._return_error)
        self._api_title = r.get("title", self._server._return_empty)

    # ..........................................................................
    # Public methods
    # ..........................................................................

    # ..........................................................................
    # Properties
    # ..........................................................................

    @property
    def api_message(self):
        return self._api_message

    @property
    def api_querystring(self):
        return self._api_querystring

    @property
    def api_status(self):
        return self._api_status

    @property
    def api_title(self):
        return self._api_title

    @property
    def idx(self):
        return self._idx

    @property
    def devices(self):
        return self._Devices

    @property
    def name(self):
        return self._Name

    @property
    def order(self):
        return self._Order

    @property
    def server(self):
        return self._server
