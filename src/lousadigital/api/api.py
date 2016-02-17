# -*- coding: utf-8 -*-
# @author: Damis Garcia

import urllib2
import requests

import json
import os

SERVER = "http://digitalclass.lme.ufc.br"

class Authorization(object):
    class __Authorization:
        credential = ".db/.credential"

        def __init__(self):
            self.getToken()
        #.....

        def getToken(self):
            try:
                with open(self.credential,"r") as f:
                    self.token = f.read()
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
            return { "code":0, "error": e.message }
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
            with open(self.instance.credential,"w") as f:
                f.write("%s\n" %credential)
            self.instance.getToken()
            return 1
        except Exception as e:
            return { "code":0, "exception": e.message }
    #...


    def __login(self,params):
        url = '%s/oauth/token' %(SERVER)
        req = urllib2.Request(url)
        req.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(req, json.dumps(params))
        jsonp = json.load(response)
        return jsonp
    #...

    def __profile(self,token):
        url = "%s/api/v1/users/profile?access_token=%s" %(SERVER,token)
        req = urllib2.Request(url)
        req.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(req)
        jsonp = json.load(response)
        return jsonp
    #...

class API:
    class __Upload:
        def create_contract(self,auth_token,lesson,title,description,privilege):
            url = "%s/api/v1/recordings/lesson/%s?access_token=%s"%(SERVER,lesson,auth_token)
            data = {
                'title' : title,
                'description' : description,
                'type' : int(privilege)
            }

            r = requests.post(url, data=data)
            return r.content

        def send_file(self,auth_token,recording_id,media_type,archive):
            url = "%s/api/v1/recordings/upload?access_token=%s"%(SERVER,auth_token)
            data = {
                'recording_id' : recording_id,
                'filename' : self.filename_generator(media_type),
                'type' : self.media_types(media_type)
            }

            with open(archive,"rb") as f:
                files = { "file" : f }
                r = requests.post(url, data=data, files=files)
                return r.content
            #...

        def media_types(self,arg):
            enum = {
                "video":0,
                "audio":1,
                "poster":2
            }
            return enum.get(arg,"invalid")
        #

        def filename_generator(self,arg):
            filename = os.urandom(16).encode('hex')
            enum = {
                "video":  "%s.%s" % (filename, "mp4"),
                "audio":  "%s.%s" % (filename, "mp3"),
                "poster": "%s.%s" % (filename, "jpg")
            }
            return enum.get(arg,"invalid")
        #.
    #...

    Uploader = __Upload()
