#!/usr/bin/env python
# -*- coding: utf-8 -*-
import DomoticzAPI as dom


def main():
    server = dom.Server(address="192.168.0.13")
    dev1 = dom.Device(server, "17")
    print(dev1)
    if dev1.exists():
        print("Has battery = " + str(dev1.hasBattery()))
        print("Hardware ID = " + str(dev1.hardwareid))
    else:
        print("Device " + dev1.idx + " doesn't exists or is disabled")
    # print(vars(dev1))
    dir(dev1)


if __name__ == "__main__":
    main()
