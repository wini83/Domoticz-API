#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#from .const import(RETURN_EMPTY, RETURN_ERROR, RETURN_OK)
from .api import API
from .setting import Setting
from .translation import Translation
import json
from datetime import datetime
from urllib.parse import quote

"""
    Server
"""


class Server:

    DEFAULT_ADDRESS = "localhost"
    DEFAULT_PORT = "8080"
    DEFAULT_LANGUAGE = "en"

    # type parameter
    _type = "type"
    _type_command = "command"

    _url_command = "{}={}&".format(_type, _type_command)

    # param parameter
    _param = "param={}"
    _param_checkforupdate = "checkforupdate"
    _param_execute_script = "execute_script"
    _param_getauth = "getauth"
    _param_getlanguage = "getlanguage"
    _param_log = "addlogmessage"
    _param_reboot = "system_reboot"
    _param_shutdown = "system_shutdown"
    _param_sun = "getSunRiseSet"
    _param_version = "getversion"

    # rights
    RIGHTS_LOGIN_REQUIRED = -1
    RIGHTS_NOT_DEFINED = 0
    RIGHTS_LOGGED_IN = 2

    def __init__(self, address=DEFAULT_ADDRESS, port=DEFAULT_PORT, **kwargs):
        """The Server class represents the Domoticz server
            Args:
                address (:obj:`str`, optional): the IP-address or hostname of your Domoticz installation. Default = "localhost".
                port (:obj:`str`, optional): the port number of your Domoticz installation. Default = "8080"
                user (:obj:`str`, optional): the username to access Domoticz.
                password (:obj:`str`, optional): the password to access Domoticz.
        """
        self._address = address
        self._port = port
        self._user = kwargs.get("user")
        self._password = kwargs.get("password")
        self._rights = self.RIGHTS_NOT_DEFINED
        self._currentdate_dt = datetime.now().date()
        self._language = self.DEFAULT_LANGUAGE
        self._api = API(self)
        self._setting = Setting(self)
        # Check if authorization is required
        self._getAuth()
        if self._rights == self.RIGHTS_LOGGED_IN or (
                self._rights == self.RIGHTS_LOGIN_REQUIRED and self._user is not None):
            # No need to initialize all time properties. Next procedures will do that.
            self._getVersion()
            if self._rights == self.RIGHTS_LOGIN_REQUIRED and self._DomoticzUpdateURL is None:
                self._api.status = self._api.ERROR
                self._api.message = "Invalid login"
            else:
                self._checkForUpdate()
                self._getSunRiseSet(True)
        else:
            self._api.status = self._api.ERROR
            self._api.message = "Authorization is required"
        self._getLanguage()
        self._translation = Translation(self, language=self._language)

    def __str__(self):
        txt = "{}(\"{}\", \"{}\")".format(
            self.__class__.__name__, self._address, self._port)
        return txt

    def __getattr__(self, item):
        return None

    # ..........................................................................
    # Private methods
    # ..........................................................................
    def _getAuth(self):
        # /json.htm?type=command&param=getauth
        self._api.querystring = "type=command&param={}".format(
            self._param_getauth)
        self._api.call()
        if self._api.data:
            self._rights = self._api.data.get("rights")

    def _getVersion(self):
        # /json.htm?type=command&param=getversion
        self._api.querystring = "type=command&param={}".format(
            self._param_version)
        self._api.call()
        self._build_time = self._api.data.get("build_time")
        self._DomoticzUpdateURL = self._api.data.get("DomoticzUpdateURL")
        self._dzvents_version = self._api.data.get("dzvents_version")
        self._hash = self._api.data.get("hash")
        self._HaveUpdate = self._api.data.get("HaveUpdate")
        self._python_version = self._api.data.get("python_version")
        self._Revision = self._api.data.get("Revision")
        self._SystemName = self._api.data.get("SystemName")
        self._version = self._api.data.get("version")

    def _checkForUpdate(self):
        # /json.htm?type=command&param=checkforupdate
        self._api.querystring = "type=command&param={}".format(
            self._param_checkforupdate)
        self._api.call()
        self._DomoticzUpdateURL = self._api.data.get("DomoticzUpdateURL")
        self._HaveUpdate = self._api.data.get("HaveUpdate")
        self._Revision = self._api.data.get("Revision")
        self._SystemName = self._api.data.get("SystemName")
        self._statuscode = self._api.data.get("statuscode")

    def _getLanguage(self):
        # /json.htm?type=command&param=getlanguage
        self._api.querystring = "type=command&param={}".format(
            self._param_getlanguage)
        self._api.call()
        self._language = self._api.data.get("language")

    def _getSunRiseSet(self, now=False):
        # /json.htm?type=command&param=getSunRiseSet
        if isinstance(self._currentdate_dt, datetime):
            if datetime.now().date() > self._currentdate_dt:
                now = True
        if now:
            self._api.querystring = "type=command&param={}".format(
                self._param_sun)
            self._api.call()
            self._ActTime = self._api.data.get("ActTime")
            self._AstrTwilightEnd = self._api.data.get("AstrTwilightEnd")
            self._AstrTwilightStart = self._api.data.get("AstrTwilightStart")
            self._CivTwilightEnd = self._api.data.get("CivTwilightEnd")
            self._CivTwilightStart = self._api.data.get("CivTwilightStart")
            self._NautTwilightEnd = self._api.data.get("NautTwilightEnd")
            self._NautTwilightStart = self._api.data.get("NautTwilightStart")
            self._Sunrise = self._api.data.get("Sunrise")
            self._Sunset = self._api.data.get("Sunset")
            self._SunAtSouth = self._api.data.get("SunAtSouth")
            self._DayLength = self._api.data.get("DayLength")
            self._ServerTime = self._api.data.get("ServerTime")

    def _getConfig(self):
        # /json.htm?type=command&param=getconfig
        # Not required yet. May be interesting to get latitude and longitude. Most is GUI stuff.
        pass

    def _setSettings(self):
        # /storesettings.webem
        # To store settings?
        pass

    def checkForUpdate(self):
        """
        Retrieves Domoticz version information
        """
        self._checkForUpdate()

    def exists(self):
        # Unable to use something else?
        return self._api.status == self._api.OK

    def logmessage(self, text):
        """
            Send text to the Domoticz log
        """
        # /json.htm?type=command&param=addlogmessage&message=MESSAGE
        if self.exists():
            self._api.querystring = "type=command&param={}&message={}".format(
                self._param_log,
                quote(text))
            self._api.call()

    def reboot(self):
        """Reboot the Domoticz server"""
        # /json.htm?type=command&param=system_reboot
        if self.exists():
            self._api.querystring = "type=command&param={}".format(
                self._param_reboot)
            self._api.call()

    def shutdown(self):
        """Shutdown the Domoticz server"""
        # /json.htm?type=command&param=system_shutdown
        if self.exists():
            self._api.querystring = "type=command&param={}".format(
                self._param_shutdown)
            self._api.call()

    # ..........................................................................
    # Properties
    # ..........................................................................
    # /json.htm?type=command&param=getSunRiseSet
    #
    # Used undocumented url's:
    #
    # /json.htm?type=command&param=getversion
    # /json.htm?type=command&param=checkforupdate
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
    def api(self):
        return self._api

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
        return datetime.strptime(self._build_time, "%Y-%m-%d %H:%M:%S") if self._api.status == self._api.OK else None

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
    # getlanguage
    def language(self):
        return self._language

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
    def setting(self):
        return self._setting

    @property
    # getSunRiseSet
    def servertime(self):
        self._getSunRiseSet(True)
        if self._api.status == self._api.OK:
            self._currentdate = self._ServerTime[:10]  # yyyy-mm-dd
            self._currentdate_dt = datetime.strptime(
                self._ServerTime, "%Y-%m-%d %H:%M:%S").date()
        else:
            self._ServerTime = None
        return self._ServerTime

    @property
    def servertime_dt(self):
        return datetime.strptime(self._ServerTime, "%Y-%m-%d %H:%M:%S") if self._api.status == self._api.OK else None

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
                                 "%Y-%m-%d %H:%M") if self._api.status == self._api.OK else None

    @property
    # getSunRiseSet
    def sunrise(self):
        self._getSunRiseSet()
        return self._Sunrise

    @property
    def sunrise_dt(self):
        return datetime.strptime(self._currentdate + " " + self._Sunrise,
                                 "%Y-%m-%d %H:%M") if self._api.status == self._api.OK else None

    @property
    # getSunRiseSet
    def sunset(self):
        self._getSunRiseSet()
        return self._Sunset

    @property
    def sunset_dt(self):
        return datetime.strptime(self._currentdate + " " + self._Sunset,
                                 "%Y-%m-%d %H:%M") if self._api.status == self._api.OK else None

    @property
    # getversion & checkforupdate
    def systemname(self):
        return self._SystemName

    @property
    def translation(self):
        return self._translation

    @property
    # getversion
    def version(self):
        return self._version
