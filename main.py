import os
import time
import webapp2
import jinja2
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + "/html"))


class Show(ndb.Model):
    name = ndb.StringProperty(indexed=True)
    capacity = ndb.IntegerProperty(indexed=False)
    available = ndb.IntegerProperty(indexed=False)


class Msg(ndb.Model):
    msg = ndb.StringProperty(indexed=True)


#Home page
class MainHandler(webapp2.RequestHandler):
    def get(self):
        # Msg(msg = "Hello").put()
        self.response.out.write(template.render(os.path.join(os.path.dirname(__file__), 'html/index.html'), {}))

#Booking a ticket
class SelectShowHandler(webapp2.RequestHandler):
    def get(self):
        message = Msg.query().fetch(1)
        search_query = Show.query().order(Show.name)
        title = "Buy Tickets"
        template_vars = {
            'title': title,
            'search_query': search_query,
            'message': message
        }
        template = JINJA_ENVIRONMENT.get_template('buy.html')
        self.response.out.write(template.render(template_vars))
        message[0].msg = ''
        message[0].put()

    def post(self):
        item = ndb.Key(urlsafe = self.request.get('id')).get()
        title = "Book Tickets"
        template_vars = {
            'title': title,
            'item': item
        }
        template = JINJA_ENVIRONMENT.get_template('tickets.html')
        self.response.out.write(template.render(template_vars))


class BookHandler(webapp2.RequestHandler):
    def post(self):
        tickets = int(self.request.get('tickets'))
        item = ndb.Key(urlsafe = self.request.get('id')).get()
        item.available -= tickets
        item.put()
        message = Msg.query().fetch(1)
        message[0].msg = self.request.get('tickets') + " ticket(s) booked for " + item.name
        message[0].put()
        time.sleep(0.3)
        self.redirect('/buy.html')


#Viewing sold details
class SoldHandler(webapp2.RequestHandler):
    def get(self):
        search_query = Show.query().order(Show.name)
        title = "Sold Details"
        template_vars = {
            'title': title,
            'search_query': search_query
        }
        template = JINJA_ENVIRONMENT.get_template('sold.html')
        self.response.out.write(template.render(template_vars))


#Adding a new show
class AddHandler(webapp2.RequestHandler):
    def get(self):
        title = "Add Show"
        message = Msg.query().fetch(1)
        template_vars = {
            'title': title,
            'message': message
        }
        template = JINJA_ENVIRONMENT.get_template('add.html')
        self.response.out.write(template.render(template_vars))
        message[0].msg = ""
        message[0].put()

    def post(self):
        Show(name=self.request.get('show_name'), available=int(self.request.get('capacity')), capacity=int(self.request.get('capacity'))).put()
        message = Msg.query().fetch(1)
        message[0].msg = self.request.get('show_name') + " added with capacity " + self.request.get('capacity')
        message[0].put()
        time.sleep(0.3)
        self.redirect('/add.html')


#Removing an existing show
class RemoveHandler(webapp2.RequestHandler):
    def get(self):
        search_query = Show.query().order(Show.name)
        message = Msg.query().fetch(1)
        title = "Remove Show"
        template_vars = {
            'title': title,
            'search_query': search_query,
            'message': message
        }
        template = JINJA_ENVIRONMENT.get_template('remove.html')
        self.response.out.write(template.render(template_vars))
        message[0].msg = ""
        message[0].put()

    def post(self):
        message = Msg.query().fetch(1)
        item = ndb.Key(urlsafe = self.request.get('id')).get()
        message[0].msg = item.name + " show removed "
        message[0].put()
        item.key.delete()
        time.sleep(0.3)
        self.redirect('/remove.html')


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/index.html', MainHandler),
    ('/buy.html', SelectShowHandler),
    ('/sold.html', SoldHandler),
    ('/add.html', AddHandler),
    ('/remove.html', RemoveHandler),
    ('/add', AddHandler),
    ('/remove', RemoveHandler),
    ('/buy', SelectShowHandler),
    ('/tickets', BookHandler),
], debug=True)