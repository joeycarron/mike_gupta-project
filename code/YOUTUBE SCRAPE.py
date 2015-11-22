__author__ = 'Joer'

#from bs4 import BeautifulSoup
#import html5lib
import json, urllib2
#import re
#import pydot
#import itertools
#import time
#import ast
import csv

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import pandas as pd


DEVELOPER_KEY = "AIzaSyAgiuJaqOqrsrFIfIdp3S17urARba7MHvo"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY) 

def setup():
	query = raw_input("Enter your query: ")
	argparser.add_argument("--q", help="Search term", default=query) #change the default to the search term you want to search
	argparser.add_argument("--max-results", help="Max results", default=1) #default number of results which are returned. It can vary from 0 - 100
	options = argparser.parse_args()
	search_response = youtube.search().list( # Call the search.list method to retrieve results matching the specified query term.
	 q=options.q,
	 type="video",
	 part="id,snippet",
	 maxResults=options.max_results
	).execute()

	return search_response

def scrape(search_response):
	videos = {} # Add each result to the appropriate list, and then display the lists of matching videos. Filter out channels, and playlists.
	for search_result in search_response.get("items", []):
	 if search_result["id"]["kind"] == "youtube#video": #videos.append("%s" % (search_result["id"]["videoId"]))
	    videos[search_result["id"]["videoId"]] = search_result["snippet"]["title"]
		#print "Videos:\n", "\n".join(videos), "\n"
	s = ','.join(videos.keys())

	videos_list_response = youtube.videos().list(
	 id=s,
	 part='id,statistics,snippet'
	).execute()
	res = []

	# print videos_list_response['items']

	for i in videos_list_response['items']:
	 temp_res = dict(v_id = i['id'], v_title = videos[i['id']])
	 temp_res.update(i['statistics'])
	 temp_res.update(i['snippet'])


	 dislikes = i['statistics']['dislikeCount']
	 likes = i['statistics']['likeCount']
	 reputability = int(likes) / int(dislikes
	 if reputability >= 0.7:
		 res.append(temp_res)


	df = pd.DataFrame.from_dict(res)

	print json.dumps(res[0], indent=4, sort_keys=True)
	# print df
	df.to_csv("first50scraped.csv", sep='\t', encoding='utf-8')

	first25scraped = open(r'first25scraped.txt','w+')
	for x in res:
	    first25scraped.write(str(x) + "\n")
	first25scraped.close()

def main():
	setup_variable = setup()
	scrape(setup_variable)

if __name__ == '__main__':
	import profile
	profile.run("main()")