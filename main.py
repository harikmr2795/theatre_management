import os
import webapp2
from google.appengine.ext.webapp import template
import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote
from google.appengine.ext import ndb
# import pycrypto

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

DELETE_REQUEST = endpoints.ResourceContainer(message_types.VoidMessage, token=messages.StringField(1, variant=messages.Variant.STRING))

BOOK_REQUEST = endpoints.ResourceContainer(BookRequest, token=messages.StringField(1, variant=messages.Variant.STRING, required=True))

class ShowDetails(messages.Message):
    available = messages.IntegerField(1)
    capacity = messages.IntegerField(2)
    name = messages.StringField(3)
    token = messages.StringField(4)

class ListResponse(messages.Message):
    items = messages.MessageField(ShowDetails, 1, repeated=True)

class MessageResponse(messages.Message):
    message = messages.StringField(1)

@endpoints.api(name='theatre_management', version='v1')
class TheatreManagementApi(remote.Service):
    #Get Shows
    @endpoints.method(message_types.VoidMessage, ListResponse, path='theatre_management', http_method='get', name='list')
    def list(self, request):
        return ListResponse(items = [{'name': item.name, 'capacity': item.capacity, 'available': item.available, 'token': item.key.urlsafe()} for item in Show.query().order(Show.name)])

    # Add Show
    @endpoints.method(AddRequest, MessageResponse, path='theatre_management', http_method='post', name='add')
    def add(self, request):
        Show(name = request.name, available = request.capacity, capacity = request.capacity).put()
        return MessageResponse(message = "Successfully added " + request.name)

    #Remove Show
    @endpoints.method(DELETE_REQUEST, MessageResponse, path='theatre_management/{token}', http_method='delete', name='remove')
    def delete(self, request):
        show = ndb.Key(urlsafe = request.token).get()
        show.key.delete()
        return MessageResponse(message = str(show.name) + " successfully removed")

    #Book Tickets
    @endpoints.method(BOOK_REQUEST, MessageResponse, path='theatre_management/{token}', http_method='put', name='book')
    def book(self, request):
        show = ndb.Key(urlsafe = request.token).get()
        if show.available >= request.tickets:
            show.available -= request.tickets
            show.put()
            return MessageResponse(message = "Successfully Booked " + str(request.tickets) + " ticket(s)")
        else:
            return MessageResponse(message = "Oops, We don't have " + str(request.tickets) + " ticket(s)")


#Home page
class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(template.render(os.path.join(os.path.dirname(__file__), 'html/index.html'), {}))

#Booking a ticket
class SelectShowHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(template.render(os.path.join(os.path.dirname(__file__), 'html/buy.html'), {}))

#Viewing sold details
class SoldHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(template.render(os.path.join(os.path.dirname(__file__), 'html/sold.html'), {}))

#Adding a new show
class AddHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(template.render(os.path.join(os.path.dirname(__file__), 'html/add.html'), {}))
         
#Removing an existing show
class RemoveHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(template.render(os.path.join(os.path.dirname(__file__), 'html/remove.html'), {}))


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/index.html', MainHandler),
    ('/buy.html', SelectShowHandler),
    ('/sold.html', SoldHandler),
    ('/add.html', AddHandler),
    ('/remove.html', RemoveHandler)
], debug=True)

application = endpoints.api_server([TheatreManagementApi])