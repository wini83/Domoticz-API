#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .server import Server
from .api import API


class RoomPlan:
    """
        Domoticz RoomPlan class
    """

    _type_roomplans = "plans"

    # Undocumented API calls
    _param_add_roomplan = "addplan"
    _param_delete_roomplan = "deleteplan"
    _param_update_roomplan = "updateplan" # Only to update the name
    # /json.htm?type=command&param=getunusedplandevices&unique=true (false)
    # /json.htm?type=command&param=addplanactivedevice&idx=IDX&activetype=XXX&activeidx=DEVICEIDX
    # /json.htm?type=command&param=getplandevices&idx=IDX
    # /json.htm?type=command&param=setplandevicecoords&idx=IDX&planidx=PLANIDX&xoffset=XOFFSET&yoffset=YOFFSET&DevSceneType=DEVSCENETYPE
    # /json.htm?type=command&param=deleteallplandevices&idx=IDX
    # /json.htm?type=command&param=changeplanorder&idx=IDX&way=0 (0=up, 1=down)
    # /json.htm?type=command&param=changeplandeviceorder&idx=IDX&planid=PLANID&way=0 (0=up, 1=down)

    def __init__(self, server, **kwargs):
        if isinstance(server, Server) and server.exists():
            self._server = server
        else:
            self._server = None
        self._api = self._server.api
        self._devices = None
        self._idx = kwargs.get("idx")
        self._name = kwargs.get("name")
        self._order = None
        self._init()

    def __str__(self):
        return "{}({}, {}: \"{}\")".format(self.__class__.__name__, str(self._server), self._idx, self._name)

    # ..........................................................................
    # Private methods
    # ..........................................................................

    def _init(self):
        myDict = {}
        if self._server is not None:
            # /json.htm?type=plans
            self._api.querystring = self._api.TYPE.format(self._type_roomplans)
            self._api.call()
            if self._api.status == self._api.OK:
                if self._api.result:
                    for resDict in self._api.result:
                        if self._idx is not None and int(resDict.get("idx")) == self._idx:
                            myDict = resDict
                            break
                        if self._idx is None and resDict.get("Name") == self._name:
                            myDict = resDict
                            break
        self._idx = myDict.get("idx")
        self._devices = myDict.get("Devices")
        self._name = myDict.get("Name", self._name)
        self._order = myDict.get("Order")

    # ..........................................................................
    # Public methods
    # ..........................................................................
    def add(self):
        if self._idx is None and self._name is not None:
            # /json.htm?type=command&param=addplan&name=NAME
            self._api.querystring = "type=command&param={}&name={}".format(
                self._param_add_roomplan,
                self._name)
            self._api.call()
            if self._api.status == self._api.OK:
                self._init()  # Try to get idx? In Domoticz roomplan name is not unique!
    
    def add_device(self, device_idx):
        pass

    def delete(self):
        if self._idx is not None:
            # /json.htm?type=command&param=deleteplan&idx=IDX
            self._api.querystring = "type=command&param={}&idx={}".format(
                self._param_delete_roomplan,
                self._idx)
            self._api.call()
            if self._api.status == self._api.OK:
                self._idx = None
                self._devices = None
                self._name = None
                self._order = None

    def exists(self):
        return self._idx is not None and self._name is not None

    # ..........................................................................
    # Properties
    # ..........................................................................
    @property
    def devices(self):
        """ Number of devices in this roomplan """
        return self._devices

    @property
    def idx(self):
        return self._idx

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if len(value) > 0:
            if self._idx is not None:
                # /json.htm?type=command&param=updateplan&idx=IDX&name=NAME
                self._api.querystring = "type=command&param={}&idx={}&name={}".format(
                    self._param_update_roomplan,
                    self._idx,
                    value)
                self._api.call()
        self._name = value
        self._init()
        
    @property
    def order(self):
        """ 
        Order in list in the GUI. So not relevant to set in this API and useless for this API!

        To set:
            /json.htm?type=command&param=changeplanorder&idx=IDX&way=WAY

        """
        return self._order

    @property
    def server(self):
        return self._server
