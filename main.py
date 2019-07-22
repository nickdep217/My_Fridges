import os

from google.appengine.ext import ndb

import jinja2
import webapp2

from google.appengine.api import users
# import unirest
# response = unirest.get("https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/479101/information",
#  headers={
#    "X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
#    "X-RapidAPI-Key": "6b47611c55msh1be60a217eb3ca8p152ba2jsn2181feb853cb"
#  }
# )
# print (response.body["sourceName"])

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

class AboutPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/aboutpage.html')
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render())


#class RecipePage(webapp2.RequestHandler):
    #def get(self):
        #template = JINJA_ENVIRONMENT.get_template('templates/homepage.html'
#class ShoppingListPage(webapp2.RequestHandler):
#def get(self):
    #    template = JINJA_ENVIRONMENT.get_template('templates/homepage.html'


app = webapp2.WSGIApplication([
    ('/', HomePage),
    ('/about', AboutPage)
    #('/fridge', FridgePage),
    #'/recipe', RecipePage),
    #('/shopping_list', ShoppingListPage)
], debug=True)
