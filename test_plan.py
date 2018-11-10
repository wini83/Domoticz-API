#!/usr/bin/env python
# -*- coding: utf-8 -*-
import DomoticzAPI as dom


def main():
    server = dom.Server(address="192.168.0.16", port="8080")
    print("{}: {} - {}".format(server, server.api_status, server.api_title))
    plan1 = dom.Plan(server, 2)
    print("Name: " + plan1.name)
    print("Order: " + str(plan1.order))
    print("Devices: " + str(plan1.devices))


if __name__ == "__main__":
    main()
