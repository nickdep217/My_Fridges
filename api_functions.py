import api_key
from google.appengine.api import urlfetch
import json

def get_recipes(recipe_id):#fix summary option
    headers = {"X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com","X-RapidAPI-Key": api_key.RapidAPI}
    url="https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/"+ str(recipe_id)+ "/information"
    result = urlfetch.fetch(
    url=url,
    method=urlfetch.GET,
    headers=headers)
    get_results = json.loads(result.content)
    ingredients = []
    amounts = []
    units=[]
    image_url = get_results["image"]
    instructions = get_results["instructions"]
    for x in range(0,len(get_results["extendedIngredients"])):
        ingredients.append(get_results["extendedIngredients"][x]["name"])
        amounts.append(get_results["extendedIngredients"][x]["amount"])
        units.append(get_results["extendedIngredients"][x]["unit"])
    #Grab name of the recipe, seperate http request
    result_two = urlfetch.fetch(
    url="https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/" + str(recipe_id) + "/summary",
    method=urlfetch.GET,
    headers=headers)
    get_results_two = json.loads(result_two.content)
    #print get_results_two
    name = get_results_two["title"]
    summary = get_results_two["summary"]
    return {"ingredients":ingredients,"amounts":amounts, "units": units, "instructions":instructions, "image_url":image_url,
    "name":name,"summary":summary, "id": recipe_id}

def search_recipes(args,num=5):
        headers = {"X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com","X-RapidAPI-Key": api_key.RapidAPI}
        args_string=""
        for arg in args:
            args_string="%2C".join(args) #fix bug
            args_string=args_string.replace(' ','+')
        result = urlfetch.fetch(
        url="https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/findByIngredients?number="+str(num)+"&ranking=2&ignorePantry=false&ingredients="+args_string,
        method=urlfetch.GET,
        headers=headers)
        pretty_result = json.loads(result.content)
        pretty_results=[]
        for x in range(0,num):
             pretty_results.append(pretty_result[x]["id"])
        return pretty_results


def search_recipes_new(args,num=5):
        headers = {"X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com","X-RapidAPI-Key": api_key.RapidAPI}
        args_string=""
        for arg in args:
            args_string="%2C".join(args) #fix bug
            args_string=args_string.replace(' ','+')
        result = urlfetch.fetch(
        url="https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/findByIngredients?number="+str(num)+"&ranking=2&ignorePantry=false&ingredients="+args_string,
        method=urlfetch.GET,
        headers=headers)
        pretty_result = json.loads(result.content)
        pretty_id=[]
        pretty_names =[]
        pretty_usedingredients=[]
        pretty_missingingredients=[]
        for x in range(0,num):
             pretty_id.append(str(pretty_result[x]["id"]))
             pretty_names.append(pretty_result[x]["title"])
             pretty_usedingredients.append(pretty_result[x]["usedIngredientCount"])
             pretty_missingingredients.append(pretty_result[x]["missedIngredientCount"])
        return {"id":pretty_id, "names": pretty_names, "used ingredients": pretty_usedingredients,
         "missing ingredients":pretty_missingingredients}
