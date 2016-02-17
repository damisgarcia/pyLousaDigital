# -*- coding: utf-8 -*-

from lousadigital.model.activerecord import ActiveRecord

"""
    @author:Damis Garcia
    class:  Capture
    type:   Model
    description: 'Classe Capture será utilizada para mapear e como bypass para as informações extraidas do Banco de Dados'
"""
class CaptureModel(object):
    _id = lesson_id = synchronised = 0
    name = created_at = ""


    def __init__(self,_id,lesson_id,name,synchronised,created_at):
        self._id = _id
        self.lesson_id = lesson_id
        self.name = name
        self.synchronised = synchronised
        self.created_at = created_at


    def to_json(self):
        return "{u'id':%r,u'lesson_id':%r,u'name':%r,u'synchronised':%r,u'created_at':%r}" %(self._id,self.lesson_id,self.name,self.synchronised,self.created_at)

    def to_hash(self):
        return {"id":self._id,"lesson_id":self.lesson_id,"name":self.name,"synchronised":self.synchronised,"created_at":self.created_at}


class Capture(CaptureModel):
    class __ActiveRecord(ActiveRecord):
        table = "captures"
        model = CaptureModel

    active_record = __ActiveRecord()

    def __init__(self,_id,lesson_id,name,synchronised,created_at):
        CaptureModel.__init__(_id,lesson_id,name,synchronised,created_at)
