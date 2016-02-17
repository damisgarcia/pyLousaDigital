# -*- coding: utf-8 -*-
import sqlite3

class DBFactory(object):
    class __DBFactory:
        uri = ".db/ld.db"

        def __init__(self):
            try:
                self.connection = sqlite3.connect(self.uri)
                self.createTables()
                self.connection.close()
                pass
            except Exception as e:
                raise
        #...

        def open(self):
            self.connection = sqlite3.connect(self.uri)

        def close(self):
            self.connection.close()

        def commit(self):
            self.connection.commit()

        def createTables(self):
            # Table: captures
            # fields: id => interger, name => string, lesson_id => interger, synchronised => boolean, created_at => string
            sql_table_captures = "CREATE TABLE captures( \
             id INTEGER PRIMARY KEY AUTOINCREMENT,\
             name TEXT NOT NULL,\
             lesson_id INTEGER NOT NULL,\
             synchronised INTEGER DEFAULT 0,\
             created_at TEXT NOT NULL\
             );"

            sql_table_captures_exist = "SELECT name FROM sqlite_master WHERE type='table' AND name='captures';"

            #
            # Table: media
            # fields:
            #         id => interger, capture_id => interger,
            #         type => enum[:master,:webcam,:desktop,:audio,:thumbnail], origin => string,deleted => boolean,
            #         created_at => string
            #

            sql_table_media = "CREATE TABLE media( \
             id INTEGER PRIMARY KEY,\
             capture_id INTEGER ,\
             type INTEGER NOT NULL,\
             origin TEXT NOT NULL,\
             deleted INTEGER DEFAULT 0,\
             created_at TEXT NOT NULL,\
             FOREIGN KEY(capture_id) REFERENCES captures(id)\
             );"

            sql_table_media_exist = "SELECT name FROM sqlite_master WHERE type='table' AND name='media';"

            try:
                cursor = self.connection.cursor()

                r1 = cursor.execute(sql_table_captures_exist).fetchall()
                if len(r1) <= 0:
                    cursor.execute(sql_table_captures)
                    self.commit()

                r2 = cursor.execute(sql_table_media_exist).fetchall()
                if len(r2) <= 0:
                    cursor.execute(sql_table_media)
                    self.commit()

            except sqlite3.OperationalError as e:
                raise
            except Exception as e:
                raise
            finally:
                self.close()
            #
        #

    factory = __DBFactory()

    def __init__(self): pass
