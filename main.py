import os

from google.appengine.ext import ndb

import jinja2
import webapp2

from google.appengine.api import users


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class HomePage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template = JINJA_ENVIRONMENT.get_template('templates/homepage.html')
        data = {
          'user': user,
          'login_url': users.create_login_url('/'),
          'logout_url': users.create_logout_url(self.request.uri),
        }
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render(data))


#class RecipePage(webapp2.RequestHandler):
    #def get(self):
        #template = JINJA_ENVIRONMENT.get_template('templates/homepage.html'
#class ShoppingListPage(webapp2.RequestHandler):
#def get(self):
    #    template = JINJA_ENVIRONMENT.get_template('templates/homepage.html'


app = webapp2.WSGIApplication([
    ('/', HomePage),
    #('/fridge', FridgePage),
    #'/recipe', RecipePage),
    #('/shopping_list', ShoppingListPage)
], debug=True)
