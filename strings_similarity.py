import gensim, logging, wikipedia, re
from gensim.models import word2vec
from gensim.parsing import PorterStemmer
from wikipedia import page, search, exceptions

# Set default text encoding method
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def read_keywords():
	fd = open('business_chara.txt', 'r+')
	keyword_list = []
	for line in fd:
		keywords = line.split(',')
		for k in keywords[:len(keywords)-1]:
			keyword_list.append(k)
	return keyword_list

def get_articles():
	keyword_list = read_keywords()
	remaining_keyword = len(keyword_list)
	for key in keyword_list:
		remaining_keyword -= 1
		print str("\nRemaining keyword: " + str(remaining_keyword) + "/" + str(len(keyword_list)))
		print str("Now crawling articles for keyword: \'" + key + "\'")
		# Get relevant titles
		titles = search(key)
		fd = open("wiki_text_raw.txt", 'a+')
		# Search pages according to titles
		for t in titles:
			# page may raise exceptions
			try:
				pages = page(t)
				print str("^_^ Page for \'" + t + "\' retrieved!")
			except wikipedia.exceptions.DisambiguationError as e:
				print str("+_+ Ambiguous keyword: \'" + t + "\'")
			except wikipedia.exceptions.PageError as e:
				print str("+_+ Cannot find the page for: \'" + t + "\'")
			fd.write(pages.content)
		fd.close()

def tokenize():
	fd = open("wiki_text_raw.txt", 'r+')
	fd_tk = open("wiki_text_tokenized.txt", 'a+')
	for line in fd:
		wordlist = re.findall(r"[a-zA-Z]+", line)
		if len(wordlist) > 10:
			for index, word in enumerate(wordlist):
				# Stem each word in word list
				wordlist[index] = PorterStemmer().stem(word)
			for word in wordlist:
				fd_tk.write(str(word + ' '))
			fd_tk.write('\n')

# Word2Vec model training
def train_model():
	sentences = word2vec.LineSentence('wiki_text_tokenized.txt')
	model = word2vec.Word2Vec(sentences, sg=1, min_count=5, size=180, window=4)
	model.save('word2vec_model.txt')

def similarity(a, b):
	text_a = a
	text_b = b
	a = a.split(' ')
	b = b.split(' ')
	for index, word in enumerate(a):
		a[index] = PorterStemmer().stem(word)
	for index, word in enumerate(b):
		b[index] = PorterStemmer().stem(word)
	model = word2vec.Word2Vec.load('word2vec_model.txt')

	b_cp = b[:]
	for word in b:
		if word not in model.vocab:
			del b_cp[b_cp.index(word)]

	a_cp = a[:]
	for word in a:
		if word not in model.vocab:
			del a_cp[a_cp.index(word)]

	return model.n_similarity(a_cp, b_cp)









