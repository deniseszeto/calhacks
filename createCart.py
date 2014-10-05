from xml.dom.minidom import parse
from urllib.request import urlopen
from urllib.parse import urlencode
import base64, hashlib, hmac, time
import operator

def createCart (objectList):
	xml = getXML ("Apple")
	#TODO


def getXML (keyword):
	AWS_KEY = ""
	AWS_SECRET_KEY = ""

	base_url = "http://webservices.amazon.com/onca/xml?"
	url_params = dict(
		Service='AWSECommerceService', 
		Operation='ItemSearch', 
		SearchIndex='Kitchen',
		Availability='Available',
		Keywords = keyword,
		AWSAccessKeyId=AWS_KEY)
	url_params['Timestamp'] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
	url_params = sorted(url_params.items(), key=operator.itemgetter(0))

	url_string = urlencode(url_params)

	amzdate = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
	datestamp = time.strftime("%Y%m%d", time.gmtime())
	string_to_sign = stringToSign (amzdate, datestamp, url_string)

	sigKey = getSignatureKey(AWS_SECRET_KEY, amzdate, "us-west-1", "iam")

	signature = sign (sigKey, string_to_sign)
	signature = base64.encodestring(signature).strip()

	url_string += "&Signature=%s" % signature

	url = base_url + url_string

	print(url)
	page = urlopen(url)
	xml = parse(page)
	return xml

	'''
	canonical_querystring = "?Service=AWSECommerceService"

	canonical_querystring += "&AWSAccessKeyId=" + AWS_KEY + "&Operation=ItemSearch&Availability=Available&SearchIndex=Kitchen"

	canonical_querystring += "&Keywords=" + keyword

	amzdate = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
	canonical_querystring += "&Timestamp=" + amzdate

	datestamp = time.strftime("%Y%m%d", time.gmtime())
	sigKey = getSignatureKey(AWS_SECRET_KEY, amzdate, "us-west-1", "iam")
	
	string = stringToSign(amzdate, datestamp, canonical_querystring)

	code = sign (sigKey, string)
	url += canonical_querystring + "&Signature=" + ''.join('{:02x}'.format(x) for x in code)

	print(url)
	page = urlopen(url)
	xml = parse(page)
	return xml
	'''

def sign(key, msg):
	return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

def getSignatureKey(key, dateStamp, regionName, serviceName):
	kDate = sign(("AWS4" + key).encode("utf-8"), dateStamp)
	kRegion = sign(kDate, regionName)
	kService = sign(kRegion, serviceName)
	kSigning = sign(kService, "aws4_request")
	return kSigning

def stringToSign (amzdate, datestamp, canonical_querystring):
	stringToSign = "AWS4-HMAC-SHA256\n"

	host = 'webservices.amazon.com'
	stringToSign += amzdate + "\n"

	credential = datestamp + "/" + "us-west-1/iam/aws4_reqeust\n" 
	stringToSign += credential

	method = "GET"
	canonical_uri = '/onca/xml'
	canonical_headers = 'host:' + host + '\n' + 'x-amz-date:' + amzdate + '\n'
	signed_headers = 'host;x-amz-date'

	string = ''
	encoded = string.encode('utf-8')
	payload_hash = hashlib.sha256(encoded).hexdigest()
	canonical_request =  method + '\n' + canonical_uri + '\n' + canonical_querystring + '\n' + canonical_headers + '\n' + signed_headers + '\n' + payload_hash
	stringToSign += hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()

	return stringToSign