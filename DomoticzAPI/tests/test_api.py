#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import DomoticzAPI as dom
from datetime import datetime


def main():
    print("********************************************************************************")
    print("Test script ........... : {} ({})".format(__file__, dom.VERSION))
    print("********************************************************************************")

    server = dom.Server()
    if server.exists():
        print("\r")
        print("--------------------------------------------------------------------------------")
        print("Current values")
        print("--------------------------------------------------------------------------------")
        print("server.servertime ........ : {}".format(server.servertime))
        print("server.servertime_dt ..... : {}".format(server.servertime_dt))
        print("server.sunrise ........... : {}".format(server.sunrise))
        print("server.sunset ............ : {}".format(server.sunset))
        print("server.sunset_dt ......... : {}".format(server.sunset_dt))
        print("\r")
        print("--------------------------------------------------------------------------------")
        print("Current properties")
        print("--------------------------------------------------------------------------------")
        print("server.api ............... : {}".format(server.api))
        print("server.api.data .......... : {}".format(server.api.data))
        print("server.api.message ....... : {}".format(server.api.message))
        print("server.api.payload ....... : {}".format(server.api.payload))
        print("server.api.querystring ... : {}".format(server.api.querystring))
        print("server.api.status ........ : {}".format(server.api.status))
        print("server.api.title ......... : {}".format(server.api.title))
        print("server.api.url ........... : {}".format(server.api.url))
        print("\r")
        print("--------------------------------------------------------------------------------")
        print("Setting properties")
        print("--------------------------------------------------------------------------------")
        print("server.api.message         = test")
        server.api.message = "test"
        print("server.api.message ....... : {}".format(server.api.message))
        print("server.api.status          = test")
        server.api.status = "test"
        print("server.api.status ........ : {}".format(server.api.status))
        print("server.api.title           = test")
        server.api.title = "test"
        print("server.api.title ......... : {}".format(server.api.title))
        print("server.api.querystring     = type=command&param=getversion")
        server.api.querystring = "type=command&param=getversion"
        print("server.api.querystring ... : {}".format(server.api.querystring))
        print("\r")
        print("--------------------------------------------------------------------------------")
        print("Call methods")
        print("--------------------------------------------------------------------------------")
        print("Method ................... : {} with {}".format(
            "call", server.api.querystring))
        server.api.call()
        print("\r")
        print("--------------------------------------------------------------------------------")
        print("New properties")
        print("--------------------------------------------------------------------------------")
        print("server.api ............... : {}".format(server.api))
        print("server.api.data .......... : {}".format(server.api.data))
        print("server.api.message ....... : {}".format(server.api.message))
        print("server.api.payload ....... : {}".format(server.api.payload))
        print("server.api.querystring ... : {}".format(server.api.querystring))
        print("server.api.status ........ : {}".format(server.api.status))
        print("server.api.title ......... : {}".format(server.api.title))
        print("server.api.url ........... : {}".format(server.api.url))
        print("version .................. : {}".format(server.api.data.get("version")))
    else:
        print("Server not found!!!")
        print(server.api.message)


if __name__ == "__main__":
    main()
