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
        self.output = dt.strftime("%d-%B-%Y-%I-%M-%S")
        self.ffmpegExec.args.output = self.target + self.output + ".mp4"
        self.ffmpegExec.args.videoIn.fgInput = "/dev/video0"
        self.ffmpegExec.execute()
        # command = "ffmpeg -video_size 1920x1080 -framerate 25 -f x11grab -i :0.0 -s 1280x768 www/files/%s.mp4" %(self.output)
        # self.process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, preexec_fn=os.setsid)

        # self.ffmpegExec.args.output = self.target + self.output + ".mp4"

        # self.ffmpegExec.execute()
        #command = "ffmpeg -video_size 1920x1080 -framerate 20 -f x11grab -i :0.0 -s 1280x768 www/files/%s.mp4" %(self.output)
        #self.process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, preexec_fn=os.setsid)

        # ffmpeg -y -video_size 1920x1080 -f x11grab -i :0.0 -i /dev/video0 -filter_complex "[0:v]setpts=PTS-STARTPTS[background];[1:v]setpts=PTS-STARTPTS,scale= 320:-1[foreground];[background][foreground]overlay=main_w-overlay_w-5:main_h-overlay_h-5" -f pulse -i default -strict -2 -codec:a aac -b:a 64k output.mp4



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
