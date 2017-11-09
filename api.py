import endpoints
from protorpc import remote
from models import *

@endpoints.api(name="theatreManagement", version="v1", description="Theatre Management API")
class TheatreManagementApi(remote.Service):
    @Show.method(path="show/insert", name="show.insert", http_method="POST")
    def show_insert(self, request):
        """  Inserts a new show into the Datastore. """
        if request.from_datastore:
            show = request
        else:
            show = Show(name=request.name, capacity=request.capacity, available=request.capacity)
        show.put()
        return show
    
    @Show.method(path="show/book", name="show.book", http_method="POST")
    def book_ticket(self, request):
        """  Book a ticket """
        if request.from_datastore:
            show = request
        else:
            request.available
            show = Show(name=request.name, capacity=request.capacity, available=request.capacity)
        show.put()
        return show
    
    @Show.query_method(path="show/list", name="show.list", http_method="GET")
    def show_list(self, query):
        """ Returns Movie Quotes """
        return query
    
    @Show.method(request_fields=("entityKey",), path="show/delete/{entityKey}", name="show.delete", http_method="DELETE")
    def moviequote_delete(self, request):
        """ Delete the given show from the Datastore. """
        if not request.from_datastore:
            raise endpoints.NotFoundException("Show not found")
        request.key.delete()
        return Show(name="deleted")

app = endpoints.api_server([TheatreManagementApi], restricted=False)