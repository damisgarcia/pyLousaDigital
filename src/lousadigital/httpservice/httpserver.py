# -*- coding: utf-8 -*-

#
# @author: Damis Garcia
#
import sys
import random

import json
import re
import urllib

import SimpleHTTPServer
import SocketServer

import os, signal, subprocess

from lousadigital.api.api import API
from lousadigital.api.api import Authorization

from lousadigital.so.client import *
from lousadigital.io.io import FileManager
from lousadigital.io.io import Internet
from lousadigital.io.io import Devices
from lousadigital.ffmpeg.basic import Basic
import lousadigital.ffmpeg.FFMpeg as ffmpeg

from threading import Thread

class CustomHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    queue_recordings = []
    uri_compiler = re.compile("^([/\w0-9]+)\?([\w\0-9\S]+)")

    def __init__(self,request, client_address, server, fake=False):
        self.auth = Authorization()
        self.filemanager = FileManager("www/files")

        if fake == False:
            SimpleHTTPServer.SimpleHTTPRequestHandler.__init__(self, request, client_address, server)
        pass
    #

    """
        @description: 'Toda requisição GET é passada por esse método.'
        @params: mode => ['1'=> 'Tela e Áudio','2' => 'Webcam, Áudio','3'=> 'Tela, Áudio e Webcam']
    """

    def do_GET(self):
        try:
            result = self.uri_compiler.match(self.path)
            self.path = result.group(1)
            self.params = self.toParams(result.group(2))
            pass
        except Exception as e:
            pass
        if self.path == "/auth/singin":
            self.params["grant_type"] = "password"
            res = self.auth.save(self.params)

            if res["code"] is 1:
                self.setHeader(200)
                self.wfile.write(json.dumps(res))
            else:
                self.setHeader(403)
                self.wfile.write(json.dumps(res))
            return

        if self.path == '/auth/token/get':
            res = self.auth.token()
            if res["code"] is 1:
                self.setHeader(200)
                body = json.dumps(res)
                self.wfile.write(body)
            else:
                self.setHeader(403)
                body = json.dumps(res)
                self.wfile.write(body)
            return

        if self.path == '/auth/token/destroy':
            is_destroyed = self.auth.destroy_token()
            if is_destroyed is 1:
                self.setHeader(200)
                body = '{"success":true}'
                self.wfile.write(body)
            else:
                self.setHeader(403)
                body = json.dumps(is_destroyed)
                self.wfile.write(body)
            return

        if self.path=='/capture/new':
            #TODO: passar dispositivo de camera e microfone p/ captureWebcamAndDesktop
            mode = int(self.params["mode"])
            args = {}

            if self.params["videodevice"]:
                args["videoInput"] = self.params["videodevice"]

            if self.params["audiodevice"]:
                args["audioInput"] = "'%s'" % self.params["audiodevice"]

            if self.params["audiochannel"]:
                args["audioChannel"] = int( self.params["audiochannel"] )

            print args

            if mode == 1:
                self.queue_recordings.append(Basic(ffmpeg.captureDesktop(**args)))
            elif mode == 2:
                if isLinux():
                    self.queue_recordings.append(Basic(ffmpeg.captureWebcam(**args)))
                if isWindows():
                    self.queue_recordings.append(Basic(ffmpeg.captureWebcam(**args)))
            elif mode == 3:
                self.queue_recordings.append(Basic(ffmpeg.captureWebcamAndDesktop(**args)))

            self.queue_recordings[-1].start()
            self.setHeader(200)
            self.wfile.write('{"success":"Recording" }')
            return

        elif self.path=='/capture/save':
            self.queue_recordings[-1].ffmpegExec.stop()
            self.queue_recordings[-1].createThumbnail()
            self.setHeader(200)
            self.wfile.write('{"success":"Is Stoped" }')
            return

        elif self.path == '/capture/update':
            origins = self.filemanager.findFileByName(self.params["old"])
            self.filemanager.rename(origins,self.params["new"])

            self.setHeader(200)
            self.wfile.write('{"success":"Is Stoped" }')
            return

        elif self.path == '/capture/destroy':
            origins = self.filemanager.findFileByName(self.params["target"])
            self.filemanager.remove(origins)
            self.setHeader(200)
            self.wfile.write('{"success":"Is Stoped" }')
            return

        elif self.path == '/capture/upload':
            try:
                archives = self.filemanager.findFileByName(self.params["archive"])
                for archive in archives:
                    begin = ( len(archive) - 4 )
                    end = len(archive)
                    if archive.find(".mp4",begin,end) != -1: API.Uploader.send_file( self.params["access_token"], self.params["lesson_id"], "video", archive )
                    elif archive.find(".mp3",begin,end) != -1: API.Uploader.send_file( self.params["access_token"], self.params["lesson_id"], "audio", archive )

                self.setHeader(200)
                body = '{"success":1}'
                pass
            except Exception as e:
                self.setHeader(400)
                body = '{"success":0, "message": %s}' % e.message
                pass


            self.wfile.write(body)
            return

        elif self.path == '/repository/list':
            self.setHeader(200)
            body = json.dumps({ 'recorders': self.filemanager.getFiles() })
            self.wfile.write(body)
            return

        elif self.path == '/devices/list/webcam':
            self.setHeader(200)
            print Devices.WebCam.get_list()
            body = json.dumps({ 'devices': Devices.WebCam.get_list() })
            self.wfile.write(body)
            return

        elif self.path == '/devices/list/mic':
            self.setHeader(200)
            print Devices.Microphone.get_list()
            body = json.dumps({ 'devices': Devices.Microphone.get_list() })
            self.wfile.write(body)
            return

        elif self.path == '/connection':
            isConnected = Internet().is_connected()
            self.setHeader(200)
            self.wfile.write( '{"online":%d}'%isConnected )

        else:
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
        #
    #...

    """
        @description: 'Configura para o servidor retornar um JSON'
        @void
    """

    def setHeader(self,code):
        self.send_response(code)
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
            params[param[0]] = urllib.unquote(param[1]) # Normalizando String
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
