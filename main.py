











app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/fridge', FridgePage),
    ('/recipe', RecipePage)
], debug=True)
