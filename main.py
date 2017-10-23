import os
import time
import webapp2
import jinja2
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
        #Msg(msg = "Hello").put()
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.out.write(template.render())


class SelectShowHandler(webapp2.RequestHandler):
    def get(self):
        message = Msg.query().fetch()
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


class AddHandler(webapp2.RequestHandler):
    def get(self):
        title = "Add Show"
        message = Msg.query().fetch()
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
        message = Msg.query().fetch()
        message[0].msg = self.request.get('show_name') + " added with capacity " + self.request.get('capacity')
        message[0].put()
        time.sleep(0.3)
        self.redirect('/add.html')


class DeleteHandler(webapp2.RequestHandler):
    def get(self):
        search_query = Show.query().order(Show.name)
        message = Msg.query().fetch()
        title = "Delete Show"
        template_vars = {
            'title': title,
            'search_query': search_query,
            'message': message
        }
        template = JINJA_ENVIRONMENT.get_template('delete.html')
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
        self.redirect('/delete.html')


class BookHandler(webapp2.RequestHandler):
    def post(self):
        tickets = int(self.request.get('tickets'))
        item = ndb.Key(urlsafe = self.request.get('id')).get()
        item.available -= tickets
        item.put()
        message = Msg.query().fetch()
        message[0].msg = self.request.get('tickets') + " ticket(s) booked for " + item.name
        message[0].put()
        time.sleep(0.3)
        self.redirect('/buy.html')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/index.html', MainHandler),
    ('/buy.html', SelectShowHandler),
    ('/sold.html', SoldHandler),
    ('/add.html', AddHandler),
    ('/delete.html', DeleteHandler),
    ('/add', AddHandler),
    ('/delete', DeleteHandler),
    ('/buy', SelectShowHandler),
    ('/tickets', BookHandler),
], debug=True)