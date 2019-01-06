#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .api import API
from .server import Server
from .hardware import Hardware
from .color import Color
from .const import(NUM_MAX, NUM_MIN)
from urllib.parse import quote


class Device:
    """
        Device class
    """
    _type_devices = "devices"
    _type_create_device = "createdevice"
    _type_create_dummy = "createvirtualsensor"
    _type_delete_device = "deletedevice"
    _type_set_used = "setused"
    _type_events = "events"

    _param_make_favorite = "makefavorite"
    _param_rename_device = "renamedevice"
    _param_update_device = "udevice"
    _param_switch_light = "switchlight"
    _param_set_color_brightness = "setcolbrightnessvalue"
    _param_reset_security_status = "resetsecuritystatus"
    _param_current_states = "currentstates"

    # Parameters used for: setcolbrightnessvalue
    SWITCH_ON = "On"
    SWITCH_OFF = "Off"
    SWITCH_TOGGLE = "Toggle"
    SWITCH_SET_LEVEL = "Set Level"

    switch_light_values = {
        SWITCH_ON,
        SWITCH_OFF,
        SWITCH_TOGGLE,
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
            #   dev = dom.Device(server, 180)
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
            self._SubType = kwargs.get("subtype")
            self._Type = kwargs.get("type")
            self._TypeName = kwargs.get("typename")
        else:
            self._idx = kwargs.get("idx")
            if self._idx is None:
                self._Hardware = kwargs.get("hardware")
                self._Name = kwargs.get("name")
                self._SubType = kwargs.get("subtype")
                self._Type = kwargs.get("type")
                self._TypeName = kwargs.get("typename")
        if self._TypeName is not None:
            self._Type = None
            self._SubType = None
        self._api = self._server.api
        self._initDevice()

    def __str__(self):
        return "{}({}, {}: \"{}\")".format(self.__class__.__name__, str(self._server), self._idx, self._Name)

    # ..........................................................................
    # Private methods
    # ..........................................................................

    def _initDevice(self):
        if self._idx is not None:
            # Retrieve status of specific device: /json.htm?type=devices&rid=IDX
            querystring = "type={}&rid={}".format(
                self._type_devices, self._idx)
        elif self._Name is not None:
            # Get all devices: /json.htm?type=devices&filter=all
            querystring = "type={}&filter=all".format(self._type_devices)
        else:
            querystring = ""
        self._api.querystring = querystring
        self._api.call()
        myDict = {}
        if self._api.status == self._api.OK:
            d = self._api.data
            # For some reason next property is only given in device calls. No idea about the meaning!
            self._server._ActTime = d.get("ActTime")
            # Update the server properties.
            self._server._AstrTwilightEnd = d.get("AstrTwilightEnd")
            self._server._AstrTwilightStart = d.get("AstrTwilightStart")
            self._server._CivTwilightEnd = d.get("CivTwilightEnd")
            self._server._CivTwilightStart = d.get("CivTwilightStart")
            self._server._DayLength = d.get("DayLength")
            self._server._NautTwilightEnd = d.get("NautTwilightEnd")
            self._server._NautTwilightStart = d.get("NautTwilightStart")
            self._server._ServerTime = d.get("ServerTime")
            self._server._SunAtSouth = d.get("SunAtSouth")
            self._server._Sunrise = d.get("Sunrise")
            self._server._Sunset = d.get("Sunset")
            # In param=getversion it is "version"
            self._server._version = d.get("app_version") 
            # Search for the given device
            if self._api.result:
                for resDict in self._api.result:
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
        self._BatteryLevel = myDict.get("BatteryLevel", NUM_MAX)
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
        #     /json.htm?type=command&param=getlightswitches
        #     /json.htm?type=devices&filter=light&used=true&order=Name
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
        self._PlanID = myDict.get("PlanID") # The first RoomPlan to which this device was assigned?
        self._PlanIDs = myDict.get("PlanIDs") # List of RoomPlan idxs containg this device
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
            # /json.htm?type=createdevice&idx=IDX&sensorname=SENSORNAME&devicetype=DEVICETYPE&devicesubtype=SUBTYPE
            self._api.querystring = "type={}&idx={}&sensorname={}&devicetype={}&devicesubtype={}".format(
                self._type_create_device,
                self._Hardware._idx,
                quote(self._Name),
                self._Type,
                self._SubType)
            self._api.call()
            if self._api.status == self._api.OK:
                self._idx = self._api.data.get("idx", None)
                self._initDevice()

    def delete(self):
        if self.exists():
            # /json.htm?type=deletedevice&idx=IDX
            self._api.querystring = "type={}&idx={}".format(
                self._type_delete_device,
                self._idx)
            self._api.call()
            if self._api.status == self._api.OK:
                self._Hardware = None
                self._idx = None

    def exists(self):
        """
            Check if device exists in Domoticz
        """
        return not (self._idx is None or self._Hardware is None)

    def has_battery(self):
        """
            Check if this device is using a battery
        """
        return not (self._BatteryLevel is None or self._BatteryLevel == NUM_MAX)

    def is_dimmer(self):
        return ((self.is_switch() and self._SwitchType == "Dimmer") or (self._isDimmer == True))

    def is_favorite(self):
        return not (self._Favorite is None or self._Favorite == 0)

    def is_switch(self):
        return self._SwitchType is not None

    def is_thermometer(self):
        return self._Temp is not None

    def is_hygrometer(self):
        return self._Humidity is not None

    def reset_security_status(self, value):
        """
            Reset security status for eg. Smoke detectors
        """
        if self.exists():
            if self.is_switch():
                if value in self.switch_reset_security_statuses:
                    # /json.htm?type=command&param=resetsecuritystatus&idx=IDX&switchcmd=VALUE
                    self._api.querystring = "type=command&param={}&idx={}&switchcmd={}".format(
                        self._param_reset_security_status,
                        self._idx,
                        value
                    )
                    self._api.call()
                    self._initDevice()

    def update(self, nvalue=0, svalue=""):
        # /json.htm?type=command&param=udevice&idx=IDX&nvalue=NVALUE&svalue=SVALUE
        if self.exists():
            self._api.querystring = "type=command&param={}&idx={}&nvalue={}".format(
                self._param_update_device,
                self._idx,
                nvalue)
            if len(svalue) > 0:
                self._api.querystring += "&svalue={}".format(svalue)
            self._api.call()
            self._initDevice()

    def update_switch(self, value, level=0):
        if self.exists():
            if self.is_switch():
                if value in self.switch_light_values:
                    # /json.htm?type=command&param=switchlight&idx=IDX&switchcmd=On
                    # /json.htm?type=command&param=switchlight&idx=IDX&switchcmd=Off
                    # /json.htm?type=command&param=switchlight&idx=IDX&switchcmd=Toggle
                    self._api.querystring = "type=command&param={}&idx={}&switchcmd={}".format(
                        self._param_switch_light,
                        self._idx,
                        value
                    )
                    self._api.call()
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
            if self.is_switch():
                # /json.htm?type=command&param=setcolbrightnessvalue&idx=IDX&color=COLOR&brightness=LEVEL
                self._api.querystring = "type=command&param={}&idx={}&color={}&brightness={}".format(
                    self._param_set_color_brightness,
                    self._idx,
                    quote(value.color),
                    self._Level
                )
                self._api.call()
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
        # /json.htm?type=command&param=makefavorite&idx=IDX&isfavorite=FAVORITE
        if isinstance(value, bool) and self.exists():
            if value:
                int_value = self._int_value_on
            else:
                int_value = self._int_value_off
            self._api.querystring = "type=command&param={}&idx={}&isfavorite={}".format(
                self._param_make_favorite,
                self._idx,
                str(int_value)
                )
            self._api.call()
            if self._api.status == self._api.OK:
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
        return int(self._idx) if self._idx is not None else None

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
        if self.is_switch():
            # /json.htm?type=command&param=switchlight&idx=IDX&switchcmd=Set%20Level&level=LEVEL
            self._api.querystring = "type=command&param={}&idx={}&switchcmd={}&level={}".format(
                self._param_switch_light,
                self._idx,
                quote(self.SWITCH_SET_LEVEL),
                value
            )
            self._api.call()
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
            # /json.htm?type=command&param=renamedevice&idx=idx&name=
            self._api.querystring = "type=command&param={}&idx={}&name={}".format(
                self._param_rename_device,
                self._idx,
                quote(str(value))
                )
            self._api.call()
            if self._api.status == self._api.OK:
                self._Name = value

    @property
    def notifications(self):
        return self._Notifications

    @property
    def nvalue(self):
        # The only way to get a current value from a device is by calling:
        #
        #   /type=events&param=currentstates
        #
        # Where:
        #   idx = self._idx
        #   value = nvalue (if string, then take value before '/' in values)
        #
        if self.exists():
            # /json.htm?type=events&param=currentstates
            self._api.querystring = "type={}&param={}".format(
                self._type_events,
                self._param_current_states
            )
            self._api.call()
            myDict = {}
            if self._api.status == self._api.OK and self._api.payload:
                for resDict in self._api.payload:
                    if self._idx is not None and resDict.get("id") == self.idx:
                        # Found device :)
                        myDict = resDict
                        break
            value = myDict.get("value")
            values = myDict.get("values")
            try:
                nvalue = float(value)
            except:
                nvalue = None
            if nvalue is None:
                try:
                    nvalue = float(values.partition("/")[0])
                except:
                    nvalue = None
            return nvalue
        # if self._Usage is not None:
        #     return float(self._Usage.split()[0])
        # elif self._Data is not None:
        #     return float(self._Data.split()[0])
        # else:
        #     return None

    @property
    def options(self):
        return self._Options

    @property
    def planid(self):
        return int(self._PlanID) if self._PlanID is not None else None

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
            # /json.htm?type=setused&idx=IDX&used=true|false
            self._api.querystring = "type={}&idx={}&used={}".format(
                self._type_set_used,
                self._idx,
                str_value
                )
            self._api.call()
            if self._api.status == self._api.OK:
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
