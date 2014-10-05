from xml.dom.minidom import parse
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.parse import urlparse
import datetime
import base64, hashlib, hmac, time
import operator
from math import log

AWS_KEY = "AKIAJSAPQI6HUEC2WTCA"
AWS_SECRET_KEY = b'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'

def createCart (objectList):
	""" 
		Takes list of search keywords for kitchen instruments.
		Searches Amazon for the items and evaluates top 10 hits based on heuristic(...)
		Pulls best offerings listed and returns a URL for the cart created with all the items inputted.

		Uses Following Methods:
			queryCartCreate (offerListings)
			querySearch (keyword)
			heuristic(listPrice, amountSaved, primeFlag)
	"""

	objectIds =[]

	for elem in objectList:
		elem = elem.replace(" ",",")
		xml = querySearch(elem)
		searchList = xml.getElementsByTagName("Item")
		maxval = [0, None]
		for item in searchList:
			itemId = item.getElementsByTagName("OfferListingId")[0].firstChild.nodeValue
			primeFlag = item.getElementsByTagName("IsEligibleForSuperSaverShipping")[0].firstChild.nodeValue

			listPrice = item.getElementsByTagName("Price")[0].getElementsByTagName("FormattedPrice")[0].firstChild.nodeValue
			amountSaved = item.getElementsByTagName("AmountSaved")
			if len(amountSaved) != 0:
				amountSaved = item.getElementsByTagName("AmountSaved")[0].getElementsByTagName("FormattedPrice")[0].firstChild.nodeValue
			else:
				amountSaved = "0"

			listPrice = listPrice.replace("$", "")
			amountSaved = amountSaved.replace("$", "")

			val = heuristic (listPrice, amountSaved, primeFlag)
			if val > maxval[0]:
				maxval[0] = val
				maxval[1] = itemId
		objectIds.append(maxval[1])

	cart = queryCartCreate(objectIds)
	return cart.getElementsByTagName("PurchaseURL")[0].firstChild.nodeValue
		

def heuristic(listPrice, amountSaved, primeFlag):
    """ Evaluates an item based on Price, AmountSaved, Best Seller Index, and SuperSave Shipping Availability. """
    
    listPrice, amountSaved = float(listPrice), float(amountSaved)

    return 20.0 / listPrice + 0.008*amountSaved + 0.1*int(primeFlag)

def queryCartCreate (offerListings):
	""" Takes offer listings and generates URL tags for Amazon API cart creation """

	url_param = {'Service': 'AWSECommerceService',
		'AWSAccessKeyId': AWS_KEY,
		'Operation': 'CartCreate',
		'AssociateTag': "dummy_Var"
	}
	index = 0
	for offerListing in offerListings:
		url_param["Item." + str(index) + ".OfferListingId"] = offerListing
		url_param["Item." + str(index) + ".Quantity"] = 1
		index+=1
	
	return signAndRequest(url_param)

def querySearch (keyword):
	""" Takes search keyword(s) and generates URL tags for Amazon API query """

	url_param = {'Service': 'AWSECommerceService',
		'AWSAccessKeyId': AWS_KEY,
		'Operation': 'ItemSearch',
		'Availability': 'Available',
		'SearchIndex': 'Kitchen',
		'Keywords': keyword,
		'AssociateTag': "dummy_Var",
		'ResponseGroup': 'Offers',
		'MerchantId': 'All',
	}
	return signAndRequest(url_param)

def signAndRequest(url_param):
	""" Timestamp generation and signature generation; returns parsed XML that is fetched from Amazon """

	t = datetime.datetime.utcnow()
	amzdate = t.strftime('%Y-%m-%dT%H:%M:%SZ')
	datestamp = t.strftime('%Y%m%d')
	url_param['Timestamp'] = amzdate
	url_param = sorted(url_param.items(), key=operator.itemgetter(0))

	url = urlencode(url_param)
	string_to_sign = canonical_string(url)

	signature = hmac.new(
		AWS_SECRET_KEY,
		msg=string_to_sign.encode('utf-8'),
		digestmod=hashlib.sha256).digest()
	signature = base64.b64encode(signature).decode()
	
	last_param = dict(Signature = signature)
	last_param = urlencode(last_param)

	url = "http://webservices.amazon.com/onca/xml?" + url +"&"+ last_param
	page = urlopen(url)
	xml = parse(page)
	return xml


def canonical_string(query):
	""" Auxiliary method for generating canonical string """

	res = "GET\nwebservices.amazon.com\n/onca/xml\n"
	return res + query