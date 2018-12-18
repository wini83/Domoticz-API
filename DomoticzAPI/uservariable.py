#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .server import Server
from .api import API
from datetime import datetime

"""
    User variable
"""


class UserVariable:
    # Types
    # 0 = Integer, e.g. -1, 1, 0, 2, 10
    # 1 = Float, e.g. -1.1, 1.2, 3.1
    # 2 = String
    # 3 = Date in format DD/MM/YYYY
    # 4 = Time in 24 hr format HH:MM
    # 5 = DateTime (but the format is not checked)

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
    _param_get_user_variables = "getuservariables"
    _param_add_user_variable = "adduservariable"
    _param_update_user_variable = "updateuservariable"
    _param_delete_user_variable = "deleteuservariable"

    _date = "%d/%m/%Y"
    _time = "%H:%M"

    def __init__(self, server, name, type="string", value=""):
        """
        Args:
            server (Server): Domoticz server object where to maintain the user variable
            name (:obj:`str`): Name of the user variable
            type (:obj:`str`, optional): Type of the user variable
            value (:obj:`str`, optional): Value of the user variable
        """
        if isinstance(server, Server) and server.exists():
            self._server = server
        else:
            self._server = None
        if server is not None and len(name) > 0:
            self._server = server
            self._name = name
            if type in self._vtype2num:
                self._type = type
                self._typenum = self._vtype2num[type]
            else:
                self._type = ""
                self._typenum = ""
            self._value = self.__value(self._type, value)
            self._api = self._server.api
            self._idx = None
            self._lastupdate = ""
            self.__getvar()

    def __str__(self):
        return "{}({}, {}: \"{}\", \"{}\", \"{}\")".format(self.__class__.__name__, str(self._server), self._idx, self._name,
                                                       self._type, self._value)

    # ..........................................................................
    # Private methods
    # ..........................................................................

    def __getvar(self):
        # /json.htm?type=command&param=getuservariables
        self._api.querystring = "type=command&param={}".format(
            self._param_get_user_variables)
        self._api.call()
        if self._api.result:
            for var in self._api.result:
                if var.get("Name") == self._name:
                    self._idx = var.get("idx")
                    self._value = var.get("Value")
                    self._type = self._vtype2string[var.get("Type")]
                    self._lastupdate = var.get("LastUpdate")
                    break

    def __value(self, type, value):
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
    # Public methods
    # ..........................................................................
    def exists(self):
        if self._idx is None:
            return False
        else:
            return True

    # /json.htm?type=command&param=saveuservariable&vname=NAME&vtype=TYPE&vvalue=VALUE
    def add(self):
        if not self.exists():
            if len(self._name) > 0 and len(self._type) > 0 and len(self._value) > 0:
                self._api.querystring = "type=command&param={}&vname={}&vtype={}&vvalue={}".format(
                    self._param_add_user_variable,
                    self._name,
                    self._typenum,
                    self._value)
                self._api.call()
                if self._api.status == self._api.OK:
                    self.__getvar()

    # /json.htm?type=command&param=updateuservariable&idx=IDX&vname=NAME&vtype=TYPE&vvalue=VALUE
    def update(self):
        if self.exists():
            self._api.querystring = "type=command&param={}&idx={}&vname={}&vtype={}&vvalue={}".format(
                self._param_update_user_variable,
                self._idx,
                self._name,
                self._typenum,
                self._value)
            self._api.call()
            self.__getvar()

    # /json.htm?type=command&param=deleteuservariable&idx=IDX
    def delete(self):
        if self.exists():
            self._api.querystring = "type=command&param={}&idx={}".format(
                self._param_delete_user_variable,
                self._idx)
            self._api.call()
        self._idx = None

    # ..........................................................................
    # Properties
    # ..........................................................................
    @property
    def api(self):
        return self._api

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
    def server(self):
        return self._server

    @property
    def type(self):
        return self._type

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = self.__value(self._type, value)
