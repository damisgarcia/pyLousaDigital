#!/usr/bin/python
# encoding utf-8

#
# @author: Damis Garcia
#
import sys
import random

import json

import SimpleHTTPServer
import SocketServer

from io.io import FileManager
from ffmpeg.basic import Basic

from threading import Thread

class CustomHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        if not hasattr(self,'Recorder'):
            self.Recorder = Basic()
        if self.path=='/capture/new':
            self.Recorder.start()
            self.Recorder.join()
            self.send_response(200)
            self.send_header('Content-type','application/json')
            self.end_headers()
            self.wfile.write('{"success":"Recording" }') #call sample function here
            return
        elif self.path=='/capture/save':
            self.Recorder.terminate()
            self.send_response(200)
            self.send_header('Content-type','application/json')
            self.end_headers()
            self.wfile.write('{"success":"Is Stoped" }') #call sample function here
            return
        elif self.path=='/repository/list':
            self.send_response(200)
            self.send_header('Content-type','application/json')
            self.end_headers()
            # ffmpeg -video_size 1024x768 -framerate 25 -f x11grab -i :0.0+100,200 output.mp4
            body = json.dumps({'recorders': FileManager("www/files").getFiles() })
            self.wfile.write(body) #call sample function here
            return
        else:
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
        #
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
