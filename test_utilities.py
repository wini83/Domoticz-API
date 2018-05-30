#!/usr/bin/env python
# -*- coding: utf-8 -*-
import DomoticzAPI as dom


def main():
    print("-273.15 C = " + str(dom.TempC2F(-273.15)) + " F")
    print("-40 C = " + str(dom.TempC2F(-40)) + " F")
    print("0 C = " + str(dom.TempC2F(0)) + " F")
    print("20 C = " + str(dom.TempC2F(20)) + " F")
    print("100 C = " + str(dom.TempC2F(100)) + " F")
    print("\n")
    print("-40 F = " + str(dom.TempF2C(-40)) + " C")
    print("0 F = " + str(dom.TempF2C(0)) + " C")
    print("68 F = " + str(dom.TempF2C(68)) + " C")
    print("100 F = " + str(dom.TempF2C(100)) + " C")


if __name__ == "__main__":
    main()
