#!/usr/bin/python
# encoding utf-8

#
# @author: Damis Garcia
#
import os, sys, signal
import subprocess
from datetime import datetime, date, time

from threading import Thread

class Basic(Thread):
    def __init__(self):
        self.stdout = None
        self.stderr = None
        self.proc = None
        Thread.__init__(self)
    #

    def run(self):
        dt = datetime.now()
        self.output = dt.strftime("%d-%B-%Y_%I:%M:%S")
        self.command = "ffmpeg -video_size 1024x768 -framerate 25 -f x11grab -i :0.0+100,200 www/files/%s.mp4" % self.output
        self.proc = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    #

    def terminate(self):
        self.proc.terminate()
    #
#...
