from nltk.stem.porter import PorterStemmer

from fileReader import FileReader

class Bot:
	"""
		Method Documentation goes here
			-constructor to initialize constant class variables	 
	"""
	def __init__(self):
		self.stemmer = PorterStemmer()
		self.conditions = {}
		self.initialize()
		self.setUserName()
		self.initializeChat()

	"""
		Method Documentation goes here
			-using the file reader to read in the data. using the stemmer class to check if the key matches the condition of the word. 
	"""
	def initialize(self):
		self.data = FileReader().getFileContent()
		self.nodes = self.data['nodes']

		for key in self.data['conditions'].keys():
			words = [self.stemmer.stem(word) for word in self.data['conditions'][key]]
			self.conditions[key] = words

	"""
		Method Documentation goes here
			-returns a node for the given id, if exists.
	"""
	def findNode(self, id):
		if id is None:
			return None
		for node in self.nodes:
			if node['id'] == id:
				return node
		return None

	"""
		Method Documentation goes here
			-Asks instructed questions and returns the user's name.
			-includes a couple logic error catch
	"""
	def setUserName(self):
		self.name = input("Hello, I am Psych-Bot. What is your name? ")
		
		while len(self.name) == 0:
			self.name = input("I didn't get your name, please, repeat.\n- ")

		response = input(f"Hello {self.name}.\nI am glad to have you here today, How are you feeling?\n- ")

		while len(response) == 0:
			response = input("Sorry, what did you say?\n- ")

		self.current = self.nodes[0]
	
	"""
		Method Documentation goes here
			Return the user's name
	"""
	def getUserName(self):
		return self.name
 
	"""
		Method Documentation goes here
			-this runs the main chat loop, exits when the next node is none.
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
					for word in self.conditions[child['condition']]:
						if word in answer_words:
							nodeValue = child
					if nodeValue == child:
						break

"""
	Method Documentation goes here
		-runs the chat with the command 'python bot.py'
"""
if __name__ == '__main__':
	Bot()