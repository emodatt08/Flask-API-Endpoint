from urllib2 import Request, urlopen
import urllib
import feedparser
from pprint import pprint

class Yelp:

    def __init__(self):
        self.url = "https://api.yelp.com/v3/businesses/search?%s"
        self.header = "bearer 3ZkLDsLWal_oWNIOHxA7rDw4mtILfmy0Lab68o47H9gUeD_ap8_6j5Ar8npMQFA_h16WO7Hw5upS3FXYHR0h4FPlW52mwbbggx9hcLyXl9nm3-TMyBGyORTVsqciW3Yx"

    
    def getBusinesses(self, data):
        if data('term'):
            term = data('term') or ''
        params = urllib.urlencode({'latitude': data('latitude'), 'longitude': data('longitude'), 'term': term})
        request = Request(self.url % params) #send request
        request.add_header('Authorization', self.header)
        response = urlopen(request) #Download Json       
        data = response.read() #Parse json
        return data


    def rss(self):
       url = " https://api.rss2json.com/v1/api.json?rss_url=http%3A%2F%2Ffeeds.feedburner.com%2FTEDTalks_video"
       request = Request(url) #send request
       response = urlopen(request) #Download Json    
       data = response.read()
       return data





    



    
