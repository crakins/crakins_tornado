import requests
from bs4 import BeautifulSoup

def get_level(riverID):
	url = "http://waterdata.usgs.gov/usa/nwis/uv?" + str(riverID)	
	response = requests.get(url)
	soup = BeautifulSoup(response.text)
	tag = soup.find_all('td', 'highlight2')
	soup2 = BeautifulSoup(str(tag))	
	try:		
		level = soup2.td.string	
	except: 
		level = " "
	return level
