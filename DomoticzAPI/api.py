#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request as request
import urllib.parse as parse
import base64
import json


class API:

    PROTOCOL_HTTP = "http"
    PROTOCOL_HTTPS = "https"
    PROTOCOLS = {
        PROTOCOL_HTTP,
        PROTOCOL_HTTPS,
    }

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
    RESULTS = {
        OK,
        ERROR,
        UNKNOWN,
    }

    def __init__(self, server):
        """ API class to maintain status of the API calls

            Args:
                server (:obj:`Server`): Domoticz server object where to maintain the device            
        """
        self._message = None
        self._querystring = None
        self._payload = None
        self._protocol = self.PROTOCOL_HTTP
        self._server = server
        self._status = self.UNKNOWN
        self._title = None

    def __str__(self):
        return "{}({}): {}-{}".format(self.__class__.__name__, self.url, self._title, self._status)

    # ..........................................................................
    # Public methods
    # ..........................................................................
    def call(self):
        """Call the Domoticz API"""
        if self._server is not None:
            req = request.Request(self.url)
            if self._server._rights == self._server.RIGHTS_LOGIN_REQUIRED:
                base64string = base64.encodestring(("{}:{}".format(
                    self._server._user,
                    self._server._password)).encode()).decode().replace("\n", "")
                req.add_header("Authorization",
                               "Basic {}".format(base64string))
            try:
                response = request.urlopen(req).read()
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

    def isOK(self):
        return self.status == self.OK

    # ..........................................................................
    # Properties
    # ..........................................................................
    @property
    def data(self):
        """ The complete response from the call """
        return self._data

    @property
    def message(self):
        """ Sometimes a message is returned """
        return self._message

    @message.setter
    def message(self, value):
        self._message = value

    @property
    def payload(self):
        """ The payload (result) part of the response """
        return self._payload

    @property
    def protocol(self):
        """ The protocol used for the call 
        
        Args:
            `str`: API.PROTOCOL_HTTP or API.PROTOCOL_HTTPS
        """
        return self._protocol

    @protocol.setter
    def protocol(self, value):
        if value in self.PROTOCOLS:
            self._protocol = value

    @property
    def querystring(self):
        """ The querystring used in the call """
        return self._querystring

    @querystring.setter
    def querystring(self, value):
        self._querystring = value

    @property
    def server(self):
        """ The Domoticz server """
        return self._server

    @property
    def status(self):
        """ The status in the response
        
        Args:
            `str`: API.OK, API.ERROR, or API.UNKNOWN
        """
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
                # Sometimes the status contains error text!!!
                self._status = self.ERROR

    @property
    def title(self):
        """ Title returned in the response """
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def url(self):
        """ The complete url used to call the Domoticz json/API """
        return ("{}://{}:{}/{}?{}".format(
            self._protocol,
            self._server._address,
            self._server._port,
            self.URL,
            parse.quote(self._querystring, safe="&=")))
