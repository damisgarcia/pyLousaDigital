# -*- coding: utf-8 -*-
import sqlite3

class DBFactory(object):
    class __DBFactory:
        uri = ".db/ld.db"
        def __init__(self):
            try:
                self.connection = sqlite3.connect(self.uri)
                pass
            except Exception as e:
                self.connection = None
                print(e.message)
        #...

        def close(self):
            self.connection.close()
        #...
    factory = __DBFactory(self)

    def __init__(self): pass
