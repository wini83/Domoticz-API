#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import DomoticzAPI as dom
from datetime import datetime


def main():
    print("********************************************************************************")
    print("Test script ........... : {}".format(__file__))
    print("********************************************************************************")

    server = dom.Server()
    if server.exists():
        print("server ................ : {}".format(server))
        print("Domoticz version ...... : {}".format(server.version))
        print("Build time ............ : {}".format(server.build_time_dt))
        print("DomoticzUpdateURL ..... : {}".format(server.domoticzupdateurl))
        print("Update available ...... : {}".format(server.haveupdate))
        print("\r")

        if server.haveupdate:
            server.update()

        print("--------------------------------------------------------------------------------")
        print("SunRiseSet")
        print("--------------------------------------------------------------------------------")
        print("Servertime ............ : {}".format(server.servertime))
        print("ServertimeDT .......... : {}".format(server.servertime_dt))
        print("Sunrise ............... : {}".format(server.sunrise))
        print("Sunset ................ : {}".format(server.sunset))
        print("SunsetDT .............. : {}".format(server.sunset_dt))
        print("\r")

        print("--------------------------------------------------------------------------------")
        print("Log message")
        print("--------------------------------------------------------------------------------")
        server.logmessage("Test 1")
        print("querystring ........... : {}".format(server.api.querystring))
        print("\r")

        print("--------------------------------------------------------------------------------")
        print("Settings")
        print("--------------------------------------------------------------------------------")
        print("AcceptNewHardware ..... : {}".format(
            server.setting.value("AcceptNewHardware")))
        print("Latitude .............. : {}".format(
            server.setting.value("Location").get("Latitude")))
        print("SecPassword ........... : {}".format(
            server.setting.value("SecPassword")))

    else:
        print("Server not found!!!")
        print(server.api.message)


if __name__ == "__main__":
    main()
