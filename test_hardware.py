#!/usr/bin/env python
# -*- coding: utf-8 -*-
import DomoticzAPI as dom


def main():
    server = dom.Server()
    # hw1 = dom.Hardware(server, "180")
    hw1 = dom.Hardware(server, idx="18")
    print("{}: {} {}".format(hw1, hw1.api_status, hw1.api_title))
    if hw1.exists():
        print("Name = " + str(hw1.name))
    else:
        print("Hardware " + hw1.idx + " doesn't exists")

    hw2 = dom.Hardware(server, Type=15, Port=1, Name="Sensors 1", Enabled="true")
    hw2.add()
    print("{}: {} - {}".format(hw2, hw2.api_status, hw2.api_title))
    hw2.name = "Sensors 2"
    hw2.update()
    print("{}: {} - {}".format(hw2, hw2.api_status, hw2.api_title))
    hw2.delete()
    print("{}: {} - {}".format(hw2, hw2.api_status, hw2.api_title))
    hw2.address = "10.10.0.10"
    hw2.serialport = "1234"
    hw2.add()
    print("{}: {} - {}".format(hw2, hw2.api_status, hw2.api_title))


if __name__ == "__main__":
    main()
