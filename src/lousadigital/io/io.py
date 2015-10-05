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
        for filepath in sorted(glob.glob(p),reverse=True):
            f = open(filepath)
            fst = os.stat(filepath)

            hfile = { "filename":f.name, "size":fst.st_size, "path": filepath }
            files.append(hfile)
        #...
        return files
    #

    def rename(self,old,new):
        try:
            for i in range(1,len(old)) :
                os.rename(old[i], new[i])
            #
            return { "success":True }
        except Exception as e:
            return { "error:" "não foi possível renomear este arquivo" }
    #

    def remove(self,targets):
        try:
            for target in targets :
                os.remove(target)
            #
            return { "success":True }
        except Exception as e:
            return { "error":"não foi possível excluir este arquivo" }
    #
#
