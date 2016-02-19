from lousadigital.persistence.factory import DBFactory
from lousadigital.model.media import Media

Media.active_record.insert({})
results =  Media.active_record.all
