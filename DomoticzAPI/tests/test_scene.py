#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import DomoticzAPI as dom


def main():
    print("********************************************************************************")
    print("Test script ........... : {} ({})".format(__file__, dom.VERSION))
    print("********************************************************************************")
    server = dom.Server()
    print(server)

    print("\r")
    print("********************************************************************************")
    print("Non existing scene")
    print("********************************************************************************")
    scene1 = dom.Scene(server, name="xyz")
    print("scene1 ................. : {}".format(scene1))
    if not scene1.exists():
        print("Scene {} does not exist!!!".format(scene1.name))

    print("\r")
    print("********************************************************************************")
    print("Existing scene")
    print("********************************************************************************")
    scene2 = dom.Scene(server, name="Woonkamer")
    print("scene2 ................. : {}".format(scene2))
    if not scene2.exists():
        print("Scene {} does not exist!!!".format(scene2.name))

    print("\r")
    print("********************************************************************************")
    print("Create new scene")
    print("********************************************************************************")
    print("scene1 ................. : {}".format(scene1))
    scene1.name = "Test API Scene"
    print("scene1 ................. : {}".format(scene1))
    scene1.type = dom.Scene.STYPE_SCENE
    print("scene1 ................. : {}".format(scene1))
    scene1.add()
    print("scene1 ................. : {}".format(scene1))

    scene1.name = "Test API Scene renamed"
    print("scene1 ................. : {}".format(scene1))

    scene1.type = dom.Scene.STYPE_GROUP
    print("scene1 ................. : {}".format(scene1))

    print("scene1.status .......... : {}".format(scene1.status))
    scene1.status = dom.ON
    print("scene1.status .......... : {}".format(scene1.status))
    scene1.status = dom.OFF
    print("scene1.status .......... : {}".format(scene1.status))

    print("scene1.favorite ........ : {}".format(scene1.favorite))
    scene1.favorite = True
    print("scene1.favorite ........ : {}".format(scene1.favorite))
    scene1.favorite = False
    print("scene1.favorite ........ : {}".format(scene1.favorite))    

    print("scene1.protected ....... : {}".format(scene1.protected))
    scene1.protected = True
    print("scene1.protected ....... : {}".format(scene1.protected))
    scene1.protected = False
    print("scene1.protected ....... : {}".format(scene1.protected))

    print("scene1.onaction ........ : {}".format(scene1.onaction))
    scene1.onaction = "Grumppfff"
    print("scene1.onaction ........ : {}".format(scene1.onaction))
    scene1.onaction = None
    print("scene1.onaction ........ : {}".format(scene1.onaction))

    print("\r")
    print("********************************************************************************")
    print("Cleanup test data")
    print("********************************************************************************")
    scene1.delete()


if __name__ == "__main__":
    main()
