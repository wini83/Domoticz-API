#!/usr/bin/env python
# -*- coding: utf-8 -*-
import DomoticzAPI as dom


def main():
    server = dom.Server(address="192.168.0.13")
    # hw1 = dom.Hardware(server, "180")
    hw1 = dom.Hardware(server, idx="180")
    print(hw1)
    if hw1.exists():
        print("Name = " + str(hw1.Name))
    else:
        print("Hardware " + hw1.idx + " doesn't exists")

    hw2 = dom.Hardware(server, Type=15, Port=1, Name="Sensors1", Enabled="true")
    hw2.add()
    print(hw2.status)
    print(hw2)

if __name__ == "__main__":
    main()
