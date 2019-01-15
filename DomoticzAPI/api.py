#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    API class
    To maintain status of the API calls
"""
import urllib.request
import base64
import json


class API:

    # type parameter
    TYPE = "type={}"
    TYPE_COMMAND = TYPE.format("command")

    PARAM = "param={}"
    IDX = "idx={}"

    TYPE_COMMAND_PARAM = "{}&{}".format(TYPE_COMMAND, PARAM)

    # Constants used by api
    URL = "json.htm"

    RESULT = "result"
    MESSAGE = "message"
    STATUS = "status"
    TITLE = "title"

    OK = "OK"
    ERROR = "ERR"
    UNKNOWN = "???"

    RESULTS = [OK, ERROR, UNKNOWN]

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
            req = urllib.request.Request("http://{}:{}/{}?{}".format(
                self._server._address,
                self._server._port,
                self.URL,
                self._querystring))
            if self._server._rights == self._server._rights_login_required:
                base64string = base64.encodestring(("{}:{}".format(
                    self._server._user,
                    self._server._password)).encode()).decode().replace("\n", "")
                req.add_header("Authorization",
                               "Basic {}".format(base64string))
            try:
                response = urllib.request.urlopen(req).read()
                data = json.loads(response.decode("utf-8"))
                self._data = data
                self._message = data.get(self.MESSAGE)
                self._payload = data.get(self.RESULT)
                self.status = data.get(self.STATUS)  # set correct value
                self._title = data.get(self.TITLE)
            except:
                self._data = {}
                self._message = "Invalid call"
                self._payload = None
                self._status = None
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
            value = value[:3]
            if value in self.RESULTS:
                self._status = value
            else:
                self._status = self.ERROR

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def url(self):
        return "http://{}:{}/{}?{}".format(self._server._address, self._server._port, self.URL, self._querystring)
