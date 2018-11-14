#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import DomoticzAPI as dom
from datetime import datetime
import time
import os

def main():
    print("********************************************************************************")
    print("Test script ........... : {}".format(os.path.basename(__file__)))
    print("********************************************************************************")
    server = dom.Server()

    print("\r")
    print("********************************************************************************")
    print("Non existing device")
    print("********************************************************************************")
    dev2 = dom.Device(server, name="xyz")
    print(dev2)
    if dev2.exists():
        print("Value .................. : {}".format(dev2.data))
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
        print("dev3.hardware: {}".format(dev3.hardware))
        print("{}: {} - {}".format(dev3, dev3.api_status, dev3.api_title))

        dev3.add()
        print("{}: {} - {}".format(dev3, dev3.api_status, dev3.api_title))
        if dev3.exists():
            print("Switch successfully created")
            print("Status: {}".format(dev3.data))
            print("Switch device: {}".format(dev3.switchOn))
            dev3.updateSwitch(dev3.switchOn)
            print("Status: {}".format(dev3.data))
            print("Switch device: {}".format(dev3.switchOff))
            dev3.updateSwitch(dev3.switchOff)
            print("Status: {}".format(dev3.data))
            print("Switch device: {}".format(dev3.switchToggle))
            dev3.updateSwitch(dev3.switchToggle)
            print("Status: {}".format(dev3.data))
            print("Switch device: {}".format(dev3.switchSetLevel))
            print("Level: {}".format(dev3.level))
            dev3.level = 50
            print("Level: {}".format(dev3.level))
            print("Status: {}".format(dev3.data))
            # Check Color class
            temp_t = dev3.color.t
            new_color = dev3.color
            for x in range(0, 255, 10):
                new_color.t = x
                dev3.color = new_color
                time.sleep(1)
            new_color.t = temp_t
            dev3.color = new_color
    # Cleanup test data
    hw3.delete()

if __name__ == "__main__":
    main()
