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
import pygame.camera

import pyaudio

class Devices(object):
    class __Webcam:
        def get_list(self):
            pygame.init()
            pygame.camera.init()
            return pygame.camera.list_cameras()

    class __Microphone:
        def get_list(self):
            pyaudio_devices = pyaudio.PyAudio()
            devices = []
            for i in range(pyaudio_devices.get_device_count()):
                device_name = pyaudio_devices.get_device_info_by_index(i).get('name')
                device_channel = pyaudio_devices.get_device_info_by_index(i).get('maxInputChannels')
                devices.append({'name':device_name,'channel':device_channel})
            return devices

    WebCam = __Webcam()
    Microphone = __Microphone()
