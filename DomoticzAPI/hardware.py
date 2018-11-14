#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from urllib.parse import quote

"""
    Hardware
"""


class Hardware:
    """
    The Hardware class represents the Domoticz hardware
    """
    _type_hardware = "hardware"

    _param_add_hardware = "addhardware"
    _param_delete_hardware = "deletehardware"
    _param_update_hardware = "updatehardware"

    _htype_dummy = 15
    _htype_python_plugin = 94

    # def __init__(self, server, idx):
    def __init__(self, server, *args, **kwargs):
        self._api_status = ""
        self._api_title = ""
        self._api_querystring = ""
        self._Address = None
        self._DataTimeout = 0
        self._Enabled = "true"
        self._Extra = None
        self._HardwareType = None
        self._idx = None
        self._Mode1 = None
        self._Mode2 = None
        self._Mode3 = None
        self._Mode4 = None
        self._Mode5 = None
        self._Mode6 = None
        self._Name = None
        self._Password = None
        self._Port = None
        self._server = server
        self._SerialPort = None
        self._Type = None
        self._Username = None
        if len(args) == 1:
            # For existing hardware
            #   hw = dom.Hardware(server, 180)
            self._idx = args[0]
        else:
            if self._idx is None:
                # For existing hardware
                #   hw = dom.Hardware(server, idx=180)
                idx = kwargs.get("idx", None)
                self._idx = int(idx) if idx is not None else None
                if self.idx is None:
                    # For new hardware
                    #   hw = dom.Hardware(server, type=15, port=1, name="Sensors1", enabled="true")
                    self.address = kwargs.get("address", None)
                    self.datatimeout = kwargs.get("datatimeout", 0)
                    self.enabled = kwargs.get("enabled", "true")
                    self.extra = kwargs.get("extra", None)
                    self.mode1 = kwargs.get("mode1", None)
                    self.mode2 = kwargs.get("mode2", None)
                    self.mode3 = kwargs.get("mode3", None)
                    self.mode4 = kwargs.get("mode4", None)
                    self.mode5 = kwargs.get("mode5", None)
                    self.mode6 = kwargs.get("mode6", None)
                    self.name = kwargs.get("name", None)
                    self.password = kwargs.get("password", None)
                    self.port = kwargs.get("port", None)
                    self.serialport = kwargs.get("serialport", None)
                    self.type = kwargs.get("type", None)
                    self.username = kwargs.get("username", None)
        if self._idx is not None:
            self._initHardware()

    def __str__(self):
        return "{}({}, {}: \"{}\", {})".format(self.__class__.__name__, str(self.server), self.idx, self.name,
                                               self.type)

    # ..........................................................................
    # Private methods
    # ..........................................................................

    def _initHardware(self):
        querystring = "type={}".format(self._type_hardware)
        self._api_querystring = querystring
        res = self._server._call_api(querystring)
        self._set_status(res)
        result = res.get("result")
        myDict = {}
        if len(result) > 0:
            for myDict in result:
                if myDict.get("idx") == str(self._idx):
                    break
        self.address = myDict.get("Address")
        self.datatimeout = myDict.get("DataTimeout")
        self.enabled = myDict.get("Enabled")
        self.extra = myDict.get("Extra")
        self.mode1 = myDict.get("Mode1")
        self.mode2 = myDict.get("Mode2")
        self.mode3 = myDict.get("Mode3")
        self.mode4 = myDict.get("Mode4")
        self.mode5 = myDict.get("Mode5")
        self.mode6 = myDict.get("Mode6")
        self.name = myDict.get("Name")
        self.password = myDict.get("Password")
        self.port = myDict.get("Port")
        self.serialport = myDict.get("SerialPort")
        self.type = myDict.get("Type")
        self.username = myDict.get("Username")

    def _set_status(self, r):
        self._api_status = r.get("status", self._server._return_error)
        self._api_title = r.get("title", self._server._return_empty)
        self._api_message = r.get("message", self._server._return_empty)

    # ..........................................................................
    # Public methods
    # ..........................................................................

    def exists(self):
        return self._idx is not None and self._Name is not None

    def add(self):
        self._api_querystring = self._server._return_empty
        self._api_title = self._server._return_empty
        self._api_status = self._server._return_error
        # At least Name and Type are required
        if self._idx is None and self._Name is not None and self._Type is not None:
            # Currently only Dummy device is allowed to create
            if self._Type == self._htype_dummy:
                querystring = "param={}".format(self._param_add_hardware)
                querystring += "&address={}".format(self._Address) if self._Address is not None else ""
                querystring += "&datatimeout={}".format(self._DataTimeout)
                querystring += "&enabled={}".format(self._Enabled)
                querystring += "&extra={}".format(self._Extra) if self._Extra is not None else ""
                querystring += "&htype={}".format(self._Type)
                querystring += "&Mode1={}".format(self._Mode1) if self._Mode1 is not None else ""
                querystring += "&Mode2={}".format(self._Mode2) if self._Mode2 is not None else ""
                querystring += "&Mode3={}".format(self._Mode3) if self._Mode3 is not None else ""
                querystring += "&Mode4={}".format(self._Mode4) if self._Mode4 is not None else ""
                querystring += "&Mode5={}".format(self._Mode5) if self._Mode5 is not None else ""
                querystring += "&Mode6={}".format(self._Mode6) if self._Mode6 is not None else ""
                querystring += "&name={}".format(quote(self._Name))
                querystring += "&password={}".format(self._Password) if self._Password is not None else ""
                querystring += "&port={}".format(self._Port) if self._Port is not None else ""
                querystring += "&serialport={}".format(self._SerialPort) if self._SerialPort is not None else ""
                querystring += "&username={}".format(self._Username) if self._Username is not None else ""
                self._api_querystring = querystring
                res = self._server._call_command(querystring)
                self._set_status(res)
                if self._api_status == self._server._return_ok:
                    self._idx = int(res.get("idx"))
                    self._initHardware()

    def add_virtual(self):
        self._Type = self._htype_dummy
        self.add()

    def delete(self):
        self._api_querystring = self._server._return_empty
        self._api_title = self._server._return_empty
        self._api_status = self._server._return_error
        if self.exists():
            querystring = "param={}".format(self._param_delete_hardware)
            querystring += "&idx={}".format(self.idx)
            self._api_querystring = querystring
            res = self._server._call_command(querystring)
            self._set_status(res)
            if self._api_status == self._server._return_ok:
                self._idx = None

    def isDummy(self):
        return self._Type == self._htype_dummy

    def isPythonPlugin(self):
        return self._Type == self._htype_python_plugin

    def update(self):
        # json.htm?type=command&param=updatehardware&htype=94&idx=idx
        if self.exists():
            querystring = "param={}".format(self._param_update_hardware)
            querystring += "&idx={}".format(self._idx)
            querystring += "&address={}".format(self._Address) if self._Address is not None else ""
            querystring += "&datatimeout={}".format(self._DataTimeout)
            querystring += "&enabled={}".format(self._Enabled)
            querystring += "&extra={}".format(self._Extra) if self._Extra is not None else ""
            if self._Type == self._htype_dummy:
                querystring += "&htype={}".format(self._Type)
            querystring += "&Mode1={}".format(self._Mode1) if self._Mode1 is not None else ""
            querystring += "&Mode2={}".format(self._Mode2) if self._Mode2 is not None else ""
            querystring += "&Mode3={}".format(self._Mode3) if self._Mode3 is not None else ""
            querystring += "&Mode4={}".format(self._Mode4) if self._Mode4 is not None else ""
            querystring += "&Mode5={}".format(self._Mode5) if self._Mode5 is not None else ""
            querystring += "&Mode6={}".format(self._Mode6) if self._Mode6 is not None else ""
            querystring += "&name={}".format(quote(self._Name))
            querystring += "&password={}".format(self._Password) if self._Password is not None else ""
            querystring += "&port={}".format(self._Port) if self._Port is not None else ""
            querystring += "&serialport={}".format(self._SerialPort) if self._SerialPort is not None else ""
            querystring += "&username={}".format(self._Username) if self._Username is not None else ""
            self._api_querystring = querystring
            res = self._server._call_command(querystring)
            self._set_status(res)

    # **************************************************************************
    # Properties
    # **************************************************************************

    @property
    def address(self):
        return self._Address

    @address.setter
    def address(self, value):
        self._Address = str(value) if value is not None else None

    @property
    def api_message(self):
        return self._api_message

    @property
    def api_status(self):
        return self._api_status

    @property
    def api_title(self):
        return self._api_title

    @property
    def api_querystring(self):
        return self._api_querystring

    @property
    def datatimeout(self):
        return int(self._DataTimeout)

    @datatimeout.setter
    def datatimeout(self, value):
        self._DataTimeout = int(value)

    @property
    def enabled(self):
        return self._Enabled

    @enabled.setter
    def enabled(self, value):
        if str(value) in ("true", "false"):
            self._Enabled = value

    @property
    def extra(self):
        return self._Extra

    @extra.setter
    def extra(self, value):
        self._Extra = str(value) if value is not None else None

    @property
    # In / json.htm?type = devices: HardwareID
    def idx(self):
        return self._idx

    @property
    def mode1(self):
        return self._Mode1

    @mode1.setter
    def mode1(self, value):
        self._Mode1 = str(value) if value is not None else None

    @property
    def mode2(self):
        return self._Mode2

    @mode2.setter
    def mode2(self, value):
        self._Mode2 = str(value) if value is not None else None

    @property
    def mode3(self):
        return self._Mode3

    @mode3.setter
    def mode3(self, value):
        self._Mode3 = str(value) if value is not None else None

    @property
    def mode4(self):
        return self._Mode4

    @mode4.setter
    def mode4(self, value):
        self._Mode4 = str(value) if value is not None else None

    @property
    def mode5(self):
        return self._Mode5

    @mode5.setter
    def mode5(self, value):
        self._Mode5 = str(value) if value is not None else None

    @property
    def mode6(self):
        return self._Mode6

    @mode6.setter
    def mode6(self, value):
        self._Mode6 = str(value) if value is not None else None

    @property
    # In / json.htm?type = devices: HardwareName
    def name(self):
        return self._Name

    @name.setter
    def name(self, value):
        self._Name = str(value)

    @property
    def password(self):
        return self._Password

    @password.setter
    def password(self, value):
        self._Password = str(value) if value is not None else None

    @property
    def port(self):
        return self._Port

    @port.setter
    def port(self, value):
        self._Port = int(value) if value is not None else None

    @property
    def serialport(self):
        return self._SerialPort

    @serialport.setter
    def serialport(self, value):
        self._SerialPort = str(value) if value is not None else None

    @property
    def server(self):
        return self._server

    @property
    # In /json.htm?type=devices: HardwareTypeVal
    def type(self):
        return self._Type

    @type.setter
    def type(self, value):
        self._Type = int(value) if value is not None else None

    @property
    # For some reason, this value is only returned in eg. /json.htm?type=devices
    def type_description(self):
        return self._HardwareType

    @property
    def username(self):
        return self._Username

    @username.setter
    def username(self, value):
        self._Username = str(value) if value is not None else None
