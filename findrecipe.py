from urllib.request import urlopen
from xml.dom.minidom import parse
from random import randint

def parsePage(url, tag=""):
    """ Returns the parsed xml and optionally the value of a tag. """
    
    page = urlopen(url)
    xml = parse(page)
    if tag == "":
        return xml
    else:
        return xml, xml.getElementsByTagName(tag)[0].firstChild.nodeValue

def findRecipe(keywords="Calhacks"):
    """ Returns a tuple (Recipe Name, Set of Ingredients). """
    
    apiKey = "dvxI9e588cOKNvbOzd24EXsVRW9Y2OW8"

    # Base URL for Big Oven API
    url = "http://api.bigoven.com/recipes?pg=0&rpp=1"

    # Searching for the input Keywords
    url += "&title_kw=" + keywords.replace(" ", "+")

    # Adding the developer's API Key
    url += "&api_key=" + apiKey

    recipeCount = parsePage(url, 'ResultCount')[1]
    
    # No recipes are found.
    if recipeCount == "0":
        return keywords, set(["No such recipe found"])

    randomRecipe = randint(1, int(recipeCount))
    url = url.replace("pg=0", "pg=" + str(randomRecipe))

    recipeID = parsePage(url, 'RecipeID')[1]
    
    # Return the list of ingredients in the Recipe
    recipe_url = "http://api.bigoven.com/recipe/" + recipeID
    recipe_url += "?api_key=" + apiKey

    xml, recipe_title = parsePage(recipe_url, 'Title')

    recipe_list = set()
    for el in xml.getElementsByTagName('Name'):
        recipe_list.add(el.firstChild.nodeValue)

    return recipe_title, recipe_list
