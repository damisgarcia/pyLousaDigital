# -*- coding: utf-8 -*-

import requests
import json

token = "aa0f5b3196214b2757a95ec564604b9a4854f2f4e6709198edb70421084fb0b6"
url = "http://localhost:3000/api/v1/repositories/lesson/3?access_token=%s"%token


data = { 'lesson_id'    : 3, 'lesson_media' : "video"   }

headers = {'Accept':'application/json','Content-type': 'application/json'}

files = { 'file': open('files/19-outubro-2015-10-11-11.mp4', 'rb') }
r = requests.post(url, data=data, files=files)
print r.json()
