#!/usr/bin/env python
# -*- coding: utf-8 -*-
from urllib.parse import quote


################################################################################
# Notification                                                                 #
################################################################################
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
    }

    def __init__(self, server, subject=None, body=None, subsystem=None):
        self._server = server
        self._subject = subject
        self._body = body
        if subsystem in self._subsystems:
            self._subsystem = subsystem
        else:
            self._subsystem = None
        self._api_status = ""
        self._api_title = ""

    def __str__(self):
        return "{}({})".format(self.__class__.__name__, self._subject)

    # ..........................................................................
    # Properties
    # ..........................................................................

    @property
    def api_status(self):
        return self._api_status

    @property
    def api_title(self):
        return self._api_title

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

    # ..........................................................................
    # Public methods
    # ..........................................................................
    def send(self):
        if self._subject is not None and self._body is not None:
            querystring = self._server._param.format(self._param_notification) + "&subject={}&body={}".format(quote(self._subject), quote(self._body))
            if self._subsystem is not None:
                querystring += "&subsystem={}".format(self._subsystem)
            res = self._server._call_command(querystring)
            self._api_status = res.get("status", self._server._return_error)
            self._api_title = res.get("title", self._server._return_empty)
