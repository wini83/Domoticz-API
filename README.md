# Python Domoticz API

The goal of this project is to have access to other devices, user variables, send notifications, etc. in Domoticz Python plugins.
This API uses the interfaces as defined at [Domoticz API/JSON URL's](https://www.domoticz.com/wiki/Domoticz_API/JSON_URL%27s). This page does not describe all available url's. This API also uses some 'undocumented' api url's.

## This is an beta version

Therefore this api is not fully tested, or contains incorrect or incomplete documentation in the [Wiki](https://github.com/Xorfor/Domoticz-API/wiki), etc.
Use the code at your own risk.
Please look at the `test_*.py`-examples how to use this api. The `plugin.py` contains an implementation of this api.

## Status
| Class                                                                    | Status
| :---                                                                     | :---
| [Server](../../wiki/Server)             | <img src="https://img.shields.io/badge/Status-Stable-green.svg" />
| [API](../../wiki/API)                   | <img src="https://img.shields.io/badge/Status-Stable-green.svg" />
| [Hardware](../../wiki/Hardware)         | <img src="https://img.shields.io/badge/Status-Stable-green.svg" />
| [Device](../../wiki/Device)             | <img src="https://img.shields.io/badge/Status-Stable-green.svg" />
| [UserVariable](../../wiki/UserVariable) | <img src="https://img.shields.io/badge/Status-Stable-green.svg" />
| [Notification](../../wiki/Notification) | <img src="https://img.shields.io/badge/Status-Stable-green.svg" />
| [Color](../../wiki/Color)               | <img src="https://img.shields.io/badge/Status-Stable-green.svg" />
| [Plan](../../wiki/RoomPlan)             | <img src="https://img.shields.io/badge/Status-Stable-green.svg" />

## History

| Version | Description
| :---    | :---
| 0.7.0   | Introduced API class as property of Server for more flexibility
| 0.6.0   | Added (Room)Plan class
| 0.4.3   | Added resetSecurityStatus in Device
| 0.4.2   | Implemented Color class in Device
| 0.4.1   | Code cleanup
| 0.4.0   | Added ability to switch on, off or toggle (switch) devices and set the level for a light switch.
