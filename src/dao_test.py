# -*- coding: utf-8 -*-
from lousadigital.model.capture import *
from lousadigital.model.media import *

from time import gmtime, strftime
import json

print "select ALL"

for ctp in Capture.active_record.all():
    print ctp.to_json()

now = strftime("%Y-%m-%d %H:%M:%S", gmtime())
inserts = {"lesson_id":1,"name":"Lorem","created_at":now}
Capture.active_record.insert(inserts)
# Capture.active_record.update(updates)
