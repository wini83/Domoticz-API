#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
import subprocess
from datetime import datetime
from urllib.parse import quote

"""
    Server
"""


class Server:
    """
    The Server class represents the Domoticz server
    """
    # Responses
    _return_ok = "OK"
    _return_error = "ERR"
    _return_empty = ""

    # type parameter
    _type = "type"
    _type_command = "command"

    _url_command = "{}={}&".format(_type, _type_command)

    # param parameter
    _param = "param={}"
    _param_checkforupdate = "checkforupdate"
    _param_execute_script = "execute_script"
    _param_getauth = "getauth"
    _param_log = "addlogmessage"
    _param_reboot = "system_reboot"
    _param_shutdown = "system_shutdown"
    _param_sun = "getSunRiseSet"
    _param_version = "getversion"

    # rights
    _rights_login_required = -1
    _rights_not_defined = 0
    _rights_logged_in = 2

    def __init__(self, address="127.0.0.1", port="8080", **kwargs):
        self._address = address
        self._api_status = self._return_error
        self._port = port
        self._user = kwargs.get("user")
        self._password = kwargs.get("password")
        self._rights = self._rights_not_defined
        self._api_message = self._return_empty
        self._url = "http://{}:{}/json.htm?".format(self._address, self._port)
        self._currentdate_dt = None
        # Check if authorization is required
        self._getAuth()
        if self._rights == self._rights_logged_in or (
                self._rights == self._rights_login_required and self._user is not None):
            # No need to initialize all time properties. Next procedures will do that.
            self._getVersion()
            if self._rights == self._rights_login_required and self._DomoticzUpdateURL is None:
                self._api_status = self._return_error
                self._api_message = "Invalid login"
            else:
                self._checkForUpdate()
                self._getSunRiseSet(True)
        else:
            self._api_status = self._return_error
            self._api_message = "Authorization is required"

    def __str__(self):
        txt = "{}(\"{}\", \"{}\")".format(
            self.__class__.__name__, self._address, self._port)
        return txt

    # ..........................................................................
    # Private methods
    # ..........................................................................
    def _getAuth(self):
        # json.htm?type=command&param=getauth
        querystring = self._param.format(self._param_getauth)
        self._api_querystring = querystring
        res = self._call_command(querystring)
        if res is None:
            self._api_status = self._return_error
            self._api_title = "getAuth"
        else:
            self._rights = res.get("rights")
            self._set_status(res)

    def _getVersion(self):
        # json.htm?type=command&param=getversion
        querystring = self._param.format(self._param_version)
        self._api_querystring = querystring
        res = self._call_command(querystring)
        self._build_time = res.get("build_time")
        self._DomoticzUpdateURL = res.get("DomoticzUpdateURL")
        self._dzvents_version = res.get("dzvents_version")
        self._hash = res.get("hash")
        self._HaveUpdate = res.get("HaveUpdate")
        self._python_version = res.get("python_version")
        self._Revision = res.get("Revision")
        self._SystemName = res.get("SystemName")
        self._version = res.get("version")
        self._set_status(res)

    def _checkForUpdate(self):
        # json.htm?type=command&param=checkforupdate
        querystring = self._param.format(self._param_checkforupdate)
        self._api_querystring = querystring
        res = self._call_command(querystring)
        self._DomoticzUpdateURL = res.get("DomoticzUpdateURL")
        self._HaveUpdate = res.get("HaveUpdate")
        self._Revision = res.get("Revision")
        self._SystemName = res.get("SystemName")
        self._statuscode = res.get("statuscode")
        self._set_status(res)

    def _getSunRiseSet(self, now=False):
        # json.htm?type=command&param=getSunRiseSet
        if isinstance(self._currentdate_dt, datetime):
            if datetime.now().date() > self._currentdate_dt:
                now = True
        if now:
            querystring = self._param.format(self._param_sun)
            self._api_querystring = querystring
            res = self._call_command(querystring)
            self._ActTime = res.get("ActTime")
            self._AstrTwilightEnd = res.get("AstrTwilightEnd")
            self._AstrTwilightStart = res.get("AstrTwilightStart")
            self._CivTwilightEnd = res.get("CivTwilightEnd")
            self._CivTwilightStart = res.get("CivTwilightStart")
            self._NautTwilightEnd = res.get("NautTwilightEnd")
            self._NautTwilightStart = res.get("NautTwilightStart")
            self._Sunrise = res.get("Sunrise")
            self._Sunset = res.get("Sunset")
            self._SunAtSouth = res.get("SunAtSouth")
            self._DayLength = res.get("DayLength")
            self._ServerTime = res.get("ServerTime")
            self._set_status(res)

    def _getConfig(self):
        # json.htm?type=command&param=getconfig
        # Not required yet. May be interesting to get latitude and longitude. Most is GUI stuff.
        pass

    def _call_command(self, text):
        return self._call_api(self._url_command + text)

    def _call_api(self, text):
        return self.__call_url(self._url + text, "", "")

    def __call_url(self, url, username="", password=""):
        command = "curl"
        if self._rights == self._rights_login_required:
            command += " -u {}:{}".format(self._user, self._password)
        command += " -s -X GET"
        options = "'" + url + "'"
        try:
            res = self.os_command(command, options)
            if res is not None:
                res = json.loads(res)
            return res
        except:
            self._api_status = self._return_error
            self._api_message = "Invalid call"

    def _set_status(self, r):
        self._api_status = r.get("status", self._return_error)
        self._api_title = r.get("title", self._return_empty)
        self._api_message = r.get("message", self._return_empty)

    # ..........................................................................
    # Global methods
    # ..........................................................................

    def checkForUpdate(self):
        """
        Retrieves Domoticz version information
        """
        self._checkForUpdate()

    def exists(self):
        # Unable to use something else?
        return self._api_status == self._return_ok

    def logmessage(self, text):
        """
            Send text to the Domoticz log
        """
        if self.exists():
            querystring = self._param.format(
                self._param_log) + "&message={}".format(quote(text))
            self._api_querystring = querystring
            res = self._call_command(querystring)
            self._set_status(res)

    def os_command(self, command, options=None):
        """
           Execute OS command and returns result. If an error occurs, None is returned 
        """
        try:
            if options is None:
                options = ""
            p = subprocess.Popen(command + " " + options, shell=True,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            p.wait()
            data, errors = p.communicate()
            if p.returncode != 0:
                result = None
            else:
                result = data.decode("utf-8", "ignore")
        except:
            result = None
        return result

    def reboot(self):
        if self.exists():
            querystring = self._param.format(self._param_reboot)
            self._api_querystring = querystring
            res = self._call_command(querystring)
            self._set_status(res)

    def shutdown(self):
        if self.exists():
            querystring = self._param.format(self._param_shutdown)
            self._api_querystring = querystring
            res = self._call_command(querystring)
            self._set_status(res)

    # ..........................................................................
    # Properties
    # ..........................................................................
    # json.htm?type=command&param=getSunRiseSet
    #
    # Used undocumented url's:
    #
    # json.htm?type=command&param=getversion
    # json.htm?type=command&param=checkforupdate
    # ..........................................................................

    @property
    # Returned from device calls, together with the getSunRiseSet values
    def act_time(self):
        return self._ActTime

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        self._address = value

    @property
    def api_message(self):
        return self._api_message

    @property
    def api_status(self):
        return self._api_status

    @property
    def api_title(self):
        return self._api_title

    @property
    def api_querystring(self):
        return self._api_querystring

    @property
    # getSunRiseSet
    def astrtwilightend(self):
        self._getSunRiseSet()
        return self._AstrTwilightEnd

    @property
    def astrtwilightend_dt(self):
        return datetime.strptime(self._currentdate + " " + self._AstrTwilightEnd, "%Y-%m-%d %H:%M")

    @property
    # getSunRiseSet
    def astrtwilightstart(self):
        self._getSunRiseSet()
        return self._AstrTwilightStart

    @property
    def astrtwilightstart_dt(self):
        return datetime.strptime(self._currentdate + " " + self._AstrTwilightStart, "%Y-%m-%d %H:%M")

    @property
    # getversion
    def build_time(self):
        return self._build_time

    @property
    def build_time_dt(self):
        return datetime.strptime(self._build_time, "%Y-%m-%d %H:%M:%S") if self._api_status == self._return_ok else None

    @property
    # getSunRiseSet
    def civtwilightend(self):
        self._getSunRiseSet()
        return self._CivTwilightEnd

    @property
    def civtwilightend_dt(self):
        return datetime.strptime(self._currentdate + " " + self._CivTwilightEnd, "%Y-%m-%d %H:%M")

    @property
    # getSunRiseSet
    def civtwilightstart(self):
        self._getSunRiseSet()
        return self._CivTwilightStart

    @property
    def civtwilightstart_dt(self):
        return datetime.strptime(self._currentdate + " " + self._CivTwilightStart, "%Y-%m-%d %H:%M")

    @property
    # getSunRiseSet
    def daylength(self):
        self._getSunRiseSet()
        return self._DayLength

    @property
    # getversion & checkforupdate
    def domoticzupdateurl(self):
        return self._DomoticzUpdateURL

    @property
    # getversion
    def dzvents_version(self):
        return self._dzvents_version

    @property
    # getversion & checkforupdate
    def haveupdate(self):
        return self._HaveUpdate

    @property
    # getversion
    def hash(self):
        return self._hash

    @property
    # getSunRiseSet
    def nauttwilightend(self):
        self._getSunRiseSet()
        return self._NautTwilightEnd

    @property
    def nauttwilightend_dt(self):
        return datetime.strptime(self._currentdate + " " + self._NautTwilightEnd, "%Y-%m-%d %H:%M")

    @property
    # getSunRiseSet
    def nauttwilightstart(self):
        self._getSunRiseSet()
        return self._NautTwilightStart

    @property
    def nauttwilightstart_dt(self):
        return datetime.strptime(self._currentdate + " " + self._NautTwilightStart, "%Y-%m-%d %H:%M")

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, port):
        self._port = port

    @property
    # getversion
    def python_version(self):
        return self._python_version

    @property
    # getversion & checkforupdate
    def revision(self):
        return self._Revision

    @property
    # getauth
    def rights(self):
        return self._rights

    @property
    # getSunRiseSet
    def servertime(self):
        self._getSunRiseSet()
        if self._api_status == self._return_ok:
            self._currentdate = self._ServerTime[:10]  # yyyy-mm-dd
            self._currentdate_dt = datetime.strptime(
                self._ServerTime, "%Y-%m-%d %H:%M:%S").date()
        else:
            self._ServerTime = None
        return self._ServerTime

    @property
    def servertime_dt(self):
        return datetime.strptime(self._ServerTime, "%Y-%m-%d %H:%M:%S") if self._api_status == self._return_ok else None

    @property
    # checkforupdate
    def statuscode(self):
        return self._statuscode

    @property
    # getSunRiseSet
    def sunatsouth(self):
        self._getSunRiseSet()
        return self._SunAtSouth

    @property
    def sunatsouth_dt(self):
        return datetime.strptime(self._currentdate + " " + self._SunAtSouth,
                                 "%Y-%m-%d %H:%M") if self._api_status == self._return_ok else None

    @property
    # getSunRiseSet
    def sunrise(self):
        self._getSunRiseSet()
        return self._Sunrise

    @property
    def sunrise_dt(self):
        return datetime.strptime(self._currentdate + " " + self._Sunrise,
                                 "%Y-%m-%d %H:%M") if self._api_status == self._return_ok else None

    @property
    # getSunRiseSet
    def sunset(self):
        self._getSunRiseSet()
        return self._Sunset

    @property
    def sunset_dt(self):
        return datetime.strptime(self._currentdate + " " + self._Sunset,
                                 "%Y-%m-%d %H:%M") if self._api_status == self._return_ok else None

    @property
    # getversion & checkforupdate
    def systemname(self):
        return self._SystemName

    @property
    # getversion
    def version(self):
        return self._version
