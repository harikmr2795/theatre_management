import webapp2
import jinja2
import os
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template

JINJA_ENVIRONMENT = jinja2.Environment(
	loader = jinja2.FileSystemLoader(os.path.dirname(__file__) + "/html"))

class Show(ndb.Model):
	name = ndb.StringProperty(indexed = True)
	capacity = ndb.StringProperty(indexed = True)

class Add(webapp2.RequestHandler):
	def post(self):
		s = Show()
		s.name = self.request.get('show_name')
		s.capacity = self.request.get('capacity')
		s.put()
		template = JINJA_ENVIRONMENT.get_template('add.html')
		self.response.out.write(template.render())

class MainHandler(webapp2.RequestHandler):
    def get(self):
		template = JINJA_ENVIRONMENT.get_template('index.html')
		self.response.out.write(template.render())

class BuyHandler(webapp2.RequestHandler):
    def get(self):
		title = "Buy Tickets"
		template_vars = {
			'title': title
		}
		template = JINJA_ENVIRONMENT.get_template('buy.html')
		self.response.out.write(template.render(template_vars))

class SoldHandler(webapp2.RequestHandler):
    def get(self):
		title = "Sold Details"
		template_vars = {
			'title': title
		}
		template = JINJA_ENVIRONMENT.get_template('sold.html')
		self.response.out.write(template.render(template_vars))

class AddHandler(webapp2.RequestHandler):
    def get(self):
		title = "Add Show"
		template_vars ={
			'title': title
		}
		template = JINJA_ENVIRONMENT.get_template('add.html')
		self.response.out.write(template.render(template_vars))

class DeleteHandler(webapp2.RequestHandler):
    def get(self):
		title = "Delete Show"
		template_vars = {
			'title': title
		}
		template = JINJA_ENVIRONMENT.get_template('delete.html')
		self.response.out.write(template.render(template_vars))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
	('/index.html', MainHandler),
	('/buy.html', BuyHandler),
	('/sold.html', SoldHandler),
	('/add.html', AddHandler),
	('/delete.html', DeleteHandler),
	('/add', Add),
], debug=True)