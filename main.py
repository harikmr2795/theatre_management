import os
import time
# import jinja2
import webapp2
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template
from models import *



# JINJA_ENVIRONMENT = jinja2.Environment(
#     loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + "/html"))


#Home page
class MainHandler(webapp2.RequestHandler):
    def get(self):
#         Msg(msg = "Hello").put()
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
#         
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
    ('/remove.html', RemoveHandler),
    ('/add', AddHandler),
    ('/remove', RemoveHandler),
], debug=True)