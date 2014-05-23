import requests
import xml.etree.ElementTree as ET
import csv

DEBUG = 1

TRULIA_API_KEY = "INSERT KEY HERE"

API_CALL = "http://api.trulia.com/webservices.php?library=TruliaStats&function=getCityStats"
payload = {'city':'Arcadia', 'state':'CA', 'startDate':'2003-01-01', 'endDate':'2014-03-31', 'statType':'listings', 'apikey':'z9hey9s7kabkuhbfmursjdzy'}
request = requests.get(API_CALL, params=payload)
print("Request url:"); print(request.url)
print(request.text)

tree = ET.fromstring(request.content)

# CSV writer
writer = csv.writer(open('trulia_data.csv', 'wb'), delimiter=',')
header = ["weekEndingDate", "allNum", "allMedian", "allAvg", "1Num", "1Median", "1Avg", "2Num", "2Median", "2Avg", "3Num", "3Median", "3Avg",
	"4Num", "4Median", "4Avg", "5Num", "5Median", "5Avg", "6Num", "6Median", "6Avg", "7Num", "7Median", "7Avg", "8Num", "8Median", "8Avg",
	"9Num", "9Median", "9Avg", "10Num", "10Median", "10Avg", "11Num", "11Median", "11Avg"]
writer.writerow(header)
listings = tree.findall("./response/TruliaStats/listingStats/")
for listing in listings:
	entry = []
	print listing.tag, listing.attrib, listing.items(), listing.text
	categories = listing.findall("./")
	weekEndingDate = categories[0].text

	#print weekEndingDate
	entry.append(weekEndingDate)
	listingPrice = categories[1]
	num_bedroom = 1

	for subcategory in listingPrice.findall("./"):
		print "Subcategory:", subcategory
		property_type = subcategory.findall("./")
		print "Length of entries in subcategory:", len(property_type)
		print num_bedroom
		if "All" in property_type[0].text:
			entry.append(property_type[1].text)
			entry.append(property_type[2].text)
			entry.append(property_type[3].text)
		else: 
			while (str(num_bedroom) not in property_type[0].text):
				entry.append("")
				entry.append("")
				entry.append("")
				num_bedroom += 1;
			entry.append(property_type[1].text)
			entry.append(property_type[2].text)
			entry.append(property_type[3].text)
			num_bedroom += 1;
		for temp in property_type:
			print temp.text
		print "--"
	writer.writerow(entry)
	print("------")
