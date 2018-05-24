#!/usr/bin/env python
# -*- coding: utf-8 -*-
import DomoticzAPI as dom


def main():
    server = dom.Server()
    notification = dom.Notification(server)
    notification.subject = "Test"
    notification.body = "Hello World!"
    print(notification)
    notification.send()

    print("Result = {}".format(notification.api_status))
    notification.subject = "Test only for Kodi"
    notification.subsystem = "kodi"
    print(notification)
    notification.send()

    print("{}: {} - {}".format(notification, notification.api_status, notification.api_title))

if __name__ == "__main__":
    main()
