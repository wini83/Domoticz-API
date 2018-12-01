'''
    Constants
'''
# Color Modes
COLOR_MODE_NONE = 0  # Illegal
COLOR_MODE_WHITE = 1  # White. Valid fields: none
COLOR_MODE_TEMP = 2  # White with color temperature. Valid fields: t
COLOR_MODE_RGB = 3  # Color. Valid fields: r, g, b.
# Custom (color + white). Valid fields: r, g, b, cw, ww, depending on device capabilities
COLOR_MODE_CUSTOM = 4

# Limit on number values
NUM_MIN = 0
NUM_MAX = 255

# Requests
REQUEST_URL = "json.htm?"
REQUEST_TYPE = "type"
REQUEST_PARAM = "param"

TYPE_COMMAND = "command"
TYPE_HARDWARE = "hardware"

REQUEST_COMMAND = "{}={}&".format(REQUEST_TYPE, TYPE_COMMAND)

REQUEST_TYPE_COMMAND = "{}={}".format(REQUEST_TYPE, TYPE_COMMAND)
REQUEST_COMMANDPARAM = "{}&{}".format(REQUEST_TYPE_COMMAND, REQUEST_PARAM) + "={}"

# Responses
RETURN_OK = "OK"
RETURN_ERROR = "ERR"

# Switch parameters used for: setcolbrightnessvalue
SWITCH_ON = "On"
SWITCH_OFF = "Off"
SWITCH_TOGGLE = "Toggle"

SWITCH_LIGHT_VALUES = {
    SWITCH_ON,
    SWITCH_OFF,
    SWITCH_TOGGLE,
}

SWITCH_SET_LEVEL = "Set Level"

# Version
VERSION_MAJOR = 0
VERSION_MINOR = 6
VERSION_MICRO = 2

VERSION_SHORT = '{}.{}'.format(VERSION_MAJOR, VERSION_MINOR)
VERSION = "{}.{}.{}".format(VERSION_MAJOR, VERSION_MINOR, VERSION_MICRO)