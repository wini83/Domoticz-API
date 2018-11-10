#!/usr/bin/env python
# -*- coding: utf-8 -*-
import DomoticzAPI as dom


def main():
    server = dom.Server()
    plan1 = dom.Plan(server, 2)
    print(plan1)
    print("Name: " + plan1.name)
    print("Order: " + str(plan1.order))
    print("Devices: " + str(plan1.devices))


if __name__ == "__main__":
    main()
