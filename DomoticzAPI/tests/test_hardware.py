#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import DomoticzAPI as dom


def main():
    print("********************************************************************************")
    print("Test script ........... : {}".format(__file__))
    print("********************************************************************************")
    server = dom.Server()

    hw2 = dom.Hardware(server, type=15, port=1,
                       name="Sensors 1", enabled="true")
    hw2.add()
    if hw2.exists():
        print("hw2 ................... : {}".format(hw2))

    hw1 = dom.Hardware(server, idx=hw2.idx)
    print("hw1 ................... : {}".format(hw1))
    if not hw1.exists():
        print("Hardware .............. : {} doesn't exists".format(hw1.idx))

    hw2.name = "Sensors 2"
    print("hw2 ................... : {}".format(hw2))
    hw2.delete()
    
    print("hw2 ................... : {}".format(hw2))
    hw2.address = "10.10.0.10"
    hw2.port = 9876
    hw2.serialport = "1234"
    hw2.add()
    print("hw2 ................... : {}".format(hw2))
    hw2.delete()


if __name__ == "__main__":
    main()
