#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .server import *
from .hardware import *
import datetime
from urllib.parse import quote
'''
    Device class
'''

class Device:

    _type_devices = "devices"
    _type_create_device = "createdevice"
    _type_create_dummy = "createvirtualsensor"
    _type_delete_device = "deletedevice"
    _type_set_used = "setused"

    _param_make_favorite = "makefavorite"
    _param_rename_device = "renamedevice"
    _param_update_device = "udevice"

    _int_value_off = 0
    _int_value_on = 1

    def __init__(self, server, *args, **kwargs):
        self._idx = None
        self._Hardware = None
        self._Name = None
        self._Type = None
        self._SubType = None
        self._TypeName = None
        self._htype = None
        if isinstance(server, Server) and server.exists():
            self._server = server
        else:
            self._server = None
        # Existing device: def __init__(self, server, idx)
        if len(args) == 1:
            # For existing device
            #   hw = dom.Device(server, 180)
            self._idx = args[0]
        # New device:      def __init__(self, server, hardware, name, type=None, subtype=None):
        elif len(args) == 2:
            self._idx = None
            if isinstance(args[0], Hardware):
                if args[0].exists():
                    self._Hardware = args[0]
            else:
                self._Hardware = None
            self._Name = args[1]
            # Try to get named parameters
            self._SubType = kwargs.get("subtype", None)
            self._Type = kwargs.get("type", None)
            self._TypeName = kwargs.get("typename", None)
        else:
            self._idx = kwargs.get("idx", None)
            if self._idx is None:
                self._Hardware = kwargs.get("hardware", None)
                self._Name = kwargs.get("name", None)
                self._SubType = kwargs.get("subtype", None)
                self._Type = kwargs.get("type", None)
                self._TypeName = kwargs.get("typename", None)
        if self._TypeName is not None:
            self._Type = None
            self._SubType = None
        self._initDevice()

    def __str__(self):
        return "{}({}, {}: \"{}\")".format(self.__class__.__name__, str(self._server), self._idx, self._Name)

    # ..........................................................................
    # Private methods
    # ..........................................................................

    def _initDevice(self):
        if self._idx is not None:
            querystring = "type=devices&rid={}".format(self._idx)
        elif self._Name is not None:
            querystring = "type=devices&filter=all&used=true&order=Name"
        else:
            querystring = ""
        self._api_querystring = querystring
        res = self._server._call_api(querystring)
        self._api_status = res.get("status", self._server._return_error)
        self._api_title = res.get("title", self._server._return_empty)
        myDict = {}
        if self._api_status == self._server._return_ok:
            self._server._ActTime = res.get("ActTime")  # for some reason only given in device calls. No idea about the meaning!
            # Update the server properties.
            self._server._AstrTwilightEnd = res.get("AstrTwilightEnd")
            self._server._AstrTwilightStart = res.get("AstrTwilightStart")
            self._server._CivTwilightEnd = res.get("CivTwilightEnd")
            self._server._CivTwilightStart = res.get("CivTwilightStart")
            self._server._NautTwilightEnd = res.get("NautTwilightEnd")
            self._server._NautTwilightStart = res.get("NautTwilightStart")
            self._server._Sunrise = res.get("Sunrise")
            self._server._Sunset = res.get("Sunset")
            self._server._SunAtSouth = res.get("SunAtSouth")
            self._server._DayLength = res.get("DayLength")
            self._server._ServerTime = res.get("ServerTime")
            result = res.get("result")
            if result is not None:
                if len(result) > 0:
                    for resDict in result:
                        if (self._idx is not None and resDict.get("idx") == self._idx) \
                        or (self._Name is not None and resDict.get("Name") == self._Name):
                            myDict = resDict
                            break
        self._AddjMulti = myDict.get("AddjMulti")
        self._AddjMulti2 = myDict.get("AddjMulti2")
        self._AddjValue = myDict.get("AddjValue")
        self._AddjValue2 = myDict.get("AddjValue2")
        self._BatteryLevel = myDict.get("BatteryLevel", 255)
        self._CounterToday = myDict.get("CounterToday")
        self._CustomImage = myDict.get("CustomImage")
        self._Data = myDict.get("Data")
        self._Description = myDict.get("Description")
        self._DimmerType = myDict.get("DimmerType")
        self._Favorite = myDict.get("Favorite")
        self._HaveDimmer = myDict.get("HaveDimmer")
        self._HaveGroupCmd = myDict.get("HaveGroupCmd")
        self._HaveTimeout = myDict.get("HaveTimeout")
        self._Humidity = myDict.get("Humidity")
        self._ID = myDict.get("ID")
        self._idx = myDict.get("idx", self._idx)
        self._Image = myDict.get("Image")
        self._InternalState = myDict.get("InternalState")
        self._IsSubDevice = myDict.get("IsSubDevice")
        self._LastUpdate = myDict.get("LastUpdate")
        self._Level = myDict.get("Level")
        self._LevelInt = myDict.get("LevelInt")
        self._MaxDimLevel = myDict.get("MaxDimLevel")
        self._Name = myDict.get("Name", self._Name)
        self._Notifications = myDict.get("Notifications")
        self._PlanID = myDict.get("PlanID")
        self._PlanIDs = myDict.get("PlanIDs")
        self._Protected = myDict.get("Protected")
        self._SensorType = myDict.get("SensorType")
        self._SensorUnit = myDict.get("SensorUnit")
        self._ShowNotifications = myDict.get("ShowNotifications")
        self._SignalLevel = myDict.get("SignalLevel")
        self._Status = myDict.get("Status")
        self._StrParam1 = myDict.get("StrParam1")
        self._StrParam2 = myDict.get("StrParam2")
        self._SubType = myDict.get("SubType", self._SubType)
        self._SwitchType = myDict.get("SwitchType")
        self._SwitchTypeVal = myDict.get("SwitchTypeVal")
        self._Temp = myDict.get("Temp")
        self._Timers = myDict.get("Timers")
        self._Type = myDict.get("Type", self._Type)
        self._TypeImg = myDict.get("TypeImg")
        self._Unit = myDict.get("Unit")
        self._Used = myDict.get("Used")
        self._UsedByCamera = myDict.get("UsedByCamera")
        self._Voltage = myDict.get("Voltage")
        self._XOffset = myDict.get("XOffset")
        self._YOffset = myDict.get("YOffset")

        # Some info from the hardware also comes
        HardwareID = myDict.get("HardwareID")
        if HardwareID is not None:
            hw = Hardware(self._server, idx=HardwareID)
            if hw.exists():
                self._Hardware = hw
                # Following 3 values should be in de hardware class
                # self._HardwareName = myDict.get("HardwareName")
                self._Hardware._HardwareType = myDict.get("HardwareType")
                # self._HardwareTypeVal = myDict.get("HardwareTypeVal")
            else:
                self._Hardware = None

    # ..........................................................................
    # Public methods
    # ..........................................................................

    def add(self):
        if self._idx is None \
                and self._Hardware is not None \
                and self._Name is not None \
                and self._Type is not None \
                and self._SubType is not None:
            # type=createdevice&idx=IDX&sensorname=SENSORNAME&devicetype=DEVICETYPE&devicesubtype=SUBTYPE
            querystring = "type={}".format(self._type_create_device)
            querystring += "&idx={}".format(self._Hardware._idx)
            querystring += "&sensorname={}".format(quote(self._Name))
            querystring += "&devicetype={}".format(self._Type)
            querystring += "&devicesubtype={}".format(self._SubType)
            self._api_querystring = querystring
            res = self._server._call_api(querystring)
            self._api_status = res.get("status", self._server._return_error)
            self._api_title = res.get("title", self._server._return_empty)
            if self._api_status == self._server._return_ok:
                self._idx = res.get("idx", None)
                self._initDevice()

    def delete(self):
        if self.exists():
            # type=deletedevice&idx=29
            querystring = "type={}&idx={}".format(self._type_delete_device, self._idx)
            self._api_querystring = querystring
            res = self._server._call_command(querystring)
            self._api_status = res.get("status", self._server._return_error)
            self._api_title = res.get("title", self._server._return_empty)
            if self._api_status == self._server._return_ok:
                # self._Hardware = None
                self._idx = None

    def exists(self):
        return self._idx is not None and self._Hardware is not None

    def hasBattery(self):
        return not (self._BatteryLevel is None or self._BatteryLevel == 255)

    def isDimmer(self):
        return self.isSwitch() and self._SwitchType == "Dimmer"

    def isFavorite(self):
        return not (self._Favorite is None or self._Favorite == 0)

    def isSwitch(self):
        return self._SwitchType is not None

    def isThermometer(self):
        return self._Temp is not None

    def isHygrometer(self):
        return self._Humidity is not None

    def update(self, nvalue=0, svalue=""):
        # /json.htm?type=command&param=udevice&idx=IDX&nvalue=NVALUE&svalue=SVALUE
        if self.exists():
            querystring = "param={}".format(self._param_update_device)
            querystring += "&idx={}".format(self._idx)
            querystring += "&nvalue={}".format(nvalue)
            if len(svalue) > 0:
                querystring += "&svalue={}".format(svalue)
            self._api_querystring = querystring
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

    @property
    def api_querystring(self):
        return self._api_querystring

    # ..........................................................................

    @property
    def addjmulti(self):
        return self._AddjMulti

    @property
    def addjmulti2(self):
        return self._AddjMulti2

    @property
    def addjvalue(self):
        return self._AddjValue

    @property
    def addjvalue2(self):
        return self._AddjValue2

    @property
    def batterylevel(self):
        return self._BatteryLevel

    @property
    def customimage(self):
        return self._CustomImage

    @property
    def data(self):
        return self._Data

    @property
    def description(self):
        return self._Description

    @property
    def dimmertype(self):
        return self._DimmerType

    @property
    # For some reason this attribute in Domoticz is an 'int'. Boolean is more logical.
    def favorite(self):
        if self._Favorite == 1:
            return True
        else:
            return False

    @favorite.setter
    def favorite(self, value):
        # json.htm?type=command&param=makefavorite&idx=" + id + "&isfavorite=" + isfavorite
        if isinstance(value, bool) and self.exists():
            if value:
                int_value = self._int_value_on
            else:
                int_value = self._int_value_off
            querystring = self._server._param.format(self._param_make_favorite)
            querystring += "&idx={}&isfavorite={}".format(self._idx, str(int_value))
            self._api_querystring = querystring
            res = self._server._call_command(querystring)
            self._api_status = res.get("status", self._server._return_error)
            self._api_title = res.get("title", self._server._return_empty)
            if self._api_status == self._server._return_ok:
                self._Favorite = int_value

    @property
    def hardware(self):
        return self._Hardware

    @property
    def havedimmer(self):
        return self._HaveDimmer

    @property
    def havegroupcmd(self):
        return self._HaveGroupCmd

    @property
    def havetimeout(self):
        return self._HaveTimeout

    @property
    def humidity(self):
        return self._Humidity

    @property
    def id(self):
        return self._ID

    @property
    def idx(self):
        return self._idx

    @property
    def image(self):
        return self._Image

    @property
    def internalstate(self):
        return self._InternalState

    @property
    def issubdevice(self):
        return self._IsSubDevice

    @property
    def lastupdate(self):
        return self._LastUpdate

    @property
    def level(self):
        return self._Level

    @property
    def levelint(self):
        return self._LevelInt

    @property
    def maxdimlevel(self):
        return self._MaxDimLevel

    @property
    def name(self):
        return self._Name

    @name.setter
    def name(self, value):
        if self.exists():
            # json.htm?type=command&param=renamedevice&idx=idx&name=
            querystring = self._server._param.format(self._param_rename_device)
            querystring += "&idx={}&name={}".format(self._idx, quote(str(value)))
            self._api_querystring = querystring
            res = self._server._call_command(querystring)
            self._api_status = res.get("status", self._server._return_error)
            self._api_title = res.get("title", self._server._return_empty)
            if self._api_status == self._server._return_ok:
                self._Name = value

    @property
    def notifications(self):
        return self._Notifications

    @property
    def planid(self):
        return self._PlanID

    @property
    def planids(self):
        return self._PlanIDs

    @property
    def protected(self):
        return self._Protected

    @property
    def sensortype(self):
        return self._SensorType

    @property
    def sensorunit(self):
        return self._SensorUnit

    @property
    def shownotifications(self):
        return self._ShowNotifications

    @property
    def signallevel(self):
        return self._SignalLevel

    @property
    def subtype(self):
        return self._SubType

    @property
    def temp(self):
        return self._Temp

    @property
    def timers(self):
        return self._Timers

    @property
    def title(self):
        return self._title

    @property
    def type(self):
        return self._Type

    @property
    def typeimg(self):
        return self._TypeImg

    @property
    def unit(self):
        return self._Unit

    @property
    # For some reason this attribute in Domoticz is an 'int'. Boolean is more logical.
    def used(self):
        if self._Used == 1:
            return True
        else:
            return False

    @used.setter
    def used(self, value):
        # The url needs "true" or "false"!!!
        if isinstance(value, bool) and self.exists():
            if value:
                int_value = self._int_value_on
                str_value = "true"
            else:
                int_value = self._int_value_off
                str_value = "false"
            # json.htm?type=setused&idx=IDX&used=true|false
            querystring = "type={}&idx={}&used={}".format(self._type_set_used, self._idx, str_value)
            self._api_querystring = querystring
            res = self._server._call_api(querystring)
            self._api_status = res.get("status", self._server._return_error)
            self._api_title = res.get("title", self._server._return_empty)
            if self._api_status == self._server._return_ok:
                self._Used = int_value

    @property
    def voltage(self):
        return self._Voltage

    @property
    def xoffset(self):
        return self._XOffset

    @property
    def yoffset(self):
        return self._YOffset

