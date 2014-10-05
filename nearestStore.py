from urllib.request import urlopen
import xml.etree.ElementTree as ET

def nearestStore(cuisineType, latitude, longitude):
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
        result = root.find("result")
    except AttributeError:
        return "THIS SHOULD NOT HAPPEN"

    address = result.find("name").text + "+" + result.find("vicinity").text
    return address.replace(" ", "+")