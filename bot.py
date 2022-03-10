from nltk.stem.porter import PorterStemmer
import nltk 
nltk.download('wordnet')
from nltk.corpus import wordnet
from fileReader import FileReader
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import pos_tag

class Bot:
	"""
		Constructor to initialize constant class variables, and start the program.
	"""
	def __init__(self):
		self.stemmer = PorterStemmer()
		self.conditions = {}
		self.sid = SentimentIntensityAnalyzer()
		self.initialize()
		self.setUserName()
		self.initializeChat()

	"""
		Using the file reader to read in the data. using the stemmer class to check if the key matches the condition of the word.
	"""
	def initialize(self):
		self.data = FileReader().getFileContent()
		self.nodes = self.data['nodes']

		for key in self.data['conditions'].keys():
			words = [self.stemmer.stem(word) for word in self.data['conditions'][key]]
			self.conditions[key] = words

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
		Method asks user for their name, and sets the name to a class variable.
		If the program receives an empty response, user will be prompted to enter the answer again.
		The response to the second question is saved to the node, which will be used in initializeChat method.
	"""
	def setUserName(self):
		self.name = input("Hello, I am Psych-Bot. What is your name? ")
		
		while len(self.name) == 0:
			self.name = input("I didn't get your name, please, repeat.\n- ")

		print(f"Hello {self.name}.")

		self.current = self.nodes[0]
	
	"""
		This runs the main chat loop, exits when the next node is none.
		If the user inputs keyword "quit," program will exit.
		If the user inputs an empty input, program will prompt to enter correct response.
	"""
	def initializeChat(self):
		nodeValue = self.current
		
		while nodeValue != None:
			if 'print' in nodeValue:
				print(nodeValue['text'])
				nodeValue = self.findNode(nodeValue['children'][0])
				continue
			
			answer = input(f"{nodeValue['text']}\n- ")
			
			while len(answer) == 0:
				answer = input("Sorry, what did you say?\n- ")

			if answer.lower() == "quit":
				print("Thank you for your questions. Have a nice day!")
				break

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
					

"""
	Runs the chat with the command 'python bot.py'.
"""
if __name__ == '__main__':
	Bot()