#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import DomoticzAPI as dom
import os

def main():
    print("********************************************************************************")
    print("Test script ........... : {}".format(os.path.basename(__file__)))
    print("********************************************************************************")
    server = dom.Server()
    dev1 = dom.Device(server, 11)
    print("dev1 .................. : {}".format(dev1))
    print("Name .................. : {}".format(dev1.name))
    print("Color ................. : {}".format(dev1.color))
    color = dev1.color
    print("m ..................... : {}".format(color.m))
    print("color ................. : {}".format(color))


if __name__ == "__main__":
    main()
