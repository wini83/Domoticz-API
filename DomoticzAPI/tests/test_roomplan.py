#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import DomoticzAPI as dom
import os


def main():
    print("********************************************************************************")
    print("Test script ........... : {}".format(os.path.basename(__file__)))
    print("********************************************************************************")
    server = dom.Server()
    # Or use an other number as can be found as planid in a device
    roomplan1 = dom.RoomPlan(server, idx=9999)
    print(roomplan1)
    print("api ................... : {}".format(server.api))
    print("querystring ........... : {}".format(server.api.querystring))
    print("exists ................ : {}".format(roomplan1.exists()))

    roomplan2 = dom.RoomPlan(server, name="RoomPlan2")
    print(roomplan2)
    print("Add roomplan2")
    roomplan2.add()
    print("exists ................ : {}".format(roomplan2.exists()))
    print("idx ................... : {}".format(roomplan2.idx))
    print("Name .................. : {}".format(roomplan2.name))
    print("Order ................. : {}".format(roomplan2.order))
    print("Devices ............... : {}".format(roomplan2.devices))
    print("Delete roomplan2")
    roomplan2.delete()
    print("exists ................ : {}".format(roomplan2.exists()))

if __name__ == "__main__":
    main()
