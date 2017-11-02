from flask import Flask, render_template, jsonify
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import tweepy
import os
import sys

ckey="LkCHfBuPi8PGz9vSBVhqxACdH"
csecret="IccB4NkWkt6yTQR9MQ1QIjfznTGK0s9lzMqcOxPl9Q873ea6zU"
atoken="2723867282-PrlcyW8uxtvUYzZh48Ux4WzbeVuHCcUv1ABG7Y4"
asecret="8YUT51BTd51YSxsmXFVVEWH4lhYR2QeizlB7qloTm8Ox9"

app = Flask(__name__)


geores1 = []


@app.route('/')	
def frontend():
	print "here "
	return render_template('index1.html')

@app.route('/tweetdata')
def map_func():
	auth = tweepy.OAuthHandler(ckey, csecret)
	auth.set_access_token(atoken, asecret)
	
	flag = 0
	count = 0
	if len(geores1)==100:
		geores1.reverse()
		for i in range(0,10):				
			geores1.pop()
		geores1.reverse()
		api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
		results = api.search(q="Global Warming",geocode="40.7128,-74.0060,1000km",count=90)#distance taken is 1000km
		data2 = [s._json for s in results]
		for d in data2:
			if "place" in d.keys(): 
				if d["place"]:
					geores2=[]
					geores2.append(d["text"])
					print "place:long", d["place"]["bounding_box"]["coordinates"][0][0][0]
					geores2.append(d["place"]["bounding_box"]["coordinates"][0][0][1])
					print "place:lat", d["place"]["bounding_box"]["coordinates"][0][0][1]
					geores2.append(d["place"]["bounding_box"]["coordinates"][0][0][0])
					geores1.append(geores2)
					flag+=1
	else: #if empty
		kx = 100-len(geores1)
		api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
		results = api.search(q="great",geocode="40.7128,-74.0060,1000km",count=kx)
		data2 = [s._json for s in results]
		for d in data2:
			if "place" in d.keys(): #fetching place 
				if d["place"]:
					geores2=[]
					geores2.append(d["text"])
					print "place:long", d["place"]["bounding_box"]["coordinates"][0][0][0]
					geores2.append(d["place"]["bounding_box"]["coordinates"][0][0][1])
					print "place:lat", d["place"]["bounding_box"]["coordinates"][0][0][1]
					geores2.append(d["place"]["bounding_box"]["coordinates"][0][0][0])
					geores1.append(geores2)
					flag+=1

	for i in range(0,len(geores1)):
		for j in range(0,3):
			print geores1[i][j]
		
	res = []
	for i in geores1:
		myDict = {}
		myDict["coords"] = {}
		myDict["coords"]["lat"] = i[1]
		myDict["coords"]["lng"] = i[2]
		myDict["content"] = i[0]
		res.append(myDict)

	return jsonify(res)
				


if __name__ == '__main__':
	app.run()
