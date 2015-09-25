#!/usr/bin/python
# encoding utf-8

#
#   @author: Damis Iuri Garcia do Vale
#

from gi.repository import WebKit

class WebView:
    def __init__(self):
        self.view = WebKit.WebView()
        self.view.open("http://www.google.com.br")
    #...
#
