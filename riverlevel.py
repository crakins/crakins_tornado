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
		level = "N/A"
	return level

def get_level_cswc(riverID):
	url = "http://www.dwr.state.co.us/SurfaceWater/data/detail_graph.aspx?ID=%s&MTYPE=DISCHRG" % (riverID)

	response = requests.get(url)
	soup = BeautifulSoup(response.text)
	tag = soup.find_all(id="ctl00_ContentPlaceHolder1_recentvaluelabel")
	soup2 = BeautifulSoup(str(tag))	
	try:		
		level = soup2.span.string
	except: 
		level = "N/A"
	return level
