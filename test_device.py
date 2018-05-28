#!/usr/bin/env python
# -*- coding: utf-8 -*-
import DomoticzAPI as dom
from datetime import datetime

def main():
    server = dom.Server()
    print("Existing device")
    dev1 = dom.Device(server, 2)
    print(dev1.hardware)
    print("server.act_time: " + str(server.act_time))
    print("API Status: " + dev1.api_status)
    print(dev1)
    print("Value: " + str(dev1.data))
    if dev1.exists():
        print("Has battery = " + str(dev1.hasBattery()))
        print("Hardware ID = " + str(dev1.hardware.idx))
        print(dev1.hardware)
        print("Favorite: " + str(dev1.favorite))
        dev1.favorite = not dev1.favorite
        print("Favorite: " + str(dev1.favorite))
        print("Is favorite: " + str(dev1.isFavorite()))
    else:
        print("Device " + str(dev1.idx) + " doesn't exists or is disabled")

    print("\n")
    print("Non existing device")
    dev2 = dom.Device(server, name="PiMonitor - Connections")
    print(dev2)
    if dev2.exists():
        print("Value: " + str(dev2.data))

    print("\n")
    print("Create new hardware")
    hw3 = dom.Hardware(server, type=15, name="Test 3 Hardware")  # Dummy hardware
    hw3.add()
    print(hw3)
    print("{}: {} - {}".format(hw3, hw3.api_status, hw3.api_title))

    if hw3.exists():
        print("Add device to new hardware")
        print("hw3: " + str(hw3))
        dev3 = dom.Device(server, hw3, "Test 3 Device", type=243, subtype=8)
        print("dev3.hardware: " + str(dev3.hardware))
        print("{}: {} - {}".format(dev3, dev3.api_status, dev3.api_title))

        dev3.add()
        print("{}: {} - {}".format(dev3, dev3.api_status, dev3.api_title))
        print(dev3.__dict__)

if __name__ == "__main__":
    main()
