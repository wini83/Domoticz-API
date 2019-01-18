#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Solar data
#
# Author: Xorfor
#
"""
<plugin key="xfr_energy" name="Energy" author="Xorfor" version="1.0.0">
    <params>
        <param field="Mode6" label="Debug" width="75px">
            <options>
                <option label="True" value="Debug"/>
                <option label="False" value="Normal" default="true"/>
            </options>
        </param>
    </params>
</plugin>
"""
import Domoticz
import DomoticzAPI as dom


class BasePlugin:
    __DEBUG_NONE = 0
    __DEBUG_ALL = 1

    __HEARTBEATS2MIN = 6
    __MINUTES = 1  # or use a parameter

    # Device units
    __UNIT_ENERGY = 1

    def __init__(self):
        self.__runAgain = 0
        self.__server = dom.Server()
        # Device that measures the usage
        self.__usage = [
            dom.Device(self.__server, 69),  # P1 Dongle
        ]
        # Devices that generates energy, eg. windmills and solar panels
        self.__return = [
            dom.Device(self.__server, 82),
            dom.Device(self.__server, 91),
            dom.Device(self.__server, 105),
        ]

    def onCommand(self, Unit, Command, Level, Color):
        Domoticz.Debug(
            "onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))

    def onConnect(self, Connection, Status, Description):
        Domoticz.Debug("onConnect called")

    def onDeviceAdded(self, Unit):
        Domoticz.Debug("onDeviceAdded called for Unit " + str(Unit))

    def onDeviceModified(self, Unit):
        Domoticz.Debug("onDeviceModified called for Unit " + str(Unit))

    def onDeviceRemoved(self, Unit):
        Domoticz.Debug("onDeviceRemoved called for Unit " + str(Unit))

    def onStart(self):
        Domoticz.Debug("onStart called")
        if Parameters["Mode6"] == "Debug":
            Domoticz.Debugging(self.__DEBUG_ALL)
        else:
            Domoticz.Debugging(self.__DEBUG_NONE)
        # Images
        # Check if images are in database
        # if "xfr_template" not in Images:
        #     Domoticz.Image("xfr_template.zip").Create()
        # try:
        #     image = Images["xfr_template"].ID
        # except:
        #     image = 0
        # Domoticz.Debug("Image created. ID: " + str(image))
        # Validate parameters
        # Create devices
        if len(Devices) == 0:
            Domoticz.Device(Unit=self.__UNIT_ENERGY,
                            Name="Energy",
                            TypeName="kWh",
                            Used=1).Create()
        # Log config
        DumpAllToLog()
        # Connection

    def onStop(self):
        Domoticz.Debug("onStop called")

    def onMessage(self, Connection, Data):
        Domoticz.Debug("onMessage called")

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Debug("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(
            Priority) + "," + Sound + "," + ImageFile)

    def onDisconnect(self, Connection):
        Domoticz.Debug("onDisconnect called")

    def onHeartbeat(self):
        Domoticz.Debug("onHeartbeat called")
        self.__runAgain -= 1
        if self.__runAgain <= 0:
            self.__runAgain = self.__HEARTBEATS2MIN * self.__MINUTES
            # Execute your command
            # Get production data
            _energy = 0.0
            for dev in self.__return:
                Domoticz.Debug(str(dev) + ": " +
                               str(dev.nvalue) + " - " + str(dev.idx))
                _energy += dev.nvalue
            Domoticz.Debug("Return: " + str(_energy))
            # Get usage
            for dev in self.__usage:
                Domoticz.Debug(str(dev) + ": " + str(dev.nvalue))
                _energy -= dev.nvalue
            Domoticz.Debug("Total: " + str(_energy))
            UpdateDevice(self.__UNIT_ENERGY,
                         int(_energy),
                         str(_energy) + ";" + str(_energy))
        else:
            Domoticz.Debug("onHeartbeat called, run again in " +
                           str(self.__runAgain) + " heartbeats.")


global _plugin
_plugin = BasePlugin()


def onCommand(Unit, Command, Level, Color):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Color)


def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)


def onDeviceAdded(Unit):
    global _plugin
    _plugin.onDeviceAdded(Unit)


def onDeviceModified(Unit):
    global _plugin
    _plugin.onDeviceModified(Unit)


def onDeviceRemoved(Unit):
    global _plugin
    _plugin.onDeviceRemoved(Unit)


def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)


def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()


def onMessage(Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data)


def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status,
                           Priority, Sound, ImageFile)


def onStart():
    global _plugin
    _plugin.onStart()


def onStop():
    global _plugin
    _plugin.onStop()


################################################################################
# Generic helper functions
################################################################################
def DumpDevicesToLog():
    # Show devices
    Domoticz.Debug("Device count.........: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device...............: " +
                       str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device Idx...........: " + str(Devices[x].ID))
        Domoticz.Debug("Device Type..........: " +
                       str(Devices[x].Type) + " / " + str(Devices[x].SubType))
        Domoticz.Debug("Device Name..........: '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue........: " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue........: '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device Options.......: '" +
                       str(Devices[x].Options) + "'")
        Domoticz.Debug("Device Used..........: " + str(Devices[x].Used))
        Domoticz.Debug("Device ID............: '" +
                       str(Devices[x].DeviceID) + "'")
        Domoticz.Debug("Device LastLevel.....: " + str(Devices[x].LastLevel))
        Domoticz.Debug("Device Image.........: " + str(Devices[x].Image))


def DumpImagesToLog():
    # Show images
    Domoticz.Debug("Image count..........: " + str(len(Images)))
    for x in Images:
        Domoticz.Debug("Image '" + x + "...': '" + str(Images[x]) + "'")


def DumpParametersToLog():
    # Show parameters
    Domoticz.Debug("Parameters count.....: " + str(len(Parameters)))
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug("Parameter '" + x + "'...: '" +
                           str(Parameters[x]) + "'")


def DumpSettingsToLog():
    # Show settings
    Domoticz.Debug("Settings count.......: " + str(len(Settings)))
    for x in Settings:
        Domoticz.Debug("Setting '" + x + "'...: '" + str(Settings[x]) + "'")


def DumpAllToLog():
    DumpDevicesToLog()
    DumpImagesToLog()
    DumpParametersToLog()
    DumpSettingsToLog()


def DumpHTTPResponseToLog(httpDict):
    if isinstance(httpDict, dict):
        Domoticz.Debug("HTTP Details (" + str(len(httpDict)) + "):")
        for x in httpDict:
            if isinstance(httpDict[x], dict):
                Domoticz.Debug(
                    "....'" + x + " (" + str(len(httpDict[x])) + "):")
                for y in httpDict[x]:
                    Domoticz.Debug("........'" + y + "':'" +
                                   str(httpDict[x][y]) + "'")
            else:
                Domoticz.Debug("....'" + x + "':'" + str(httpDict[x]) + "'")


def UpdateDevice(Unit, nValue, sValue, TimedOut=0, AlwaysUpdate=False):
    if Unit in Devices:
        if Devices[Unit].nValue != nValue or Devices[Unit].sValue != sValue or Devices[
                Unit].TimedOut != TimedOut or AlwaysUpdate:
            Devices[Unit].Update(
                nValue=nValue, sValue=str(sValue), TimedOut=TimedOut)
            Domoticz.Debug(
                "Update " + Devices[Unit].Name + ": " + str(nValue) + " - '" + str(sValue) + "'")


def UpdateDeviceOptions(Unit, Options={}):
    if Unit in Devices:
        if Devices[Unit].Options != Options:
            Devices[Unit].Update(nValue=Devices[Unit].nValue,
                                 sValue=Devices[Unit].sValue, Options=Options)
            Domoticz.Debug("Device Options update: " +
                           Devices[Unit].Name + " = " + str(Options))


def UpdateDeviceImage(Unit, Image):
    if Unit in Devices and Image in Images:
        if Devices[Unit].Image != Images[Image].ID:
            Devices[Unit].Update(nValue=Devices[Unit].nValue,
                                 sValue=Devices[Unit].sValue, Image=Images[Image].ID)
            Domoticz.Debug("Device Image update: " +
                           Devices[Unit].Name + " = " + str(Images[Image].ID))
