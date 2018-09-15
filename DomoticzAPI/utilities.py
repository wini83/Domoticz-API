import platform
from .server import *

__version_major__ = 0
__version_minor__ = 4
__version_micro__ = 4

__version__ = "{}.{}.{}".format(__version_major__, __version_minor__, __version_micro__)


def machine():
    return platform.machine()


def node():
    return platform.node()


def os_command(command, options):
    server = Server()
    res = server.os_command(command, options)
    return res


def os_release():
    return platform.release()


def os_version():
    return platform.version()


def processor():
    return platform.processor()


def python_version():
    return platform.python_version()


def system():
    return platform.system()


def version():
    return __version__


def version_major():
    return __version_major__


def version_minor():
    return __version_minor__


def version_micro():
    return __version_micro__


# Temperature conversion from Celsius to Fahrenheit
def TempC2F(value):
    return (value * 1.8) + 32


# Temperature conversion from Fahrenheit to Celsius
def TempF2C(value):
    return (value - 32) / 1.8

# Convert bearing in degrees to a direction
def Bearing2Status(d):
    """
    Based on https://gist.github.com/RobertSudwarts/acf8df23a16afdb5837f
    """
    dirs = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]

    count = len(dirs)  # Number of entries in list
    step = 360 / count  # Wind direction is in steps of 22.5 degrees (360/16)
    ix = int((d + (step / 2)) / step)  # Calculate index in the list
    return dirs[ix % count]
