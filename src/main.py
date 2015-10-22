#!/usr/bin/python
# encoding utf-8

#
# @author: Damis Garcia
#

import sys
import thread

from lousadigital.so.client import *

from gi.repository import Gtk
from gi.repository import Gdk

from lousadigital.httpservice.httpserver import HttpServer
from lousadigital.browser.webkit import WebView
from lousadigital.persistence.factory import DBFactory

class RunTime(Gtk.VBox):
    version = "0.1.3"

    def __init__(self):
        # HttpServer
        self.server = HttpServer()
        self.server.start()
        # Desktop Screen
        self.screen_sizes = Gdk.Screen.get_default()
    	SCREEN_WIDTH =  self.screen_sizes.get_width()
    	SCREEN_HEIGHT = self.screen_sizes.get_height()

        # Database
        self.database = DBFactory()
        # Import UI
        self.gladefile = "../glade/browser-gtk2.glade"
        self.glade = Gtk.Builder()
        self.glade.add_from_file(self.gladefile)
        self.glade.connect_signals(self)
        # Instanciando Window
        self.win = self.glade.get_object("main")
        self.win.resize(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.win.show_all()

        self.win.set_title("Digital Class - Version " + self.version)
        self.win.set_icon_from_file('icon.png')
        self.win.connect("delete-event",self.exitFromClose)
        # Instanciando WebView
        self.appendWebViem( WebView(self.server.port).view )

        # Bind Events

        # Top Menu =>
        self.glade.get_object("FileExit").connect("activate",self.exitFromMenu)
    #

    def appendWebViem(self,webview):
        self.glade.get_object("webview").add(webview)
        self.renderAll()
    #...

    def renderAll(self):
        self.win.show_all()
    #...

    def exitFromMenu(self,Args1):
        self.server.terminate()
        sys.exit()
    #...

    def exitFromClose(self,Args1,Args2):
        self.server.terminate()
        sys.exit()
    #...
#


if __name__ == "__main__":
    a = RunTime()

    Gtk.main()
