#!/usr/bin/env python
# -*- coding: utf-8 -*-
import DomoticzAPI as dom
from datetime import datetime

def main():
    print("DomoticzAPI: {}\n".format(dom.version()))

    # server = dom.Server(address="192.168.0.13")
    server = dom.Server()
    print(server)
    print("Domoticz version: " + server.version)
    print("Build time: " + str(server.build_time_dt))
    print("DomoticzUpdateURL: " + str(server.domoticzupdateurl))
    print("Update available: " + str(server.haveupdate))
    if server.haveupdate:
        server.update()
        print("Domoticz version: " + server.version)
    print("\nServer = " + server.servertime)
    print("ServerDT = " + str(server.servertime_dt))
    print("Sunrise = " + server.sunrise)
    print("Sunset = " + server.sunset)
    print("SunsetDT = " + str(server.sunset_dt))
    print("API Status = " + server.api_status)
    print("API Title = " + server.api_title)
    server.logmessage("Test")
    print("API Status = " + server.api_status)
    print("API Title = " + server.api_title)

if __name__ == "__main__":
    main()
