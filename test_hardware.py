#!/usr/bin/env python
# -*- coding: utf-8 -*-
import DomoticzAPI as dom


def main():
    server = dom.Server()
    # hw1 = dom.Hardware(server, "180")
    hw1 = dom.Hardware(server, idx="3")
    print("__init__: {}".format(hw1.api_querystring))
    print("{}: {} {}".format(hw1, hw1.api_status, hw1.api_title))
    if hw1.exists():
        print("Name = " + str(hw1.name))
    else:
        print("Hardware " + hw1.idx + " doesn't exists")

    hw2 = dom.Hardware(server, type=15, port=1, name="Sensors 1", enabled="true")
    # print(hw2.__dict__)
    hw2.add()
    print("Add: {}".format(hw2.api_querystring))
    print("{}: {} - {}".format(hw2, hw2.api_status, hw2.api_title))
    #print(hw2.__dict__)
    hw2.name = "Sensors 2"
    hw2.update()
    print("Update: {}".format(hw2.api_querystring))
    print("{}: {} - {}".format(hw2, hw2.api_status, hw2.api_title))
    hw2.delete()
    print("Delete: {}".format(hw2.api_querystring))
    print("{}: {} - {}".format(hw2, hw2.api_status, hw2.api_title))
    hw2.address = "10.10.0.10"
    hw2.port = 9876
    hw2.serialport = "1234"
    hw2.add()
    print("Add: {}".format(hw2.api_querystring))
    print("{}: {} - {}".format(hw2, hw2.api_status, hw2.api_title))
    print(hw2.__dict__)


if __name__ == "__main__":
    main()
