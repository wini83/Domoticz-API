#!/usr/bin/env python
# -*- coding: utf-8 -*-
import DomoticzAPI as dom


def main():
    server = dom.Server(address="192.168.0.16", port="8080")
    print("{}: {} - {}".format(server, server.api_status, server.api_title))
    dev1 = dom.Device(server, 62)
    print("Name: " + dev1.name)
    print("Color: " + dev1.color)
    color = dom.Color(color=dev1.color)
    print("m: " + str(color.m))
    print("color: " + color.color)


if __name__ == "__main__":
    main()
