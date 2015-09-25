#!/usr/bin/python
# encoding utf-8

#
# @author: Damis Garcia
#

import sys
import thread

from gi.repository import Gtk, Gdk
from httpservice.httpserver import HttpServer
from browser.webkit import WebView

class Browser2(Gtk.VBox):
    version = "0.0.6"

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
        self.win=self.glade.get_object("window1")
        self.win.show_all()
        self.win.resize(1024, 728)
        self.win.set_title("Lousa Digital - Version " + self.version)
        self.win.connect("delete-event",self.exitFromClose)
        # Instanciando WebView
        self.appendWebViem( WebView().view )

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
    a = Browser2()

    Gtk.main()
