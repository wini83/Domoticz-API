#!/usr/bin/env python
# -*- coding: utf-8 -*-
import DomoticzAPI as dom


def main():
    server = dom.Server(address="192.168.0.13")
    print(server)
    var1 = dom.UserVariable(server, "Test1")
    var1.add()
    print(var1)
    var2 = dom.UserVariable(server, "Test2", "float")
    var2.add()
    var2.value = "11.87"
    var2.update()
    print(var2)
    var3 = dom.UserVariable(server, "Test3", "float", "1.23")
    var3.add()
    print(var3)
    var1.delete()
    var2.delete()
    # var3.delete()


if __name__ == "__main__":
    main()
