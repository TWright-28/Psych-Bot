from nltk.stem.porter import PorterStemmer

from fileParser import FileReader

class Bot:
	def __init__(self):
		self.stemmer = PorterStemmer()
		self.conditions = {}
		self.initialize()
		self.setUserName()
		self.initializeChat()

	def initialize(self):
		self.data = FileReader().getFileContent()
		self.nodes = self.data['nodes']

		for key in self.data['conditions'].keys():
			words = [self.stemmer.stem(word) for word in self.data['conditions'][key]]
			self.conditions[key] = words

	def findNode(self, id):
		if id is None:
			return None
		for node in self.nodes:
			if node['id'] == id:
				return node
		return None

	def setUserName(self):
		name = input("Hello, I am Psych-Bot. What is your name? ")

		input(f"Hello {name}, how are you feeling today? ")
		self.current = self.nodes[0]
	
	def initializeChat(self):
		nodeValue = self.current

		while nodeValue != None:
			if 'print' in nodeValue:
				print(nodeValue['text'])
				nodeValue = self.findNode(nodeValue['children'][0])
				continue
			
			answer = input(f"{nodeValue['text']}\n- ")
			
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

if __name__ == '__main__':
	Bot()
