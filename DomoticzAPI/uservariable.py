#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .server import Server
from .api import API
from datetime import datetime
from urllib.parse import quote


class UserVariable:
    """
        UserVariable(server, name, type, value)

        Args:
            server (Server): Domoticz server object where to maintain the user variable
            name (:obj:`str`): Name of the user variable
            type (:obj:`int`, optional): Type of the user variable (default = UVE_TYPE_STRING)
                UVE_TYPE_INTEGER    = Integer, e.g. -1, 1, 0, 2, 10
                UVE_TYPE_FLOAT      = Float, e.g. -1.1, 1.2, 3.1
                UVE_TYPE_STRING     = String
                UVE_TYPE_DATE       = Date in format DD/MM/YYYY
                UVE_TYPE_TIME       = Time in 24 hr format HH:MM
                UVE_TYPE_DATETIME   = DateTime (but the format is not checked)
            value (:obj:`str`, optional): Value of the user variable (default = None)
    """
    UVE_TYPE_INTEGER = 0
    UVE_TYPE_FLOAT = 1
    UVE_TYPE_STRING = 2
    UVE_TYPE_DATE = 3
    UVE_TYPE_TIME = 4
    UVE_TYPE_DATETIME = 5
    UVE_TYPES = [
        UVE_TYPE_INTEGER,
        UVE_TYPE_FLOAT,
        UVE_TYPE_STRING,
        UVE_TYPE_DATE,
        UVE_TYPE_TIME,
        UVE_TYPE_DATETIME,
    ]

    _param_get_user_variable = "getuservariable"
    _param_get_user_variables = "getuservariables"
    _param_add_user_variable = "adduservariable"
    _param_update_user_variable = "updateuservariable"
    _param_delete_user_variable = "deleteuservariable"

    _date = "%d/%m/%Y"
    _time = "%H:%M"

    def __init__(self, server, name, type=UVE_TYPE_STRING, value=None):
        if isinstance(server, Server) and server.exists():
            self._server = server
        else:
            self._server = None
        if server is not None and len(name) > 0:
            self._server = server
            self._name = name
            if type in self.UVE_TYPES:
                self._type = type
            else:
                self._type = None
            if value is not None:
                self._value = self.__value(self._type, value)
            else:
                self._value = None
            self._api = self._server.api
            self._idx = None
            self._lastupdate = None
            self.__getvar()
        print(self)

    def __str__(self):
        return "{}({}, {}: \"{}\", {}, \"{}\")".format(
            self.__class__.__name__,
            str(self._server),
            self._idx,
            self._name,
            self._type,
            self._value)

    # ..........................................................................
    # Private methods
    # ..........................................................................
    def __getvar(self):
        # /json.htm?type=command&param=getuservariables
        self._api.querystring = "type=command&param={}".format(
            self._param_get_user_variables)
        self._api.call()
        if self._api.status == self._api.OK and self._api.payload is not None:
            for var in self._api.payload:
                if var.get("Name") == self._name:
                    self._idx = int(var.get("idx"))
                    self._value = var.get("Value")
                    self._type = int(var.get("Type"))
                    self._lastupdate = var.get("LastUpdate")
                    break

    # /json.htm?type=command&param=updateuservariable&idx=IDX&vname=NAME&vtype=TYPE&vvalue=VALUE
    def __update(self):
        if self.exists():
            self._api.querystring = "type=command&param={}&idx={}&vname={}&vtype={}&vvalue={}".format(
                self._param_update_user_variable,
                self._idx,
                quote(self._name),
                self._type,
                quote(self._value))
            print(self._api.querystring)
            self._api.call()
            self.__getvar()

    def __value(self, type, value):
        if value is None:
            result = value
        elif type == self.UVE_TYPE_INTEGER:
            result = str(int(float(value)))
        elif type == self.UVE_TYPE_FLOAT:
            result = str(float(value))
        elif type == self.UVE_TYPE_DATE:
            try:
                dt = datetime.strptime(value, self._date)
            except:
                dt = None
            if dt is not None:
                result = dt.strftime(self._date)
            else:
                result = None
        elif type == self.UVE_TYPE_TIME:
            try:
                dt = datetime.strptime(value, self._time)
            except:
                dt = None
            if dt is not None:
                result = dt.strftime(self._time)
            else:
                result = None
        elif type == self.UVE_TYPE_DATETIME:
            try:
                dt = datetime.strptime(value, self._date + " " + self._time)
            except:
                dt = None
            if dt is not None:
                result = dt.strftime(self._date + " " + self._time)
            else:
                result = None
        elif type == self.UVE_TYPE_STRING:
            result = value
        else:  # string
            result = None
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
            if len(self._name) > 0 and self._type in self.UVE_TYPES and len(self._value) > 0:
                self._api.querystring = "type=command&param={}&vname={}&vtype={}&vvalue={}".format(
                    self._param_add_user_variable,
                    quote(self._name),
                    self._type,
                    quote(self._value))
                self._api.call()
                if self._api.status == self._api.OK:
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
        return int(self._idx) if self._idx is not None else None

    @property
    def lastupdate(self):
        return self._lastupdate

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        self.__update()

    @property
    def server(self):
        return self._server

    @property
    def type(self):
        return int(self._type) if self._type is not None else None

    @type.setter
    def type(self, value):
        if value in self.UVE_TYPES:
            self._type = value
            self.__update()

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = self.__value(self._type, value)
        self.__update()
