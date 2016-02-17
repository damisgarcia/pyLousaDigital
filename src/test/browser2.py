#!/usr/bin/python
# encoding utf-8

#
# @author: Damis Garcia
#

import sys
import thread

from gi.repository import Gtk, Gdk, WebKit
from HttpService.HttpServer import HttpServer

import SimpleHTTPServer
import SocketServer

class Browser2(Gtk.VBox):
    version = "0.0.6"

    def __init__(self):
        # Import UI
        self.gladefile = "../glade/browser.glade"
        self.glade = Gtk.Builder()
        self.glade.add_from_file(self.gladefile)
        self.glade.connect_signals(self)
        # Instanciando Window
        self.win=self.glade.get_object("window1")
        self.win.show_all()
        self.win.resize(800, 600)
        self.win.set_title("Lousa Digital - Version " + self.version)

        # Bind Events

        # Top Menu =>
        self.glade.get_object("FileExit").connect("activate",exit)
    #

    def appendWebViem(self,wbv):
        self.glade.get_object("row").add(wbv)
        self.renderAll()
    #...

    def renderAll(self):
        self.win.show_all()
    #...
#

class WebkitView:
    def __init__(self):
        self.view = WebKit.WebView()
        self.view.open("http://www.google.com.br")
    #...
#


if __name__ == "__main__":
 a = Browser2()
 v = WebkitView()
 a.appendWebViem(v.view)
 Gtk.main()
