#!/usr/bin/env python
# -*- coding: utf-8 -*-
import DomoticzAPI as dom


def main():
    print("DomoticzAPI version: " + dom.version())
    print("System: " + dom.system())
    print("Machine: " + dom.machine())
    print("Node: " + dom.node())
    print("Processor: " + dom.processor())
    print("OS Version: " + dom.os_version())
    print("OS Release: " + dom.os_release())
    print("Python version: " + dom.python_version())
    print("\r")
    print("-273.15 C = " + str(dom.TempC2F(-273.15)) + " F")
    print("-40 C = " + str(dom.TempC2F(-40)) + " F")
    print("0 C = " + str(dom.TempC2F(0)) + " F")
    print("20 C = " + str(dom.TempC2F(20)) + " F")
    print("100 C = " + str(dom.TempC2F(100)) + " F")
    print("\r")
    print("-40 F = " + str(dom.TempF2C(-40)) + " C")
    print("0 F = " + str(dom.TempF2C(0)) + " C")
    print("68 F = " + str(dom.TempF2C(68)) + " C")
    print("100 F = " + str(dom.TempF2C(100)) + " C")
    print("\r")
    res = dom.os_command("/opt/vc/bin/vcgencmd", "measure_temp")
    print("CPU temperature: " + res.split("=")[1][:-3])
    res = dom.os_command("ls", "-al")
    print("ls: " + str(res))


if __name__ == "__main__":
    main()
