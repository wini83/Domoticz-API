#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import DomoticzAPI as dom


def main():
    print("********************************************************************************")
    print("Test script ........... : {}".format(__file__))
    print("********************************************************************************")
    server = dom.Server()
    # Or use an other number as can be found as planid in a device
    roomplan1 = dom.RoomPlan(server, idx=2)
    print(roomplan1)
    print("api ................... : {}".format(server.api))
    print("querystring ........... : {}".format(server.api.querystring))
    print("exists ................ : {}".format(roomplan1.exists()))
    print("Devices ............... : {}".format(roomplan1.devices))
    
    dev = dom.Device(server, 61)
    print(dev)
    roomplan1.delete_device(dev)
    print("querystring ........... : {}".format(server.api.querystring))
    print("Devices ............... : {}".format(roomplan1.devices))
    roomplan1.add_device(dev)
    print("querystring ........... : {}".format(server.api.querystring))
    print("Devices ............... : {}".format(roomplan1.devices))

    roomplan2 = dom.RoomPlan(server, name="RoomPlan2")
    print(roomplan2)
    print("Add roomplan2")
    roomplan2.add()
    print("exists ................ : {}".format(roomplan2.exists()))
    print("idx ................... : {}".format(roomplan2.idx))
    print("Name .................. : {}".format(roomplan2.name))
    print("Order ................. : {}".format(roomplan2.order))
    print("Devices ............... : {}".format(roomplan2.devices))

    roomplan3 = dom.RoomPlan(server, name="XXX")
    roomplan3.name = "RoomPlan3"
    print("Add roomplan3")
    roomplan3.add()
    print("exists ................ : {}".format(roomplan3.exists()))
    print("idx ................... : {}".format(roomplan3.idx))
    print("Name .................. : {}".format(roomplan3.name))
    print("Order ................. : {}".format(roomplan3.order))
    print("Devices ............... : {}".format(roomplan3.devices))

    print("Delete roomplan2")
    roomplan2.delete()
    print("exists ................ : {}".format(roomplan2.exists()))
    print("Delete roomplan3")
    roomplan3.delete()
    print("exists ................ : {}".format(roomplan3.exists()))


if __name__ == "__main__":
    main()
