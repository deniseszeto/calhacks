from urllib.parse import unquote
from urllib.request import urlopen
import xml.etree.ElementTree as ET
from math import log

def heuristic(salePrice, rating, reviews):
    """ Evaluates an item based on Price, Rating, and Number of Reviews. """
    
    salePrice, rating, reviews = float(salePrice), float(rating), float(reviews)
    return 20.0 / salePrice + log((rating + 1.0) * (reviews + 20.0))

def createCart(toolsList=[]):
    """ Returns a list of (tool, url) from input list of tools. """
    
    apiKey = "bqrefaq33zj9dk59nw9hz62g"

    # Base URL for Walmart API Search (can set numItems to display)
    url = "http://api.walmartlabs.com/v1/search?format=xml"

    # Adding the developer's API Key
    url += "&apiKey=" + apiKey

    # Sorting by ascending price for evaluation function
    url += "&sort=price&ord=asc"

    returnList = []
    epsilon, prodName, prodUrl = 0, "", ""
    for tool in toolsList:
        xml = ET.parse(urlopen(url + "&query=" + tool.replace(" ", "+")))
        root = xml.getroot()
        if root.find("totalResults").text != "0":
            for item in xml.find("items").findall("item"):
                salePrice = item.find("salePrice").text
                try:
                    rating = item.find("customerRating").text
                    reviews = item.find("numReviews").text
                except AttributeError:
                    rating, reviews = "3", "0"
                    
                value = heuristic(salePrice, rating, reviews)
                if value > epsilon:
                    epsilon = value
                    prodName = item.find("name").text
                    prodUrl = item.find("productUrl").text
            endUrl = prodUrl.find("%3F")
            returnList.append((prodName, unquote(prodUrl[37:endUrl])))
            epsilon = 0
            
    return returnList
                
    
