#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import urllib.request

import subprocess
from datetime import datetime


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
    __param_sun = "getSunRiseSet"
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
    __url_sunrise_set = _url_command + "param=" + __param_sun
    __url_log_message = _url_command + "param=" + __param_log + "&message="

    def __init__(self, address="localhost", port="8080"):
        self._address = address
        self._port = port
        self._url = "http://" + self._address + ":" + self._port + "/json.htm?"

    def __str__(self):
        txt = __class__.__name__ + "\n"
        txt += "  address: " + self._address + "\n"
        txt += "  port: " + self._port + "\n"
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


################################################################################
# User variable                                                                #
################################################################################
class UserVariable:
    # Types
    # 0 = Integer, e.g. - 1, 1, 0, 2, 10
    # 1 = Float, e.g. - 1.1, 1.2, 3.1
    # 2 = String
    # 3 = Date in format DD/MM/YYYY
    # 4 = Time in 24 hr format HH:MM
    # 5 = DateTime(but the format is not checked)

    _vtype2num = {
        "integer": "0",
        "float": "1",
        "string": "2",
        "date": "3",
        "time": "4",
        "datetime": "5",
    }

    _vtype2string = {
        "0": "integer",
        "1": "float",
        "2": "string",
        "3": "date",
        "4": "time",
        "5": "datetime",
    }

    _param_get_user_variable = "getuservariable"
    _param_save_user_variable = "saveuservariable"
    _param_update_user_variable = "updateuservariable"
    _param_delete_user_variable = "deleteuservariable"

    _date = "%d/%m/%Y"
    _time = "%H:%M"

    def __init__(self, dom, name, type="string", value=""):
        if dom is not None and len(name) > 0:
            self._dom = dom
            self._name = name
            if type in self._vtype2num:
                self._type = type
                self._typenum = self._vtype2num[type]
            else:
                self._type = ""
                self._typenum = ""
            self._value = self.__value(self._type, value)
            self._status = ""
            self._idx = ""
            self._lastupdate = ""
            self.__getvar()

    def __str__(self):
        txt = __class__.__name__ + ":\n"
        txt += "  idx: " + self._idx + "\n"
        txt += "  name: " + self._name + "\n"
        txt += "  type: " + self._type + " (" + self._typenum + ")\n"
        txt += "  value: " + self._value + "\n"
        txt += "  status: " + self._status + "\n"
        txt += "  lastupdate: " + self._lastupdate + "\n"
        return txt

    def __getvar(self):
        message = "param=getuservariables"
        res = self._dom.call_command(message)
        if res.get("result"):
            for var in res["result"]:
                if var["Name"] == self._name:
                    self._idx = var["idx"]
                    self._value = var["Value"]
                    self._type = self._vtype2string[var["Type"]]
                    self._lastupdate = var["LastUpdate"]
                    break

    def __value(self, type, value):
        print("type: " + type + " value: " + value)
        if value == "":
            result = value
        elif type == "integer":
            result = str(int(float(value)))
        elif type == "float":
            result = str(float(value))
        elif type == "date":
            try:
                dt = datetime.strptime(value, self._date)
            except:
                dt = None
            if dt is not None:
                result = dt.strftime(self._date)
            else:
                result = ""
        elif type == "time":
            try:
                dt = datetime.strptime(value, self._time)
            except:
                dt = None
            if dt is not None:
                result = dt.strftime(self._time)
            else:
                result = ""
        elif type == "datetime":
            try:
                dt = datetime.strptime(value, self._date + " " + self._time)
            except:
                dt = None
            if dt is not None:
                result = dt.strftime(self._date + " " + self._time)
            else:
                result = ""
        elif type == "string":
            result = value
        else:  # string
            result = ""
        return result

    # ..........................................................................
    # Properties
    # ..........................................................................
    @property
    def idx(self):
        return self._idx

    @property
    def lastupdate(self):
        return self._lastupdate

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = self.__value(self._type, value)

    @property
    def status(self):
        return self._status

    # ..........................................................................
    # Methods
    # ..........................................................................
    def exists(self):
        if len(self._idx) > 0:
            return True
        else:
            return False

    # json.htm?type=command&param=saveuservariable&vname=Test&vtype=1&vvalue=1.23
    def add(self):
        if not self.exists():
            if len(self._name) > 0 and len(self._type) > 0 and len(self._value) > 0:
                message = "param={}&vname={}&vtype={}&vvalue={}".format(self._param_save_user_variable, self._name,
                                                                        self._typenum, self._value)
                res = self._dom.call_command(message)
                self._status = res["status"]
                if self._status == self._dom._return_ok:
                    self.__getvar()

    # json.htm?type=command&param=updateuservariable&vname=Test&vtype=1&vvalue=1.23
    def update(self):
        if self.exists():
            message = "param={}&vname={}&vtype={}&vvalue={}".format(self._param_update_user_variable, self._name,
                                                                    self._typenum, self._value)
            res = self._dom.call_command(message)
            self.__getvar()

    # json.htm?type=command&param=deleteuservariable&idx=3
    def delete(self):
        if self.exists():
            message = "param={}&idx={}".format(self._param_delete_user_variable, self._idx)
            res = self._dom.call_command(message)
            self._idx = ""
