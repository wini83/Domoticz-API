#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import DomoticzAPI as dom
import os

def main():
    print("********************************************************************************")
    print("Test script ........... : {}".format(os.path.basename(__file__)))
    print("********************************************************************************")
    server = dom.Server()

    hw2 = dom.Hardware(server, type=15, port=1, name="Sensors 1", enabled="true")
    hw2.add()
    print("Add ................... : {}".format(hw2.api_querystring))
    print("{}: {} - {}".format(hw2, hw2.api_status, hw2.api_title))

    hw1 = dom.Hardware(server, idx=hw2.idx)
    print("__init__ .............. : {}".format(hw1.api_querystring))
    print("{}: {} {}".format(hw1, hw1.api_status, hw1.api_title))
    if hw1.exists():
        print("Name .................. : {}".format(hw1.name))
    else:
        print("Hardware .............. : {} doesn't exists".format(hw1.idx))

    hw2.name = "Sensors 2"
    hw2.update()
    print("Update ................ : {}".format(hw2.api_querystring))
    print("{}: {} - {}".format(hw2, hw2.api_status, hw2.api_title))
    hw2.delete()
    print("Delete ................ : {}".format(hw2.api_querystring))
    print("{}: {} - {}".format(hw2, hw2.api_status, hw2.api_title))
    hw2.address = "10.10.0.10"
    hw2.port = 9876
    hw2.serialport = "1234"
    hw2.add()
    print("Add ................... : {}".format(hw2.api_querystring))
    print("{}: {} - {}".format(hw2, hw2.api_status, hw2.api_title))
    print(hw2.__dict__)
    hw2.delete()


if __name__ == "__main__":
    main()
