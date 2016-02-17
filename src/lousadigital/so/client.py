# -*- coding: utf-8 -*-
import platform
import sys

def isLinux():
    if platform.system() == "Linux":
        return True
    return False

def isWindows():
    if platform.system() == "Windows":
        return True
    return False
#...
