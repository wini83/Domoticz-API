#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#from .const import(RETURN_EMPTY, RETURN_ERROR, RETURN_OK)
from .api import API
from .setting import Setting
from .translation import Translation
import json
from datetime import datetime


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

    _param_downloadupdate = "downloadupdate"
    _param_downloadready = "downloadready"
    _param_execute_script = "execute_script"

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
        if self._api.status == self._api.OK:
            self._exists = True
        else:
            self._exists = False
        if self._rights == self.RIGHTS_LOGGED_IN or (
                self._rights == self.RIGHTS_LOGIN_REQUIRED and self._user is not None):
            # No need to initialize all time properties. Next procedures will do that.
            self._getVersion()
            if self._rights == self.RIGHTS_LOGIN_REQUIRED and self._domoticzupdateurl is None:
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
        self._domoticzupdateurl = self._api.data.get("DomoticzUpdateURL")
        self._dzvents_version = self._api.data.get("dzvents_version")
        self._hash = self._api.data.get("hash")
        self._haveupdate = self._api.data.get("HaveUpdate")
        self._python_version = self._api.data.get("python_version")
        self._revision = self._api.data.get("Revision")
        self._systemname = self._api.data.get("SystemName")
        self._version = self._api.data.get("version")

    def _checkForUpdate(self):
        # /json.htm?type=command&param=checkforupdate
        self._api.querystring = "type=command&param={}&forced=true".format(
            self._param_checkforupdate)
        self._api.call()
        self._domoticzupdateurl = self._api.data.get("DomoticzUpdateURL")
        self._haveupdate = self._api.data.get("HaveUpdate")
        self._revision = self._api.data.get("Revision")
        self._systemname = self._api.data.get("SystemName")
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
            self._astrtwilightend = self._api.data.get("AstrTwilightEnd")
            self._astrtwilightstart = self._api.data.get("AstrTwilightStart")
            self._civtwilightend = self._api.data.get("CivTwilightEnd")
            self._civtwilightstart = self._api.data.get("CivTwilightStart")
            self._nauttwilightend = self._api.data.get("NautTwilightEnd")
            self._nauttwilightstart = self._api.data.get("NautTwilightStart")
            self._sunrise = self._api.data.get("Sunrise")
            self._sunset = self._api.data.get("Sunset")
            self._sunatsouth = self._api.data.get("SunAtSouth")
            self._daylength = self._api.data.get("DayLength")
            self._servertime = self._api.data.get("ServerTime")
            # Remember the datetime from this call
            if self._api.status == self._api.OK:
                self._currentdate = self._servertime[:10]  # yyyy-mm-dd
                self._currentdate_dt = datetime.strptime(
                    self._servertime, "%Y-%m-%d %H:%M:%S").date()
            else:
                self._currentdate = None
                self._currentdate_dt = None
            # Calculate acttime
            d = datetime.utcnow()
            epoch = datetime(1970, 1, 1)
            self._acttime = int((d - epoch).total_seconds())

    def _getConfig(self):
        # /json.htm?type=command&param=getconfig
        # Not required yet. May be interesting to get latitude and longitude. Most is GUI stuff.
        pass

    def _setSettings(self):
        # /storesettings.webem
        # To store settings?
        pass

    # ..........................................................................
    # Public Methods
    # ..........................................................................
    def checkForUpdate(self):
        """
        Retrieves Domoticz version information
        """
        self._checkForUpdate()

    def exists(self):
        """ Check if Domoticz server exists """
        return self._exists

    def logmessage(self, text):
        """
            Send text to the Domoticz log
        """
        # /json.htm?type=command&param=addlogmessage&message=MESSAGE
        if self.exists():
            self._api.querystring = "type=command&param={}&message={}".format(
                self._param_log,
                text
            )
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

    def update(self):
        """Update the Domoticz software"""
        self._checkForUpdate()
        if self._haveupdate:
            # /json.htm?type=command&param=downloadupdate
            self._api.querystring = "type=command&param={}".format(
                self._param_downloadupdate
            )
            self._api.call()
            if self._api.status == self._api.OK:
                # Wait until download is completed
                condition = False
                while not condition:
                    # /json.htm?type=command&param=downloadready
                    self._api.querystring = "type=command&param={}".format(
                        self._param_downloadready
                    )
                    self._api.call()
                    condition = self._api.data.get("downloadok", False)
                # Download complete: update the software
                self._api.querystring = "type=command&param={}&scriptname=update_domoticz&direct=false".format(
                    self._param_execute_script
                )
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
    def act_time(self):
        """Current date time on the Domoticz server expressed as condensed UTC-label.
        Also returned from device calls, together with the getSunRiseSet values.
        """
        self._getSunRiseSet(True)
        return self._acttime

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
        return self._astrtwilightend

    @property
    def astrtwilightend_dt(self):
        return datetime.strptime(self._currentdate + " " + self._astrtwilightend, "%Y-%m-%d %H:%M")

    @property
    # getSunRiseSet
    def astrtwilightstart(self):
        self._getSunRiseSet()
        return self._astrtwilightstart

    @property
    def astrtwilightstart_dt(self):
        return datetime.strptime(self._currentdate + " " + self._astrtwilightstart, "%Y-%m-%d %H:%M")

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
        return self._civtwilightend

    @property
    def civtwilightend_dt(self):
        return datetime.strptime(self._currentdate + " " + self._civtwilightend, "%Y-%m-%d %H:%M")

    @property
    # getSunRiseSet
    def civtwilightstart(self):
        self._getSunRiseSet()
        return self._civtwilightstart

    @property
    def civtwilightstart_dt(self):
        return datetime.strptime(self._currentdate + " " + self._civtwilightstart, "%Y-%m-%d %H:%M")

    @property
    # getSunRiseSet
    def daylength(self):
        self._getSunRiseSet()
        return self._daylength

    @property
    # getversion & checkforupdate
    def domoticzupdateurl(self):
        return self._domoticzupdateurl

    @property
    # getversion
    def dzvents_version(self):
        return self._dzvents_version

    @property
    # getversion & checkforupdate
    def haveupdate(self):
        return self._haveupdate

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
        return self._nauttwilightend

    @property
    def nauttwilightend_dt(self):
        return datetime.strptime(self._currentdate + " " + self._nauttwilightend, "%Y-%m-%d %H:%M")

    @property
    # getSunRiseSet
    def nauttwilightstart(self):
        self._getSunRiseSet()
        return self._nauttwilightstart

    @property
    def nauttwilightstart_dt(self):
        return datetime.strptime(self._currentdate + " " + self._nauttwilightstart, "%Y-%m-%d %H:%M")

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
        return self._revision

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
        return self._servertime

    @property
    def servertime_dt(self):
        return datetime.strptime(self._servertime, "%Y-%m-%d %H:%M:%S") if self._api.status == self._api.OK else None

    @property
    # checkforupdate
    def statuscode(self):
        return self._statuscode

    @property
    # getSunRiseSet
    def sunatsouth(self):
        self._getSunRiseSet()
        return self._sunatsouth

    @property
    def sunatsouth_dt(self):
        return datetime.strptime(self._currentdate + " " + self._sunatsouth,
                                 "%Y-%m-%d %H:%M") if self._api.status == self._api.OK else None

    @property
    # getSunRiseSet
    def sunrise(self):
        self._getSunRiseSet()
        return self._sunrise

    @property
    def sunrise_dt(self):
        return datetime.strptime(self._currentdate + " " + self._sunrise,
                                 "%Y-%m-%d %H:%M") if self._api.status == self._api.OK else None

    @property
    # getSunRiseSet
    def sunset(self):
        self._getSunRiseSet()
        return self._sunset

    @property
    def sunset_dt(self):
        return datetime.strptime(self._currentdate + " " + self._sunset,
                                 "%Y-%m-%d %H:%M") if self._api.status == self._api.OK else None

    @property
    # getversion & checkforupdate
    def systemname(self):
        return self._systemname

    @property
    def translation(self):
        return self._translation

    @property
    # getversion
    def version(self):
        return self._version
