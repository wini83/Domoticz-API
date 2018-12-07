#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import DomoticzAPI as dom
from datetime import datetime
import os


def main():
    print("********************************************************************************")
    print("Test script ........... : {}".format(os.path.basename(__file__)))
    print("********************************************************************************")

    server = dom.Server()
    if server.api.status == server.api.OK:
        print("Servertime ............... : {}".format(server.servertime))
        print("ServertimeDT ............. : {}".format(server.servertime_dt))
        print("Sunrise .................. : {}".format(server.sunrise))
        print("Sunset ................... : {}".format(server.sunset))
        print("SunsetDT ................. : {}".format(server.sunset_dt))
        print("\n")
        print("server.api ............... : {}".format(server.api))
        print("server.api.data .......... : {}".format(server.api.data))
        print("server.api.message ....... : {}".format(server.api.message))
        print("server.api.querystring ... : {}".format(server.api.querystring))
        print("server.api.payload ....... : {}".format(server.api.payload))
        print("server.api.status ........ : {}".format(server.api.status))
        print("server.api.title ......... : {}".format(server.api.title))
    else:
        print("Server not found!!!")
        print(server.api.message)


if __name__ == "__main__":
    main()
