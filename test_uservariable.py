#!/usr/bin/env python
# -*- coding: utf-8 -*-
import DomoticzAPI as dom


def main():
    server = dom.Server(address="192.168.0.13")

    var1 = dom.UserVariable(server, "Test1")
    var1.add()
    if var1.exists():
        print("var1 exists in Domoticz")
    print(var1)

    var2 = dom.UserVariable(server, "Test2", "float", "3.21")
    var2.add()
    var2.value = "11.87"
    var2.update()
    print(var2)
    if var2.exists():
        print("var2 exists in Domoticz")

    var3 = dom.UserVariable(server, "Test3", "float", "1.23")
    var3.value = 4.56
    var3.add()
    print(var3)
    if var3.exists():
        print("var3 exists in Domoticz")

    var4 = dom.UserVariable(server, "Test4", "integer")
    var4.value = 4.56
    var4.add()
    var4.update()
    if var4.exists():
        print("var4 exists in Domoticz")
    print(var4)

    var1.delete()
    var2.delete()
    var3.delete()


if __name__ == "__main__":
    main()
