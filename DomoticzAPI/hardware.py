#!/usr/bin/env python
# -*- coding: utf-8 -*-
from urllib.parse import quote


################################################################################
# Hardware                                                                     #
################################################################################
class Hardware:

    _type_hardware = "hardware"

    _param_add_hardware = "addhardware"
    # https://github.com/domoticz/domoticz/blob/8d290f216e5e25be48178ad30273129d2c84ad69/www/app/HardwareController.js
    _param_delete_hardware = "deletehardware"
    _param_update_hardware = "updatehardware"

    # def __init__(self, server, idx):
    def __init__(self, server, *args, **kwargs):
        self._server = server
        self._idx = None
        self._Address = None
        self._DataTimeout = 0
        self._Enabled = "true"
        self._Extra = None
        self._Mode1 = None
        self._Mode2 = None
        self._Mode3 = None
        self._Mode4 = None
        self._Mode5 = None
        self._Mode6 = None
        self._Name = None
        self._Password = None
        self._Port = None
        self._SerialPort = None
        self._api_status = ""
        self._api_title = ""
        self._Type = None
        self._Username = None
        if len(args) == 1:
            # For existing hardware
            #   hw = dom.Hardware(server, "180")
            self._idx = args[0]
        else:
            # For existing hardware
            #   hw = dom.Hardware(server, idx="180")
            # For new hardware
            #   hw = dom.Hardware(server, Type=15, Port=1, Name="Sensors1", Enabled="true")
            if self._idx is None:
                self._idx = kwargs.get("idx", None)
                if self._idx is None:
                    self._Address = kwargs.get("Address", None)
                    self._DataTimeout = kwargs.get("DataTimeout", 0)
                    self._Enabled = kwargs.get("Enabled", "false")
                    self._Extra = kwargs.get("Extra", None)
                    self._Mode1 = kwargs.get("Mode1", None)
                    self._Mode2 = kwargs.get("Mode2", None)
                    self._Mode3 = kwargs.get("Mode3", None)
                    self._Mode4 = kwargs.get("Mode4", None)
                    self._Mode5 = kwargs.get("Mode5", None)
                    self._Mode6 = kwargs.get("Mode6", None)
                    self._Name = kwargs.get("Name", None)
                    self._Password = kwargs.get("Password", None)
                    self._Port = kwargs.get("Port", None)
                    self._SerialPort = kwargs.get("SerialPort", None)
                    self._Type = kwargs.get("Type", None)
                    self._Username = kwargs.get("Username", None)
        if self._idx is not None:
            self._initHardware()

    def __str__(self):
        return "{}({}, \"{}\", \"{}\")".format(self.__class__.__name__, str(self._server), self._idx, self._Name)

    # ..........................................................................
    # Public methods
    # ..........................................................................
    def exists(self):
        return self._idx is not None and self._Name is not None

    def add(self):
        # At least Name, Type and Enabled are required
        if self._idx is None and self._Name is not None and self._Type is not None:
            querystring = "param={}".format(self._param_add_hardware)
            querystring += "&address={}".format(self._Address)
            querystring += "&datatimeout={}".format(self._DataTimeout)
            querystring += "&enabled={}".format(self._Enabled)
            querystring += "&extra={}".format(self._Extra)
            querystring += "&htype={}".format(self._Type)
            querystring += "&Mode1={}".format(self._Mode1)
            querystring += "&Mode2={}".format(self._Mode2)
            querystring += "&Mode3={}".format(self._Mode3)
            querystring += "&Mode4={}".format(self._Mode4)
            querystring += "&Mode5={}".format(self._Mode5)
            querystring += "&Mode6={}".format(self._Mode6)
            querystring += "&name={}".format(quote(self._Name))
            querystring += "&password={}".format(self._Password)
            querystring += "&port={}".format(self._Port)
            querystring += "&serialport={}".format(self._SerialPort)
            querystring += "&username={}".format(self._Username)
            res = self._server._call_command(querystring)
            self._api_status = res.get("status", self._server._return_error)
            self._api_title = res.get("title", self._server._return_empty)
            if self._api_status == self._server._return_ok:
                self._idx = res.get("idx")
                self._initHardware()

    def delete(self):
        if self.exists():
            querystring = "param={}".format(self._param_delete_hardware)
            querystring += "&idx={}".format(self._idx)
            res = self._server._call_command(querystring)
            self._api_status = res.get("status", self._server._return_error)
            self._api_title = res.get("title", self._server._return_empty)
            if self._api_status == self._server._return_ok:
                self._idx = None

    def update(self):
        # json.htm?type=command&param=updatehardware&htype=94&idx=idx
        if self.exists():
            querystring = "param={}".format(self._param_update_hardware)
            querystring += "&idx={}".format(self._idx)
            querystring += "&address={}".format(self._Address)
            querystring += "&datatimeout={}".format(self._DataTimeout)
            querystring += "&enabled={}".format(self._Enabled)
            querystring += "&extra={}".format(self._Extra)
            querystring += "&htype={}".format(self._Type)
            querystring += "&Mode1={}".format(self._Mode1)
            querystring += "&Mode2={}".format(self._Mode2)
            querystring += "&Mode3={}".format(self._Mode3)
            querystring += "&Mode4={}".format(self._Mode4)
            querystring += "&Mode5={}".format(self._Mode5)
            querystring += "&Mode6={}".format(self._Mode6)
            querystring += "&name={}".format(quote(self._Name))
            querystring += "&password={}".format(self._Password)
            querystring += "&port={}".format(self._Port)
            querystring += "&serialport={}".format(self._SerialPort)
            querystring += "&username={}".format(self._Username)
            res = self._server._call_command(querystring)
            self._api_status = res.get("status", self._server._return_error)
            self._api_title = res.get("title", self._server._return_empty)

    # ..........................................................................
    # Properties
    # ..........................................................................

    @property
    def api_status(self):
        return self._api_status

    @property
    def api_title(self):
        return self._api_title

    # ..........................................................................

    @property
    def address(self):
        return self._Address

    @address.setter
    def address(self, value):
        self._Address = str(value)

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
        self._Extra = str(value)

    @property
    def idx(self):
        return self._idx

    @property
    def mode1(self):
        return self._Mode1

    @mode1.setter
    def mode1(self, value):
        self._Mode1 = str(value)

    @property
    def mode2(self):
        return self._Mode2

    @mode2.setter
    def mode2(self, value):
        self._Mode2 = str(value)

    @property
    def mode3(self):
        return self._Mode3

    @mode3.setter
    def mode3(self, value):
        self._Mode3 = str(value)

    @property
    def mode4(self):
        return self._Mode4

    @mode4.setter
    def mode4(self, value):
        self._Mode4 = str(value)

    @property
    def mode5(self):
        return self._Mode5

    @mode5.setter
    def mode5(self, value):
        self._Mode5 = str(value)

    @property
    def mode6(self):
        return self._Mode6

    @mode6.setter
    def mode6(self, value):
        self._Mode6 = str(value)

    @property
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
        self._Password = str(value)

    @property
    def port(self):
        return self._Port

    @port.setter
    def port(self, value):
        self._Port = int(value)

    @property
    def serialport(self):
        return self._SerialPort

    @serialport.setter
    def serialport(self, value):
        self._SerialPort = str(value)

    @property
    def server(self):
        return self._server

    @property
    def type(self):
        return self._Type

    @type.setter
    def type(self, value):
        self._Type = int(value)

    @property
    def username(self):
        return self._Username

    @username.setter
    def username(self, value):
        self._Username = str(value)

    # ..........................................................................
    # Private methods
    # ..........................................................................
    def _initHardware(self):
        querystring = "type={}".format(self._type_hardware)
        res = self._server._call_api(querystring)
        self._api_status = res.get("status", self._server._return_error)
        self._api_title = res.get("title", self._server._return_empty)
        result = res.get("result")
        if len(result) > 0:
            for myDict in result:
                if myDict.get("idx") == self._idx:
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
                    break
