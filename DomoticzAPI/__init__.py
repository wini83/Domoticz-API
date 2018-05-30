#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .server import *
from .hardware import *
from .device import *
from .uservariable import *
from .notification import *
from .utilities import *

__version_major__ = 0
__version_minor__ = 2
__version_micro__ = 0

__version__ = "{}.{}.{}".format(__version_major__, __version_minor__, __version_micro__)


def version():
    return __version__


def version_major():
    return __version_major__


def version_minor():
    return __version_minor__


def version_micro():
    return __version_micro__
