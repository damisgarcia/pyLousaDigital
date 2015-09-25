#!/usr/bin/python
# encoding utf-8

#
# @author: Damis Garcia
#
import sys

import SimpleHTTPServer
import SocketServer

from threading import Thread

class HttpServer(Thread):
    port = 9000
    def __init__(self):
        Thread.__init__(self)
        self.handler = SimpleHTTPServer.SimpleHTTPRequestHandler
        self.httpd = SocketServer.TCPServer(("", self.port), self.handler)
    #...

    def run(self):
        try:
            self.httpd.serve_forever()
        except Exception as e:
            print(e)
            sys.exit()
        #
    #...

    def terminate(self):
        self.httpd.server_close()
    #...
#
