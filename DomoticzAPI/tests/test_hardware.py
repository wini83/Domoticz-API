#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import DomoticzAPI as dom
from test_all import SUFFIX, WIDTH_LABEL


def main():
    print("********************************************************************************")
    print("Test script ..................: {} ({})".format(__file__, dom.VERSION))
    print("********************************************************************************")
    server = dom.Server()
    print("\r")

    print("********************************************************************************")
    print("Create hw2 Class")
    print("********************************************************************************")
    hw2 = dom.Hardware(server,
                       type=dom.HTYPE_DUMMY,
                       port=1,
                       name="Test API hw2",
                       enabled="true")
    print("{:{}<{}}: {}".format("hw2", SUFFIX, WIDTH_LABEL, hw2))
    print("\r")

    print("********************************************************************************")
    print("Add hw2 to Domoticz")
    print("********************************************************************************")
    hw2.add()
    if hw2.exists():
        print("{:{}<{}}: {}".format("hw2", SUFFIX, WIDTH_LABEL, hw2))
        print("{:{}<{}}: {}".format("type_name",
                                    SUFFIX, WIDTH_LABEL, hw2.type_name))
    else:
        print("{:{}<{}}: {}".format(
            "hw2", SUFFIX, WIDTH_LABEL, "doesn't exists"))
    print("\r")

    print("********************************************************************************")
    print("Create class hw1 from hw2 in Domoticz")
    print("********************************************************************************")
    hw1 = dom.Hardware(server, idx=hw2.idx)
    print("{:{}<{}}: {}".format("hw1", SUFFIX, WIDTH_LABEL, hw2))
    if not hw1.exists():
        print("{:{}<{}}: {}".format(
            "hw1", SUFFIX, WIDTH_LABEL, "doesn't exists"))
    print("\r")

    print("********************************************************************************")
    print("Rename hw2")
    print("********************************************************************************")
    hw2.name = "Test API hw2 renamed"
    print("{:{}<{}}: {}".format("hw2", SUFFIX, WIDTH_LABEL, hw2))
    print("\r")

    print("********************************************************************************")
    print("Delete hw2 to Domoticz")
    print("********************************************************************************")
    hw2.delete()
    print("{:{}<{}}: {}".format("hw2", SUFFIX, WIDTH_LABEL, hw2))
    print("\r")

    print("********************************************************************************")
    print("Modify object hw2 and add to Domoticz")
    print("********************************************************************************")
    print("{:{}<{}}: {}".format("hw2", SUFFIX, WIDTH_LABEL, hw2))
    hw2.address = "10.10.0.10"
    hw2.port = 9876
    hw2.serialport = "1234"
    hw2.add()
    print("{:{}<{}}: {}".format("hw2", SUFFIX, WIDTH_LABEL, hw2))
    print("\r")
        
    print("********************************************************************************")
    print("Clean up test data")
    print("********************************************************************************")
    hw1.delete()
    hw2.delete()
    print("{:{}<{}}: {}".format("hw1", SUFFIX, WIDTH_LABEL, hw1))
    print("{:{}<{}}: {}".format("hw2", SUFFIX, WIDTH_LABEL, hw2))


if __name__ == "__main__":
    main()
