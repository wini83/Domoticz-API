#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import DomoticzAPI as dom
import os
import time


def main():
    print("********************************************************************************")
    print("Test script ........... : {}".format(os.path.basename(__file__)))
    print("********************************************************************************")
    server = dom.Server(address="192.168.0.16")
    dev1 = dom.Device(server, 77)
    print("name .................. : {}".format(dev1.name))
    print("color ................. : {}".format(dev1.color))
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


if __name__ == "__main__":
    main()
