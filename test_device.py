#!/usr/bin/env python
# -*- coding: utf-8 -*-
import DomoticzAPI as dom


def main():
    server = dom.Server(address="192.168.0.13")

    dev1 = dom.Device(server, "71")
    print(dev1)

if __name__ == "__main__":
    main()
