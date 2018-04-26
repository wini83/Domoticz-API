#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
