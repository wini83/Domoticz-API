#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import DomoticzAPI as dom


def main():
    print("********************************************************************************")
    print("Test script ........... : {}".format(__file__))
    print("********************************************************************************")
    server = dom.Server()
    roomplan1 = dom.RoomPlan(server, name="DomoticzAPI Test Roomplan")
    print(roomplan1)
    print("exists ................ : {}".format(roomplan1.exists()))
    if not roomplan1.exists():
        roomplan1.add()
        print("exists ................ : {}".format(roomplan1.exists()))
    print(roomplan1)

    roomplan1.name = "DomoticzAPI Test Roomplan 2"
    print(roomplan1)

    print("Devices ............... : {}".format(roomplan1.devices))

    dev = dom.Device(server, 61)
    print(dev)
    roomplan1.add_device(dev)
    print("Nr of devices ......... : {}".format(roomplan1.device_count))
    print("Devices ............... : {}".format(roomplan1.devices))
    roomplan1.delete_device(dev)
    print("Nr of devices ......... : {}".format(roomplan1.device_count))
    print("Devices ............... : {}".format(roomplan1.devices))
    roomplan1.add_device(dev)
    print("Nr of devices ......... : {}".format(roomplan1.device_count))
    print("Has devices ........... : {}".format(roomplan1.has_devices()))
    print("Devices ............... : {}".format(roomplan1.devices))
    roomplan1.delete_all_devices()
    print("Nr of devices ......... : {}".format(roomplan1.device_count))
    print("Has devices ........... : {}".format(roomplan1.has_devices()))
    print("Devices ............... : {}".format(roomplan1.devices))

    print("Delete roomplan1")
    roomplan1.delete()
    print("exists ................ : {}".format(roomplan1.exists()))


if __name__ == "__main__":
    main()
