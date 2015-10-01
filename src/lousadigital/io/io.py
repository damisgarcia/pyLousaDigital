#!/usr/bin/python
# -*- coding: utf-8 -*-
# @author: Damis Garcia

import sys
import random

import os
import os.path
import glob
import mimetypes

class FileManager:
    def __init__(self,path):
        self.path = path
    #

    def getFiles(self):
        p = "%s/*" % self.path
        files = []
        for filepath in sorted(glob.glob(p)):
            f = open(filepath)
            fst = os.stat(filepath)

            hfile = { "filename":f.name, "size":fst.st_size, "path": filepath }
            files.append(hfile)
        #...
        return files
    #
#
