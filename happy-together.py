#!/usr/bin/python

# install beautiful soup
# sudo pip install beautifulsoup4

# to manually compile a Python file into a runnable binary: 
#>>> import py_compile
#>>> py_compile.compile('happy-together1.py')

# just so that we can use sleep() later to lessen the load on the CL website,
# or at least not appear like such a leech
import time 

# native HTML parser: http://docs.python.org/2/library/htmlparser.html
#from HTMLParser import HTMLParser

# *new* HTML parser: http://www.crummy.com/software/BeautifulSoup/bs4/doc/
from bs4 import BeautifulSoup

# rss parser: https://pypi.python.org/pypi/feedparser/
import feedparser

# regular expressions
import re

# database functionality
#import sqlite3

# URL stuff
import urllib

cities = [ 'boston','newyork','sfbay','losangeles','chicago','miami','seattle','washingtondc', ]

my_city = cities[0]

rss_feed = 'http://' + my_city + '.craigslist.org/mis/index.rss'
#rss_feed =  'index.rss' # for local filesytem

print 'using feed:' , rss_feed
# exit()

# empty list of webpages
webpages = []  

# empty list of posts
posts = []  

# filenames of posts
filenames = []

post_dir = 'posts'

# we'll proably want two lists: one for MEs, and another for YOUs
#me_descs = []
#you_descs = []

################################################################################
"""
End of variables.
"""
################################################################################

################################################################################
"""
1. Download a list of 100 URLs via the RSS feed.
2. Loop through each URL and pull out the full text of the post.
3. Search the posts for "You:" and "Me:"
"""
################################################################################

feed = feedparser.parse( rss_feed )

max_range = 2 #for debugging
# set the range here: 100
max_range = len(feed['items'])


# grab the webpage URLs from the RSS feed, add to webpages array
for link_index in range(max_range):
	webpages.append(feed['items'][link_index]['link'])
	url_list = webpages[link_index].split('/')
	#print url_list
	filenames.append(url_list[-1])

#print str(webpages)
#print str(filenames)
#exit()

for page in range(max_range):
	# be nice to CL, pause 
	time.sleep(2)
	print "processing", str(page+1), ":", webpages[page]
	sock = urllib.urlopen(webpages[page])
	HTMLSource = sock.read()
	sock.close()
	postHTML = BeautifulSoup(HTMLSource)
	# put post into 'posts' array
	posts.append(postHTML)

	# write it to a file
	cl_post_file = open ( post_dir + '/' + my_city + '/' + filenames[page], 'w' )
	cl_post_file.write ( str(postHTML) )
	cl_post_file.close ( )

	#print postHTML.find(id='postingbody').get_text()

	if postHTML.find(id='postingbody'):
		postText = postHTML.find(id='postingbody').get_text()

		youPattern = re.compile(".*?(You\:.*?(\.|\!))", re.DOTALL )
		youMatch = youPattern.match ( postText.strip() )

		# note: it's possible there is a "You:" match _without_
		# a corresponding "Me:" match. Fix this at some point.
		if youMatch:
			print youMatch.group(1)

			mePattern = re.compile(".*?(Me\:.*?\.)", re.DOTALL)
			meMatch = mePattern.match ( postText.strip() )

			if meMatch:
				print meMatch.group(1)

