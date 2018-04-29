#!/usr/bin/env python
# -*- coding: utf-8 -*-
import DomoticzAPI as dom


def main():
    server = dom.Server(address="192.168.0.13")
    notification = dom.Notification(server)
    notification.subject = "Test"
    notification.body = "Hello World!"
    print(notification)
    notification.send()
    print("Result = {}".format(notification.status))
    notification.subject = "Test only for Kodi"
    notification.subsystem = "kodi"
    print(notification)
    notification.send()
    print("Result = {}".format(notification.status))
    print("Title = {}".format(notification.title))

if __name__ == "__main__":
    main()
