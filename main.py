import webapp2
import jinja2
import os
from google.appengine.ext import ndb

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + "/html"))

class Show(ndb.Model):
    name = ndb.StringProperty(indexed=True)
    capacity = ndb.IntegerProperty(indexed=True)
    available = ndb.IntegerProperty(indexed=True)

class Msg(ndb.Model):
    msg = ndb.StringProperty(indexed=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        m = Msg()
        #m.msg = "Hello"
        #m.put()
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.out.write(template.render())


class BuyHandler(webapp2.RequestHandler):
    def get(self):
        show_lst = Show.query()
        search_query = show_lst.order(Show.name)
        title = "Buy Tickets"
        template_vars = {
            'title': title,
            'search_query': search_query
        }
        template = JINJA_ENVIRONMENT.get_template('buy.html')
        self.response.out.write(template.render(template_vars))

    def post(self):
        search_query = Show.query()
        name = self.request.get('name')
        for item in search_query:
            pass_item = item
            if item.name == name:
                break

        title = "Book Tickets"
        template_vars = {
            'title': title,
            'item': pass_item
        }
        template = JINJA_ENVIRONMENT.get_template('tickets.html')
        self.response.out.write(template.render(template_vars))


class SoldHandler(webapp2.RequestHandler):
    def get(self):
        show_lst = Show.query()
        search_query = show_lst.order(Show.name)
        title = "Sold Details"
        template_vars = {
            'title': title,
            'search_query': search_query
        }
        template = JINJA_ENVIRONMENT.get_template('sold.html')
        self.response.out.write(template.render(template_vars))


class AddHandler(webapp2.RequestHandler):
    def get(self):
        title = "Add Show"
        template_vars = {
            'title': title
        }
        template = JINJA_ENVIRONMENT.get_template('add.html')
        self.response.out.write(template.render(template_vars))

    def post(self):
        s = Show()
        s.name = self.request.get('show_name')
        s.available = s.capacity = int(self.request.get('capacity'))
        s.put()
        title = "Add Show"
        message = Msg.query()
        template_vars = {
            'title': title,
            'message': message
        }
        for item in message:
            item.msg = self.request.get('show_name') + " added with capacity " + self.request.get('capacity')
            item.put()
        template = JINJA_ENVIRONMENT.get_template('add.html')
        self.response.out.write(template.render(template_vars))
        #self.get()


class DeleteHandler(webapp2.RequestHandler):
    def get(self):
        show_lst = Show.query()
        search_query = show_lst.order(Show.name)
        title = "Delete Show"
        template_vars = {
            'title': title,
            'search_query': search_query
        }
        template = JINJA_ENVIRONMENT.get_template('delete.html')
        self.response.out.write(template.render(template_vars))

    def post(self):
        name = self.request.get('name')
        show_lst = Show.query()
        search_query = show_lst.filter(Show.name == name)
        for item in search_query:
            item.key.delete()
        message = Msg.query()
        show_lst = Show.query()
        search_query = show_lst.order(Show.name)
        title = "Delete Show"
        template_vars = {
            'title': title,
            'search_query': search_query,
            'message': message
        }
        for item in message:
            item.msg = self.request.get('name') + " show removed "
            item.put()
        template = JINJA_ENVIRONMENT.get_template('delete.html')
        self.response.out.write(template.render(template_vars))
        #self.get()


class TicketsHandler(webapp2.RequestHandler):
    def post(self):
        name = self.request.get('name')
        tickets = int(self.request.get('tickets'))
        show_lst = Show.query()
        search_query = show_lst.filter(Show.name == name)
        for item in search_query:
            item.available -= tickets
            item.put()

        message = Msg.query()
        show_lst = Show.query()
        search_query = show_lst.order(Show.name)
        title = "Buy Tickets"
        template_vars = {
            'title': title,
            'search_query': search_query,
            'message': message
        }
        for item in message:
            item.msg = self.request.get('tickets') + " ticket(s) booked for " + self.request.get('name')
            item.put()
        template = JINJA_ENVIRONMENT.get_template('buy.html')
        self.response.out.write(template.render(template_vars))



app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/index.html', MainHandler),
    ('/buy.html', BuyHandler),
    ('/sold.html', SoldHandler),
    ('/add.html', AddHandler),
    ('/delete.html', DeleteHandler),
    ('/add', AddHandler),
    ('/delete', DeleteHandler),
    ('/buy', BuyHandler),
    ('/tickets', TicketsHandler),
], debug=True)