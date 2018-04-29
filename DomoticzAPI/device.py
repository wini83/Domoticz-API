#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
# Device                                                                       #
################################################################################
class Device:

    def __init__(self, server, idx):
        self._server = server
        self._idx = idx
        self._status = ""
        self._AddjMulti = None
        self._AddjMulti2 = None
        self._AddjValue = None
        self._AddjValue2 = None
        self._BatteryLevel = None
        self._CustomImage = None
        self._Data = None
        self._Description = None
        self._Favorite = None
        self._HardwareID = None
        self._HardwareName = None
        self._HardwareType = None
        self._HardwareTypeVal = None
        self._HaveTimeout = None
        self._ID = None
        self._Image = None
        self._LastUpdate = None
        self._Name = None
        self._Notifications = None
        self._PlanID = None
        self._PlanIDs = None
        self._Protected = None
        self._SensorType = None
        self._SensorUnit = None
        self._ShowNotifications = None
        self._SignalLevel = None
        self._SubType = None
        self._Timers = None
        self._Type = None
        self._TypeImg = None
        self._Unit = None
        self._Used = None
        self._XOffset = None
        self._YOffset = None
        self._getDevice()

    def __str__(self):
        return "{0}({1}, \"{2}\", \"{3}\")".format(self.__class__.__name__, str(self._server), self._idx, self._Name)

    # ..........................................................................
    # Public methods
    # ..........................................................................
    def exists(self):
        return self._HardwareID is not None

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
    def _getDevice(self):
        message = "type=devices&rid={}".format(self._idx)
        res = self._server._call_api(message)
        res = res["result"] if res.get("result") else ""
        if len(res) > 0:
            for myDict in res:
                if myDict["idx"] == self._idx:
                    # Used one line if ... then ... else for more compact code
                    self._AddjMulti = myDict["AddjMulti"]
                    self._AddjMulti2 = myDict["AddjMulti2"]
                    self._AddjValue = myDict["AddjValue"]
                    self._AddjValue2 = myDict["AddjValue2"]
                    self._BatteryLevel = myDict["BatteryLevel"] if myDict.get("BatteryLevel") else 255
                    self._CustomImage = myDict["CustomImage"]
                    self._Data = myDict["Data"]
                    self._Description = myDict["Description"]
                    self._Favorite = myDict["Favorite"]
                    self._HardwareID = myDict["HardwareID"] if myDict.get("HardwareID") else -1
                    #self._HardwareID = myDict["HardwareID"]
                    self._HardwareName = myDict["HardwareName"]
                    self._HardwareType = myDict["HardwareType"]
                    self._HardwareTypeVal = myDict["HardwareTypeVal"]
                    self._HaveTimeout = myDict["HaveTimeout"]
                    self._ID = myDict["ID"]
                    self._Image = self._EmptyIfNotExist(myDict, "Image")
                    self._LastUpdate = myDict["LastUpdate"]
                    self._Name = myDict["Name"]
                    self._Notifications = myDict["Notifications"]
                    self._PlanID =myDict["PlanID"]
                    self._PlanIDs = myDict["PlanIDs"]
                    self._Protected = myDict["Protected"]
                    self._SensorType = self._EmptyIfNotExist(myDict, "SensorType")
                    self._SensorUnit = self._EmptyIfNotExist(myDict, "SensorUnit")
                    self._ShowNotifications = myDict["ShowNotifications"]
                    self._SignalLevel = myDict["SignalLevel"]
                    self._SubType = myDict["SubType"]
                    self._Timers = myDict["Timers"]
                    self._Type = myDict["Type"]
                    self._TypeImg = myDict["TypeImg"]
                    self._Unit = myDict["Unit"]
                    self._Used = myDict["Used"]
                    self._XOffset = myDict["XOffset"]
                    self._YOffset = myDict["YOffset"]


    def _EmptyIfNotExist(self, d, attr):
        res = d[attr] if d.get(attr) else ""
        return res
