#!/usr/bin/env python
# -*- coding: utf-8 -*-
import DomoticzAPI as dom


def main():
    server = dom.Server()
    print("{}: {} - {}".format(server, server.api_status, server.api_title))
    dev1 = dom.Device(server, 11)
    print("Name: " + dev1.name)
    print("Color: " + str(dev1.color))
    color = dev1.color
    print("m: " + str(color.m))
    print("color: " + str(color))


if __name__ == "__main__":
    main()
