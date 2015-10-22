# -*- coding: utf-8 -*-
# @author: Damis Garcia

import sys
import random

import os
import os.path
import glob
import mimetypes

import re
import json

import socket

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

    def findFileByName(self,expression):
        p = "%s/%s.*"%(self.path, expression)

        origins = []

        for filepath in sorted(glob.glob(p)):
            origins.append(filepath)

        return origins

    def rename(self,old,new):
        try:
            for i in old:
                basename = os.path.basename(i)
                basename_without_extension =  os.path.splitext(basename)[0]
                _new = i.replace(basename_without_extension, new)
                os.rename(i, _new)
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

class Internet(object):
    def is_connected(self):
      try:
        host = socket.gethostbyname("www.google.com.br")
        s = socket.create_connection((host, 80), 2)
        return 1
      except Exception as e:
         print(e)
         pass
      return 0

import pygame

class Devices(object):
    class __Webcam:
        def get_list(self):
            pygame.camera.list_cameras()

    WebCam = __Webcam()
