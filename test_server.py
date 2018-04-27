#!/usr/bin/env python
# -*- coding: utf-8 -*-
import DomoticzAPI as dom


def main():
    server = dom.Server(address="192.168.0.13")
    print(server)
    print("ServerTime = " + server.ServerTime)
    print("Sunrise = " + server.Sunrise)
    print("Sunset = " + server.Sunset)
    server.logmessage("Test")
    print("Status = " + server.Status)

if __name__ == "__main__":
    main()
