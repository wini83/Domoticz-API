#!/usr/bin/env python
# -*- coding: utf-8 -*-

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# For this test, first create a uservariable in Domoticz with the name Test0
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

import DomoticzAPI as dom


def main():
    #server = dom.Server(address="192.168.0.13")
    #server = dom.Server(address="127.0.0.1")
    server = dom.Server()

    # Define an user variable only by name, which does exists in Domoticz
    var0 = dom.UserVariable(server, "Test0")
    print(var0)
    print("Check {}".format(var0.name))
    if var0.exists():
        print("{} exists in Domoticz".format(var0.name))
    else:
        print("{} NOT exists in Domoticz".format(var0.name))

    print("\n")
    # Define an user variable only by name, which does not exists in Domoticz
    var1 = dom.UserVariable(server, "Test1")
    print(var1)
    print("Check {}".format(var1.name))
    if var1.exists():
        print("{} exists in Domoticz".format(var1.name))
    else:
        print("{} NOT exists in Domoticz".format(var1.name))

    print("\n")
    # Create an new user variable
    var2 = dom.UserVariable(server, "Test2", "float", "1.23")
    print("Add {}".format(var2.name))
    var2.add()
    print(var2)
    if var2.exists():
        print("{} exists in Domoticz".format(var2.name))
    else:
        print("{} NOT exists in Domoticz".format(var2.name))
    var2.value = "11.87"
    print("Update {}".format(var2.name))
    var2.update()
    print(var2)
    print("Delete {}".format(var2.name))
    var2.delete()
    if var2.exists():
        print("{} exists in Domoticz".format(var2.name))
    else:
        print("{} NOT exists in Domoticz".format(var2.name))

    print("\n")
    var3 = dom.UserVariable(server, "Test3", "integer")
    print(var3)
    flt = 4.56
    print("Update value for {}({}) with: {}".format(var3.name, var3.type, flt))
    var3.value = flt
    print("Add {}".format(var3.name))
    var3.add()
    print(var3)
    if var3.exists():
        print("{} exists in Domoticz".format(var3.name))
    else:
        print("{} NOT exists in Domoticz".format(var3.name))
    print("Delete {}".format(var3.name))
    var3.delete()
    if var3.exists():
        print("{} exists in Domoticz".format(var3.name))
    else:
        print("{} NOT exists in Domoticz".format(var3.name))


if __name__ == "__main__":
    main()
