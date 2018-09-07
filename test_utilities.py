#!/usr/bin/env python
# -*- coding: utf-8 -*-
import DomoticzAPI as dom


def main():
    print("********************************************************************************")
    print("DomoticzAPI: test_utilities")
    print("********************************************************************************")

    print("\r")
    print("********************************************************************************")
    print("API properties")
    print("********************************************************************************")
    print("DomoticzAPI version ... : {}".format(dom.version()))
    print("System ................ : {}".format(dom.system()))
    print("Machine ............... : {}".format(dom.machine()))
    print("Node .................. : {}".format(dom.node()))
    print("Processor ............. : {}".format(dom.processor()))
    print("OS Version ............ : {}".format(dom.os_version()))
    print("OS Release ............ : {}".format(dom.os_release()))
    print("Python version ........ : {}".format(dom.python_version()))

    print("\r")
    print("********************************************************************************")
    print("Temperature conversion")
    print("********************************************************************************")
    print("-273.15 C ............. : {} F".format(dom.TempC2F(-273.15)))
    print("-40 C ................. : {} F".format(dom.TempC2F(-40)))
    print("0 C ................... : {} F".format(dom.TempC2F(0)))
    print("20 C .................. : {} F".format(dom.TempC2F(20)))
    print("100 C ................. : {} F".format(dom.TempC2F(100)))
    print("\r")
    print("-40 F ................. : {} C".format(dom.TempF2C(-40)))
    print("0 F ................... : {} C".format(dom.TempF2C(0)))
    print("68 F .................. : {} C".format(dom.TempF2C(68)))
    print("100 F ................. : {} C".format(dom.TempF2C(100)))

    print("\r")
    print("********************************************************************************")
    print("Bearing conversion")
    print("********************************************************************************")
    print("0 ..................... : {}".format(dom.Bearing2Status(0)))
    print("90 .................... : {}".format(dom.Bearing2Status(90)))
    print("180 ................... : {}".format(dom.Bearing2Status(180)))
    print("270 ................... : {}".format(dom.Bearing2Status(270)))
    print("360 ................... : {}".format(dom.Bearing2Status(360)))
    print("450 ................... : {}".format(dom.Bearing2Status(450)))
    print("40 .................... : {}".format(dom.Bearing2Status(40)))

    print("\r")
    print("********************************************************************************")
    print("OS commands (Unix)")
    print("********************************************************************************")
    res = dom.os_command("/opt/vc/bin/vcgencmd", "measure_temp")
    print("CPU temperature: {}".format(res.split("=")[1][:-3]))
    res = dom.os_command("ls", "-al")
    print("ls:\n{}".format(res))

    print("\r")
    print("********************************************************************************")
    print("OS commands (Windows)")
    print("********************************************************************************")
    res = dom.os_command("vol", "")
    print("vol:\n{}".format(res))


if __name__ == "__main__":
    main()
