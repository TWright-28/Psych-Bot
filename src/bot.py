from nltk.stem.porter import PorterStemmer
import nltk 
nltk.download('wordnet')
nltk.download('vader_lexicon')
nltk.download('omw-1.4')
nltk.download('averaged_perceptron_tagger')
from nltk.corpus import wordnet
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import pos_tag

import os
import sys

cur_path=os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, cur_path+"/..")
from src.fileReader import FileReader

class Bot:
	"""
		Constructor to initialize constant class variables, and setup the responses.
	"""
	def __init__(self, pathFile):
		self.name = ""
		self.stemmer = PorterStemmer()
		self.conditions = {}
		self.initialize(pathFile)
		self.sid = SentimentIntensityAnalyzer()


	"""
		Using the file reader to read in the data. using the stemmer class to check if the key matches the condition of the word.
	"""
	def initialize(self, filePath):
		self.data = FileReader(filePath).getFileContent()
		self.nodes = self.data['nodes']

		for key in self.data['conditions'].keys():
			words = [self.stemmer.stem(word) for word in self.data['conditions'][key]]
			self.conditions[key] = words

	"""
		Returns the content of JSON Object of data.json file.
	"""
	def getData(self):
		return self.data

	"""
		Returns a node for the given id, if exists.
	"""
	def findNode(self, id):
		if id is None:
			return None
		for node in self.nodes:
			if node['id'] == id:
				return node
		return None

	"""
		Method sets the name to a class variable.
		If input of username is empty, return -1.
		The response to the second question is saved to the node, which will be used in initializeChat method.
	"""
	def setUserName(self, name):
		if len(name.strip()) == 0:
			return -1
		
		self.name = name
		self.current = self.nodes[0]
		return f"> Bot: Hello {self.name}.\nI am glad to have you here today, How are you feeling?\n\n"

	"""
		Return the user's name. If user's name is not defined, return
	"""
	def getUserName(self):
		if len(self.name) == 0:
			return -1
		return self.name
 
	"""
		Method looks over the node of the responses based on the user's input.
		If main node has subnodes(e.g., the user answered yes to the question instead of), method will look for the child nodes to find 
		correct answer.
		On the other hand, if the node doesn't have subnodes, it will proceed to the next node based on the user's response.
		Method also uses nltk and portstemmer libraries to detect the part of speech, synonym recognition, and sentiment analysis.
		Method also validates if username was provided, and if user asked to quit the program.
		The method return object of node.
	"""
	def getResponse(self, answer):
		
		if self.getUserName() == -1:
			return None

		nodeValue = self.current
		
		if 'print' in nodeValue:
			nodeValue = self.findNode(nodeValue['children'][0])
			self.current = nodeValue
			return nodeValue

		if answer.lower() == "quit":
			return -1
		
		if len(nodeValue['children']) == 1:
			nodeValue = self.findNode(nodeValue['children'][0])
		else:
			answer_words = [self.stemmer.stem(word) for word in answer.lower().split(" ")]
			for child in nodeValue['children']:
				child = self.findNode(child)
				
				if 'default' in child:
					nodeValue = child
					break
				
				if 'pos' in child:
					found = len(self.getPosTag(child, answer_words)) > 0	
					if not found:
						continue

				if 'sentiment' in child:
					p_scores = self.getSentimentPolarityScore(answer_words)
					for sentiment in child['sentiment']:
						if p_scores[sentiment] > 0.5:
							nodeValue = child
							break
				elif 'condition' in child:
					for word in self.conditions[child['condition']]:
						for answer_word in answer_words:
							synonyms = [answer_word]
							synonyms = self.getWordNetSynsetResult(answer_word)
							synonyms = [self.stemmer.stem(synonym) for synonym in synonyms]
							if word in synonyms:
								nodeValue = child
								break
				else:
					nodeValue = child 
				if nodeValue == child:
					break

		self.current = nodeValue
		return nodeValue

	"""
		@api
		Returns the list of predicted POS from the sentense the user has provided to the bot. 
	"""
	def getPosTag(self, child, response):
		tags = pos_tag(response)
		pos_tags = []
		for pos in child['pos']:
			if any(pos == tag[1] for tag in tags):
				pos_tags.append(pos)
		return pos_tags
	

	"""
		@api
		Returns synonyms from the wordnet list based on the input provided by the user.
	"""
	def getWordNetSynsetResult(self, response):
		if len(response.strip()) == 0:
			return -1

		synonyms = [response]
		for syn in wordnet.synsets(response):
			for l in syn.lemmas():
				synonyms.append(l.name())
		return synonyms

	"""
		@api
		Returns the sentimental analysis of the user's input. Determines if the response is positive, negative or neutral
	"""
	def getSentimentPolarityScore(self, response):
		if len(response) == 0:
			return -1

		p_scores = self.sid.polarity_scores(" ".join(response))
		return p_scores