#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import DomoticzAPI as dom
from test_all import (WIDTH_LABEL, FILE, TEST, H2, CRLF, SUFFIX)


def main():
    print(FILE)
    print("{:{}<{}}: {}".format("Test script", SUFFIX, WIDTH_LABEL, __file__))
    print(FILE)
    server = dom.Server()

    print(CRLF)
    print(TEST)
    print("Create hw2 Class")
    print(TEST)
    hw2 = dom.Hardware(server,
                       type=dom.HTYPE_DUMMY,
                       port=1,
                       name="Test API hw2",
                       enabled="true")
    print("{:{}<{}}: {}".format("hw2", SUFFIX, WIDTH_LABEL, hw2))

    print(CRLF)
    print(TEST)
    print("Add hw2 to Domoticz")
    print(TEST)
    hw2.add()
    if hw2.exists():
        print("{:{}<{}}: {}".format(
            "hw2", SUFFIX, WIDTH_LABEL, hw2))
        print("{:{}<{}}: {}".format(
            "type_name", SUFFIX, WIDTH_LABEL, hw2.type_name))
    else:
        print("{:{}<{}}: {}".format(
            "hw2", SUFFIX, WIDTH_LABEL, "doesn't exists"))

    print(CRLF)
    print(TEST)
    print("Create class hw1 from hw2 in Domoticz")
    print(TEST)
    hw1 = dom.Hardware(server, idx=hw2.idx)
    print("{:{}<{}}: {}".format("hw1", SUFFIX, WIDTH_LABEL, hw2))
    if not hw1.exists():
        print("{:{}<{}}: {}".format(
            "hw1", SUFFIX, WIDTH_LABEL, "doesn't exists"))

    print(CRLF)
    print(TEST)
    print("Rename hw2")
    print(TEST)
    hw2.name = "Test API hw2 renamed"
    print("{:{}<{}}: {}".format("hw2", SUFFIX, WIDTH_LABEL, hw2))

    print(CRLF)
    print(TEST)
    print("Delete hw2 to Domoticz")
    print(TEST)
    hw2.delete()
    print("{:{}<{}}: {}".format("hw2", SUFFIX, WIDTH_LABEL, hw2))

    print(CRLF)
    print(TEST)
    print("Modify object hw2 and add to Domoticz")
    print(TEST)
    print("{:{}<{}}: {}".format("hw2", SUFFIX, WIDTH_LABEL, hw2))
    hw2.address = "10.10.0.10"
    hw2.port = 9876
    hw2.serialport = "1234"
    hw2.add()
    print("{:{}<{}}: {}".format("hw2", SUFFIX, WIDTH_LABEL, hw2))

    print(CRLF)
    print(TEST)
    print("Clean up test data")
    print(TEST)
    hw1.delete()
    hw2.delete()
    print("{:{}<{}}: {}".format("hw1", SUFFIX, WIDTH_LABEL, hw1))
    print("{:{}<{}}: {}".format("hw2", SUFFIX, WIDTH_LABEL, hw2))


if __name__ == "__main__":
    main()
