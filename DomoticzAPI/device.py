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
        self._getDevice()

    def __str__(self):
        txt = __class__.__name__ + ":\n"
        txt += "  addjmulti: " + str(self._AddjMulti) + "\n"
        txt += "  batterylevel: " + str(self._BatteryLevel) + "\n"
        txt += "  id: \"" + self._ID + "\"\n"
        txt += "  idx: \"" + self._idx + "\"\n"
        txt += "  name: \"" + self._Name + "\"\n"
        return txt

    # ..........................................................................
    # Properties
    # ..........................................................................
    @property
    def addjmulti(self):
        return self._AddjMulti

    @property
    def batterylevel(self):
        return self._BatteryLevel

    @property
    def id(self):
        return self._ID

    @property
    def idx(self):
        return self._idx

    @property
    def name(self):
        return self._Name

    # ..........................................................................
    # Global methods
    # ..........................................................................

    # ..........................................................................
    # Private methods
    # ..........................................................................
    def _getDevice(self):
        message = "type=devices&rid={}".format(self._idx)
        res = self._server._call_api(message)
        res = res["result"] if res.get("result") else ""
        if len(res) > 0:
            dev = res[0]
            if dev["idx"] == self._idx:
                self._AddjMulti = dev["AddjMulti"]
                self._AddjMulti2 = dev["AddjMulti2"]
                self._AddjValue = dev["AddjValue"]
                self._AddjValue2 = dev["AddjValue2"]
                self._BatteryLevel = dev["BatteryLevel"]
                self._CustomImage = dev["CustomImage"]
                self._Data = dev["Data"]
                self._Description = dev["Description"]
                self._Favorite = dev["Favorite"]
                self._HardwareID = dev["HardwareID"]
                self._HardwareName = dev["HardwareName"]
                self._HardwareType = dev["HardwareType"]
                self._HardwareTypeVal = dev["HardwareTypeVal"]
                self._HaveTimeout = dev["HaveTimeout"]
                self._ID = dev["ID"]
                self._Image = dev["Image"]
                self._LastUpdate = dev["LastUpdate"]
                self._Name = dev["Name"]
                self._Notifications = dev["Notifications"]
                self._PlanID =dev["PlanID"]
                self._PlanIDs = dev["PlanIDs"]
                self._Protected = dev["Protected"]
                self._SensorType = dev["SensorType"]
                self._SensorUnit = dev["SensorUnit"]
                self._ShowNotifications = dev["ShowNotifications"]
                self._SignalLevel = dev["SignalLevel"]
                self._SubType = dev["SubType"]
                self._Timers = dev["Timers"]
                self._Type = dev["Type"]
                self._TypeImg = dev["TypeImg"]
                self._Unit = dev["Unit"]
                self._Used = dev["Used"]
                self._XOffset = dev["XOffset"]
                self._YOffset = dev["YOffset"]
