#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import DomoticzAPI as dom
from datetime import datetime
import os


def main():
    print("********************************************************************************")
    print("Test script ........... : {}".format(os.path.basename(__file__)))
    print("********************************************************************************")

    # server = dom.Server(address="localhost", port="8080")
    server = dom.Server()
    # server = dom.Server(user="user", password="password")
    if server.api_status == server._return_ok:
        print("{}: {} - {}".format(server, server.api_status, server.api_title))
        print("Domoticz version ...... : {}".format(server.version))
        print("Build time ............ : {}".format(server.build_time_dt))
        print("DomoticzUpdateURL ..... : {}".format(server.domoticzupdateurl))
        print("Update available ...... : {}".format(server.haveupdate))
        print("\r")

        print("Server ................ : {}".format(server.servertime))
        print("ServerDT .............. : {}".format(server.servertime_dt))
        print("Sunrise ............... : {}".format(server.sunrise))
        print("Sunset ................ : {}".format(server.sunset))
        print("SunsetDT .............. : {}".format(server.sunset_dt))
        print("{}: {} - {}".format(server, server.api_status, server.api_title))
        server.logmessage("Test 1")
        print("querystring ........... : {}".format(server.api_querystring))
        print("{}: {} - {}".format(server, server.api_status, server.api_title))
        # print(server.__dict__)
        res = server.os_command("/opt/vc/bin/vcgencmd", "measure_temp")
        print("CPU temperature ....... : {}".format(res.split("=")[1][:-3]))
    else:
        print("Server not found!!!")
        print(server.api_message)


if __name__ == "__main__":
    main()
