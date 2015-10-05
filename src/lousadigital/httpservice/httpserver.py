#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# @author: Damis Garcia
#
import sys
import random

import json

import SimpleHTTPServer
import SocketServer

import os, signal, subprocess

from lousadigital.io.io import FileManager
from lousadigital.ffmpeg.basic import Basic
import lousadigital.ffmpeg.FFMpeg as ffmpeg

from threading import Thread

class CustomHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    queue_recordings = []

    def __init__(self,request, client_address, server, fake=False):
        if fake == False:
            SimpleHTTPServer.SimpleHTTPRequestHandler.__init__(self, request, client_address, server)
        pass
    #

    def do_GET(self):
        if self.path=='/capture/new':
            self.queue_recordings.append(Basic(ffmpeg.captureWebcamAndDesktop()))
            self.queue_recordings[-1].start()
            self.setHeader()
            self.wfile.write('{"success":"Recording" }')
            return
        elif self.path=='/capture/save':
            # self.queue_recordings[-1].ffmpegExec.stop()
            os.killpg(self.queue_recordings[-1].process.pid, signal.SIGTERM)
            self.queue_recordings[-1].createThumbnail()

            self.setHeader()

            self.wfile.write('{"success":"Is Stoped" }')
            return
        elif self.path=='/capture/update':
            print( self.headers )
            self.setHeader()
            self.wfile.write('{"success":"Is Stoped" }')
            return
        elif self.path=='/repository/list':
            self.setHeader()
            body = json.dumps({'recorders': FileManager("www/files").getFiles() })
            self.wfile.write(body)
            return
        else:
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
        #
    #...

    def setHeader(self):
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()
    #...
#...

class HttpServer(Thread):
    def __init__(self):
        Thread.__init__(self)

        for i in range(1,999):
            try:
                self.port = random.randrange(9000, 9999)
                self.handler = CustomHandler
                self.httpd = SocketServer.TCPServer(("", self.port), self.handler)
                break
            except IOError as e:
                continue
            #
        #
    #...

    def run(self):
        try:
            self.httpd.serve_forever()
        except IOError as e:
            print(e)
            sys.exit()
        #
    #...

    def terminate(self):
        self.httpd.server_close()
    #...
#
