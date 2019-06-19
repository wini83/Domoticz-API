#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------------
# Look in Domoticz log for the results
# --------------------------------------------------------------------------------
import DomoticzAPI as dom


def main():
    print("********************************************************************************")
    print("Test script ........... : {}".format(__file__))
    print("********************************************************************************")
    server = dom.Server()
    print("Server: {}".format(server))
    
    dom.Notification(server,
                     subject="Test '1' subject",
                     body="Hello World!"
                     ).send()

    print("{}: {} - {}".format("Test '1'",
                               server.api.status,
                               server.api.title)
          )

    notification = dom.Notification(
        server,
        subject="Test 2 subject",
        body="Test body")
    notification.send()

    print("{}: {} - {}".format(notification,
                               server.api.status,
                               server.api.title)
          )

    notification.subject = "Test 3 only for Kodi"
    notification.body = "Hello Kodi's"
    notification.subsystem = "kodi"
    notification.send()

    print("{}: {} - {}".format(notification,
                               server.api.status,
                               server.api.title)
          )


if __name__ == "__main__":
    main()
