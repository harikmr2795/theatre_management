from google.appengine.ext import ndb
from endpoints_proto_datastore.ndb.model import EndpointsModel

class Show(EndpointsModel):
    """ Save a show to the datastore """
    name = ndb.StringProperty(indexed=True)
    capacity = ndb.IntegerProperty()
    available = ndb.IntegerProperty()
    _message_fields_schema = ("entityKey", "name", "capacity", "available")