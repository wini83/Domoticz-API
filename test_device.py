#!/usr/bin/env python
# -*- coding: utf-8 -*-
import DomoticzAPI as dom


def main():
    server = dom.Server(address="192.168.0.13")
    # Existing device
    dev1 = dom.Device(server, "104")
    print("API Status: " + dev1.api_status)
    print(dev1)
    print("Value: " + str(dev1.data))
    if dev1.exists():
        print("Has battery = " + str(dev1.hasBattery()))
        print("Hardware ID = " + str(dev1.hardwareid))
        hw1 = dom.Hardware(server, str(dev1.hardwareid))
        print(hw1)
        print("Favorite: " + str(dev1.favorite))
        dev1.favorite = False
        print("Favorite: " + str(dev1.favorite))
        print("Is favorite: " + str(dev1.isFavorite()))
    else:
        print("Device " + dev1.idx + " doesn't exists or is disabled")

    # Non existing device
    dev2 = dom.Device(server, name="PiMonitor - Connections")
    print(dev2)
    if dev2.exists():
        print("Value: " + str(dev2.data))

if __name__ == "__main__":
    main()
