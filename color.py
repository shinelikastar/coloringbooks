from cmd import Cmd
from gensim.models import Word2Vec
from collections import Counter
import nltk
from nltk.tokenize import sent_tokenize 
from nltk.corpus import stopwords
import gzip
import logging
import re
import string
import sys

class Prompt(Cmd):

	prompt = '\n--> '

	# if len(sys.argv) < 2:
	# 	pass
	# else:
	# 	try:
	# 		corpus = open(sys.argv[1:][0], encoding='utf8').read().lower()
	# 		corpus = corpus.translate(string.punctuation)
	# 		color_corpus = open(sys.argv[1:][1], 'w+')
	# 	except IOError:
	# 		print('let me chew on [some words]')

	color_list = ['red', 'orange', 'yellow', 'green', 'blue', 'purple',
				'black', 'white', 'grey'] 

	def do_find_neighbors(self, args):
		"""give me [color] [text]"""
		command = args.split()
		file = command[0]
		color_corpus = open(command[1], 'w+')

		corpus = open(file, encoding='utf8').read().lower()
		stoplist = set(stopwords.words('english'))
		clean = [word for word in corpus.split() if word not in stoplist]
		clean = ' '.join(clean)

		text = clean.split('.')
		text = list(map(lambda x: x.split(), text))
		#clean_text = [x for x in text if x]

		sentences = text
		model = Word2Vec(sentences, min_count=1)
		words = list(model.wv.vocab)
		model.save('model.bin')
		# load model
		new_model = Word2Vec.load('model.bin')
		#color1 = [color]
		#print(model.wv.most_similar(positive=color1,topn=10))

		for color in self.color_list:
			color_corpus.write(color + " ")
			sys.stdout.write(color + " ")
			if color not in model.wv.vocab:
				color_corpus.write("\n")
				sys.stdout.write("\n")
				continue
			neighbors = model.wv.most_similar(positive=[color],topn=10)
			for neighbor, val in neighbors:
				color_corpus.write(neighbor + " ")
				sys.stdout.write(neighbor + " ")
			color_corpus.write("\n")
			sys.stdout.write("\n")
		color_corpus.close()
		sys.stdout.flush()
		pass

	def do_find_colors(self, args):

		command = args.split()

		corpus = open(command[0], encoding='utf8').read().lower()
		corpus = corpus.translate(string.punctuation)
		color_corpus = open(command[1], 'w+')

		text_lst = re.split('\s|(?<!\d)[.]|[.](?!\d)', corpus)
		clean_text = [x for x in text_lst if x] 

		# key: word, val: number of occurrences
		c = Counter()

		for line in clean_text:
			for word in line.split():
				if word in self.color_list:
					c[word] += 1

		total_colors = sum(c.values())

		for color in self.color_list:
			color_corpus.write('%s %f ' % (color, (c[color] / total_colors)*100))
			print("%s %f" % (color, (c[color] / total_colors)*100))
		color_corpus.close()

	def do_q(self, args):
		"""enter <q> to stop this madness """
		print('The End...')
		return True

	def do_quit(self, args):
		"""enter <quit> to stop this madness """
		print('The End...')
		return True


if __name__ == '__main__':
	Prompt().cmdloop()
	# if len(sys.argv) < 2:
	# 	print('let me chew on [some words] [spit out some colors]...')
	# else:
	# 	Prompt().cmdloop()