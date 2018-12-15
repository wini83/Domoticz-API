#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    API class
    To maintain status of the API calls
"""
import json
import subprocess


class API:

    URL = "json.htm"

    TYPE = "type={}"

    RESULT = "result"
    MESSAGE = "message"
    STATUS = "status"
    TITLE = "title"

    OK = "OK"
    ERROR = "ERR"

    def __init__(self, server):
        self._message = None
        self._querystring = None
        self._payload = None
        self._server = server
        self._status = self.ERROR
        self._title = None

    def __str__(self):
        return "{}({}): {}-{}-{}".format(self.__class__.__name__, self.url, self._title, self._status, self._message)

    # ..........................................................................
    # Public methods
    # ..........................................................................
    def call(self):
        if self._server is not None:
            command = "curl"
            if self._server._rights == self._server._rights_login_required:
                command += " -u {}:{}".format(self._server._user,
                                              self._server._password)
            command += " -s -X GET \"http://{}:{}/{}?{}\"".format(
                self._server._address, self._server._port, self.URL, self._querystring)
            try:
                p = subprocess.Popen(
                    command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                p.wait()
                data, errors = p.communicate()
                if p.returncode != 0:
                    r = None
                else:
                    r = json.loads(data.decode("utf-8", "ignore"))
                self._data = r
                self._message = r.get(self.MESSAGE)
                self._payload = r.get(self.RESULT)
                self.status = r.get(self.STATUS)
                self._title = r.get(self.TITLE)
            except:
                self._data = {}
                self._message = "Invalid call"
                self._payload = None
                self.status = None
                self._title = None

    # ..........................................................................
    # Properties
    # ..........................................................................
    @property
    def data(self):
        return self._data

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = value

    @property
    def payload(self):
        return self._payload

    @property
    def querystring(self):
        return self._querystring

    @querystring.setter
    def querystring(self, value):
        self._querystring = value

    # Obsolete!
    @property
    def result(self):
        return self._payload

    @property
    def server(self):
        return self._server

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if value is None:
            self._status = self.ERROR
        else:
            # Sometimes ERROR is returned, so truncated to first 3 characters
            self._status = value[:3]

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def url(self):
        return "http://{}:{}/{}?{}".format(self._server._address, self._server._port, self.URL, self._querystring)
