# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http import HttpResponse, HttpResponseBadRequest

import urllib, json, time

import requests
from bs4 import BeautifulSoup
import lxml, time, csv, codecs
from requests import get
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
import ssl


class MyAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1)

def GoogGeoAPI(latlang):
		api="AIzaSyC_CLJ6o3qTGcJhMQWVbvzFuXpIlDkvoVM"
		delay=5
		base = r"https://maps.googleapis.com/maps/api/geocode/json?"
		addP = "latlng=" + latlang
		GeoUrl = base + addP + "&key=" + api
		response = urllib.urlopen(GeoUrl)
		jsonRaw = response.read()
		jsonData = json.loads(jsonRaw)
		if jsonData['status'] == 'OK':
			resu = jsonData['results'][0]
			finList = resu['formatted_address']
		else:
			finList = [None,None,None]
		time.sleep(delay) #in seconds
		return finList


# Create your views here.
def house(request,lat,longitude):
	print lat
	print longitude

	###look up of zipcode based on coordinates can do this through angular as well
	fin_string = GoogGeoAPI(str(lat)+",-"+str(longitude))
	fin_list  = fin_string.split(',')
	postal = fin_list[2].split(' ')[2]


	###making the request to craigslist
	s = requests.Session()
	s.mount('url', MyAdapter())

	      
	craigslist_base = "https://sfbay.craigslist.org/search/sfc/rea?query=tlc&search_distance=30&postal="+str(postal)+"&max_price=600000&min_bedrooms=2&min_bathrooms=1&minSqft=900&availabilityMode=0&housing_type=6"
	print craigslist_base

	try:

		raw = s.get(craigslist_base).text

		soup = BeautifulSoup(raw, "lxml")
		#print soup

		# list_of_tags = ['<li>']
		# print soup.findAll('li')
		# print [str(tag) for tag in soup.find_all('li')]
		result = soup.findAll("a", { "class" : "result-title hdrlnk" })
		print result
		return HttpResponse(json.dumps(str(result)), content_type="application/json")

	except:

		return HttpResponseBadRequest("Home not found.")
