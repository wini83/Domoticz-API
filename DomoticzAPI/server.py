#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import subprocess
from datetime import datetime
from urllib.parse import quote

################################################################################
# Server                                                                       #
################################################################################
class Server:

    # Responses
    _return_ok = "OK"
    _return_error = "ERR"

    # type parameter
    _type = "type"
    _type_command = "command"

    # param parameter
    _param = "param={}"
    _param_shutdown = "system_shutdown"
    _param_reboot = "system_reboot"
    _param_sun = "getSunRiseSet"
    _param_log = "addlogmessage"

    _url_command = _type + "=" + _type_command + "&"

    def __init__(self, address="localhost", port="8080"):
        self._address = address
        self._port = port
        self._status = ""
        self._title = ""
        self._url = "http://" + self._address + ":" + self._port + "/json.htm?"
        self._currentdate_dt = None
        # No need to initialize all time properties. Next procedure will do that.
        self._getSunRiseSet(True)

    def __str__(self):
        txt = "{}(\"{}\", \"{}\")".format(self.__class__.__name__, self._address, self._port)
        return txt

    # ..........................................................................
    # Properties
    # ..........................................................................
    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, address):
        self._address = address

    @property
    def astrtwilightend(self):
        self._getSunRiseSet()
        return self._AstrTwilightEnd

    @property
    def astrtwilightend_dt(self):
        return datetime.strptime(self._currentdate + " " + self._AstrTwilightEnd, "%Y-%m-%d %H:%M")

    @property
    def astrtwilightstart(self):
        self._getSunRiseSet()
        return self._AstrTwilightStart

    @property
    def astrtwilightstart_dt(self):
        return datetime.strptime(self._currentdate + " " + self._AstrTwilightStart, "%Y-%m-%d %H:%M")

    @property
    def daylength(self):
        self._getSunRiseSet()
        return self._DayLength

    @property
    def civtwilightend(self):
        self._getSunRiseSet()
        return self._CivTwilightEnd

    @property
    def civtwilightend_dt(self):
        return datetime.strptime(self._currentdate + " " + self._CivTwilightEnd, "%Y-%m-%d %H:%M")

    @property
    def civtwilightstart(self):
        self._getSunRiseSet()
        return self._CivTwilightStart

    @property
    def civtwilightstart_dt(self):
        return datetime.strptime(self._currentdate + " " + self._CivTwilightStart, "%Y-%m-%d %H:%M")

    @property
    def nauttwilightend(self):
        self._getSunRiseSet()
        return self._NautTwilightEnd

    @property
    def nauttwilightend_dt(self):
        return datetime.strptime(self._currentdate + " " + self._NautTwilightEnd, "%Y-%m-%d %H:%M")

    @property
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
    def server(self):
        self._getSunRiseSet()
        if self._status == self._return_ok:
            self._currentdate = self._ServerTime[:10]  # yyyy-mm-dd
            self._currentdate_dt = datetime.strptime(self._ServerTime, "%Y-%m-%d %H:%M:%S").date()
        return self._ServerTime

    @property
    def server_dt(self):
        return datetime.strptime(self._ServerTime, "%Y-%m-%d %H:%M:%S") if self._status == self._return_ok else None

    @property
    def status(self):
        return self._status

    @property
    def sunatsouth(self):
        self._getSunRiseSet()
        return self._SunAtSouth

    @property
    def sunatsouth_dt(self):
        return datetime.strptime(self._currentdate + " " + self._SunAtSouth, "%Y-%m-%d %H:%M") if self._status == self._return_ok else None

    @property
    def sunrise(self):
        self._getSunRiseSet()
        return self._Sunrise

    @property
    def sunrise_dt(self):
        return datetime.strptime(self._currentdate + " " + self._Sunrise, "%Y-%m-%d %H:%M") if self._status == self._return_ok else None

    @property
    def sunset(self):
        self._getSunRiseSet()
        return self._Sunset

    @property
    def sunset_dt(self):
        return datetime.strptime(self._currentdate + " " + self._Sunset, "%Y-%m-%d %H:%M") if self._status == self._return_ok else None

    @property
    def title(self):
        return self._title

    # ..........................................................................
    # Global methods
    # ..........................................................................
    def logmessage(self, text):
        if self.exists():
            message = self._param.format(self._param_log) + "&message={}".format(quote(text))
            res = self._call_command(message)
            self._status = res["status"] if res.get("status") else ""
            self._title = res["title"] if self._status == self._return_ok else ""

    def reboot(self):
        if self.exists():
            message = self._param.format(self._param_reboot)
            res = self._call_command(message)
            self._status = res["status"] if res.get("status") else ""
            self._title = res["title"] if self._status == self._return_ok else ""

    def shutdown(self):
        if self.exists():
            message = self._param.format(self._param_shutdown)
            res = self._call_command(message)
            self._status = res["status"] if res.get("status") else ""
            self._title = res["title"] if self._status == self._return_ok else ""

    def exists(self):
        return self._status == self._return_ok

    # ..........................................................................
    # Private methods
    # ..........................................................................
    def _getSunRiseSet(self, now=False):
        if isinstance(self._currentdate_dt, datetime):
            if datetime.now().date() > self._currentdate_dt:
                now=True
        if now:
            message = self._param.format(self._param_sun)
            res = self._call_command(message)
            self._status = res["status"] if res.get("status") else ""
            self._AstrTwilightEnd = res["AstrTwilightEnd"] if res.get("AstrTwilightEnd") else ""
            self._AstrTwilightStart = res["AstrTwilightStart"] if res.get("AstrTwilightStart") else ""
            self._CivTwilightEnd = res["CivTwilightEnd"] if res.get("CivTwilightEnd") else ""
            self._CivTwilightStart = res["CivTwilightStart"] if res.get("CivTwilightStart") else ""
            self._NautTwilightEnd = res["NautTwilightEnd"] if res.get("NautTwilightEnd") else ""
            self._NautTwilightStart = res["NautTwilightStart"] if res.get("NautTwilightStart") else ""
            self._Sunrise = res["Sunrise"] if res.get("Sunrise") else ""
            self._Sunset = res["Sunset"] if res.get("Sunset") else ""
            self._SunAtSouth = res["SunAtSouth"] if res.get("SunAtSouth") else ""
            self._DayLength = res["DayLength"] if res.get("DayLength") else ""
            self._ServerTime = res["ServerTime"] if res.get("ServerTime") else ""
            self._title = res["title"] if res.get("title") else ""

    def _call_command(self, text):
        return self._call_api(self._url_command + text)

    def _call_api(self, text):
        return self.__call_url(self._url + text, "", "")

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
        try:
            command = "curl -s "
            options = "'" + url + "'"
            p = subprocess.Popen(command + " " + options, shell=True, stdout=subprocess.PIPE)
            p.wait()
            data, errors = p.communicate()
            if p.returncode != 0:
                pass
            res = json.loads(data.decode("utf-8", "ignore"))
        except:
            res = json.loads("{ \"status\" : \"ERR\" }")
        return res
