# NOT MAINTAINED ANYMORE!!!
I am disappointed in the way Domoticz developes: 
* 1 stable version per year, I had to wait 4 months until a bug was fixed
* no reaction on reported bugs, also if you give a direction for solution
* lost data after upgrade to a new stable versions
* etc.

So I moved to Home Assistant, and have no time/environment to maintain this plugin

# Python Domoticz API

The goal of this project is to have access to other devices, user variables, send notifications, etc. in Domoticz Python plugins.
This API uses the interfaces as defined at [Domoticz API/JSON URL's](https://www.domoticz.com/wiki/Domoticz_API/JSON_URL%27s). This page does not describe all available url's. This API also uses some 'undocumented' api url's.

##Installation

sudo pip install git+git://github.com/wini83/Domoticz-API.git

## This is an beta version

Therefore this api is not fully tested, or contains incorrect or incomplete documentation in the [Wiki](https://github.com/Xorfor/Domoticz-API/wiki), etc.
Use the code at your own risk.
Please look at the [`test_*.py`](https://github.com/Xorfor/Domoticz-API/tree/master/DomoticzAPI/tests)-examples how to use this api. The `plugin.py` contains an implementation of this api.

## Status
| Class                                   | Status
| :---                                    | :---
| [API](../../wiki/API)                   | <img src="https://img.shields.io/badge/Status-Stable-green.svg?style=flat-square" />
| [Color](../../wiki/Color)               | <img src="https://img.shields.io/badge/Status-Stable-green.svg?style=flat-square" />
| [Device](../../wiki/Device)             | <img src="https://img.shields.io/badge/Status-Stable-green.svg?style=flat-square" />
| [Hardware](../../wiki/Hardware)         | <img src="https://img.shields.io/badge/Status-Stable-green.svg?style=flat-square" />
| [Notification](../../wiki/Notification) | <img src="https://img.shields.io/badge/Status-Stable-green.svg?style=flat-square" />
| [RoomPlan](../../wiki/RoomPlan)         | <img src="https://img.shields.io/badge/Status-Stable-green.svg?style=flat-square" />
| [Server](../../wiki/Server)             | <img src="https://img.shields.io/badge/Status-Stable-green.svg?style=flat-square" />
| [Scene](../../wiki/Scene-(Group))         | <img src="https://img.shields.io/badge/Status-Stable-green.svg?style=flat-square" />
| [Setting](../../wiki/Setting)           | <img src="https://img.shields.io/badge/Status-Stable-green.svg?style=flat-square" />
| [Translation](../../wiki/Translation)   | <img src="https://img.shields.io/badge/Status-Stable-green.svg?style=flat-square" />
| [UserVariable](../../wiki/UserVariable) | <img src="https://img.shields.io/badge/Status-Stable-green.svg?style=flat-square" />

## History

| Version | Description
| :---    | :---
| 0.12.6  | Added Scene class
| 0.11.0  | Improvements
| 0.10.0  | Added server.update to update Domoticz software on server
| 0.9.0   | Added Translation class
| 0.8.0   | Added Setting class
| 0.7.1   | Added functions to add, list and delete devices in RoomPlans
| 0.7.0   | Introduced API class as property of Server for more flexibility
| 0.6.0   | Added (Room)Plan class
| 0.4.3   | Added resetSecurityStatus in Device
| 0.4.2   | Implemented Color class in Device
| 0.4.1   | Code cleanup
| 0.4.0   | Added ability to switch on, off or toggle (switch) devices and set the level for a light switch.
