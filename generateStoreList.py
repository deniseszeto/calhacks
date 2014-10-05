from urllib.request import urlopen
from xml.dom.minidom import parse

def generateStoreList():
	""" 
		Generate the dictionary of unique stores that are recorded in SupermarketAPI.

		storedict has state initials as keys and dictionary statestore as item;

		statestore has stores' names as keys and stores' id as item; We will be making an

		assumption that when a certain chain grocery store has an item in one location, then other

		locations will also have it, since SupermarketAPI's dataset isn't complete. 

	"""

	apikey = "cdc08667c7"
	storedict = {}

	page = urlopen("http://www.supermarketapi.com/api.asmx/AllUSStates")
	xml = parse(page)
	states = xml.getElementsByTagName("State")
	for state in states:
		url = "http://www.SupermarketAPI.com/api.asmx/CitiesByState?APIKEY="+ apikey + "&SelectedState=" + state.firstChild.nodeValue
		page = urlopen(url)
		xml = parse(page)
		storeset = set()
		statestore = {}
		cities = xml.getElementsByTagName("City")

		for city in cities:
			cityname = city.firstChild.nodeValue.replace(" ", "+")
			url = "http://www.SupermarketAPI.com/api.asmx/StoresByCityState?APIKEY=" + apikey + "&SelectedCity=" + cityname + "&SelectedState=" + state.firstChild.nodeValue
			page = urlopen(url)
			xml = parse(page)
			storeList = xml.getElementsByTagName("Store")
			for store in storeList:
				storename = store.getElementsByTagName("Storename")[0]
				storeid = store.getElementsByTagName("StoreId")[0]
				if (storename.firstChild is None or storeid.firstChild is None):
					continue
				if storename not in storeset:
					storeset.add(storename.firstChild.nodeValue)
					statestore[storename.firstChild.nodeValue] = storeid.firstChild.nodeValue

		storedict[state.firstChild.nodeValue] = statestore

	return storedict