from urllib.request import urlopen
from xml.dom import minidom
from xml.dom.minidom import parse
import xml.etree.ElementTree as ET
import operator

#Uses Supermarket API

def findStore(ingredients, state):
	apikey = "cdc08667c7"
	#Storelist generated from generateStoreList.py; dictionary of dictionary.
	storeList = {'CA': {'Ralphs  ': 'e6k3fjw251k', 'Joke': 'a61bae6f2f', "Ralph's": '1b624c85c5', 'Walmart  ': 'e1eb38866b', "Trader Joe's": '0869439469', 'Gamgnams': 'ab977627bb', 'Kroger  ': '25f088a250', 'Mollie Stones Market  ': 'e6k3fjw191k', 'Save Mart  ': 'e6k3fjw217k', 'Walmart Supercenter Store': '3f088025d7', 'WinCo  ': '64cb39966e', 'Grocery Outlet': '1bd3f28b6c', 'Food 4 Less  ': 'cf886348a8', 'The Real Food Company  ': 'ee210b7b3a', 'Target  ': 'a995a35f8f', 'Grocery Outlet  ': 'e6k3fjw219k', 'Safeway': '70259da07b', 'Lucky': '6e87e9eb65', 'Trader Joes  ': 'e6k3fjw237k', 'CALA Foods  ': '6f040ac0da', 'Safeway  ': 'a95682ebc3', 'Cost Less Market  ': '95d3ccf390', 'Samm': '9afd8d5eb0', "Adronico's Community Markets  ": '8611b7ce3d', "Raley's": 'aea2d1557e', 'Raleys  ': 'de4ec97446', 'Cardenas': '59020b3822', 'Cunha Country Grocery Store  ': '9c8570d574', 'FoodsCo  ': '4c6ce64c4e', "Mollie Stone's Market  ": '06cb41b570', 'Andronicos Market   ': 'e6k3fjw190k', 'Walmart': 'd35bf28410', 'Stu Store': '1d58e626c6', 'Luckys  ': 'e6k3fjw195k', 'Food 4 Less': 'd86e27ff9a', 'Walmart Neighborhood Market': '17378e3b5c', "Von's": '933baffef6', 'Albertsons': '8783f86594', "Albertson's": 'c3f6da5154', 'FoodMaxx  ': '6754bc972d', 'Vons  ': 'e6k3fjw107k', 'Lucky Supermarkets  ': '0d665a3670', 'Pavillions  ': 'e6k3fjw99k', 'JJ & F Food Store   ': 'e6k3fjw192k', 'Sprouts': '994692cf60', 'Safeway - Vons': 'd8aa7fa841'}, 'CO': {'City Market': '3184a53059', 'Safeway  ': '257ec307fc', 'City Market  ': '40041b574e', 'Safeway': '7bbdbb138c', 'King Soopers': '59a089f25b', 'Target  ': 'af9f101a75'}, 'KS': {'Hyvee Food & Drug  ': 'cc130b33bb'}, 'GA': {'H Mart  ': 'f8ea1a844e', 'Publix  ': '2b94fd328c', 'Ingles Markert': '08bc0bb4b5', 'Kroger  ': '879be72361', 'Whole Foods Market  ': '57f0d25c2e'}, 'AL': {'Wal-Mart  ': '3146878421'}, 'WV': {'Kroger  ': 'a59db344ea'}, 'AR': {'Kroger  ': 'b92d248706'}, 'AZ': {'Safeway ': 'fa83ecf266', 'Safeway  ': 'c8cce58299'}, 'VT': {'Hannaford  ': 'ae4fdb2aa8'}, 'WY': {'Safeway  ': '617f471fa4'}, 'NC': {'Kroger  ': '4478fa6dca'}, 'ND': {'Albertsons  ': '0eef592646'}, 'NE': {'Safeway  ': '60b2d42c45'}, 'UT': {'Harmons  ': '42acc6b07f'}, 'NH': {'Hannaford  ': '6370c6e024'}, 'NJ': {'A&P Supermarket Stores  ': 'b0f09ee947', 'Super Fresh': 'c19e3e5355', 'Wegmans  ': 'e6k3fjw165k', 'A&P Supermarket  ': '5694289b6f', 'Acme Markets  ': '4556c4a616', 'Waldbaums  ': '83f3d53421'}, 'LA': {'Albertsons  ': 'be0bbc0727', 'Hj': '0d3c7b04ca'}, 'NM': {'Albertsons  ': 'c55c9a4ef2'}, 'HI': {'Safeway  ': '9e1d8657cf'}, 'ME': {'Hannaford  ': 'b4ac3eec65'}, 'WI': {'Sendiks Market  ': 'fd9ed32930'}, 'SD': {'Safeway  ': 'b2ae7cbd2a'}, 'SC': {'Kroger  ': '7cd3aecb5f'}, 'NV': {'Safeway  ': '98d4da812e'}, 'DE': {'Acme Markets  ': '57a3dd0954'}, 'NY': {'A&P Supermarket Stores  ': '6aaa9cb8c3', 'Tops  ': '40f77b90c2', 'Tops Supermarket  ': '591562e431', "Trader Joe's": '9710c9e34b', 'A&P Supermarket  ': 'c4868f1b3d', 'Gristedes  ': '9c5fada7df', 'Waldbaums  ': 'a971137be5', 'Wegmans  ': 'e6k3fjw155k', 'Walmart': '29337872db', 'Walmart Supercenter Store': 'f44bf9cd46', "Shelly's": 'e20880fbfe', 'Fairway': 'b9d5a25738'}, 'WA': {'Winco Foods': '9c879db9bd', 'Safeway': 'd7aa924eec', 'Winco': 'b0175baf7c'}, 'AK': {'Safeway  ': '9458c5540c', 'CARRS Safeway  ': '0ff6bb3c90'}, 'DC': {'Safeway  ': '2f55da6731'}, 'FL': {'Publix': '2a328ea1e5', 'Kroger (TOM THUMB FOOD STORE)': 'ea1e1b0a1e', 'Publix  ': '10298943a5', 'Public': 'cdab7d9f4f', 'Publix Super Markets': 'c8ee3a2fe2', 'Walmart Supercenter Store': '84c3411562', 'Publix Super Market': '58e19a19bb'}, 'VA': {'Farm Fresh': 'a0069eee93', "Martin's  ": '456d05f404', 'Wegmans  ': 'e6k3fjw185k'}, 'MO': {'Schnucks Lake St. Louis  ': '0e47f191fe', 'Schnucks Florissant  ': '96ff5099e5', 'Save A lot': '46d376859b', 'Schnucks Kirkwood  ': 'a8b4a95908', 'Schnucks City Plaza  ': '3c1ed94b4b', 'Kroger  ': 'b6f2f4e06e', 'Schnucks   ': 'd9ecbb6fa6', 'Schnucks  ': '703283b621', 'Schnucks University City  ': '1d76db5052', 'Schnucks Westfall Plaza  ': 'd34b320bd4', 'Schnucks Belleville West  ': '049e3a09d2', 'Schnucks Kossuth  ': '0397230453', 'Schnucks Twin Oaks  ': '91fbae8b48', 'Schnucks Cottleville  ': '1cd26396bc', 'Schnucks Cool Valley  ': '3bd5463e4f', 'Global Foods Market  ': 'b8301f3e39', 'Schnucks Eureka Pointe  ': 'fc5e59f6cd', 'Schnucks Richmond Center  ': '762fb28527'}, 'MN': {'Hy-Vee  ': '4d28ae93d8'}, 'MI': {'Meijer  ': '3e90434b92', 'Save a Lot  ': '4458744b1e', 'Walmart  ': '3af7076120', 'Vons': '377c0a6f2b', 'Kroger  ': 'ae50fe1258', 'Save a Lot': 'bb2ee952ea', 'Save A lot': '6bc3ef837c', 'Walmart': '8baef980ac', 'Walmart Supercenter Store': '600ccd90b5', 'Value Center Market': 'dcb819c20f', 'Harbortown Supermarket': '6aa92c5d20', 'Save a lot  ': '2a4b604bd6', 'Lafayette Foods': '39eda47c14'}, 'KY': {'Kroger  ': '6fcb57f26b'}, 'OK': {'Crest Foods  ': '11b875934c', 'Walmart ': '1a42c80c2b', 'Walmart Market': '8f0a7f4f05', 'Walmart Supercenter': 'e41c4e1d94'}, 'MD': {'Giant Food': 'f562e22299', 'Harris Teeter': 'ece145ed36', 'Wegmans  ': 'e6k3fjw158k', 'Safeway': '118a946103', 'Acme Markets  ': '7742578e89'}, 'OH': {'Sheffield Village Giant Eagle': 'ce38f38771', 'Kroger West side': '25ad4a74bf', 'Springfield Giant Eagle': '4a46ea2a44', 'Kroger  ': '5d5da23ad8'}, 'MA': {'Roche Bros  ': '99719e9c8a', 'Star Market  ': '539cb04b5d', 'Hannaford  ': 'a0e1a3c94b', "Shaw's  ": '34ba93d60f', 'Big Y': 'a215825abd', 'Big Y  ': 'd9cf3eb6c3', 'Shaws  ': '40f82927a8', 'Roche Bros.  ': 'e085a88468', 'Stop & Shop': 'f1f92be06a'}, 'ID': {'Albertsons  ': 'c506f0f7ac'}, 'OR': {'Safeway  ': '3a258cb6b7', 'Waremart': '8ca5e98002', 'SAFEWAY': '24aaca9d2a', 'Walmart  ': '3829e5fd2b'}, 'CT': {'A&P Supermarket  ': '743b97d8f1', 'Big Y  ': '819e39100f'}, 'IL': {'Walmart': 'f608e2d626', 'Kroger (RALPHS GROCERY COMPANY)': 'c4e6d63611', "Dominick's  ": '6b4a04b136', 'Safeway - Dominicks': 'dedeead20f', 'Trader Joes': '416d9cfa20', 'Save A lot': '236d98965f', 'Save a lot': '62c3ce1e31'}, 'IN': {'Ruler Foods  ': '7e95d4304c'}, 'IA': {'Fareway  ': '4b8859f0a6'}, 'MT': {'Safeway  ': 'c83aa3ec6a'}, 'TX': {'HEB': 'aed9456dbb', 'Safeway - Randalls': '7d8bcdde63', 'H-E-B Foods': '021407ed75', 'H-E-B': '582b8265e9', "Albertson's": '1dbbc95378', 'Albertsons': '878cdba150', 'Kroger  ': 'af9840a82f', 'Save A lot': 'f77e854a2a', 'Safeway - Flagship Randalls': '2b281d175b', 'Whole Foods Market': 'c0005ebb7f', 'Walmart': '1529ac6149', 'Walmart Supercenter Store': '5c09d78b9e', 'Randalls  ': 'af2b2ef2a4', 'Kroger ': '04cd53a9e6', 'Kroger': '71273db90f', 'Tom Thumb  ': '236815b14d', 'H-E-B Foods  ': 'e8787cdc02'}, 'TN': {'Kroger': 'b568b5093b', 'Kroger  ': '4aecd9f07f', 'Walmart Supercenter Store': 'edb1e76a72', 'Walmart Supercenter': '420e11dd15'}, 'RI': {'Shaws  ': '4cd2271b60'}, 'MS': {'Kroger  ': 'ca1278d42b'}, 'PA': {'Whole Foods Market': '05136635f7', 'Tops  ': '1679a65faa', 'Acme Markets  ': 'e8e279c481', 'Wegmans  ': 'e6k3fjw179k', 'Trader Joes': '52a9f14f48', 'Save A Lot': 'e90e39ed8e', 'Walgreens': '83d3fe9f5d'}}

	check = set()
	stateStore = storeList[state]
	storeCount = {}

	print(len(stateStore))
	for ingredient in ingredients:
		for storename in stateStore:
			ingredient = ingredient.strip()
			url = "http://www.SupermarketAPI.com/api.asmx/SearchForItem?APIKEY=" + apikey + "&StoreId=" + stateStore[storename] + "&ItemName=" + ingredient
			page = urlopen(url)

			xml = ET.parse(page)
			root = xml.getroot()

			if (root[0][0].text == "NOITEM"):
				continue
			else:
				if storename in check:
					storeCount[storename] +=1
				else:
					check.add(storename)
					storeCount[storename] = 1
				continue

	return sorted(storeCount.items(), key = operator.itemgetter(1))


def queryStoreByCity (city, state):
	city = city.replace(" ", "+")
	return "http://www.SupermarketAPI.com/api.asmx/StoresByCityState?APIKEY=" + apikey + "&SelectedCity=" + city + "&SelectedState=" + state

def queryStoreByZip (zipcode):
	return "http://www.SupermarketAPI.com/api.asmx/StoresByZip?APIKEY=" + apikey + "&ZipCode=" + zipcode