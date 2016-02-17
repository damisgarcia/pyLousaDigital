# -*- coding: utf-8 -*-
"""
    @author:Damis Garcia
    class:  Media
    type:   Model
    description: 'Classe Media será utilizada para mapear e como bypass para as informações extraidas do Banco de Dados, informações que dizem a respeito
    do sistema de arquivos.'
"""

from enum import Enum

from lousadigital.model.activerecord import ActiveRecord

#
# Table: media
# fields:
#         id => interger, capture_id => interger,
#         type => enum[:master,:webcam,:desktop,:audio,:thumbnail], origin => string,deleted => boolean,
#         created_at => string
#

class MediaModel:
    _id = _type = capture_id = deleted = 0
    origin = created_at = ""
    types = Enum('Types', 'master webcam desktop audio thumbnail')

    def __init__(self,_id, capture_id ,_type, origin, created_at):
        self._id = _id
        self.capture_id = capture_id
        self._type = self.types(_type)
        self.origin = origin
        self.created_at = created_at

    def to_json(self):
        return "{u'id':%r,u'capture_id':%r,u'type':%r,u'deleted':%r,u'origin':%r,u'created_at':%r}" %(self._id,self.capture_id,self._type.name,self.deleted,self.origin,self.created_at)

    def to_hash(self):
        return {"id":self._id,"capture_id":self.capture_id,"type":self.type.name,"deleted":self.deleted,"origin":self.origin,"created_at":self.created_at}


class Media(MediaModel):
    class __ActiveRecord(ActiveRecord):
        table = "media"
        model = MediaModel

    active_record = __ActiveRecord()

    def __init__(self,_id, capture_id ,_type, origin, created_at):
        MediaModel.__init__(_id, capture_id ,_type, origin, created_at)
