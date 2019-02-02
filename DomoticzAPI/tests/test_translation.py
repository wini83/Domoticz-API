#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import DomoticzAPI as dom


def main():
    print("********************************************************************************")
    print("Test script ........... : {}".format(__file__))
    print("********************************************************************************")
    server = dom.Server()
    print("Server language: {}".format(server.language))
    print(server.translation)
    print("Translation language: {}".format(server.translation.language))
    server.translation.language = "nl"
    print("Translation language: {}".format(server.translation.language))
    key = "Hours"
    print("{} ({}): {}".format(
        key,
        server.translation.language,
        server.translation.value(key)))
    key = "Friday"
    print("{} ({}): {}".format(
        key,
        server.translation.language,
        server.translation.value(key)))
    key = "Unkown string"
    print("{} ({}): {}".format(
        key,
        server.translation.language,
        server.translation.value(key)))
    key = "Hurricane"
    print("{} ({}): {}".format(
        key,
        server.translation.language,
        server.translation.value(key)))
    server.translation.language = "fr"
    print("{} ({}): {}".format(
        key,
        server.translation.language,
        server.translation.value(key)))
    server.translation.language = "de"
    print("{} ({}): {}".format(
        key,
        server.translation.language,
        server.translation.value(key)))
    server.translation.language = None
    print("{} ({}): {}".format(
        key,
        server.translation.language,
        server.translation.value(key)))


if __name__ == "__main__":
    main()
