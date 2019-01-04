#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import DomoticzAPI as dom


def main():
    print("********************************************************************************")
    print("Test script ........... : {}".format(__file__))
    print("********************************************************************************")
    server = dom.Server()
    print(server.setting)
    key = "Title"
    print("{}: {}".format(key, server.setting.value(key)))
    key = "BatterLowLevel"
    print("{}: {}".format(key, server.setting.value(key)))
    key = "AcceptNewHardware"
    print("{}: {}".format(key, server.setting.value(key)))
    key = "WeightUnit"
    print("{}: {}".format(key, server.setting.value(key)))


if __name__ == "__main__":
    main()
