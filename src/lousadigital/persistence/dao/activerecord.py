import sqlite3
import json

from lousadigital.persistence.factory import DBFactory

class ActiveRecord(object):
    database = DBFactory()
    primary_key = "id"

    def all(self):
        sql = "SELECT * FROM %r ;" % self.table
        list_captures = []
        try:
            self.database.factory.open()
            statament = self.database.factory.connection.cursor().execute(sql)
            for st in statament.fetchall():
                obj = ActiveRecord(*st)
                list_captures.append(obj)
        except Exception as e:
            print e
            pass
        finally:
            self.database.factory.close()
            return list_captures


    def find(self,arg):
        sql = ""
        capture = None

        if type(arg) is int:
            sql  = "SELECT * FROM %r WHERE %s = %d ;" % (self.table,self.primary_key,arg)
        elif type(arg) is str:
            sql  = "SELECT * FROM %r WHERE name = %r ;" % (self.table,arg)


        try:
            self.database.factory.open()
            statament = self.database.factory.connection.cursor().execute(sql)
            capture = ActiveRecord(*statament.fetchone())
            return capture
        except Exception as e:
            print e
            pass
        finally:
            self.database.factory.close()
            return capture

    def insert(self,args):
        sql = ""
        fields = ""
        symbols = ""
        values = []

        for key in args: fields += "%s," %key
        for key in args: symbols += "?, "
        for arg in args: values.append(args[arg])

        fields = fields[:-1]
        symbols = symbols[:-2]
        print fields
        print values

        sql = "INSERT INTO %s (%s) VALUES(%s) ;" %(self.table,fields,symbols)

        print sql

        try:
            self.database.factory.open()
            statament = self.database.factory.connection.cursor().execute(sql,values)
            self.database.factory.commit()
            return 1
        except Exception as e:
            print e
            return 0
        finally:
            self.database.factory.close()

    def update(self,args):
        sql = ""
        fields = ""
        values = []
        _id = 0

        for key in args:
            if key is "_id": _id = args[key]
            else: fields += "%s = ?, " %key

        for arg in args:
            if arg is "_id": next
            else: values.append(args[arg])

        fields = fields[:-2]

        sql = "UPDATE %s SET %s WHERE %s= %d" %(self.table,fields,self.primary_key,_id)

        print sql
        print values

        try:
            self.database.factory.open()
            statament = self.database.factory.connection.cursor().execute(sql,values)
            self.database.factory.commit()
            return 1
        except Exception as e:
            print e
            return 0
        finally:
            self.database.factory.close()

    def destroy(self,arg):
        sql = ""
        sql = "DELETE FROM %s WHERE %s = %d" %(self.table,self.primary_key,arg)

        try:
            self.database.factory.open()
            statament = self.database.factory.connection.cursor().execute(sql)
            self.database.factory.commit()
            return 1
        except Exception as e:
            print e
            return 0
        finally:
            self.database.factory.close()
