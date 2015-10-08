#!/usr/bin/python
# -*- coding: utf-8 -*-
# @author: Damis Garcia

import sys
import random

import os
import os.path
import glob
import mimetypes


import json

import socket
import urllib2

class FileManager:
    def __init__(self,path):
        self.path = path
    #

    def getFiles(self):
        p = "%s/*" % self.path
        files = []
        for filepath in sorted(glob.glob(p),reverse=True):
            f = open(filepath)
            fst = os.stat(filepath)

            hfile = { "filename":f.name, "size":fst.st_size, "path": filepath }
            files.append(hfile)
        #...
        return files
    #

    def rename(self,old,new):
        try:
            for i in range(1,len(old)) :
                os.rename(old[i], new[i])
            #
            return { "success":True }
        except Exception as e:
            return { "error:" "não foi possível renomear este arquivo" }
    #

    def remove(self,targets):
        try:
            for target in targets :
                os.remove(target)
            #
            return { "success":True }
        except Exception as e:
            return { "error":"não foi possível excluir este arquivo" }
    #
#

class Internet(object):
    def is_connected(self):
      try:
        host = socket.gethostbyname("www.google.com.br")
        s = socket.create_connection((host, 80), 2)
        return 1
      except Exception as e:
         print(e)
         pass
      return 0

# Singleton
class Authorization(object):
    class __Authorization:
        credential = ".db/.credential"
        server = "http://10.40.0.32"

        def __init__(self):
            self.getToken()
        #.....

        def getToken(self):
            try:
                f = open(self.credential,"r")
                self.token = f.read()
                f.close()
            except Exception as e:
                self.token = None
        #....

    instance = __Authorization()

    def __init__(self): pass

    def save(self,params):
        # Auth
        try:
            token = self.__login(params)["access_token"]
            profile = self.__profile(token)
            self.__create_credential(token)
            return {"code":1,"profile":profile,"access_token":self.instance.token}
        except Exception as e:
            # HTTPError
            self.destroy_token()
            return {"code":0, "status":e.getcode(), "message":e.message}

    #...

    def destroy_token(self):
        try:
            os.remove(self.instance.credential)
            self.instance.token = None
            return 1
        except Exception as e:
            return { "code":0, "error":e.message }
    #...

    def token(self):
        if self.instance.token:
            profile = self.__profile(self.instance.token)
            return {"code":1,"token":self.instance.token,"profile":profile}
        else:
            return {"code":0,"message":"Token de acesso não existe."}
    #...

    # @privates
    def __create_credential(self,credential):
        try:
            f = open(self.instance.credential,"w")
            f.write("%s\n" %credential)
            f.close()
            self.instance.getToken()
            return 1
        except Exception as e:
            return { "code":0, "exception": e }
    #...


    def __login(self,params):
        url = '%s/oauth/token' %(self.server)
        req = urllib2.Request(url)
        req.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(req, json.dumps(params))
        jsonp = json.load(response)
        return jsonp
    #...

    def __profile(self,token):
        url = "%s/api/v1/users/profile?access_token=%s" %(self.server,token)
        req = urllib2.Request(url)
        req.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(req)
        jsonp = json.load(response)
        return jsonp
    #...
