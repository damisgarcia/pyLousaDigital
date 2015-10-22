# -*- coding: utf-8 -*-

#
#   @author: Damis Iuri Garcia do Vale
#

from lousadigital.so.client import *


from gi.repository import WebKit

class WebView:
    def __init__(self,port):
        print("Listen: http://127.0.0.1:%d/www/" % port)
        self.view = WebKit.WebView()        
        self.view.open("http://127.0.0.1:%d/www/" % port)
    #...
#
