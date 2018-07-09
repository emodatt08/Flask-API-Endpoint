# extract links
#then indexing links
#then matching a pattern
#viewing the result of the query

import urllib2
import requests
import lxml
from bs4 import BeautifulSoup as beauty






def downlaod_page(html_page):
	headers = {
    'User-Agent': 'KadySearch',
   
}

	r = requests.get(html_page, headers=headers)
	if r.status_code != 200:
		raise Exception ("Non-Ok Status code: "+ format(r.status_code))
	
	return r.text



def parsetext(html_page):
	url = urllib2.urlopen(html_page)
	bs = beauty(url, "lxml")
	for link in bs.find_all('a'):
		print(link.get('href'))

	for img in bs.find_all('img'):
		print(img.get('src'))

	 
	
		
	


 	

see = parsetext("http://www.bing.com/search?q=bambi&go=&form=QBLH&qs=n")
see2 = parsetext("https://yandex.com/search/?text=willow%20smith&lr=20803")
print see
