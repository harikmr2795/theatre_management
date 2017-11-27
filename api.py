# import pycrypto
import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote
from google.appengine.ext import ndb

#Model
class Show(ndb.Model):
    name = ndb.StringProperty(indexed=True)
    capacity = ndb.IntegerProperty()
    available = ndb.IntegerProperty()

class BookRequest(messages.Message):
    tickets = messages.IntegerField(1)

class AddRequest(messages.Message):
    name = messages.StringField(1)
    capacity = messages.IntegerField(2)

DELETE_REQUEST = endpoints.ResourceContainer(message_types.VoidMessage, id=messages.StringField(1, variant=messages.Variant.STRING, required=True))

BOOK_REQUEST = endpoints.ResourceContainer(BookRequest, id=messages.StringField(1, variant=messages.Variant.STRING, required=True))

class ShowDetails(messages.Message):
    available = messages.IntegerField(1)
    capacity = messages.IntegerField(2)
    name = messages.StringField(3)
    id = messages.StringField(4)

class ListResponse(messages.Message):
    items = messages.MessageField(ShowDetails, 1, repeated=True)

class MessageResponse(messages.Message):
    message = messages.StringField(1)

@endpoints.api(name='theatre_management', version='v1')
class TheatreManagementApi(remote.Service):
    #Get Shows
    @endpoints.method(message_types.VoidMessage, ListResponse, path='theatre_management', http_method='get', name='list')
    def list(self, request):
        return ListResponse(items = [{'name': item.name, 'capacity': item.capacity, 'available': item.available, 'id': item.key.urlsafe()} for item in Show.query().order(Show.name)])

    # Add Show
    @endpoints.method(AddRequest, MessageResponse, path='theatre_management', http_method='post', name='add')
    def add(self, request):
        Show(name = request.name, available = request.capacity, capacity = request.capacity).put()
        return MessageResponse(message = "Successfully added " + request.name)

    #Remove Show
    @endpoints.method(DELETE_REQUEST, MessageResponse, path='theatre_management/{id}', http_method='delete', name='remove')
    def delete(self, request):
        show = ndb.Key(urlsafe = request.id).get()
        show.key.delete()
        return MessageResponse(message = show.name + " successfully removed")

    #Book Tickets
    @endpoints.method(BOOK_REQUEST, MessageResponse, path='theatre_management/{id}', http_method='put', name='book')
    def book(self, request):
        show = ndb.Key(urlsafe = request.id).get()
        if show.available >= request.tickets:
            show.available -= request.tickets
            show.put()
            return MessageResponse(message = "Successfully Booked " + str(request.tickets) + " ticket(s)")
        else:
            return MessageResponse(message = "Oops, We don't have " + str(request.tickets) + " ticket(s)")        

app = endpoints.api_server([TheatreManagementApi])