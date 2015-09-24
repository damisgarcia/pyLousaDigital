#!/usr/bin/python
# encoding utf-8
#
# @author: Damis Garcia
#

import sys
from gi.repository import Gtk, Gdk, WebKit

class Browser2:
    version = "0.0.6"
    def __init__(self):
        # Import UI
        self.gladefile = "../../glade/browser.glade"
        self.glade = Gtk.Builder()
        self.glade.add_from_file(self.gladefile)
        self.glade.connect_signals(self)
        # Instanciando Window
        self.win=self.glade.get_object("window1")
        self.win.show_all()
        self.win.resize(800, 600)
        self.win.set_title("Lousa Digital - Version " + self.version)
        #
if __name__ == "__main__":
 a = Browser2()
 Gtk.main()
