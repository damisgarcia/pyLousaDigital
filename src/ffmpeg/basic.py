#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# @author: Damis Garcia
#
import os, sys, signal, time
import subprocess
from datetime import datetime, date

from threading import Thread

class Basic(Thread):
    output = ""

    def __init__(self):
        Thread.__init__(self)
    #

    def run(self):
        dt = datetime.now()
        self.output = dt.strftime("%d-%B-%Y_%I:%M:%S")
        command = "ffmpeg -video_size 1920x1080 -framerate 25 -f x11grab -i :0.0 -s 1280x768 www/files/%s.mp4" %(self.output)
        self.process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, preexec_fn=os.setsid)
    #

    """ Captura um específico frame da aula recém capturada """
    def createThumbnail(self):
        for count in range(1,60):
            print(self.output)
            command = "ffmpeg -y -i www/files/%s.mp4 -vframes 1 -ss 1 -an www/files/%s.jpg" %(self.output,self.output)
            signal = subprocess.call(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            if(signal == 0):
                break
            else:
                time.sleep(1)
            #
        #
    #
#...
