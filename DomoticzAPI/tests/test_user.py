#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import DomoticzAPI as DA


def main():
    print("********************************************************************************")
    print("Test script ........... : {}".format(__file__))
    print("********************************************************************************")
    server = DA.Server()
    user_not_existance = DA.User(server, name="user_not_existance")
    print(user_not_existance)

    user_new = DA.User(server)
    user_new.name = "test"
    user_new.password = "test"
    user_new.rights = user_new.USER_RIGHTS_ADMIN
    print(user_new)
    user_new.add()
    print(user_new)
    print("Password: {}".format(user_new.password))
    user_new.password = "testtest"
    print("Password: {}".format(user_new.password))
    print("Tabs: {}".format(user_new.tabsenabled))
    user_new.add_tab(user_new.USER_TAB_SWITCHES)
    user_new.add_tab(user_new.USER_TAB_FLOORPLAN)
    print("Tabs: {}".format(user_new.tabsenabled))
    print("Has tab USER_TAB_FLOORPLAN: {}".format(
        user_new.has_tab(user_new.USER_TAB_FLOORPLAN)))
    print("Has tab USER_TAB_WEATHER: {}".format(
        user_new.has_tab(user_new.USER_TAB_WEATHER)))
    user_new.name = "test renamed"
    print(user_new)
    user_new.delete()


if __name__ == "__main__":
    main()
