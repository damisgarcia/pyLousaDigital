#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# @author: Damis Garcia
#
import sys
import random

import json
import re

import SimpleHTTPServer
import SocketServer

import os, signal, subprocess

from lousadigital.io.io import FileManager
from lousadigital.io.io import Internet
from lousadigital.ffmpeg.basic import Basic
import lousadigital.ffmpeg.FFMpeg as ffmpeg

from threading import Thread

class CustomHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    queue_recordings = []
    uri_compiler = re.compile("^([/\w0-9]+)\?([\w\0-9\S]+)")

    def __init__(self,request, client_address, server, fake=False):
        if fake == False:
            SimpleHTTPServer.SimpleHTTPRequestHandler.__init__(self, request, client_address, server)
        pass
    #

    """
        @description: 'Toda requisição GET é passada por esse método.'
    """

    def do_GET(self):
        print(self.path)
        try:
            result = self.uri_compiler.match(self.path)
            self.path = result.group(1)
            self.params = self.toParams(result.group(2))
            pass
        except Exception as e:
            pass


        if self.path == '/capture/new':
            print( self.params['mode'] )
            basic = Basic(ffmpeg.captureWebcamAndDesktop())
            self.queue_recordings.append(basic)
            return

        if self.path=='/capture/new':
            #TODO: passar dispositivo de camera e microfone p/ captureWebcamAndDesktop
            self.queue_recordings.append(Basic(ffmpeg.captureWebcamAndDesktop()))
            self.queue_recordings[-1].start()
            self.setHeader()
            self.wfile.write('{"success":"Recording" }')
            return

        elif self.path == '/capture/save':
            self.queue_recordings[-1].ffmpegExec.stop()
            os.killpg(self.queue_recordings[-1].process.pid, signal.SIGTERM)
            return

        elif self.path=='/capture/save':
            self.queue_recordings[-1].ffmpegExec.stop()
            #os.killpg(self.queue_recordings[-1].process.pid, signal.SIGTERM)
            self.queue_recordings[-1].createThumbnail()
            self.setHeader()
            self.wfile.write('{"success":"Is Stoped" }')
            return

        elif self.path == '/capture/update':
            self.setHeader()
            self.wfile.write('{"success":"Is Stoped" }')
            return

        elif self.path == '/capture/destroy':
            self.setHeader()
            self.wfile.write('{"success":"Is Stoped" }')
            return

        elif self.path == '/repository/list':
            self.setHeader()
            body = json.dumps({'recorders': FileManager("www/files").getFiles() })
            self.wfile.write(body)
            return
        elif self.path == '/connection':
            isConnected = Internet().is_connected()
            self.setHeader()
            self.wfile.write( '{"online":%d}'%isConnected )

        else:
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
        #
    #...

    """
        @description: 'Configura para o servidor retornar um JSON'
        @void
    """

    def setHeader(self):
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()
    #...
    """
        @description: 'Converte os parametros passados na URL para um Hashmap'
        @params: args => String
        @return: Hashmap
    """
    def toParams(self,args):
        args = args.split("&")
        params = {}
        for p in args:
            param = p.split("=")
            params[param[0]] = param[1]
        #
        return params
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
