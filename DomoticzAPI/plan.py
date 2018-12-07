#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Domoticz (Room)Plan class
"""
from .server import Server
from .api import API


class Plan:

    _type_plans = "plans"

    # _param_get_plan_devices = "getplandevices"

    def __init__(self, server, idx):
        if isinstance(server, Server) and server.exists():
            self._server = server
        else:
            self._server = None
        self._api = self._server.api
        self._idx = idx
        self._initPlan()

    def __str__(self):
        return "{}({}, {}: \"{}\")".format(self.__class__.__name__, str(self._server), self._idx, self._Name)

    # ..........................................................................
    # Private methods
    # ..........................................................................

    def _initPlan(self):
        myDict = {}
        if self._server is not None:
            # /json.htm?type=plans
            self._api.querystring = self._api.TYPE.format(self._type_plans)
            self._api.call()
            if self._api.status == self._api.OK:
                if self._api.result:
                    for resDict in self._api.result:
                        if self._idx is not None and int(resDict.get("idx")) == self._idx:
                            myDict = resDict
                            break
        self._idx = myDict.get("idx")
        self._Devices = myDict.get("Devices")
        self._Name = myDict.get("Name")
        self._Order = myDict.get("Order")

    # ..........................................................................
    # Public methods
    # ..........................................................................
    def exists(self):
        return self._idx is not None and self._Name is not None

    # ..........................................................................
    # Properties
    # ..........................................................................
    @property
    def devices(self):
        return self._Devices

    @property
    def idx(self):
        return self._idx

    @property
    def name(self):
        return self._Name

    @property
    def order(self):
        return self._Order

    @property
    def server(self):
        return self._server
