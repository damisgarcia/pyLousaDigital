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

class RunTime(Gtk.VBox):
    version = "0.1.3"

    def __init__(self):        
        # HttpServer
        self.server = HttpServer()
        self.server.start()
        # Import UI
        self.gladefile = "../glade/browser.glade"
        self.glade = Gtk.Builder()
        self.glade.add_from_file(self.gladefile)
        self.glade.connect_signals(self)
        # Instanciando Window
        self.win = self.glade.get_object("main")
        self.win.show_all()
        self.win.resize(1024, 728)
        self.win.set_title("Lousa Digital - Version " + self.version)
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
