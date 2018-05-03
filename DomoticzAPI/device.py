#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .server import Server
from .hardware import Hardware


################################################################################
# Device                                                                       #
################################################################################
class Device:
    _type_devices = "devices"
    _type_create_device = "createdevice"

    # Existing device: def __init__(self, server, idx)
    # New device:      def __init__(self, server, hardwareidx, name, type=None, subtype=None):
    def __init__(self, server, *args, **kwargs):
        if isinstance(server, Server) and server.exists():
            self._server = server
        else:
            self._server = None
        if len(args) == 1:
            # For existing hardware
            #   hw = dom.Hardware(server, "180")
            self._idx = args[0]
        elif len(args) >= 2:
            self._idx = None
            if isinstance(args[0], Hardware):
                if args[0].exists():
                    self._hardware = args[0]
                else:
                    self._hardware = None
            self._Name = args[1]
            if len(args) >= 3:
                self._HardwareType = args[2]
                if len(args) >= 4:
                    self._SubType = args[3]
                else:
                    self._SubType = None
            else:
                self._HardwareType = None
        else:
            self._idx = kwargs.get("idx", None)
            if self._idx is None:
                self._Name = kwargs.get("name", None)
                self._HardwareType = kwargs.get("type", None)
                self._SubType = kwargs.get("subtype", None)
        self._initDevice()

    def __str__(self):
        return "{0}({1}, \"{2}\", \"{3}\")".format(self.__class__.__name__, str(self._server), self._idx, self._Name)

    # ..........................................................................
    # Public methods
    # ..........................................................................
    def exists(self):
        return self._HardwareID is not None and self._idx is not None

    def add(self):
        if self._idx is None \
                and self._HardwareID is not None \
                and self._Name is not None \
                and self._HardwareType is not None \
                and self._SubType is not None:
            # type=createdevice&idx=29&sensorname=Temp5&devicetype=50&devicesubtype=5
            message = "type={}&idx={}&sensorname={}&devicetype={}&devicesubtype={}".format(self._type_create_device,
                                                                                           self._HardwareID,
                                                                                           self._Name,
                                                                                           self._HardwareType,
                                                                                           self._SubType)
        pass

    def hasBattery(self):
        return not (self._BatteryLevel is None or self._BatteryLevel == 255)

    # ..........................................................................
    # Properties
    # ..........................................................................
    @property
    def addjmulti(self):
        return self._AddjMulti

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
    def favorite(self):
        return self._Favorite

    @property
    def hardwareid(self):
        return self._HardwareID

    @property
    def hardwarename(self):
        return self._HardwareName

    @property
    def hardwaretype(self):
        return self._HardwareType

    @property
    def hardwaretypeval(self):
        return self._HardwareTypeVal

    @property
    def havetimeout(self):
        return self._HaveTimeout

    @property
    def id(self):
        return self._ID

    @property
    def image(self):
        return self._Image

    @property
    def lastupdate(self):
        return self._LastUpdate

    @property
    def name(self):
        return self._Name

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
    def used(self):
        return self._Used

    @property
    def xoffset(self):
        return self._XOffset

    @property
    def yoffset(self):
        return self._YOffset

    @property
    def idx(self):
        return self._idx

    # ..........................................................................
    # Private methods
    # ..........................................................................
    def _initDevice(self):
        if self._idx is not None:
            message = "type=devices&rid={}".format(self._idx)
        elif self._Name is not None:
            message = "type=devices&filter=all&used=true&order=Name"
        else:
            message = ""
        res = self._server._call_api(message)
        result = res.get("result")
        myDict = {}
        if len(result) > 0:
            for myDict in result:
                if (self._idx is not None and myDict.get("idx") == self._idx) \
                        or (self._Name is not None and myDict.get("Name") == self._Name):
                    break
        self._AddjMulti = myDict.get("AddjMulti")
        self._AddjMulti2 = myDict.get("AddjMulti2")
        self._AddjValue = myDict.get("AddjValue")
        self._AddjValue2 = myDict.get("AddjValue2")
        self._BatteryLevel = myDict.get("BatteryLevel", 255)
        self._CustomImage = myDict.get("CustomImage")
        self._Data = myDict.get("Data")
        self._Description = myDict.get("Description")
        self._Favorite = myDict.get("Favorite")
        self._HardwareID = myDict.get("HardwareID")
        self._HardwareName = myDict.get("HardwareName")
        self._HardwareType = myDict.get("HardwareType")
        self._HardwareTypeVal = myDict.get("HardwareTypeVal")
        self._HaveTimeout = myDict.get("HaveTimeout")
        self._ID = myDict.get("ID")
        self._idx = myDict.get("idx")
        self._Image = myDict.get("Image")
        self._LastUpdate = myDict.get("LastUpdate")
        self._Name = myDict.get("Name")
        self._Notifications = myDict.get("Notifications")
        self._PlanID = myDict.get("PlanID")
        self._PlanIDs = myDict.get("PlanIDs")
        self._Protected = myDict.get("Protected")
        self._SensorType = myDict.get("SensorType")
        self._SensorUnit = myDict.get("SensorUnit")
        self._ShowNotifications = myDict.get("ShowNotifications")
        self._SignalLevel = myDict.get("SignalLevel")
        self._SubType = myDict.get("SubType")
        self._Timers = myDict.get("Timers")
        self._Type = myDict.get("Type")
        self._TypeImg = myDict.get("TypeImg")
        self._Unit = myDict.get("Unit")
        self._Used = myDict.get("Used")
        self._XOffset = myDict.get("XOffset")
        self._YOffset = myDict.get("YOffset")
        #
        self._status = res.get("status")
        self._title = res.get("title")
