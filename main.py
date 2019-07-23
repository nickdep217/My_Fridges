import os

from google.appengine.ext import ndb

import jinja2
import webapp2
import api_functions



from google.appengine.api import users


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def root_parent():
    '''A single key to be used as the ancestor for all dog entries.

    Allows for strong consistency at the cost of scalability.'''
    return ndb.Key('Parent', 'default_parent')

class Food(ndb.Model):

    name = ndb.StringProperty()
    user = ndb.UserProperty()

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

class AboutPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template = JINJA_ENVIRONMENT.get_template('templates/aboutpage.html')
        data = {
          'user': user,
          'login_url': users.create_login_url('/'),
          'logout_url': users.create_logout_url(self.request.uri),
        }
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render(data))

class FridgePage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template = JINJA_ENVIRONMENT.get_template('templates/fridgepage.html')
        data = {
          'user': user,
          'login_url': users.create_login_url('/'),
          'logout_url': users.create_logout_url(self.request.uri),
            'food': Food.query(Food.user==user,ancestor=root_parent()).fetch(),
            # 'fruits': Fruit.query(Fruit.user==user,ancestor=root_parent()).fetch(),
            # 'pantries': Pantry.query(Pantry.user==user,ancestor=root_parent()).fetch(),
        }
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render(data))
    def post(self):
        each_food = Food(parent=root_parent())
        each_food.name = self.request.get('food_name')
        each_food.user = users.get_current_user()

        each_food.put()
            # redirect to '/' so that the get() version of this handler will run
            # and show the list of dogs.
        self.redirect('/fridge')

class ShoppingListPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template = JINJA_ENVIRONMENT.get_template('templates/shopping_listpage.html')
        data = {
          'user': user,
          'login_url': users.create_login_url('/'),
          'logout_url': users.create_logout_url(self.request.uri),
        }
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render(data))

class RecipePage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template = JINJA_ENVIRONMENT.get_template('templates/recipepage.html')
        data = {
          'user': user,
          'login_url': users.create_login_url('/'),
          'logout_url': users.create_logout_url(self.request.uri),
        }
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render(data))



class DeleteFood(webapp2.RequestHandler):
    def post(self):
        to_delete = self.request.get('to_delete', allow_multiple=True)
        for entry in to_delete:
            key = ndb.Key(urlsafe=entry)
            key.delete()
        # redirect to '/' so that the MainPage.get() handler will run and show
        # the list of dogs.
        self.redirect('/fridge')





app = webapp2.WSGIApplication([
    ('/', HomePage),
    ('/about', AboutPage),
    ('/fridge', FridgePage),
    ('/recipe', RecipePage),
    ('/shopping_list', ShoppingListPage),
    ('/delete_food', DeleteFood),
    
], debug=True)
