#!/usr/bin/env python
# -*- coding: utf-8 -*-
import DomoticzAPI as dom
from datetime import datetime

def main():
    # server = dom.Server(address="192.168.0.13", port="8080")
    server = dom.Server()
    print("{}: {} - {}".format(server, server.api_status, server.api_title))
    print("Domoticz version: " + server.version)
    print("Build time: " + str(server.build_time_dt))
    print("DomoticzUpdateURL: " + str(server.domoticzupdateurl))
    print("Update available: " + str(server.haveupdate))
    print("\nServer = " + server.servertime)
    print("ServerDT = " + str(server.servertime_dt))
    print("Sunrise = " + server.sunrise)
    print("Sunset = " + server.sunset)
    print("SunsetDT = " + str(server.sunset_dt))
    print("{}: {} - {}".format(server, server.api_status, server.api_title))
    server.logmessage("Test 1")
    print("querystring: {}".format(server.api_querystring))
    print("{}: {} - {}".format(server, server.api_status, server.api_title))
    # print(server.__dict__)
    res = server.os_command("/opt/vc/bin/vcgencmd", "measure_temp")
    print("CPU temperature: " + res.split("=")[1][:-3])

if __name__ == "__main__":
    main()
