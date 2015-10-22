#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# @author: Damis Garcia
#
import os, sys, signal, time
import subprocess
from datetime import datetime, date

from threading import Thread

from lousadigital.ffmpeg.FFMpeg import *
from lousadigital.so.client import *

class Basic(Thread):
    target = "www/files/"
    output = ""

    ffmpegExec = None

    def __init__(self,ffmpegExec):
        Thread.__init__(self)

        self.ffmpegExec = ffmpegExec
    #

    def run(self):
        dt = datetime.now()
        self.output = dt.strftime("%d-%B-%Y-%I-%M-%S")
        self.ffmpegExec.args.output = self.target + self.output + ".mp4"

        if isLinux():
            self.ffmpegExec.args.videoIn.fgInput = "/dev/video0"
        #...

        self.ffmpegExec.execute()
    #

    """
        Captura um específico frame da aula recém capturada
    """
    def createThumbnail(self):
        signal = -1
        while signal != 0:
            command = "ffmpeg -y -i %s%s.mp4 -vframes 1 -ss 1 -an %s%s.jpg" %(self.target, self.output, self.target, self.output)
            signal = subprocess.call(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            time.sleep(1)
        #
    #
#...
