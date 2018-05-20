#!/usr/bin/env python
# -*- coding: utf-8 -*-
import DomoticzAPI as dom
from datetime import datetime

def main():
    print("DomoticzAPI: {}\n".format(dom.version()))

    # server = dom.Server(address="192.168.0.13")
    server = dom.Server()
    print("{}: {} - {}".format(server, server.api_status, server.api_title))
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
    print("{}: {} - {}".format(server, server.api_status, server.api_title))
    server.logmessage("Test 1")
    print("querystring: {}".format(server.api_querystring))
    print("{}: {} - {}".format(server, server.api_status, server.api_title))

if __name__ == "__main__":
    main()
