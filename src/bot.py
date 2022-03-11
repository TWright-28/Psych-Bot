from nltk.stem.porter import PorterStemmer
import nltk 
nltk.download('wordnet')
from nltk.corpus import wordnet
from fileReader import FileReader
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import pos_tag

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
					tags = pos_tag(answer_words)
					found = False
					for pos in child['pos']:
						if any(pos == tag[1] for tag in tags):
							found = True
							break
					if not found:
						continue	
				if 'sentiment' in child:
					ss = self.sid.polarity_scores(" ".join(answer_words))
					for sentiment in child['sentiment']:
						if ss[sentiment] > 0.5:
							nodeValue = child
							break
				elif 'condition' in child:
					for word in self.conditions[child['condition']]:
						for answer_word in answer_words:
							synonyms = [answer_word]
							for syn in wordnet.synsets(answer_word):
								for l in syn.lemmas():
									synonyms.append(l.name())
							if word in synonyms:
								nodeValue = child
								break
				else:
					nodeValue = child 
				if nodeValue == child:
					break

		self.current = nodeValue
		return nodeValue