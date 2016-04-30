import facebook
import requests
import re
import os
import time
import subprocess	# For running Java program
from facebook_crawler import get_urls, get_likes, save_posts, business_charateristics
from strings_similarity import similarity
import timeit
from sys import argv

# Set default text encoding method
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def recommendation_4_customers (name, filename):
	start = time.time()
	print "---------------------------------------------------"
	print "\nFor \"" + name + "\":\n"
	subprocess.call(['java', '-jar', 'nouns_extraction.jar', filename, str("nouns_" + filename)])
	noun_list = []
	fd = open(str("nouns_" + filename), "r+")
	for noun in fd:
		word = noun.split("\n")[0]
		noun_list.append(word)

	# Calculate similarity and recommend
	business = business_charateristics()
	resta_recommend = {}
	mus_reconmmend = {}
	for b in business:
		if b == "Music":
			for gen in business["Music"]:
				s = similarity(gen, " ".join(noun_list))
				mus_reconmmend.setdefault(s, gen)
			continue
		s = similarity(" ".join(business[b]), " ".join(noun_list))
		resta_recommend.setdefault(s, b)

	recom_name = []
	recom_mus = []
	for score in sorted(resta_recommend, reverse=True)[0:3]:
		recom_name.append(resta_recommend[score])
	for score in sorted(mus_reconmmend, reverse=True)[0:2]:
		recom_mus.append(mus_reconmmend[score])

	end = time.time()
	print "\nRestaurants Recommendation:", ",".join(recom_name)
	print "Music Genre Recommendation:", ",".join(recom_mus)
	print "\nSave recommendations to file ..."
	print "\nTotal time: [" + str(round((end - start), 2)) + " sec]\n"

	
	result_fd = open("recommendation_result.txt", "ab")
	out = str(name+";"+",".join(recom_name)+";"+",".join(recom_mus)+"\n")
	result_fd.write(out)
	result_fd.close()

if __name__ == '__main__':

	if argv[1] == "-similarity":
		# Calculate similarity of two strings
		str_a = "cheesecake tiramisu pudding macaroons"
		str_b =	"ice cream horchata macapuno cantaloupe"
		print "Similarity between \"", str_a, "\" and \"", str_b, "\" is:", similarity(str_a, str_b)

	if argv[1] == "-urls":
		# Extract customers' Facebook URLs
		for info in get_urls():
			print "\nCustomer Name:", info[0], "\nCustomer Facebook URL:", str("https://www.facebook.com/"+info[1])

	if argv[1] == "-likes":
		# Get liked pages
		for info in get_likes("https://www.facebook.com/PandaExpress/"):
			print "Name: \""+info[0]+"\" ID: \""+info[1]+"\""

	if argv[1] == "-posts":
		# Save posts of users and their liked pages
		save_posts("https://www.facebook.com/PandaExpress/", "customers_data/Panda_Express.txt")
	
	if argv[1] == "-recommend":	
		# Give recommendation to each customer
		filelist = [("Alexis Augustine", "customers_data/Alexis_Augustine.txt"), ("Adrian Valenzuela", "customers_data/Adrian_Valenzuela.txt"), ("Adam A. Hillier", "customers_data/Adam.A.Hillier.txt")]
		for info in filelist:
			recommendation_4_customers(info[0], info[1])








