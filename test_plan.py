#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import DomoticzAPI as dom
import os

def main():
    print("********************************************************************************")
    print("Test script ........... : {}".format(os.path.basename(__file__)))
    print("********************************************************************************")
    server = dom.Server()
    plan1 = dom.Plan(server, 3) # Or use an other number as can be found as planid in a device
    print(plan1)
    print("api ................... : {}".format(plan1.api))
    print("querystring ........... : {}".format(plan1.api.querystring))
    print("exists ................ : {}".format(plan1.exists()))
    print("Name .................. : {}".format(plan1.name))
    print("Order ................. : {}".format(plan1.order))
    print("Devices ............... : {}".format(plan1.devices))


if __name__ == "__main__":
    main()
