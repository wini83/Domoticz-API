#!/usr/bin/env python
# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------------
# Look in Domoticz log for the results
# --------------------------------------------------------------------------------
import DomoticzAPI as dom


def main():
    server = dom.Server()
    dom.Notification(server, subject="Test 1 subject", body="Hello World!").send()

    notification = dom.Notification(server, subject="Test 2 subject", body="Test body")
    notification.send()

    print("{}: {} - {}".format(notification, notification.api_status, notification.api_title))

    notification.subject = "Test 3 only for Kodi"
    notification.body = "Hello Kodi"
    notification.subsystem = "kodi"
    notification.send()

    print("{}: {} - {}".format(notification, notification.api_status, notification.api_title))


if __name__ == "__main__":
    main()
