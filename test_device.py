#!/usr/bin/env python
# -*- coding: utf-8 -*-
import DomoticzAPI as dom
from datetime import datetime

def main():
    print("********************************************************************************")
    print("DomoticzAPI: test_device")
    print("********************************************************************************")
    server = dom.Server()

    print("\r")
    print("********************************************************************************")
    print("Non existing device")
    print("********************************************************************************")
    dev2 = dom.Device(server, name="xyz")
    print(dev2)
    if dev2.exists():
        print("Value: " + str(dev2.data))
    else:
        print("Device {} does not exist!!!".format(dev2.name))

    print("\r")
    print("********************************************************************************")
    print("Create new hardware")
    print("********************************************************************************")
    hw3 = dom.Hardware(server, type=15, name="Test Hardware")  # Dummy hardware
    hw3.add()
    print("{}: {} - {}".format(hw3, hw3.api_status, hw3.api_title))

    if hw3.exists():
        print("\r")
        print("********************************************************************************")
        print("Add device to new hardware")
        print("********************************************************************************")
        dev3 = dom.Device(server, hw3, "Test Device", type=244, subtype=73)  # Switch
        print("dev3.hardware: " + str(dev3.hardware))
        print("{}: {} - {}".format(dev3, dev3.api_status, dev3.api_title))

        dev3.add()
        print("{}: {} - {}".format(dev3, dev3.api_status, dev3.api_title))
        if dev3.exists():
            print("Switch succesfully created")
            print("Status: {}".format(dev3.data))
            dev3.switch("On")
            print("Status: {}".format(dev3.data))
            dev3.switch("Off")
            print("Status: {}".format(dev3.data))
            dev3.switch("Toggle")
            print("Status: {}".format(dev3.data))
    # Cleanup test data
    hw3.delete()

if __name__ == "__main__":
    main()
