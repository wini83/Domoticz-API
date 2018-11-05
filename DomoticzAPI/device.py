#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .server import *
from .hardware import *
from .color import *
from urllib.parse import quote

"""
    Device class
"""


class Device:

    _type_devices = "devices"
    _type_create_device = "createdevice"
    _type_create_dummy = "createvirtualsensor"
    _type_delete_device = "deletedevice"
    _type_set_used = "setused"
    _param_make_favorite = "makefavorite"
    _param_rename_device = "renamedevice"
    _param_update_device = "udevice"
    _param_switch_light = "switchlight"
    _param_set_color_brightness = "setcolbrightnessvalue"
    _param_reset_security_status = "resetsecuritystatus"

    # Parameters used for: setcolbrightnessvalue
    switchOn = "On"
    switchOff = "Off"
    switchToggle = "Toggle"
    switchSetLevel = "Set Level"

    switch_light_values = {
        switchOn,
        switchOff,
        switchToggle,
    }

    # Parameters used for: resetsecuritystatus
    switchNormal = "Normal"
    switchPanicEnd = "Panic End"

    switch_reset_security_statuses = {
        switchPanicEnd,
        switchNormal,
    }

    _int_value_off = 0
    _int_value_on = 1

    def __init__(self, server, *args, **kwargs):
        """
            Args:
                server (Server): Domoticz server object where to maintain the device            
                    idx (:obj:`int`, optional): ID of an existing device
                or
                    hardware (:obj:`obj`, optional): Hardware to add device
                    name (:obj:`str`, optional): Name of the device
                        type (:obj:`int`, optional): Device type
                        subtype (:obj:`int`, optional): Subtype of device
                    or 
                        typename (:obj:`str`, optional): Type name of the device
        """
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
            querystring = "type=devices&filter=all"
        else:
            querystring = ""
        self._api_querystring = querystring
        res = self._server._call_api(querystring)
        self._api_status = res.get("status", self._server._return_error)
        self._api_title = res.get("title", self._server._return_empty)
        myDict = {}
        if self._api_status == self._server._return_ok:
            # For some reason next property is only given in device calls. No idea about the meaning!
            self._server._ActTime = res.get("ActTime")
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
            # Search for the given device
            if res.get("result"):
                for resDict in res["result"]:
                    if (self._idx is not None and int(resDict.get("idx")) == self._idx) \
                            or (self._Name is not None and resDict.get("Name") == self._Name):
                        # Found device :)
                        myDict = resDict
                        break
        # Update device properties
        # The list below may be not complete!!!
        self._AddjMulti = myDict.get("AddjMulti")
        self._AddjMulti2 = myDict.get("AddjMulti2")
        self._AddjValue = myDict.get("AddjValue")
        self._AddjValue2 = myDict.get("AddjValue2")
        self._Barometer = myDict.get("Barometer")
        self._BatteryLevel = myDict.get("BatteryLevel", 255)
        self._CameraIdx = myDict.get("CameraIdx")
        self._Chill = myDict.get("Chill")
        self._Color = Color(color=myDict.get("Color", "{}"))
        self._Counter = myDict.get("Counter")
        self._CounterDeliv = myDict.get("CounterDeliv")
        self._CounterDelivToday = myDict.get("CounterDelivToday")
        self._CounterToday = myDict.get("CounterToday")
        self._Current = myDict.get("Current")
        self._CustomImage = myDict.get("CustomImage")
        self._Data = myDict.get("Data")
        self._DayTime = myDict.get("DayTime")
        self._Description = myDict.get("Description")
        self._Desc = myDict.get("Desc")
        self._DewPoint = myDict.get("DewPoint")
        self._DimmerType = myDict.get("DimmerType")
        self._Direction = myDict.get("Direction")
        self._DirectionStr = myDict.get("DirectionStr")
        self._displaytype = myDict.get("displaytype")
        self._Favorite = myDict.get("Favorite")
        self._Forecast = myDict.get("Forecast")
        self._ForecastStr = myDict.get("ForecastStr")
        self._Gust = myDict.get("Gust")
        self._HaveDimmer = myDict.get("HaveDimmer")
        self._HaveGroupCmd = myDict.get("HaveGroupCmd")
        self._HaveTimeout = myDict.get("HaveTimeout")
        self._Humidity = myDict.get("Humidity")
        self._HumidityStatus = myDict.get("HumidityStatus")
        self._ID = myDict.get("ID")
        self._idx = myDict.get("idx", self._idx)
        # Next property available with:
        #     type=command&param=getlightswitches
        #     type=devices&filter=light&used=true&order=Name
        self._isDimmer = myDict.get("IsDimmer")
        self._Image = myDict.get("Image")
        self._InternalState = myDict.get("InternalState")
        self._IsSubDevice = myDict.get("IsSubDevice")
        self._LastUpdate = myDict.get("LastUpdate")
        self._Level = myDict.get("Level")
        self._LevelActions = myDict.get("LevelActions")
        self._LevelInt = myDict.get("LevelInt")
        self._LevelNames = myDict.get("LevelNames")
        self._LevelOffHidden = myDict.get("LevelOffHidden")
        self._MaxDimLevel = myDict.get("MaxDimLevel")
        self._Mode = myDict.get("Mode")
        self._Modes = myDict.get("Modes")
        self._Name = myDict.get("Name", self._Name)
        self._Notifications = myDict.get("Notifications")
        self._Options = myDict.get("Options")
        self._PlanID = myDict.get("PlanID")
        self._PlanIDs = myDict.get("PlanIDs")
        self._Pressure = myDict.get("Pressure")
        self._Protected = myDict.get("Protected")
        self._Quality = myDict.get("Quality")
        self._Radiation = myDict.get("Radiation")
        self._Rain = myDict.get("Rain")
        self._RainRate = myDict.get("RainRate")
        self._SelectorStyle = myDict.get("SelectorStyle")
        self._SensorType = myDict.get("SensorType")
        self._SensorUnit = myDict.get("SensorUnit")
        self._SetPoint = myDict.get("SetPoint")
        self._ShowNotifications = myDict.get("ShowNotifications")
        self._SignalLevel = myDict.get("SignalLevel")
        self._Speed = myDict.get("Speed")
        self._State = myDict.get("State")
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
        self._Until = myDict.get("Until")
        self._Used = myDict.get("Used")
        self._Usage = myDict.get("Usage")
        self._UsageDeliv = myDict.get("UsageDeliv")
        self._UsedByCamera = myDict.get("UsedByCamera")
        self._UVI = myDict.get("UVI")
        self._ValueQuantity = myDict.get("ValueQuantity")
        self._ValueUnits = myDict.get("ValueUnits")
        self._Visibility = myDict.get("Visibility")
        self._Voltage = myDict.get("Voltage")
        self._XOffset = myDict.get("XOffset")
        self._YOffset = myDict.get("YOffset")

        # Some info from the hardware also comes
        HardwareID = myDict.get("HardwareID")
        if HardwareID is not None:
            hw = Hardware(self._server, idx=HardwareID)
            if hw.exists():
                self._Hardware = hw
                self._Hardware._HardwareType = myDict.get("HardwareType")
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
            querystring = "type={}&idx={}&sensorname={}&devicetype={}&devicesubtype={}".format(
                self._type_create_device, self._Hardware._idx, quote(self._Name), self._Type, self._SubType)
            self._api_querystring = querystring
            res = self._server._call_api(querystring)
            self._api_status = res.get(
                "status", self._server._return_error)[:3]
            self._api_title = res.get("title", self._server._return_empty)
            if self._api_status == self._server._return_ok:
                self._idx = res.get("idx", None)
                self._initDevice()

    def delete(self):
        if self.exists():
            # type=deletedevice&idx=29
            querystring = "type={}&idx={}".format(
                self._type_delete_device, self._idx)
            self._api_querystring = querystring
            res = self._server._call_command(querystring)
            self._api_status = res.get(
                "status", self._server._return_error)[:3]
            self._api_title = res.get("title", self._server._return_empty)
            if self._api_status == self._server._return_ok:
                self._Hardware = None
                self._idx = None

    def exists(self):
        """
            Check if device exists in Domoticz
        """
        return not (self._idx is None or self._Hardware is None)

    def hasBattery(self):
        """
            Check if this device is using a battery
        """
        return not (self._BatteryLevel is None or self._BatteryLevel == 255)

    def isDimmer(self):
        return ((self.isSwitch() and self._SwitchType == "Dimmer") or (self._isDimmer == True))

    def isFavorite(self):
        return not (self._Favorite is None or self._Favorite == 0)

    def isSwitch(self):
        return self._SwitchType is not None

    def isThermometer(self):
        return self._Temp is not None

    def isHygrometer(self):
        return self._Humidity is not None

    def resetSecurityStatus(self, value):
        """
            Reset security status for eg. Smoke detectors
        """
        if self.exists():
            if self.isSwitch():
                if value in self.switch_reset_security_statuses:
                    # type=command&param=resetsecuritystatus&idx=IDX&switchcmd=VALUE
                    querystring = "param={}&idx={}&switchcmd={}".format(
                        self._param_reset_security_status,
                        self._idx,
                        value
                    )
                    self._api_querystring = querystring
                    res = self._server._call_command(querystring)
                    self._api_status = res.get(
                        "status", self._server._return_error)[:3]
                    self._api_title = res.get(
                        "title", self._server._return_empty)
                    self._initDevice()

    def update(self, nvalue=0, svalue=""):
        # type=command&param=udevice&idx=IDX&nvalue=NVALUE&svalue=SVALUE
        if self.exists():
            querystring = "param={}&idx={}&nvalue={}".format(
                self._param_update_device, self._idx, nvalue)
            if len(svalue) > 0:
                querystring += "&svalue={}".format(svalue)
            self._api_querystring = querystring
            res = self._server._call_command(querystring)
            self._api_status = res.get(
                "status", self._server._return_error)[:3]
            self._api_title = res.get("title", self._server._return_empty)
            self._initDevice()

    def updateSwitch(self, value, level=0):
        if self.exists():
            if self.isSwitch():
                if value in self.switch_light_values:
                    # type=command&param=switchlight&idx=IDX&switchcmd=On
                    # type=command&param=switchlight&idx=IDX&switchcmd=Off
                    # type=command&param=switchlight&idx=IDX&switchcmd=Toggle
                    querystring = "param={}&idx={}&switchcmd={}".format(
                        self._param_switch_light,
                        self._idx,
                        value
                    )
                    self._api_querystring = querystring
                    res = self._server._call_command(querystring)
                    self._api_status = res.get(
                        "status", self._server._return_error)[:3]
                    self._api_title = res.get(
                        "title", self._server._return_empty)
                    self._initDevice()

    # ..........................................................................
    # Properties
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
    def api_status(self):
        return self._api_status

    @property
    def api_title(self):
        return self._api_title

    @property
    def api_querystring(self):
        return self._api_querystring

    @property
    def barometer(self):
        return self._Barometer

    @property
    def batterylevel(self):
        return self._BatteryLevel

    @property
    def cameraidx(self):
        return self._CameraIdx

    @property
    def chill(self):
        return self._Chill

    @property
    def color(self):
        return self._Color

    @color.setter
    def color(self, value):
        if isinstance(value, Color) and self.exists():
            if self.isSwitch():
                # type=command&param=setcolbrightnessvalue&idx=IDX&color=COLOR&brightness=LEVEL
                querystring = "param={}&idx={}&color={}&brightness={}".format(
                    self._param_set_color_brightness,
                    self._idx,
                    quote(value.color),
                    self._Level
                )
                self._api_querystring = querystring
                res = self._server._call_command(querystring)
                self._api_status = res.get(
                    "status", self._server._return_error)[:3]
                self._api_title = res.get(
                    "title", self._server._return_empty)
                self._initDevice()

    @property
    def counter(self):
        return self._Counter

    @property
    def counterdeliv(self):
        return self._CounterDeliv

    @property
    def counterdelivtoday(self):
        return self._CounterDelivToday

    @property
    def countertoday(self):
        return self._CounterToday

    @property
    def current(self):
        return self._Current

    @property
    def customimage(self):
        return self._CustomImage

    @property
    def data(self):
        return self._Data

    @property
    def daytime(self):
        return self._DayTime

    @property
    def description(self):
        return self._Description

    @property
    def desc(self):
        return self._Desc

    @property
    def dewpoint(self):
        return self._DewPoint

    @property
    def dimmertype(self):
        return self._DimmerType

    @property
    def direction(self):
        return self._Direction

    @property
    def directionstr(self):
        return self._DirectionStr

    @property
    def displaytype(self):
        return self._displaytype

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
            querystring += "&idx={}&isfavorite={}".format(
                self._idx, str(int_value))
            self._api_querystring = querystring
            res = self._server._call_command(querystring)
            self._api_status = res.get("status", self._server._return_error)
            self._api_title = res.get("title", self._server._return_empty)
            if self._api_status == self._server._return_ok:
                self._Favorite = int_value

    @property
    def forecast(self):
        return self._Forecast

    @property
    def forecaststr(self):
        return self._ForecastStr

    @property
    def gust(self):
        return self._Gust

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
    def humiditystatus(self):
        return self._HumidityStatus

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

    @level.setter
    def level(self, value):
        if self.isSwitch():
            # type=command&param=switchlight&idx=IDX&switchcmd=Set%20Level&level=LEVEL
            querystring = "param={}&idx={}&switchcmd={}&level={}".format(
                self._param_switch_light,
                self._idx,
                quote(self.switchSetLevel),
                value
            )
            self._api_querystring = querystring
            res = self._server._call_command(querystring)
            self._api_status = res.get(
                "status", self._server._return_error)[:3]
            self._api_title = res.get(
                "title", self._server._return_empty)
            self._initDevice()

    @property
    def levelactions(self):
        return self._LevelActions

    @property
    def levelint(self):
        return self._LevelInt

    @property
    def levelnames(self):
        return self._LevelNames

    @property
    def leveloffhidden(self):
        return self._LevelOffHidden

    @property
    def maxdimlevel(self):
        return self._MaxDimLevel

    @property
    def mode(self):
        return self._Mode

    @property
    def modes(self):
        return self._Modes

    @property
    def name(self):
        return self._Name

    @name.setter
    def name(self, value):
        if self.exists():
            # json.htm?type=command&param=renamedevice&idx=idx&name=
            querystring = self._server._param.format(self._param_rename_device)
            querystring += "&idx={}&name={}".format(
                self._idx, quote(str(value)))
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
    def options(self):
        return self._Options

    @property
    def planid(self):
        return self._PlanID

    @property
    def planids(self):
        return self._PlanIDs

    @property
    def pressure(self):
        return self._Pressure

    @property
    def protected(self):
        return self._Protected

    @property
    def quality(self):
        return self._Quality

    @property
    def radiation(self):
        return self._Radiation

    @property
    def rain(self):
        return self._Rain

    @property
    def rainrate(self):
        return self._RainRate

    @property
    def selectorstyle(self):
        return self._SelectorStyle

    @property
    def sensortype(self):
        return self._SensorType

    @property
    def sensorunit(self):
        return self._SensorUnit

    @property
    def server(self):
        return self._server

    @property
    def setpoint(self):
        return self._SetPoint

    @property
    def shownotifications(self):
        return self._ShowNotifications

    @property
    def signallevel(self):
        return self._SignalLevel

    @property
    def speed(self):
        return self._Speed

    @property
    def state(self):
        return self._State

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
    def type(self):
        return self._Type

    @property
    def typeimg(self):
        return self._TypeImg

    @property
    def unit(self):
        return self._Unit

    @property
    def until(self):
        return self._Until

    @property
    def usage(self):
        return self._Usage

    @property
    def usagedeliv(self):
        return self._UsageDeliv

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
            querystring = "type={}&idx={}&used={}".format(
                self._type_set_used, self._idx, str_value)
            self._api_querystring = querystring
            res = self._server._call_api(querystring)
            self._api_status = res.get("status", self._server._return_error)
            self._api_title = res.get("title", self._server._return_empty)
            if self._api_status == self._server._return_ok:
                self._Used = int_value

    @property
    def uvi(self):
        return self._UVI

    @property
    def valuequantity(self):
        return self._ValueQuantity

    @property
    def valueunits(self):
        return self._ValueUnits

    @property
    def visibilty(self):
        return self._Visibility

    @property
    def voltage(self):
        return self._Voltage

    @property
    def xoffset(self):
        return self._XOffset

    @property
    def yoffset(self):
        return self._YOffset
