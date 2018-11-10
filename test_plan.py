#!/usr/bin/env python
# -*- coding: utf-8 -*-
import DomoticzAPI as dom


def main():
    server = dom.Server()
    plan1 = dom.Plan(server, 3) # Or use an other number as can be found as planid in a device
    print(plan1)
    print("Name......: {}".format(plan1.name))
    print("Order.....: {}".format(plan1.order))
    print("Devices...: {}".format(plan1.devices))


if __name__ == "__main__":
    main()
