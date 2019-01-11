#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import DomoticzAPI as dom


def main():
    print("********************************************************************************")
    print("Test script ........... : {}".format(__file__))
    print("********************************************************************************")
    server = dom.Server()

    print("--------------------------------------------------------------------------------")
    print("Add")
    print("--------------------------------------------------------------------------------")
    var1 = dom.UserVariable(
        server, "API Test 1", dom.UserVariable.UVE_TYPE_FLOAT, "1.23")
    if var1.exists():
        print("'{}' exists in Domoticz".format(var1.name))
    else:
        print("'{}' NOT exists in Domoticz".format(var1.name))
    print("Add uservariable '{}'".format(var1.name))
    var1.add()
    print(var1)
    if var1.exists():
        print( "'{}' exists in Domoticz".format(var1.name))
    else:
        print("'{}' NOT exists in Domoticz".format(var1.name))
    print("\r")

    print("--------------------------------------------------------------------------------")
    print("Add")
    print("--------------------------------------------------------------------------------")
    var2 = dom.UserVariable(
        server, "API Test 2", dom.UserVariable.UVE_TYPE_INTEGER, "1.23")
    var2.add()
    print(var2)
    print("\r")

    print("--------------------------------------------------------------------------------")
    print("Change value")
    print("--------------------------------------------------------------------------------")
    var1.value = "11.87"
    print(var1)
    var2.value = "11.87"
    print(var2)
    print("\r")

    print("--------------------------------------------------------------------------------")
    print("Cleanup test data")
    print("--------------------------------------------------------------------------------")
    var1.delete()
    print(var1)
    var2.delete()
    print(var2)


if __name__ == "__main__":
    main()
