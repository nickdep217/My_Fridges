import os

from google.appengine.ext import ndb
from google.appengine.api import urlfetch

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

class Grocery(ndb.Model):

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
        food_items = Food.query(Food.user==user,ancestor=root_parent()).fetch()
        data = {
          'user': user,
          'login_url': users.create_login_url('/'),
          'logout_url': users.create_logout_url(self.request.uri),
          'food': food_items,

        }


        ####asdfjlas;dfjasd;lfk

        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render(data))

    def post(self):

        # each_food = Food(parent=root_parent())
        #
        # each_food.name = self.request.get('food_name')
        # each_food.user = users.get_current_user()


        foods= self.request.get('food_name',allow_multiple=True)
        for food in foods:
            each_food = Food(parent=root_parent())
            each_food.name =food
            each_food.user = users.get_current_user()
            each_food.put()
            print str(each_food.name)


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
          'grocery': Grocery.query(Grocery.user==user,ancestor=root_parent()).fetch(),

        }
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render(data))
    def post(self):
        each_grocery = Grocery(parent=root_parent())
        each_grocery.name = self.request.get('grocery_name')
        each_grocery.user = users.get_current_user()

        each_grocery.put()
            # redirect to '/' so that the get() version of this handler will run
            # and show the list of dogs.
        self.redirect('/shopping_list')

class RecipePage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template = JINJA_ENVIRONMENT.get_template('templates/recipepage.html')
        food_items = Food.query(Food.user==user,ancestor=root_parent()).fetch()
        food_list=[]
        for x in range(0,len(food_items)):
            food_list.append(food_items[x].name)
        #print food_list
        #["apples","flour","sugar"]
        #recipes_list = api_functions.search_recipes_new(food_list)
        recipes_list = api_functions.search_recipes(food_list)
        if recipes_list:
            recipes_list = [api_functions.get_recipes(x) for x in recipes_list]
        for recipe in recipes_list:
            recipe["ingredients needed"]=[x for x in recipe["ingredients"] if x not in food_list]
            recipe["ingredients used"]=[x for x in recipe["ingredients"] if x in food_list]
        data = {
          'user': user,
          'login_url': users.create_login_url('/'),
          'logout_url': users.create_logout_url(self.request.uri),
          'recipes_list': recipes_list
        }

        #print recipes_list[0]["name"]
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

class DeleteGrocery(webapp2.RequestHandler):
    def post(self):
        to_delete = self.request.get('to_delete', allow_multiple=True)
        for entry in to_delete:
            key = ndb.Key(urlsafe=entry)
            key.delete()
        # redirect to '/' so that the MainPage.get() handler will run and show
        # the list of dogs.
        self.redirect('/shopping_list')

class AddGrocery(webapp2.RequestHandler):
    def post(self):
        to_add = self.request.get('to_add', allow_multiple=True)
        for entry in to_add:
            key = ndb.Key(urlsafe=entry)
            key.delete()


        self.redirect('/shopping_list')

class IndividualRecipe(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()
        template = JINJA_ENVIRONMENT.get_template('templates/individual_recipe.html')
        id_recipe= str(self.request.get("id"))
        recipe_information= api_functions.get_recipes(id_recipe) #change the id number to a variable
        print type(recipe_information["instructions"])
        data = {
          'user': user,
          'login_url': users.create_login_url('/'),
          'logout_url': users.create_logout_url(self.request.uri),
          'recipe_info':recipe_information,
          'numingredients': range(0, len(recipe_information["ingredients"]))
        }

        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render(data))
        self.response.write("<h4>"+str(recipe_information['instructions'])+"</h4>")

class TestPage(webapp2.RequestHandler):
    def get(self):

        template = JINJA_ENVIRONMENT.get_template('templates/testpage.html')
        """
        recipies = api_functions.search_recipes_new(["apples","flour","sugar"])
        self.response.write(recipies["id"])
        print recipies["names"]
        """
        recipies= api_functions.search_recipes(['flour'],num=30)
        var2 = []
        for x in range(0, len(recipies)):
            var1 =api_functions.get_recipes(recipies[x])
            var2 = list(set(var1["ingredients"] + var2))

        print var2

        for food in var2:
            food_capitalized= food[0:1:]+food[1::]
            food_lower = food.lower()
            print '<input type="checkbox" name="food_name" value="{}" style="color:white;">{}<br>'.format(food_lower, food_capitalized)




app = webapp2.WSGIApplication([
    ('/', HomePage),
    ('/about', AboutPage),
    ('/fridge', FridgePage),
    ('/recipe', RecipePage),
    ('/shopping_list', ShoppingListPage),
    ('/delete_food', DeleteFood),
    ('/delete_grocery', DeleteGrocery),
    ('/add_to_fridge', AddGrocery),
    ('/individual_recipe_page', IndividualRecipe),
    ('/test', TestPage)
], debug=True)
