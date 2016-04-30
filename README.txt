********************************************************************************
Prerequisites:

Python version - 2.7

Required Python package: facebook, request, gensim, logging, wikipedia

Stanford NLP Parser Java Archive

********************************************************************************

Execution:

Since I currently do not have permission to access normal users' Facebook accounts, this system cannot work fully automaticly for now. But you could run each major module in this system separately.

In order to see the result of each module, you could run "recommendation_system.py" with arguments.

	python recommendation_system.py [argument] (e.g. python recommendation_system.py -urls)

Argument options:

-urls: Validate and extract customers' Facebook URLs
-posts: Crawl and save posts of users' own accounts and their liked pages
-recommend: Based on crawled Facebook content of one user, recommend businesses of the mall and to this user


*********************************************************************************
Output:

URL Extraction:
	Customers' names and their Facebook URL
Posts Collection: 
	Posts about each customer would be save in a file named with this person's name
Recommendation: 
	Save recommendations for every user to a file named "recommendation_result.txt"

*********************************************************************************

Acceptance:

The output will be said to be correct if the program runs without error and each customer would be recommended some businesses and music.

**********************************************************************************