import facebook
import requests
import re
import os

# Set default text encoding method
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Extend the expiration time of a valid OAuth access token to 60 days.
def token_ext (token_tmp):
	graph = facebook.GraphAPI(token_tmp)
	app_id = os.getenv('FB_APP_ID')
	app_secret = os.getenv('FB_SECRET')

	extended_token = graph.extend_access_token(app_id, app_secret)
	return extended_token

# Extract users' Facebook URL from social-wifi dataset
def get_urls ():
	# Use generator in case of huge dataset
	count = -1
	social_wifi = open("social_wifi.csv")

	for usr in social_wifi:
		count += 1
		if count == 0:
			continue
		res = re.findall(r"(?<=https://www.facebook.com/).+", usr.split(",")[1])
		if len(res) == 0:
			res = re.findall(r"(?<=http://www.facebook.com/).+", usr.split(",")[1])
			
			if len(res) == 0:
				print  "\nFacebook URL is unavailable for this customer"
			elif usr.split(",")[4] == "":
				print "\nE-mail address is unavailable for this customer"
			else:
				yield usr.split(",")[0], str(res[0])
		elif usr.split(",")[4] == "":
			print "\nE-mail address is unavailable for this customer"
		else:

			yield usr.split(",")[0], str(res[0])

def get_likes (url):
	graph = facebook.GraphAPI(os.getenv('FB_TOKEN_LONG'))
	usr_name = graph.get_object(url)['name']
	usr_id = graph.get_object(url)['id']
	content = graph.get_connections(usr_id, 'likes')
	for i in content['data']:
		yield i['name'], i['id']

def save_posts (url, filename):
	fd = open(filename, 'wb')
	graph = facebook.GraphAPI(os.getenv('FB_TOKEN_LONG'))
	usr_id = graph.get_object(url)['id']	# Parameter for get_object() can be either URL or ID
	ifuser = 1

	print "Now crawling posts from \"Panda Express\" ..."

	content = graph.get_connections(usr_id, 'posts')
	# Wrap this block in a while loop so we can keep paginating requests until finished.
	i = 10
	while i > 0:
	    try:
	        # Perform some action on each post in the collection we receive from Facebook.
	        for row in content['data']:
	            fd.write(row['message'])

	        # Attempt to make a request to the next page of data, if it exists.
	        content = requests.get(content['paging']['next']).json()
	        i -= 1

	    except KeyError:
	        # When there are no more pages (['paging']['next'])
	        break
	print "Done!\n"

	print "Start to crawling posts from pages that \"Panda Express\" has liked:\n"

	for likes in get_likes(url):

		print "Now crawling posts from \"" + likes[0] + "\" ... "
		usr_id = likes[1]
		content = graph.get_connections(usr_id, 'posts')

		# Wrap this block in a while loop so we can keep paginating requests until finished.
		i = 10
		while i > 0:
		    try:
		        # Perform some action on each post in the collection we receive from Facebook.
		        for row in content['data']:
		            fd.write(row['message'])

		        # Attempt to make a request to the next page of data, if it exists.
		        content = requests.get(content['paging']['next']).json()
		        i -= 1

		    except KeyError:
		        # When there are no more pages (['paging']['next'])
		        break
		print "Done!\n"

def business_charateristics ():
	fd = open("business_chara.txt", "r+")
	business = {}
	for line in fd:
		temp = line.split(":")
		keywords = temp[1].split(',')
		business.setdefault(temp[0],keywords[:len(keywords)-1])
	return business









