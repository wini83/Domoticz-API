#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .server import Server
from .api import API
from urllib.parse import quote

"""
    Notification
"""


class Notification:

    _param_notification = "sendnotification"

    _subsystems = {
        "gcm",
        "http",
        "kodi",
        "lms",
        "nma",
        "prowl",
        "pushalot",
        "pushbullet",
        "pushover",
        "pushsafer",
        "telegram",
    }

    def __init__(self, server, subject=None, body=None, subsystem=None):
        if isinstance(server, Server) and server.exists():
            self._server = server
        else:
            self._server = None
        self._subject = subject
        self._body = body
        if subsystem in self._subsystems:
            self._subsystem = subsystem
        else:
            self._subsystem = None
        self._api = self._server.api

    def __str__(self):
        return "{}({})".format(self.__class__.__name__, self._subject)

    # ..........................................................................
    # Private methods
    # ..........................................................................

    # ..........................................................................
    # Public methods
    # ..........................................................................

    def send(self):
        # /json.htm?type=command&param=sendnotification&subject=SUBJECT&body=THEBODY
        # /json.htm?type=command&param=sendnotification&subject=SUBJECT&body=THEBODY&subsystem=SUBSYSTEM
        if self._server is not None and self._subject is not None and self._body is not None:
            self._api.querystring = "type=command&param={}&subject={}&body={}".format(
                self._param_notification,
                quote(self._subject),
                quote(self._body)
            )
            if self._subsystem is not None:
                self._api.querystring += "&subsystem={}".format(
                    self._subsystem)
            self._api.call()

    # ..........................................................................
    # Properties
    # ..........................................................................
    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, value):
        self._body = value

    @property
    def server(self):
        return self._server

    @property
    def subject(self):
        return self._subject

    @subject.setter
    def subject(self, value):
        self._subject = value

    @property
    def subsystem(self):
        return self._subsystem

    @subsystem.setter
    def subsystem(self, value):
        if value in self._subsystems:
            self._subsystem = value
        else:
            self._subsystem = None
