# -*- coding: utf-8 -*-
# @author: Damis Garcia

import urllib2
import requests

import json

SERVER = "http://22b9af06.ngrok.io/"

class Authorization(object):
    class __Authorization:
        credential = ".db/.credential"
        server = "http://22b9af06.ngrok.io"

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
            with open(self.instance.credential,"w") as f:
                f.write("%s\n" %credential)
            self.instance.getToken()
            return 1
        except Exception as e:
            return { "code":0, "exception": e.message }
    #...


    def __login(self,params):
        url = '%s/oauth/token' %(self.instance.server)
        req = urllib2.Request(url)
        req.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(req, json.dumps(params))
        jsonp = json.load(response)
        return jsonp
    #...

    def __profile(self,token):
        url = "%s/api/v1/users/profile?access_token=%s" %(self.instance.server,token)
        req = urllib2.Request(url)
        req.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(req)
        jsonp = json.load(response)
        return jsonp
    #...

class API:
    class __Upload:
        def send_file(self,auth_token,lesson,media_lesson,archive):
            url = "%s/api/v1/repositories/lesson/%s?access_token=%s"%(SERVER,lesson,auth_token)
            data = {'lesson_media' : media_lesson }

            with open(archive,"rb") as f:
                files = { "file" : f }
                r = requests.post(url, data=data, files=files)
                return r.content
    #...

    Uploader = __Upload()
