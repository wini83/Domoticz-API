#!/usr/bin/env python
# -*- coding: utf-8 -*-
import DomoticzAPI as dom
from datetime import datetime

def main():
    server = dom.Server(address="192.168.0.13")
    print(server)
    print("Server = " + server.server)
    print("ServerDT = " + str(server.server_dt))
    print("Sunrise = " + server.sunrise)
    print("Sunset = " + server.sunset)
    print("SunsetDT = " + str(server.sunset_dt))
    print("Status = " + server.status)
    print("Title = " + server.title)
    server.logmessage("Test")
    print("Status = " + server.status)
    print("Title = " + server.title)

if __name__ == "__main__":
    main()
