#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import DomoticzAPI as dom
import time


def main():
    print("********************************************************************************")
    print("Test script ........... : {}".format(__file__))
    print("********************************************************************************")
    server = dom.Server()
    dev1 = dom.Device(server, 77)
    org_level = dev1.level
    org_color = dev1.color
    print("name .................. : {}".format(dev1.name))
    print("color ................. : {}".format(dev1.color))
    print("level ................. : {}".format(dev1.level))
    color = dev1.color
    t = color.t
    color.t = -10
    print("m ..................... : {}".format(color.m))
    print("t ..................... : {}".format(color.t))
    print("color ................. : {}".format(color))
    dev1.color = color
    time.sleep(3)
    color.t = 300
    print("color ................. : {}".format(color))
    dev1.color = color
    time.sleep(3)
    color.t = t
    print("color ................. : {}".format(color))
    dev1.color = color
    # Check Color temperature
    new_color = dev1.color
    for x in range(0, 255, 10):
        new_color.t = x
        dev1.color = new_color
        print("Dev color ............. : {}".format(dev1.color))
        time.sleep(1)
    dev1.color = org_color
    for y in range(0, 255, 10):
        new_color.r = y
        dev1.color = new_color
        print("Dev color ............. : {}".format(dev1.color))
        time.sleep(1)
    dev1.color = org_color
    dev1.level = org_level


if __name__ == "__main__":
    main()
