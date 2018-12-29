#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import DomoticzAPI as dom
from datetime import datetime


def main():
    print("********************************************************************************")
    print("Test script ........... : {}".format(__file__))
    print("********************************************************************************")

    server = dom.Server()
    if server.api.status == server.api.OK:
        print("server ................ : {}: {} - {}".format(server,
                                                             server.api.status,
                                                             server.api.title))
        print("Domoticz version ...... : {}".format(server.version))
        print("Build time ............ : {}".format(server.build_time_dt))
        print("DomoticzUpdateURL ..... : {}".format(server.domoticzupdateurl))
        print("Update available ...... : {}".format(server.haveupdate))
        print("\r")

        print("Servertime ............ : {}".format(server.servertime))
        print("ServertimeDT .......... : {}".format(server.servertime_dt))
        print("Sunrise ............... : {}".format(server.sunrise))
        print("Sunset ................ : {}".format(server.sunset))
        print("SunsetDT .............. : {}".format(server.sunset_dt))
        print("server ................ : {}: {} - {}".format(server,
                                                             server.api.status,
                                                             server.api.title))
        print("\r")

        server.logmessage("Test 1")
        print("querystring ........... : {}".format(server.api.querystring))
        print("server ................ : {}: {} - {}".format(server,
                                                             server.api.status,
                                                             server.api.title))
    else:
        print("Server not found!!!")
        print(server.api.message)


if __name__ == "__main__":
    main()
