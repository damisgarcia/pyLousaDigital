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
        self.output = dt.strftime("%d-%B-%Y_%I:%M:%S")

        ffmpegExec.args.output = self.output + ".mp4"

        ffmpegExec.execute()
        #command = "ffmpeg -video_size 1920x1080 -framerate 25 -f x11grab -i :0.0 -s 1280x768 www/files/%s.mp4" %(self.output)
        #self.process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, preexec_fn=os.setsid)
    #

    """
        Captura um específico frame da aula recém capturada
    """
    def createThumbnail(self):
        signal = -1
        while signal != 0:
            time.sleep(1)
            command = "ffmpeg -y -i %s%s.mp4 -vframes 1 -ss 1 -an %s%s.jpg" %(self.target, self.output, self.target, self.output)
            signal = subprocess.call(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        #
    #
#...
