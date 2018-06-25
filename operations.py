import os
import datetime
import io
import time
from flask import jsonify, json

def toJson(data):
	return json.dumps(data)


def logall(params, state, method, getRequest):
	 __timestamp = datetime.datetime.now()
	 __directory = os.getcwd()
	 ts = time.time()
	
	 if method == 1:
	 	method = "POST"
	 else:
	 	method = "GET"
	 
	 logfile = "Response: " + str(params) + " time: "+ str(datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')) + " Request: " + getRequest + " State: "+ state + "\n"
	 with open(__directory +"/logs/"+ str(datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')) +".csv","a+") as myfile:
	 	myfile.write(logfile)
	
	
def getdate():
	return datetime.datetime.now()


