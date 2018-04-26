#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import subprocess
from datetime import datetime

################################################################################
# Server                                                                       #
################################################################################
class Server:
    # Responses
    _return_ok = "OK"
    _return_error = "ERR"

    __type_command = "command"
    __type_devices = "devices"
    __type_hardware = "hardware"
    __type_create_virtual_sensor = "createvirtualsensor"
    __type_set_used = "setused"

    # History
    __type_lightlog = "lightlog"  # Switch
    __type_graph_sensor = "graph&sensor"  # Temperature

    # Param
    __param_light = "getlightswitches"
    __param_shutdown = "system_shutdown"
    __param_reboot = "system_reboot"
    _param_sun = "getSunRiseSet"
    __param_log = "addlogmessage"
    __param_notification = "sendnotification"

    __param_switch_light = "switchlight"
    __param_color_brightness = "setcolbrightnessvalue"
    __param_kelvin_level = "setkelvinlevel"

    # Scenes / Groups
    __type_scenes = "scenes"
    __type_add_scene = "addscene"
    __type_delete_scene = "deletescene"
    __type_scene_timers = "scenetimers"
    __param_switch_scene = "switchscene"
    __param_get_scene_devices = "getscenedevices"
    __param_add_scene_device = "addscenedevice"
    __param_delete_scene_device = "deletescenedevice"
    __param_add_scene_timer = "addscenetimer"

    __type_create_device = "createdevice"
    __param_add_hardware = "addhardware"
    __param_update_device = "udevice"

    # User variables
    __param_get_user_variables = "getuservariables"

    # Room Plans
    __type_plans = "plans"
    __param_get_plan_devices = "getplandevices"

    # Device Timer Schedules
    __type_schedules = "schedules"
    __param_enable_timer = "enabletimer"
    __param_disable_timer = "disabletimer"
    __param_delete_timer = "deletetimer"
    __param_update_timer = "updatetimer"
    __param_add_timer = "addtimer"
    __param_clear_timers = "cleartimers"

    # Filters
    __filter_all = "all"  # Get all devices
    __filter_light = "light"  # Get all lights / switches
    __filter_weather = "weather"  # Get all weather devices
    __filter_temp = "temp"  # Get all temperature devices
    __filter_utility = "utility"  # Get all utility devices
    #
    __filter_device = "device"  #
    __filter_scene = "scene"
    __filter_thermostat = "thermostat"

    _url_command = "type=" + __type_command + "&"
    _url_sunrise_set = _url_command + "param=" + _param_sun
    __url_log_message = _url_command + "param=" + __param_log + "&message="

    def __init__(self, address="localhost", port="8080"):
        self._address = address
        self._port = port
        self._url = "http://" + self._address + ":" + self._port + "/json.htm?"
        self._AstrTwilightEnd = ""
        self._AstrTwilightStart = ""
        self._CivTwilightEnd = ""
        self._CivTwilightStart = ""
        self._DayLength = ""
        self._NautTwilightEnd = ""
        self._NautTwilightStart = ""
        self._SunAtSouth = ""
        self._Sunrise = ""
        self._AstrTwilightEnd = ""
        self._Sunset()

    def __str__(self):
        txt = __class__.__name__ + "\n"
        txt += "  address: " + self._address + "\n"
        txt += "  port: " + self._port + "\n"
        txt += "    AstrTwilightEnd: " + self._AstrTwilightEnd + "\n"
        txt += "    AstrTwilightStart: " + self. _AstrTwilightStart + "\n"
        txt += "    CivTwilightEnd: " + self._CivTwilightEnd + "\n"
        txt += "    CivTwilightStart: " + self._CivTwilightStart + "\n"
        txt += "    NautTwilightEnd: " + self._NautTwilightEnd + "\n"
        txt += "    NautTwilightStart: " + self._NautTwilightStart + "\n"
        txt += "    Sunrise: " + self._Sunrise + "\n"
        txt += "    Sunset: " + self._Sunset + "\n"
        txt += "    SunAtSouth: " + self._SunAtSouth + "\n"
        txt += "    DayLength: " + self._DayLength + "\n"
        return txt

    # Properties

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, address):
        self._address = address

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, port):
        self._port = port

    # Global methods

    # Private methods
    def _getSunRiseSet(self):
        message = "param={}".format(self._param_sun)
        res = self.call_command(message)
        if res.get("AstrTwilightEnd"):
            self._AstrTwilightEnd = res["AstrTwilightEnd"]
        else:
            self._AstrTwilightEnd = ""
        if res.get("AstrTwilightStart"):
            self._AstrTwilightStart = res["AstrTwilightStart"]
        else:
            self._AstrTwilightStart = ""
        if res.get("CivTwilightEnd"):
            self._CivTwilightEnd = res["CivTwilightEnd"]
        else:
            self._CivTwilightEnd = ""
        if res.get("CivTwilightStart"):
            self._CivTwilightStart = res["CivTwilightStart"]
        else:
            self._CivTwilightStart = ""
        if res.get("DayLength"):
            self._DayLength = res["DayLength"]
        else:
            self._DayLength = ""
        if res.get("NautTwilightEnd"):
            self._NautTwilightEnd = res["NautTwilightEnd"]
        else:
            self._NautTwilightEnd = ""
        if res.get("NautTwilightStart"):
            self._NautTwilightStart = res["NautTwilightStart"]
        else:
            self._NautTwilightStart = ""
        if res.get("SunAtSouth"):
            self._SunAtSouth = res["SunAtSouth"]
        else:
            self._SunAtSouth = ""
        if res.get("Sunrise"):
            self._Sunrise = res["Sunrise"]
        else:
            self._Sunrise = ""
        if res.get("Sunset"):
            self._Sunset = res["Sunset"]
        else:
            self._Sunset = ""

    def log_message(self, message):
        self.__call_api(self.__url_log_message + message)

    def call_command(self, text):
        return self.call_api(self._url_command + text)

    def call_api(self, text):
        return self.__call_url(self._url + str(text), "", "")

    # def __call_url(self, url, username, password):
    #     print("__call_url: "+ url)
    #     # request = urllib.request(url)
    #     # if len(username) != 0 and len(password) != 0:
    #     #	base64string = base64.encodestring("%s:%s" % (username, password)).replace("\n", "")
    #     #	request.add_header("Authorization", "Basic %s" % base64string)
    #     req = urllib.request.urlopen(url)
    #     #res = req.read()
    #     res = json.loads(req.read().decode("utf-8", "ignore"))
    #     return res

    def __call_url(self, url, username="", password=""):
        command = "curl -s "
        options = "'" + url + "'"
        p = subprocess.Popen(command + " " + options, shell=True, stdout=subprocess.PIPE)
        p.wait()
        data, errors = p.communicate()
        if p.returncode != 0:
            pass
        res = json.loads(data.decode("utf-8", "ignore"))
        return res
