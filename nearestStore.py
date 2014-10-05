from urllib.request import urlopen
import xml.etree.ElementTree as ET
from random import randint

def nearestStore(cuisineType, latitude, longitude):
    """ Returns a nearby relevant supermarket by Name + Address. """

    RANDOM_NEAREST = 3
    
    apiKey = "AIzaSyA7UZaE5lCotDi8pWfLRYEAwHKr1KtqSJ4"

    # Base URL for Google Places API
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/xml?"

    # API Key
    url += "key=" + apiKey

    # Finds nearest supermarket for the specified cuisine type
    url += "&keyword=" + cuisineType + "+supermarkets+near+"

    # Uses the location specified by GPS or user inpet
    url += "&location=" + latitude + "," + longitude

    # Ranks by proximity to said location
    url += "&rankby=distance"

    xml = ET.parse(urlopen(url))
    root = xml.getroot()

    """
    try:
        location = root.find("result").find("geometry").find("location")
    except AttributeError:
        return "THIS SHOULD NOT HAPPEN", "THIS SHOULD NOT HAPPEN"
    
    return location.find("lat").text, location.find("lng").text
    """

    try:
        i = randint(1, RANDOM_NEAREST)
        currStore = ""
        for el in root.findall("result"):
            store = el.find("name").text
            if i <= 1 and currStore != store:
                result = el
                break
            else:
                currStore, i = store, i - 1
    except AttributeError:
        return "THIS SHOULD NOT HAPPEN"

    return (store + "+" + result.find("vicinity").text).replace(" ", "+")
