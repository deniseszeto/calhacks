# -*- coding: utf-8 -*-

from urllib.request import urlopen
from xml.dom.minidom import parse
from random import randint

def parseList(xml, tag):
    """ Returns a list of elements in the parsed xml by tag name. """
    return xml.getElementsByTagName(tag)
    
def parsePage(url, tags=[]):
    """ Returns the parsed xml and optionally the value of a tag. """
    
    page = urlopen(url)
    xml = parse(page)
    if not tags:
        return xml
    
    for i in range(len(tags)):
        tags[i] = xml.getElementsByTagName(tags[i])[0].firstChild.nodeValue

    return xml, tags

def findRecipe(keywords="Calhacks"):
    """ Returns (Recipe Name, Set of Ingredients, Instructions). """
    
    apiKey = "dvxI9e588cOKNvbOzd24EXsVRW9Y2OW8"

    # Base URL for Big Oven API
    url = "http://api.bigoven.com/recipes?pg=0&rpp=1"

    # Searching for the input Keywords
    url += "&title_kw=" + keywords.replace(" ", "+")

    # Adding the developer's API Key
    url += "&api_key=" + apiKey

    recipeCount = parsePage(url, ['ResultCount'])[1][0]
    
    # No recipes are found.
    if recipeCount == "0":
        return keywords, set(["No such recipe found"])

    randomRecipe = randint(1, int(recipeCount))
    url = url.replace("pg=0", "pg=" + str(randomRecipe))

    recipeID = parsePage(url, ['RecipeID'])[1][0]
    
    # Return the list of ingredients in the Recipe
    recipe_url = "http://api.bigoven.com/recipe/" + recipeID
    recipe_url += "?api_key=" + apiKey

    xml, [title, inst] = parsePage(recipe_url, ['Title', 'Instructions'])

    recipe_list = set()
    for el in parseList(xml, 'Name'):
        recipe_list.add(el.firstChild.nodeValue)

    return title, recipe_list, inst
